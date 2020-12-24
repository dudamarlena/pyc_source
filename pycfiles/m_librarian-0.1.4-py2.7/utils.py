# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/web/utils.py
# Compiled at: 2018-04-08 18:11:23
from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB
from os import path, remove
import socket
lock_fname = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'tmp', 'm_librarian.lock')

def get_lock(port):
    try:
        lock_file = open(lock_fname, 'r')
    except IOError:
        pass
    else:
        try:
            flock(lock_file, LOCK_EX | LOCK_NB)
        except IOError:
            port = int(lock_file.readline())
            lock_file.close()
            return (None, port)

        flock(lock_file, LOCK_UN)
        lock_file.close()

    lock_file = open(lock_fname, 'w')
    lock_file.write(str(port))
    lock_file.close()
    lock_file = open(lock_fname, 'r')
    flock(lock_file, LOCK_EX | LOCK_NB)
    return (lock_file, None)


def close_lock(lock_file):
    flock(lock_file, LOCK_UN)
    lock_file.close()
    lock_file = open(lock_fname, 'w')
    lock_file.write('')
    lock_file.close()
    remove(lock_fname)


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port