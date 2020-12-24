# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/sensei/handlers/base.py
# Compiled at: 2015-11-10 12:09:15
from random import randint
from termcolor import colored, cprint
import inspect

class HandlerException(Exception):

    def __init__(self, message):
        self.message = message


class BaseHandler(object):

    def __init__(self):
        self.overrides = {}

    @property
    def weight(self):
        return len(inspect.getmro(self.get_handled_class()))

    def is_my_field(self, field):
        return isinstance(field, self.get_handled_class())

    def get_handled_class(self):
        return self.handled_class

    def set_override_func(self, field, override_func):
        self.overrides[field.attname] = override_func

    def pre_handle(self, obj, field, sensei):
        if getattr(field, 'null', False) is True and randint(0, 1) == 1:
            return
        return self.handle(obj, field, sensei)

    def handle(self, obj, field, sensei):
        if hasattr(self, 'object_mode'):
            self.object_mode(obj, field, sensei)
            return
        if field.attname in self.overrides:
            value = self.overrides[field.attname](obj, field, sensei)
        else:
            value = self.prepare_value(obj, field, sensei)
        try:
            field.validate(value, obj)
        except Exception as e:
            print cprint('Invalid value %s for field <b>%s. Django error:%s' % (value, field.attname, str(e)), 'red')
            raise e

        setattr(obj, field.attname, value)

    def prepare_value(self, obj, field, sensei):
        raise NotImplemented