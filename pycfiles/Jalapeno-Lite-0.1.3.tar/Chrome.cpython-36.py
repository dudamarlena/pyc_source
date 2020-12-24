# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/Gutils/Chrome.py
# Compiled at: 2017-03-24 00:57:55
# Size of source mod 2**32: 656 bytes


def Browse(listen):
    from cefpython3 import cefpython as cef
    import platform, sys

    def check_versions():
        print('[hello_world.py] CEF Python {ver}'.format(ver=(cef.__version__)))
        print('[hello_world.py] Python {ver} {arch}'.format(ver=(platform.python_version()),
          arch=(platform.architecture()[0])))
        assert cef.__version__ >= '55.3', 'CEF Python v55.3+ required to run this'

    check_versions()
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url='https://127.0.0.1:5588')
    cef.MessageLoop()
    cef.Shutdown()