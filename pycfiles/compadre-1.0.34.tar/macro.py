# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compactxml/macro.py
# Compiled at: 2010-03-12 17:45:53


class UndefinedMacro(KeyError):

    def __init__(self, macroType, name):
        assert macroType in ('element', 'attribute')
        self.macroType = macroType
        self.name = name
        KeyError.__init__(self, unicode(self))

    def __unicode__(self):
        return 'No %s macro defined for name "%s".' % (self.macroType, self.name)


class Macros(object):

    def __init__(self):
        self.aAttributes = {}
        self.aElements = {}

    def __str__(self):
        return '<macro.Macros instance with %d attributes and %d elements>' % (len(self.aAttributes), len(self.aElements))

    def __repr__(self):
        return '<macro.Macros instance %r attributes, %r elements>' % (self.aAttributes, self.aElements)

    def __copy__(self):
        macros = Macros()
        macros.aAttributes = self.aAttributes.copy()
        macros.aElements = self.aElements.copy()
        return macros

    def __len__(self):
        return len(self.aAttributes) + len(self.aElements)

    def add_attribute(self, name, expansion, source):
        self.aAttributes[name] = (
         expansion, source)

    def add_element(self, name, aParameters, expansion, source):
        self.aElements[name] = (
         aParameters, expansion, source)

    def attribute(self, name):
        try:
            return self.aAttributes[name]
        except KeyError:
            raise UndefinedMacro('attribute', name)

    def element(self, name):
        try:
            return self.aElements[name]
        except KeyError:
            raise UndefinedMacro('element', name)

    def update(self, macrosToAdd):
        self.aAttributes.update(macrosToAdd.aAttributes)
        self.aElements.update(macrosToAdd.aElements)