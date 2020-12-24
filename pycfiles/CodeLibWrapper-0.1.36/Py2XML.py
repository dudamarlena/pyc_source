# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\CodeLibWrapper\Src\XMLFunction\Py2XML.py
# Compiled at: 2016-12-09 03:30:43
"""
Py2XML - Python to XML serialization

This code transforms a Python data structures into an XML document

Usage:
    serializer = Py2XML()
    xml_string = serializer.parse( python_object )
    print python_object
    print xml_string
"""

class Py2XML:

    def __init__(self):
        self.data = ''

    def parse(self, pythonObj, objName=None):
        """
        processes Python data structure into XML string
        needs objName if pythonObj is a List
        """
        if pythonObj == None:
            return ''
        else:
            if isinstance(pythonObj, dict):
                self.data = self._PyDict2XML(pythonObj)
            elif isinstance(pythonObj, list):
                self.data = self._PyList2XML(pythonObj, objName)
            else:
                self.data = '<%(n)s>%(o)s</%(n)s>' % {'n': objName, 'o': str(pythonObj)}
            return self.data

    def _PyDict2XML(self, pyDictObj, objName=None):
        """
        process Python Dict objects
        They can store XML attributes and/or children
        """
        tagStr = ''
        attributes = {}
        attrStr = ''
        childStr = ''
        for k, v in pyDictObj.items():
            if isinstance(v, dict):
                childStr += self._PyDict2XML(v, k)
            elif isinstance(v, list):
                childStr += self._PyList2XML(v, k)
            else:
                attributes.update({k: v})

        if objName == None:
            return childStr
        else:
            for k, v in attributes.items():
                attrStr += ' %s="%s"' % (k, v)

            if childStr == '':
                tagStr += '<%(n)s%(a)s />' % {'n': objName, 'a': attrStr}
            else:
                tagStr += '<%(n)s%(a)s>%(c)s</%(n)s>' % {'n': objName, 'a': attrStr, 'c': childStr}
            return tagStr

    def _PyList2XML(self, pyListObj, objName=None):
        """
        process Python List objects
        They have no attributes, just children
        Lists only hold Dicts or Strings
        """
        tagStr = ''
        childStr = ''
        for childObj in pyListObj:
            if isinstance(childObj, dict):
                childStr += self._PyDict2XML(childObj, objName[:-1])
            else:
                for string in childObj:
                    childStr += string

        if objName == None:
            return childStr
        else:
            tagStr += '<%(n)s>%(c)s</%(n)s>' % {'n': objName, 'c': childStr}
            return tagStr


def main():
    print 'Do something.'


if __name__ == '__main__':
    main()