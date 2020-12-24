# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/sensei/exceptions.py
# Compiled at: 2015-11-10 12:22:43
from termcolor import cprint

class PrecacheCollection(Exception):

    def __init__(self, field, handler, values_count=None, recomendation=None):
        cprint('Cant create collection', 'red', attrs=['bold'])
        cprint('\tHandler: %s' % handler, 'red')
        cprint('\tModel: %s' % field.model, 'red')
        cprint('\tField: %s' % field.attname, 'red')
        cprint('\tRecommendations: %s' % recomendation, 'green')