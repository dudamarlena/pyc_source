# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/flexable/template.py
# Compiled at: 2007-07-17 10:54:28
"""
>>> t = Template()
>>> t.fromstring("<div/>")
>>> str(t)
'<div/>'

>>> t.merge('hello')
>>> str(t)
'<div>hello</div>'

>>> t = Template()
>>> t.fromstring("<div><span class='y'/></div>")
>>> t.merge({'y':['1', '2']})
>>> str(t)
'<div><span class="y">1</span><span class="y">2</span></div>'

>>> t = Template()
>>> t.fromstring("<div><span class='y'/></div>")
>>> t.merge({'y':[({'@id':'m1'}, '1'), 
...               ({'@id':'m2'}, '2')]})
>>> str(t)
'<div><span class="y" id="m1">1</span><span class="y" id="m2">2</span></div>'

>>> t.fromstring("<div><div class='box'><span class='x'/><span class='y'/></div></div>")
>>> t.merge({'box':[{'x':'1', 'y':'2'},
...                 {'x':'3', 'y':'4'}]})
>>> str(t)
'<div><div class="box"><span class="x">1</span><span class="y">2</span></div><div class="box"><span class="x">3</span><span class="y">4</span></div></div>'

>>> t.fromstring("<div/>")
>>> t.merge(ET.Element('span'))
>>> str(t)
'<div><span/></div>'
"""
import lxml.etree as ET
from StringIO import StringIO
from forms import FormCollection

class Template(object):

    def __init__(self, filename=None):
        self.tree = ET.ElementTree()
        self._forms = None
        if filename is not None:
            self.fromfile(filename)
        return

    def fromfile(self, f):
        self.tree.parse(f)

    def fromstring(self, s):
        f = StringIO(s)
        self.fromfile(f)

    def merge(self, values):
        mergeValues(self.tree.getroot(), values)

    def __str__(self):
        return ET.tostring(self.tree)

    @property
    def forms(self):
        if self._forms is None:
            formElements = self.tree.xpath('//*[local-name()="form"]')
            self._forms = FormCollection(formElements)
        return self._forms


def copyTree(tree):
    element = tree.makeelement(tree.tag, tree.attrib)
    element.tail = tree.tail
    element.text = tree.text
    for child in tree:
        element.append(copyTree(child))

    return element


def mergeValues(element, value):
    ltype = type(value)
    if ltype not in (str, unicode, dict, list, tuple) and not hasattr(value, '__iter__'):
        value = str(value)
        ltype = str
    if ET.iselement(value):
        element.append(value)
    elif ltype in (str, unicode):
        element.text = value
    elif ltype == dict:
        for (k, v) in value.iteritems():
            if k.startswith('@'):
                element.set(k[1:], v)
            else:
                children = element.xpath(".//*[@id='%s']" % k)
                if len(children) == 0:
                    children = element.xpath(".//*[@class='%s']" % k)
                if len(children) > 0:
                    for child in children:
                        mergeValues(child, v)

    elif ltype == tuple:
        for v in value:
            mergeValues(element, v)

    elif ltype == list or hasattr(value, '__iter__'):
        parent = element.getparent()
        parent.remove(element)
        for v in value:
            e = copyTree(element)
            mergeValues(e, v)
            parent.append(e)

    else:
        raise Exception, 'Sorry, applicable types are str, unicode, dict, tuple and list. got %s' % ltype


if __name__ == '__main__':
    import doctest
    doctest.testmod()