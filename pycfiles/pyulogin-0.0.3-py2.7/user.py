# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyulogin/user.py
# Compiled at: 2014-03-05 06:52:49
"""
Copyright (c)2014 Gurov Dmitri 

See the file license.txt for copying permission.

UloginUser -- basic class with information about user. Class'es field were created dynamicly from    
fields parametr of constructor. 

 
fields -- dictionary with necessary for developer fields.  class field id obtain vlue from field 'uid'     
"""

class UloginUser:

    def __init__(self, fields):
        for field in fields.keys():
            setattr(self, field, fields[field])

        self.id = fields['uid']