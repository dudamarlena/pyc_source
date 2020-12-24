# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/background_color.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = "This Admin class turns the background of a Person's first\nname pink if its first name doesn't start with a capital"
from PyQt4.QtGui import QColor
from camelot.model.party import Person

def first_name_background_color(person):
    import string
    if person.first_name:
        if person.first_name[0] not in string.uppercase:
            return QColor('pink')


class Admin(Person.Admin):
    field_attributes = {'first_name': {'background_color': first_name_background_color}}