# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/firethorn/utils/type_helpers.py
# Compiled at: 2019-02-10 20:15:10
# Size of source mod 2**32: 1154 bytes
"""
Created on Nov 8, 2012

Helper functions for type checking etc

@author: stelios
"""
import config

def isCatalog(value):
    """
    Check whether value is of schema type
    """
    return value == config.types['jdbc_catalog'] or value == config.types['adql_catalog']


def isSchema(value):
    """
    Check whether value is of schema type
    """
    return value == config.types['jdbc_schema'] or value == config.types['adql_schema']


def isTable(value):
    """
    Check whether value is of table type
    """
    return value == config.types['jdbc_table'] or value == config.types['adql_table']


def isColumn(value):
    """
    Check whether value is of column type
    """
    return value == config.types['jdbc_column'] or value == config.types['adql_column']


def isRootType(value):
    """
    Check whether value is of type adql service or jdbc resource
    """
    return value == config.types['service'] or value == config.types['resource'] or value == config.types['Workspace']


def isWorkspace(value):
    """
    Check whether value is of type adql service or jdbc resource
    """
    return value == config.types['Workspace']