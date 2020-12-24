# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_attribute.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import numbers
from pyrpl.modules import Module
from pyrpl.attributes import BoolProperty, FilterProperty, SelectProperty, FloatProperty
from pyrpl.module_attributes import ModuleProperty
from pyrpl.test.test_base import TestPyrpl

class MyFilterProperty(FilterProperty):

    def valid_frequencies(self, module):
        return [ 2 ** n for n in range(14) ]


class FirstSubModule(Module):
    _setup_attributes = [
     'b1', 'b2']
    b1 = BoolProperty()
    b2 = BoolProperty()


class SecondSubModule(Module):
    _setup_attributes = [
     'b1', 'b2']
    b1 = BoolProperty()
    b2 = BoolProperty()


class DummyModule(Module):
    _gui_attributes = [
     'true_or_false']
    true_or_false = BoolProperty()
    some_number = FloatProperty(min=-10, max=10, default=1.414)
    some_filter = MyFilterProperty()
    some_options = SelectProperty(options=['foo', 'bar'])
    sub1 = ModuleProperty(FirstSubModule)
    sub2 = ModuleProperty(SecondSubModule)


class TestAttributeClass(TestPyrpl):
    source_config_file = 'nosetests_source_dummy_module'

    def test_config_file(self):
        assert 'DummyModule' in self.pyrpl.c.pyrpl.modules

    def test_dummy_module(self):
        assert isinstance(self.pyrpl.dummymodule.true_or_false, bool)
        assert isinstance(self.pyrpl.dummymodule.some_number, float)
        assert isinstance(self.pyrpl.dummymodule.some_filter, numbers.Number)
        assert isinstance(self.pyrpl.dummymodule.some_options, str)
        assert self.pyrpl.c.dummymodule.some_number == 3.123, self.pyrpl.c.dummymodule.some_number
        assert self.pyrpl.c.dummymodule.some_number == 3.123, self.pyrpl.c.dummymodule.some_number

    def test_submodule(self):
        self.sub1 = self.pyrpl.dummymodule.sub1
        self.sub2 = self.pyrpl.dummymodule.sub2
        assert self.sub1.b1 == True
        assert self.sub1.b2 == False
        self.sub2.b1 = True
        self.sub2.b2 = False
        assert self.sub2.b1 == True
        assert self.sub2.b2 == False
        self.pyrpl.dummymodule.save_state('true_false_true_false')
        self.sub1.b1 = False
        self.sub1.b2 = True
        assert self.sub1.b1 == False
        assert self.sub1.b2 == True
        self.sub2.b1 = False
        self.sub2.b2 = True
        assert self.sub2.b1 == False
        assert self.sub2.b2 == True
        self.pyrpl.dummymodule.load_state('true_false_true_false')
        assert self.sub1.b1 == True
        assert self.sub1.b2 == False
        assert self.sub2.b1 == True
        assert self.sub2.b2 == False