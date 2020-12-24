# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/script/db.py
# Compiled at: 2007-03-21 14:34:41
"""Description of module.

For copyright, license, and warranty, see bottom of file.
"""
from schevo.script.command import CommandSet
from schevo.script import db_create, db_inject, db_evolve, db_update

class Database(CommandSet):
    __module__ = __name__
    name = 'Database Activities'
    description = 'Perform actions on Schevo databases.'

    def __init__(self):
        self.commands = {'create': db_create.start, 'inject': db_inject.start, 'evolve': db_evolve.start, 'update': db_update.start}


start = Database