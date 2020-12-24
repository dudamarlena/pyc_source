# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/test/_testMonitoring.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 736 bytes


def TestOut():
    """Module self test

    """
    m = MonitorOut(store=(storing.Store()))
    print('ready to go')
    status = m.start()
    while not (status == STOPPED or status == ABORTED):
        status = m.run()


def Test():
    """Module self test

    """
    import storing
    m = Monitor(store=(storing.Store()))
    print('ready to go')
    status = m.start()
    while not (status == STOPPED or status == ABORTED):
        try:
            status = m.run()
        except KeyboardInterrupt:
            print('    Keyboard Interrupt manual shutdown of taskers ...')
            m.server.close()
            break


if __name__ == '__main__':
    Test()