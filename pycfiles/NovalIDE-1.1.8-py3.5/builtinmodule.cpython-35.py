# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/parser/builtinmodule.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1620 bytes
import sys, os, nodeast, config

class BuiltinModule(nodeast.BuiltinNode):
    type_d = {'int': config.ASSIGN_TYPE_INT, 
     'str': config.ASSIGN_TYPE_STR, 
     'list': config.ASSIGN_TYPE_LIST, 
     'tuple': config.ASSIGN_TYPE_TUPLE, 
     'dict': config.ASSIGN_TYPE_DICT, 
     'float': config.ASSIGN_TYPE_FLOAT, 
     'long': config.ASSIGN_TYPE_LONG, 
     'bool': config.ASSIGN_TYPE_BOOL, 
     'set': config.ASSIGN_TYPE_SET, 
     'file': config.ASSIGN_FILE_OBJECT}

    def __init__(self, name):
        super(BuiltinModule, self).__init__(name, config.NODE_MODULE_TYPE, None, True)
        self.type_objects = {}

    def load(self, datas):
        for data in datas['childs']:
            builtin_node = nodeast.BuiltinNode(data['name'], data['type'], self)
            if data['name'] in self.type_d:
                obj_type = self.type_d[data['name']]
                self.type_objects[obj_type] = builtin_node
            if 'childs' in data:
                for child in data['childs']:
                    child_node = nodeast.BuiltinNode(child['name'], child['type'], builtin_node)

    def GetTypeNode(self, value_type):
        type_obj = self.type_objects[value_type]
        return type_obj

    def IsBuiltInTypeOrMethod(self, name):
        if self.type_d.has_key(name):
            return True
        return False

    def GetBuiltInTypeMembers(self, name):
        if self.IsBuiltInTypeOrMethod(name):
            obj_type = self.type_d[name]
            return (
             True, self.type_objects[obj_type].GetMemberList())
        return (
         False, [])