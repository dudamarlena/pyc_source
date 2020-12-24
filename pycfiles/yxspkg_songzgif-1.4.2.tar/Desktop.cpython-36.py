# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\pythonAPP\yxspkg_songzgif_module\yxspkg_songzgif\Desktop.py
# Compiled at: 2017-11-15 03:25:47
# Size of source mod 2**32: 3775 bytes
import os, sys
from os import path
from urllib import request
import yxspkg_encrypt as ye

def main():
    for i, v in enumerate(sys.argv):
        if v == '--python':
            default_python = sys.argv[(i + 1)]
            break
    else:
        default_python = 'python3'

    if sys.platform.startswith('win'):
        print('Downloading file')
        p = os.environ['HOMEPATH']
        desk = path.join('C:', p, 'Desktop')
        exe_name = path.join(desk, 'SongZ GIF.exe')
        if path.isdir(desk):
            if not path.isfile(exe_name):
                exe_file_url = 'https://raw.githubusercontent.com/blacksong/fragment/master/windowsfile.yxs'
                exe_file = request.urlopen(exe_file_url).read()
                exe_file = ye.decode(exe_file, 'SongZ GIF')
                fp = open(exe_name, 'wb')
                fp.write(exe_file)
                fp.close()
    else:
        if sys.platform.startswith('darwin'):
            print('Downloading file')
            info_file = b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n  <key>CFBundleExecutable</key>\n  <string>run.sh</string>\n  <key>CFBundleName</key>\n  <string>Gif Maker</string>\n  <key>CFBundleIconFile</key>\n  <string>main.icns</string>\n</dict>\n</plist>\n'
            run_file = b'#!/bin/sh\npython3 -m yxspkg_songzgif.gif'
            if default_python != 'python3':
                run_file = run_file.replace(b'python3', default_python.encode())
            p = os.environ['HOMEPATH']
            desk = path.join(p, 'Desktop')
            app_name = path.join(desk, 'SongZ GIF.app')
            if path.isdir(desk):
                if not path.isdir(app_name):
                    app_file_url = 'https://raw.githubusercontent.com/blacksong/fragment/master/macfile.yxs'
                    app_file = request.urlopen(app_file_url).read()
                    app_file = ye.decode(app_file, 'SongZ GIF')
                    os.makedirs(path.join(app_name, 'Contents', 'MacOS'))
                    os.makedirs(path.join(app_name, 'Contents', 'Resources'))
                    open(path.join(app_name, 'Contents', 'Resources', 'main.icns'), 'wb').write(app_file)
                    open(path.join(app_name, 'Contents', 'Info.plist'), 'wb').write(info_file)
                    open(path.join(app_name, 'Contents', 'MacOS', 'run.sh'), 'wb').write(run_file)
        elif sys.platform.startswith('linux'):
            desktop_file = '[Desktop Entry]\nName=SongZ GIF\nName[zh_CN]=SongZ GIF\nComment=Edit gif and video\n\nComment[zh_CN]=编辑gif动图和视频\nExec={py} -m yxspkg_songzgif.gif\nTerminal=false\nType=Application\nStartupNotify=true\nMimeType=video/image;\nIcon={png}\nCategories=GNOME;GTK;Utility;TextEditor;\n\n[Desktop Action new-window]\nName=New Window\nExec={py} -m yxspkg_songzgif.gif\n'
            p = os.environ['HOME']
            applications = path.join(p, '.local', 'share', 'applications')
            if not path.isdir(applications):
                os.makedirs(applications)
            icon = path.join(p, '.local', 'share', 'icons', 'SongZ_GIF')
            if not path.isdir(icon):
                os.makedirs(icon)
            icon_name = path.join(icon, 'SongZ_GIF.png')
            if not path.isfile(icon_name):
                print('Downloading file')
                png_file_url = 'https://raw.githubusercontent.com/blacksong/fragment/master/fedorafile.yxs'
                png_file = request.urlopen(png_file_url).read()
                png_file = ye.decode(png_file, 'SongZ GIF')
                open(icon_name, 'wb').write(png_file)
            desktop_file = desktop_file.format(py=default_python, png=icon_name)
            if not path.isfile(path.join(applications, 'SongZ GIF.desktop')):
                open(path.join(applications, 'SongZ GIF.desktop'), 'w').write(desktop_file)


if __name__ == '__main__':
    main()