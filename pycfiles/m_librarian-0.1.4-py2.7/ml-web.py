# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/scripts-2.7/ml-web.py
# Compiled at: 2018-06-11 10:19:13
import argparse, time, webbrowser
from bottle import thread
from m_librarian.db import open_db
import m_librarian.web.app
from m_librarian.web.server import run_server
from m_librarian.web.utils import get_lock, close_lock, get_open_port

def start_browser(port):
    time.sleep(1)
    webbrowser.open_new('http://localhost:%d/' % port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Init')
    parser.add_argument('-p', '--port', help='HTTP server port')
    args = parser.parse_args()
    if args.port:
        port = args.port
    else:
        port = get_open_port()
    lock_file, old_port = get_lock(port)
    if lock_file:
        open_db()
        thread.start_new_thread(start_browser, (port,))
        run_server(port=port)
        close_lock(lock_file)
    else:
        start_browser(old_port)