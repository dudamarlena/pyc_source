# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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