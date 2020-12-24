# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/constrant/database_configuration.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import configuration
from summermvc.field import ValueField

@configuration
class DBConfiguration(object):
    host = ValueField('127.0.0.1')
    port = ValueError(3306)

    def __str__(self):
        return '%s{host=%s, port=%s}' % (self.__class__.__name__,
         self.host, self.port)