# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vlad/source/pySSHChat/pysshchat/__init__.py
# Compiled at: 2018-04-17 05:46:41
# Size of source mod 2**32: 443 bytes
import logging
logging.basicConfig(level=logging.WARN)

def init():
    from pysshchat.variables.loads import commands, config, text
    config()
    text()
    commands()


def run():
    from pysshchat.chats.server import run
    try:
        run()
    except KeyboardInterrupt as e:
        print('ee')
    except Exception as e:
        logging.exception(e)


def start():
    init()
    run()


if __name__ == '__main__':
    start()