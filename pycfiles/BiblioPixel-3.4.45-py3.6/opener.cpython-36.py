# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/remote/opener.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 684 bytes
import threading, time, webbrowser
from ...util import log
WEBPAGE_OPENED = False

def opener(ip_address, port, delay=1):
    """
    Wait a little and then open a web browser page for the control panel.
    """
    global WEBPAGE_OPENED
    if WEBPAGE_OPENED:
        return
    WEBPAGE_OPENED = True
    raw_opener(ip_address, port, delay)


def raw_opener(ip_address, port, delay=1):
    """
    Wait a little and then open a web browser page for the control panel.
    """

    def target():
        time.sleep(delay)
        url = 'http://%s:%d' % (ip_address, port)
        webbrowser.open(url, new=0, autoraise=True)

    threading.Thread(target=target, daemon=True).start()