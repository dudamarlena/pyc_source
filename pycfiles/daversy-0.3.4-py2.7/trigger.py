# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\trigger.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import Trigger

class TriggerBuilder(object):
    """Represents a builder for a trigger."""
    DbClass = Trigger
    XmlTag = 'trigger'
    Query = '\n        SELECT trigger_name, table_name, lower(base_object_type) AS type,\n               replace(dbms_metadata.get_ddl(\'TRIGGER\', trigger_name),\n                       \'"\' || user || \'".\') AS definition\n        FROM   sys.user_triggers\n        ORDER BY trigger_name\n    '
    PropertyList = odict((
     'TRIGGER_NAME', Property('name')), (
     'TYPE', Property('object-type')), (
     'TABLE_NAME', Property('object-name')), (
     'DEFINITION', Property('definition', None, lambda x: x.read(), cdata=True)))

    @staticmethod
    def addToState(state, trigger):
        trigger.definition = trim_spaces(trigger.definition)
        state.triggers[trigger.name] = trigger

    @staticmethod
    def createSQL(trigger):
        return trigger.definition + '\n\n'