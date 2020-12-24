# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/p.vorobyov/PycharmProjects/exyaru/commands/run.py
# Compiled at: 2019-01-24 02:56:39
from commands import Command

class Run(Command):

    def run(self):
        from app import app
        app.run(debug=True)