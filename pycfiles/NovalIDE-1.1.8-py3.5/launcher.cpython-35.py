# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/launcher.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1072 bytes
import os, sys, noval.util.apputils as apputils
from noval import model
if apputils.is_py2():
    reload(sys)
    sys.setdefaultencoding('utf-8')

def run(language):
    execDir = os.path.dirname(sys.executable)
    try:
        sys.path.index(execDir)
    except ValueError:
        sys.path.append(execDir)

    if language == model.LANGUAGE_PYTHON:
        import noval.python.pyide
        app = noval.python.pyide.PyIDEApplication()
    app.mainloop()