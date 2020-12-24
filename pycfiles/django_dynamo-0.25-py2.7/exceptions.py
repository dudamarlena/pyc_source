# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dynamo\exceptions.py
# Compiled at: 2011-08-02 15:59:24


class DuplicateFieldName(Exception):
    """
    A field is assigned to a MetaModel with a field name, that already
    exists for that MetaModel
    """
    pass


class DuplicateFieldOrder(Exception):
    """
    A field is assigned to a MetaModel with a field order, that already
    exists for that MetaModel
    """
    pass


class MetaModelAlreadyAssigned(Exception):
    """
    The current instance of the API Model class has already been assigned a
    value to it. It can only have exactly 1 model assigned
    """
    pass


class NoMetaModelAssigned(Exception):
    """
    The current instance of the API Model class has not been assigned a
    value to it yet. Thus no operations can be performed yet.
    """
    pass


class AssignedModelNotOfTypeMetaModel(Exception):
    """
    The assigned model to the API Model class must be an instance of MetaModel
    """
    pass