# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jorge/pyscrap3/pyscrap3/templateUtils/hooks.py
# Compiled at: 2014-04-02 11:52:44
# Size of source mod 2**32: 509 bytes
import os, mrbob
from datetime import datetime

def checkName(configurator, question, answer):
    print('nombre: ' + answer)
    proyectPath = os.getcwd() + '/' + answer
    print('path ' + proyectPath)
    if not os.path.exists(proyectPath):
        print('no existe, ok')
    else:
        print("Directory '" + answer + "' already exists!")
        raise mrbob.bobexceptions.ValidationError
    return answer


def setCurrentYear(configurator, question):
    question.default = datetime.now().year