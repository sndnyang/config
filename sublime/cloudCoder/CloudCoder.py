# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import traceback

import requests
from requests import session

from utility import str_obj
from utility import printDeep

def replace_html(s):
    s = s.replace('&quot;','"')
    s = s.replace('&amp;','&')
    s = s.replace('&lt;','<')
    s = s.replace('&gt;','>')
    s = s.replace('&nbsp;',' ')
    s = s.replace('\xc2\xa0','')
    return s

class CloudCoder:
    # __codeBlockUrl = 'http://localhost:5000/codeBlock'
    __codeBlockUrl = 'https://www.zhimind.com/codeBlock'
    # __uploadCodeUrl = 'http://localhost:5000/uploadCodeBlock'
    __uploadCodeUrl = 'https://www.zhimind.com/uploadCodeBlock'

    def __init__(self, apiKey="", debug=False):
        if debug:
            self._apiKey = apiKey.strip() or os.environ.get("LOCAL_TOKEN", "")
            self.__codeBlockUrl = 'http://localhost:5000/codeBlock'
            self.__uploadCodeUrl = 'http://localhost:5000/uploadCodeBlock'
        else:
            self._apiKey = apiKey.strip() or os.environ.get("ZHIMIND_TOKEN", "")
        self.__connectTimeout = 60.0
        self.__socketTimeout = 60.0
        self.__version = '0_0_0'
        self.__client = session()

    def post_code(self, data):
        header = {"Authorization": "Bearer " + self._apiKey}
        try:
            r = requests.post(url=self.__uploadCodeUrl, 
                              json=data, 
                              headers=header, 
                              verify=False)
            r.raise_for_status()
            print("status: ", r.status_code)
            return json.loads(r.content.decode('utf-8'), strict=False)
        except:
            print(traceback.print_exc())
            return "Error error"

    def get_list(self, match):
        if "," not in match and " " in match:
            match = ",".join(e for e in match.split())

        header = {"Authorization": "Bearer " + self._apiKey}
        try:
            r = requests.get(url=self.__codeBlockUrl, params={'keyword': match}, 
                             headers=header, verify=False)
            r.raise_for_status()
            print("status: " + str(r.status_code))
            return json.loads(r.content.decode('utf-8'), strict=False)
        except:
            print(traceback.print_exc())
            return "Error error"

    def show_titles(self, json):
        return '\n'.join(e['title'] + ' ' + e['url'] for e in json)

    def get_all_titles(self, match):
        data = self.get_list(match)
        if u'msg' in data or u'error' in data:
            return "Error: not find any one"
        return self.show_titles(data)

    def get_code(self, match, keys="all"):
        return self.get_code_by_parts(match, keys)

    def get_code_by_parts(self, match, keys):
        json = self.get_json(match)
        if isinstance(json, str_obj):
            return json
        if u'msg' in json or u'error' in json:
            return "Error: not find any one"
        return self.filter_json(json, keys)

    def get_json(self, match):
        return self.convert_md_json(self.get_markdown(match))

    def convert_md_json(self, content):
        if content.startswith("Error:") or content.startswith("\nOptions"):
            return content
        maps = {"code": ""}
        lines = content.replace("\r", "").split("\n")
        self.to_hierarchy_json(maps, lines, 0, 0)
        maps.pop("code")
        return maps

    def get_markdown(self, match):
        if self._apiKey:
            match_list = self.get_list(match)
            if "error" in match_list:
                return "Error: nothing find"
            if len(match_list) == 1:
                return match_list[0]['content']
            elif len(match_list) > 1:
                return "\nOptions:\n" + self.show_titles(match_list)
            else:
                return "Error: nothing find"
        return "Error: no token"

    def to_hierarchy_json(self, maps, lines, level, lineno):
        if len(lines) == lineno:
            return 0, lineno
        l = lines[lineno]

        name = "code"
        
        if not l.strip():
            return self.to_hierarchy_json(maps, lines, level, lineno+1)
        # print('%4d %4d' % (level, lineno),)

        while l.startswith("#"):
            sharp_count = len(re.search("^(#+)", l).group(1))
            obj = re.search("^#+\s*(.+)$", l)
            if obj:
                name = obj.group(1)
            else:
                name = u"无标题"
            # print('%4s %4s' % (name, sharp_count))
            # print(l)
            if level >= sharp_count:
                return sharp_count, lineno
            elif level < sharp_count:
                maps[name] = {"code": ""}
                tmp, lineno = self.to_hierarchy_json(maps[name], lines, level+1, lineno+1)
                if tmp < level or not tmp:
                    return tmp, lineno
                l = lines[lineno]       
        # print("add to ", name)

        if not level:
            return self.to_hierarchy_json(maps, lines, level, lineno+1)
        elif name == "code":
            maps[name] += l + '\n'
        else:
            maps[name]["code"] += l + '\n'    
        # print(l)
        return self.to_hierarchy_json(maps, lines, level, lineno+1)


    def filter_json(self, data, keys):
        if keys == "all":
            # printDeep(data, 0)
            return self.convert_json_plain(data, '')
        maps = {'调用':"call", "定义":"implement", "实现":"implement"}
        keys = [e.lower() for e in keys]
        en_maps = [maps[e] for e in keys if e in maps]
        parts = []
        for k in data:
            if k.lower() in keys or k.lower() in en_maps:
                parts.append(self.convert_json_plain(data[k], k))
            elif isinstance(data[k], dict):
                result = self.filter_json(data[k], keys)
                if result:
                    parts.append(result)
        return '\n'.join(parts)

    def convert_json_plain(self, data, key):
        lines = [key]
        for k in data:
            if isinstance(data[k], dict):
                lines.append(self.convert_json_plain(data[k], k))
            elif isinstance(data[k], str_obj):
                if k != "code":
                    lines.append(k)
                lines.append(data[k])
        return '\n'.join(lines)


if __name__ == '__main__':
    c_coder = CloudCoder()
    content = c_coder.get_code("Ajax")
    print(content)