# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/ZombieAgent/main.py
# Compiled at: 2012-01-03 20:40:36
import ZombieAgent.CLI, sys, logging

def main():
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('ZombieAgent')
    try:
        ZombieAgent.CLI.parse()
        return 0
    except Exception, e:
        log.exception('')
        return 1


if __name__ == '__main__':
    sys.exit(main())