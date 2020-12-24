# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/informer/config.py
# Compiled at: 2020-05-08 00:03:26
# Size of source mod 2**32: 542 bytes
MAX_LENGTH = 65471
PUBLICT_IP = '127.0.0.1'
PORT_DICT = {'vision':10001, 
 'sensor':10002, 
 'cmd':10003, 
 'debug':10004, 
 'clock':10005, 
 'message':10006, 
 'sim':10007}
RECV_KEYS = [
 'cmd', 'message', 'sim', 'clock']
REGISTER_KEYS = list(PORT_DICT.keys())
colors = [
 'black', 'white', 'darkGray', 'gray', 'lightGray', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'darkRed', 'darkGreen', 'darkBlue', 'darkCyan', 'darkMagenta', 'darkYellow']