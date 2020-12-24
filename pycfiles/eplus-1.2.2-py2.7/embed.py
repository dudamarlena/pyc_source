# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eplus/embed.py
# Compiled at: 2018-02-18 11:47:36
embed = None
if not embed:
    try:
        from IPython import embed
    except ImportError:
        pass

if not embed:
    try:
        from IPython.Shell import IPShell

        def embed():
            shell = IPShell(argv=[])
            shell.mainloop()


    except ImportError:
        pass

if not embed:
    try:
        from bpython import embed
    except ImportError:
        pass

if not embed:
    from code import interact as embed