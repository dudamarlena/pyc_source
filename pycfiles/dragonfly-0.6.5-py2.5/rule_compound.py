# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\rule_compound.py
# Compiled at: 2009-03-09 03:09:58
"""
CompoundRule class
============================================================================

The CompoundRule class is designed to make it very easy to create a rule 
based on a single compound spec.

This rule class has the following parameters to customize its behavior:

 - *spec* -- compound specification for the rule's root element
 - *extras* -- extras elements referenced from the compound spec
 - *defaults* -- default values for the extras
 - *exported* -- whether the rule is exported
 - *context* -- context in which the rule will be active

Each of these parameters can be passed as a (keyword) arguments to the 
constructor, or defined as a class attribute in a derived class.

Example usage
............................................................................

The CompoundRule class can be used to define a voice-command as follows::

    class ExampleRule(CompoundRule):

        spec = "I want to eat <food>"
        extras = [Choice("food", {
                                  "(an | a juicy) apple": "good",
                                  "a [greasy] hamburger": "bad",
                                 }
                        )
                 ]

        def _process_recognition(self, node, extras):
            good_or_bad = extras["food"]
            print "That is a %s idea!" % good_or_bad

    rule = ExampleRule()
    grammar.add_rule(rule)

Class reference
............................................................................

"""
from .rule_base import Rule
from .elements import ElementBase, Compound

class CompoundRule(Rule):
    """
        Rule class based on the compound element.

        Constructor arguments:
         - *name* (*str*) -- the rule's name
         - *spec* (*str*) -- compound specification for the rule's
           root element
         - *extras* (sequence) -- extras elements referenced from the
           compound spec
         - *defaults* (*dict*) -- default values for the extras
         - *exported* (boolean) -- whether the rule is exported
         - *context* (*Context*) -- context in which the rule will be active

    """
    _name = None
    spec = None
    extras = ()
    defaults = ()
    exported = True
    context = None

    def __init__(self, name=None, spec=None, extras=None, defaults=None, exported=None, context=None):
        if name is None:
            name = self._name or self.__class__.__name__
        if spec is None:
            spec = self.spec
        if extras is None:
            extras = self.extras
        if defaults is None:
            defaults = self.defaults
        if exported is None:
            exported = self.exported
        if context is None:
            context = self.context
        assert isinstance(name, (str, unicode))
        assert isinstance(spec, (str, unicode))
        assert isinstance(extras, (list, tuple))
        for item in extras:
            assert isinstance(item, ElementBase)

        assert exported == True or exported == False
        self._name = name
        self._spec = spec
        self._extras = dict(((element.name, element) for element in extras))
        self._defaults = dict(defaults)
        child = Compound(spec, extras=self._extras)
        Rule.__init__(self, name, child, exported=exported, context=context)
        return

    def process_recognition(self, node):
        """
            Process a recognition of this rule.

            This method is called by the containing Grammar when this
            rule is recognized.  This method collects information about
            the recognition and then calls *self._process_recognition*.

            - *node* -- The root node of the recognition parse tree.
        """
        extras = dict(self._defaults)
        for (name, element) in self._extras.iteritems():
            extra_node = node.get_child_by_name(name, shallow=True)
            if not extra_node:
                continue
            extras[name] = extra_node.value()

        self._process_recognition(node, extras)

    def _process_recognition(self, node, extras):
        """
            Default recognition processing.

            This is the method which should be overridden in most cases
            to provide derived classes with custom recognition
            processing functionality.

            This default processing method does nothing.

            - *node* -- The root node of the recognition parse tree.
            - *extras* -- A dictionary of all elements from the
              extras list contained within this recognition.
              Maps element name -> element value.
        """
        pass