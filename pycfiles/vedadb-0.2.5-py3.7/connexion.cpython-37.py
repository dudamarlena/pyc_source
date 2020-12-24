# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vedadb/connexion.py
# Compiled at: 2019-09-13 10:24:05
# Size of source mod 2**32: 531 bytes
import os, simplejson
from pg import DB

def connect(parameters_path):
    with open(parameters_path, 'r') as (fich_p):
        parameters = simplejson.loads(fich_p.read())
        db = DB(dbname=(parameters['dbname']), host=(parameters['dbserver']), port=(parameters['dbport']),
          user=(parameters['dbuser']),
          passwd=(parameters['dbpass']))
        return db