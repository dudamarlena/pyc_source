# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/cloud.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 693 bytes
import socket
from time import sleep
from bookshelf.api_v2.logging_helpers import log_yellow

def is_ssh_available(host, port=22):
    """ checks if ssh port is open """
    s = socket.socket()
    try:
        s.connect((host, port))
        return True
    except:
        return False


def wait_for_ssh(host, port=22, timeout=600):
    """ probes the ssh port and waits until it is available """
    log_yellow('waiting for ssh...')
    for iteration in xrange(1, timeout):
        sleep(1)
        if is_ssh_available(host, port):
            return True
        log_yellow('waiting for ssh...')