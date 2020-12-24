# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrefs/Academia/docente_2018_19_dium/SPLN/spln-docs/slides/aula-03/aleixo50/aleixo50/dishes.py
# Compiled at: 2018-10-11 11:45:14
# Size of source mod 2**32: 239 bytes
import os, json
from .dish import Dish
dishes = []
with open(os.path.join(os.path.dirname(__file__), 'recipes.json'), 'r') as (json_file):
    _recipes = json.loads(json_file.read())
    dishes = [Dish(r['name']) for r in _recipes]