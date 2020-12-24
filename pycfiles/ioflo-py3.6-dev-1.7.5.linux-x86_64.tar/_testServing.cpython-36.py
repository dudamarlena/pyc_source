# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/test/_testServing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 927 bytes


def TestOpenStuff():
    """    """
    import ioflo.base.storing as storing
    storing.Store.Clear()
    s1 = ServerTask(store=(storing.Store()))
    s2 = ServerTask(store=(storing.Store()))
    print(s1.server.reopen())
    print(s2.server.reopen())


def Test(verbose=False):
    """Module self test

    """
    import ioflo.base.storing as storing, ioflo.base.tasking as tasking
    storing.Store.Clear()
    tasking.Tasker.Clear()
    s = Server(store=(storing.Store()))
    s.store.expose()
    print('ready to go')
    status = s.start()
    while not (status == STOPPED or status == ABORTED):
        try:
            status = s.run()
        except KeyboardInterrupt:
            print('    Keyboard Interrupt manual shutdown of taskers ...')
            s.server.close()
            break


if __name__ == '__main__':
    Test()