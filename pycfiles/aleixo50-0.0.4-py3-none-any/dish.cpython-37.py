# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/andrefs/Academia/docente_2018_19_dium/SPLN/spln-docs/slides/aula-03/aleixo50/aleixo50/dish.py
# Compiled at: 2018-10-11 11:30:49
# Size of source mod 2**32: 370 bytes


class Dish(object):

    def __init__(self, name, ingredients=[], instructions=[]):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def __repr__(self):
        return 'Dish({0.name!r}, {0.ingredients!r}, {0.instructions!r})'.format(self)

    def __str__(self):
        return 'Dish({0.name})'.format(self)