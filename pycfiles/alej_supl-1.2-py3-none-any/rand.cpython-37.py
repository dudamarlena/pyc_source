# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/andrefs/Academia/docente_2018_19_dium/SPLN/spln-docs/slides/aula-03/aleixo50/aleixo50/rand.py
# Compiled at: 2018-10-11 11:51:47
# Size of source mod 2**32: 88 bytes
import random
from .dishes import dishes

def rand():
    return random.choice(dishes)