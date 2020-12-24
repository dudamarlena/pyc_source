# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\tests\test_core.py
# Compiled at: 2010-12-23 17:42:44
"""Core test suite mainly adopted from Trac."""
from seishub.core.exceptions import SeisHubError
from seishub.core.core import Interface, Component, implements
import unittest

class ITest(Interface):

    def test(self):
        """Dummy function."""
        pass


class ComponentTestCase(unittest.TestCase):

    def setUp(self):
        from seishub.core.core import ComponentManager, ComponentMeta
        self.compmgr = ComponentManager()
        self.old_registry = ComponentMeta._registry
        ComponentMeta._registry = {}

    def tearDown(self):
        from seishub.core.core import ComponentMeta
        ComponentMeta._registry = self.old_registry

    def test_base_class_not_registered(self):
        """
        Make sure that the Component base class does not appear in the component
        registry.
        """
        from seishub.core.core import ComponentMeta
        assert Component not in ComponentMeta._components
        self.assertRaises(SeisHubError, self.compmgr.__getitem__, Component)

    def test_abstract_component_not_registered(self):
        """
        Make sure that a Component class marked as abstract does not appear in
        the component registry.
        """
        from seishub.core.core import ComponentMeta

        class AbstractComponent(Component):
            abstract = True

        assert AbstractComponent not in ComponentMeta._components
        self.assertRaises(SeisHubError, self.compmgr.__getitem__, AbstractComponent)

    def test_unregistered_component(self):
        """
        Make sure the component manager refuses to manage classes not derived
        from `Component`.
        """

        class NoComponent(object):
            pass

        self.assertRaises(SeisHubError, self.compmgr.__getitem__, NoComponent)

    def test_component_registration(self):
        """
        Verify that classes derived from `Component` are managed by the
        component manager.
        """

        class ComponentA(Component):
            pass

        assert self.compmgr[ComponentA]
        assert ComponentA(self.compmgr)

    def test_component_identity--- This code section failed: ---

 L.  91         0  LOAD_CONST               'ComponentA'
                3  LOAD_GLOBAL           0  'Component'
                6  BUILD_TUPLE_1         1 
                9  LOAD_CODE                <code_object ComponentA>
               12  MAKE_FUNCTION_0       0  None
               15  CALL_FUNCTION_0       0  None
               18  BUILD_CLASS      
               19  STORE_FAST            1  'ComponentA'

 L.  93        22  LOAD_FAST             1  'ComponentA'
               25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  'compmgr'
               31  CALL_FUNCTION_1       1  None
               34  STORE_FAST            2  'c1'

 L.  94        37  LOAD_FAST             1  'ComponentA'
               40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             1  'compmgr'
               46  CALL_FUNCTION_1       1  None
               49  STORE_FAST            3  'c2'

 L.  95        52  LOAD_FAST             2  'c1'
               55  LOAD_FAST             3  'c2'
               58  COMPARE_OP            8  is
               61  POP_JUMP_IF_TRUE     73  'to 73'
               64  LOAD_ASSERT              AssertionError
               67  LOAD_CONST               'Expected same component instance'
               70  RAISE_VARARGS_2       2  None

 L.  96        73  LOAD_FAST             0  'self'
               76  LOAD_ATTR             1  'compmgr'
               79  LOAD_FAST             1  'ComponentA'
               82  BINARY_SUBSCR    
               83  STORE_FAST            3  'c2'

 L.  97        86  LOAD_FAST             2  'c1'
               89  LOAD_FAST             3  'c2'
               92  COMPARE_OP            8  is
               95  POP_JUMP_IF_TRUE    107  'to 107'
               98  LOAD_ASSERT              AssertionError
              101  LOAD_CONST               'Expected same component instance'
              104  RAISE_VARARGS_2       2  None

Parse error at or near `LOAD_CONST' instruction at offset 101

    def test_component_initializer(self):
        """
        Makes sure that a components' `__init__` method gets called.
        """

        class ComponentA(Component):

            def __init__(self):
                self.data = 'test'

        self.assertEqual('test', ComponentA(self.compmgr).data)
        ComponentA(self.compmgr).data = 'newtest'
        self.assertEqual('newtest', ComponentA(self.compmgr).data)

    def test_inherited_component_initializer(self):
        """
        Makes sure that a the `__init__` method of a components' super-class
        gets called if the component doesn't override it.
        """

        class ComponentA(Component):

            def __init__(self):
                self.data = 'foo'

        class ComponentB(ComponentA):

            def __init__(self):
                self.data = 'bar'

        class ComponentC(ComponentB):
            pass

        self.assertEqual('bar', ComponentC(self.compmgr).data)
        ComponentC(self.compmgr).data = 'baz'
        self.assertEqual('baz', ComponentC(self.compmgr).data)

    def test_implements_called_outside_classdef(self):
        """
        Verify that calling implements() outside a class definition raises an
        `AssertionError`.
        """
        try:
            implements()
            self.fail('Expected AssertionError')
        except AssertionError:
            pass

    def test_implements_called_twice(self):
        """
        Verify that calling implements() twice in a class definition raises an
        `AssertionError`.
        """
        try:

            class ComponentA(Component):
                implements()
                implements()

            self.fail('Expected AssertionError')
        except TypeError:
            pass
        except AssertionError:
            pass

    def test_attribute_access(self):
        """
        Verify that accessing undefined attributes on components raises an
        `AttributeError`.
        """

        class ComponentA(Component):
            pass

        comp = ComponentA(self.compmgr)
        try:
            comp.foo
            self.fail('Expected AttributeError')
        except AttributeError:
            pass

    def test_inherited_implements(self):
        """
        Verify that a component with a super-class implementing an extension
        point interface is also registered as implementing that interface.
        """

        class BaseComponent(Component):
            implements(ITest)
            abstract = True

        class ConcreteComponent(BaseComponent):
            pass

        from seishub.core.core import ComponentMeta
        assert ConcreteComponent in ComponentMeta._registry[ITest]

    def test_instantiation_doesnt_enable(self):
        """
        Make sure that a component disabled by the ComponentManager is not
        implicitly enabled by instantiating it directly.
        """
        from seishub.core.core import ComponentManager

        class DisablingComponentManager(ComponentManager):

            def isComponentEnabled(self, cls):
                return False

        class ComponentA(Component):
            pass

        mgr = DisablingComponentManager()
        ComponentA(mgr)
        self.assertEqual(None, mgr[ComponentA])
        return


def suite():
    return unittest.makeSuite(ComponentTestCase, 'test')


if __name__ == '__main__':
    unittest.main()