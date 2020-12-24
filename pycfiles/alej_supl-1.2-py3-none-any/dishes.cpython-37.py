# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/andrefs/Academia/docente_2018_19_dium/SPLN/spln-docs/slides/aula-03/aleixo50/aleixo50/dishes.py
# Compiled at: 2018-10-11 11:45:14
# Size of source mod 2**32: 239 bytes
import os, json
from .dish import Dish
dishes = []
with open(os.path.join(os.path.dirname(__file__), 'recipes.json'), 'r') as (json_file):
    _recipes = json.loads(json_file.read())
    dishes = [Dish(r['name']) for r in _recipes]