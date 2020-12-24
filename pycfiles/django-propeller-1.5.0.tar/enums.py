# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/enums.py
# Compiled at: 2017-03-08 15:32:04
try:
    from enum import Enum
except ImportError:
    from enum34 import Enum

class NavbarItemTypes(Enum):
    link = 1
    dropdown = 2
    divider = 3


class CardItemTypes(Enum):
    header = 1
    media = 2
    media_actions = 3
    actions = 4
    title = 5
    subtitle = 6