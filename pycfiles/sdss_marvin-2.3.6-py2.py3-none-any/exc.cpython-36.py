# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/wtforms-alchemy/wtforms_alchemy/exc.py
# Compiled at: 2018-01-12 14:08:15
# Size of source mod 2**32: 871 bytes


class UnknownTypeException(Exception):

    def __init__(self, column):
        Exception.__init__(self, "Unknown type '%s' for column '%s'" % (
         column.type, column.name))


class InvalidAttributeException(Exception):

    def __init__(self, attr_name):
        Exception.__init__(self, "Model does not contain attribute named '%s'." % attr_name)


class AttributeTypeException(Exception):

    def __init__(self, attr_name):
        Exception.__init__(self, "Model attribute '%s' is not of type ColumnProperty." % attr_name)


class UnknownConfigurationOption(Exception):

    def __init__(self, option):
        Exception.__init__(self, "Unknown configuration option '%s' given." % option)