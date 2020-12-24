# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\xmldict1.py
# Compiled at: 2020-01-13 13:07:08
# Size of source mod 2**32: 2703 bytes
import cElementTree as ElementTree

class XmlListConfig(list):

    def __init__(self, aList):
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            else:
                if element.text:
                    text = element.text.strip()
                    if text:
                        self.append(text)


class XmlDictConfig(dict):
    __doc__ = "\n    Example usage:\n\n    >>> tree = ElementTree.parse('your_file.xml')\n    >>> root = tree.getroot()\n    >>> xmldict = XmlDictConfig(root)\n\n    Or, if you want to use an XML string:\n\n    >>> root = ElementTree.XML(xml_string)\n    >>> xmldict = XmlDictConfig(root)\n\n    And then use xmldict for what it is... a dict.\n    "

    def __init__(self, parent_element):
        if list(parent_element.items()):
            self.update(dict(list(parent_element.items())))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                else:
                    aDict = {element[0].tag: XmlListConfig(element)}
                if list(element.items()):
                    aDict.update(dict(list(element.items())))
                self.update({element.tag: aDict})
            else:
                if list(element.items()):
                    self.update({element.tag: dict(list(element.items()))})
                else:
                    self.update({element.tag: element.text})