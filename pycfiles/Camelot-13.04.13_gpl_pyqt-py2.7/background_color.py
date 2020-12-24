# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/background_color.py
# Compiled at: 2013-04-11 17:47:52
"""This Admin class turns the background of a Person's first
name pink if its first name doesn't start with a capital"""
from PyQt4.QtGui import QColor
from camelot.model.party import Person

def first_name_background_color(person):
    import string
    if person.first_name:
        if person.first_name[0] not in string.uppercase:
            return QColor('pink')


class Admin(Person.Admin):
    field_attributes = {'first_name': {'background_color': first_name_background_color}}