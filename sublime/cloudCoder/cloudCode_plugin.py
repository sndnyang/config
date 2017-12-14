#coding=utf-8
import re
import sys

sys.path.append(r"G:\project\other\Tools\pythonlib")

import sublime
import sublime_plugin

from imp import reload
import CloudCoder
reload(CloudCoder)

c_coder = CloudCoder.CloudCoder()

class cloudcoderCommand(sublime_plugin.TextCommand):
    def run(self, edit, method):
        if method == 'get':
            self.get(edit)
        elif method == 'post':
            self.post(edit)

    def get(self, edit):
        match = self.view.find('@cloud:(.+)', 0, sublime.IGNORECASE)
        content = self.view.substr(match)
        pattern = '@cloud:(.+)'
        if re.match(pattern, content):
            content = re.match(pattern, content).group(1)
            split = content.split('?')
            search_words = split[0]
            if len(split) == 2:
                content = c_coder.get_code(search_words, split[1].split())
            else:
                content = c_coder.get_code(content)
            if content.startswith("Error: "):
                sublime.message_dialog(content)
                return
            if content.startswith("\nOptions:"):
                self.view.insert(edit, match.end(), content)
            else:
                self.view.replace(edit, match, content)

    def post(self, edit):
        contents = self.view.substr(sublime.Region(0, self.view.size()))
        response = c_coder.post_code({"content": contents})
        print(response)
        sublime.message_dialog(response['error'])
        