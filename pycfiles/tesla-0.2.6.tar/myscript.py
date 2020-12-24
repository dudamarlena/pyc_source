# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/ProjectName/projectname/scripts/myscript.py
# Compiled at: 2007-09-06 07:54:51
from paste.deploy import loadapp

def run(filename):
    """Write your commands here."""
    app = loadapp('config:' + filename)
    from projectname import model
    model.connect()