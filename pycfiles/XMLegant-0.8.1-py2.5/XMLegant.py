# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/XMLegant.py
# Compiled at: 2009-03-30 20:59:19
"""
    XMLegant
    (c) 2009 Bill Zeller
    http://from.bz/
    Version: .6   
    
    This source code is licensed under the BSD License
    The license is available here:
        http://creativecommons.org/licenses/BSD/
"""

class XMLegant:

    def __init__(self, parent=None, name=None):
        self.__dict__['_parent'] = parent
        self.__dict__['_name'] = name
        self.__dict__['_text'] = None
        self.__dict__['_attrs'] = {}
        self.__dict__['_children'] = []
        self.__dict__['_child_names'] = {}
        self.__dict__['_replace_underscores'] = True
        return

    def __call__(self, *args):
        child_dict = self.__dict__['_parent'].__dict__['_child_names'][self.__dict__['_name']]
        if len(child_dict) == 1 and child_dict[0].IsEmpty():
            child = child_dict[0]
        else:
            child = self.__dict__['_parent'].__addChild(self.__dict__['_name'])
        if len(args) == 0:
            return child
        elif len(args) == 1:
            XMLegant.setChild(child, args[0])
        elif len(args) == 2:
            child.__setitem__(args[0], args[1])
        return self.__dict__['_parent']

    def __getattr__(self, name):
        return self.__lastChildByName(name)

    def __setattr__(self, name, value):
        XMLegant.setChild(self.__lastChildByName(name), value)

    def __delattr__(self, name):
        pass

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__dict__['_parent'].__dict__['_child_names'][self.__dict__['_name']][key]
        else:
            return self.__dict__['_attrs'][key]

    def __setitem__(self, key, val):
        if isinstance(key, int):
            child = self.__dict__['_parent'].__dict__['_child_names'][self.__dict__['_name']][key]
            XMLegant.setChild(child, val)
        else:
            self.__dict__['_attrs'][key] = str(val)

    def __repr__(self):
        return '<XMLegant Name=%s, %d Children, text = %s at %#x>' % (
         self.__dict__['_name'], len(self.__dict__['_children']),
         self.__dict__['_text'], id(self))

    def __str__(self):
        return self.__repr__()

    def getParent(self):
        return self.__dict__['_parent']

    def SetReplaceUnderscores(self, replace=True):
        self.__dict__['_replace_underscores'] = replace
        for child in self.__dict__['_children']:
            child.SetReplaceUnderscores(replace)

    def hasAttrs(self):
        return self.__dict__['_attrs'] is not {}

    def hasChildren(self):
        return self.__dict__['_children']

    def __lastChildByName(self, name, create=True):
        if name in self.__dict__['_child_names']:
            return self.__dict__['_child_names'][name][(-1)]
        elif create:
            return self.__addChild(name)
        else:
            return
        return

    def __addChild(self, name):
        return self.__addChildObj(XMLegant(self, name))

    def __addChildObj(self, child):
        if child.__dict__['_name'] not in self.__dict__['_child_names']:
            self.__dict__['_child_names'][child.__dict__['_name']] = []
        self.__dict__['_child_names'][child.__dict__['_name']].append(child)
        self.__dict__['_children'].append(child)
        self.__dict__['_text'] = None
        child.__dict__['_parent'] = self
        return child

    @staticmethod
    def setChild(child, value):
        import copy
        child.deleteChildren()
        if isinstance(value, dict):
            child.__dict__['_attrs'] = copy.copy(value)
        elif isinstance(value, XMLegant):
            import copy
            if value.hasChildren():
                for valChild in value.__dict__['_children']:
                    child.__addChildObj(copy.deepcopy(valChild))

        elif value is None:
            child.__dict__['_text'] = None
        else:
            child.__dict__['_text'] = value.__str__()
        return

    def deleteChildren(self):
        self.__dict__['_child_names'] = {}
        self.__dict__['_children'] = []

    def IsEmpty(self):
        return self.__dict__['_attrs'] == {} and self.__dict__['_children'] == [] and self.__dict__['_text'] is None

    def __deepcopy__(self, memo):
        import copy
        if id(self) in memo:
            return memo[id(self)]
        obj = XMLegant()
        obj.__dict__['_name'] = self.__dict__['_name']
        obj.__dict__['_text'] = self.__dict__['_text']
        obj.__dict__['_attrs'] = copy.copy(self.__dict__['_attrs'])
        memo[id(self)] = obj
        children = self.__dict__['_children'][:]
        for child in children:
            obj.__addChildObj(copy.deepcopy(child, memo))

        return obj

    def toXML(self, header=True, writer=None):
        import xml.etree.ElementTree as ET, StringIO
        if self.__dict__['_parent'] is None:
            if self.hasChildren():
                writer = self.__dict__['_children'][0].toXML(header, None)
            tree = ET.ElementTree(writer)
            output = StringIO.StringIO()
            encoding = self.__dict__['_attrs'].get('encoding', None)
            if not header:
                encoding = None
            tree.write(output, encoding)
            xml = output.getvalue()
            return xml
        if self.__dict__['_replace_underscores']:
            name = self.__dict__['_name'].replace('_', ':')
        else:
            name = self.__dict__['_name']
        if writer is None:
            el = ET.Element(name)
        else:
            el = ET.SubElement(writer, name)
        if self.hasAttrs():
            for key in self.__dict__['_attrs']:
                if self.__dict__['_replace_underscores']:
                    el.set(key.replace('_', ':'), self.__dict__['_attrs'][key])
                else:
                    el.set(key, self.__dict__['_attrs'][key])

        if self.hasChildren():
            for child in self.__dict__['_children']:
                child.toXML(header, el)

        if self.__dict__['_text'] is not None:
            el.text = self.__dict__['_text']
        return el