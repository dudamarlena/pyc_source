# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-admin/phishdetectadmin/__init__.py
# Compiled at: 2020-01-02 10:05:19
# Size of source mod 2**32: 1999 bytes
import os, random, threading, webbrowser
from .app import app
from .config import storage_folder

def logo():
    print("\n         _     _     _         _      _            _   \n        | |   (_)   | |       | |    | |          | |  \n   _ __ | |__  _ ___| |__   __| | ___| |_ ___  ___| |_ \n  | '_ \\| '_ \\| / __| '_ \\ / _` |/ _ \\ __/ _ \\/ __| __|\n  | |_) | | | | \\__ \\ | | | (_| |  __/ ||  __/ (__| |_ \n  | .__/|_| |_|_|___/_| |_|\\__,_|\\___|\\__\\___|\\___|\\__|\n  | |                                                  \n  |_|\n\nThis is an administration utility for PhishDetect Nodes.\nA browser page will be launched in few seconds.\nYou can find more information about PhishDetect at: https://phishdetect.io\n    ")


def main():
    logo()
    if not os.path.exists(storage_folder):
        os.makedirs(storage_folder)
    port = 5000 + random.randint(0, 999)
    url = 'http://127.0.0.1:{}'.format(port)
    threading.Timer(1.25, lambda : webbrowser.open(url)).start()
    app.run(port=port, debug=False)


if __name__ == '__main__':
    main()