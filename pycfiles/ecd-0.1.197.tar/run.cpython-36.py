# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\pycharm_project\ecd\ecd\password_manage\run.py
# Compiled at: 2019-05-07 08:38:10
# Size of source mod 2**32: 971 bytes
"""
@author:ZouLingyun
@date:
@summary:
"""
import platform, time, webbrowser
from concurrent.futures import ThreadPoolExecutor
from ecd.password_manage.app.password_web import app

def open_browser(url):
    if platform.system() == 'MacOS':
        chrome_path = 'open -a /Applications/Google\\ Chrome.app %s'
    else:
        if platform.system() == 'Windows':
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        else:
            if platform.system() == 'Linux':
                chrome_path = '/usr/bin/google-chrome %s'
            else:
                raise SystemError('无法确定当前平台')
    webbrowser.get(chrome_path).open(url)


def main():
    host = '127.0.0.1'
    port = 9000
    m_pool = ThreadPoolExecutor(1)
    m_pool.submit((app.run), host=host, port=port)
    time.sleep(2)
    open_browser('http://{host}:{port}/'.format(host=host, port=port))


if __name__ == '__main__':
    main()