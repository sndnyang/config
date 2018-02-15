cp G:/project/sndnyang.github.io/pelicanconf.py github.io

cp C:/Users/Administrator/_vimrc vim

cp -rf E:/software/vim/vimfiles/ftdetect vim
cp -rf E:/software/vim/vimfiles/ftplugin vim
cp C:/Users/Administrator/.bashrc .bashrc
cp C:/Users/Administrator/pip/pip.ini pip.ini

sublime="C:/Users/Administrator/AppData/Roaming/Sublime Text 3/Packages/User"
cp "$sublime/SublimeTmpl/templates/md.tmpl" sublime/template
cp "$sublime/SublimeTmpl.sublime-settings" sublime
cp "$sublime/Preferences.sublime-settings" sublime
cp "$sublime/Package Control.sublime-settings" sublime
cp "$sublime/Default (Windows).sublime-keymap" sublime
cp -r "$sublime/../cloudCoder/cloudCoder.py" sublime/cloudCoder/cloudCode_plugin.py

cp G:/project/other/Tools/pythonlib/CloudCoder.py sublime/cloudCoder/CloudCoder.py

echo "OK? enter anything to exit"

read