# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\PythonCode\CodeLib\src\Serialization\XML2Py.py
# Compiled at: 2016-11-17 04:13:23
__doc__ = '\nXML2Py - XML to Python de-serialization\n\nThis code transforms an XML document into a Python data structure\n\nUsage:\n    deserializer = XML2Py()\n    python_object = deserializer.parse( xml_string )\n    print xml_string\n    print python_object\n'
from lxml import etree

class XML2Py:

    def __init__(self):
        self._parser = parser = etree.XMLParser(remove_blank_text=True)
        self._root = None
        self.data = None
        return

    def parse(self, xmlString):
        """
        processes XML string into Python data structure
        """
        self._root = etree.fromstring(xmlString, self._parser)
        self.data = self._parseXMLRoot()
        return self.data

    def tostring(self):
        """
        creates a string representation using our etree object
        """
        if self._root != None:
            return etree.tostring(self._root)
        else:
            return

    def _parseXMLRoot(self):
        """
        starts processing, takes care of first level idisyncrasies
        """
        childDict = self._parseXMLNode(self._root)
        return {self._root.tag: childDict['children']}

    def _parseXMLNode(self, element):
        """
        rest of the processing
        """
        childContainer = None
        if element.items():
            childContainer = {}
            childContainer.update(dict(element.items()))
        else:
            childContainer = []
        if isinstance(childContainer, list) and element.text:
            childContainer.append(element.text)
        else:
            for child_elem in element.getchildren():
                childDict = self._parseXMLNode(child_elem)
                if isinstance(childContainer, dict):
                    childContainer.update({childDict['tag']: childDict['children']})
                else:
                    childContainer.append(childDict['children'])

        return {'tag': element.tag, 'children': childContainer}


def main():
    xml_string = '\n    <documents>\n        <document date="June 6, 2009" title="The Newness of Python" author="John Doe">\n            <copyright type="CC" url="http://www.creativecommons.org/" date="June 24, 2009" />\n            <text>Python is very nice. Very, very nice.</text>\n            <formats>\n                <format type="pdf">\n                    <info uri="http://www.python.org/newness-of-python.pdf" pages="245" />\n                </format>\n                <format type="web">\n                    <info uri="http://www.python.org/newness-of-python.html" />\n                </format>\n            </formats>\n        </document>\n    </documents>\n    '
    deserializer = XML2Py()
    python_object = deserializer.parse(xml_string)
    print xml_string
    print python_object


if __name__ == '__main__':
    main()