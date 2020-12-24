# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrefs/Academia/docente_2018_19_dium/SPLN/spln-docs/slides/aula-03/aleixo50/aleixo50/rand.py
# Compiled at: 2018-10-11 11:51:47
# Size of source mod 2**32: 88 bytes
import random
from .dishes import dishes

def rand():
    return random.choice(dishes)