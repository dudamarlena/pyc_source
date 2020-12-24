# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\magic.py
# Compiled at: 2017-12-11 20:12:50
import runpy, sys
from .monkeypatch import patch_all
from .app import install_stackless
import stackless
from . import main

def run():
    try:
        try:
            if len(sys.argv) > 1:
                target = sys.argv.pop(1)
                if target == '-m' and len(sys.argv) > 1:
                    target = sys.argv.pop(1)
                    runpy.run_module(target, run_name='__main__', alter_sys=True)
                else:
                    runpy.run_path(target, run_name='__main__')
        except Exception:
            main.mainloop.exception = sys.exc_info()
            raise

    finally:
        main.mainloop.running = False


if __name__ == '__main__':
    patch_all()
    install_stackless()
    stackless.tasklet(run)()
    main.mainloop.run()