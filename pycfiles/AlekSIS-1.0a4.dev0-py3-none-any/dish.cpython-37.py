# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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