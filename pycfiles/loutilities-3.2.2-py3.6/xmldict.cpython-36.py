# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\xmldict.py
# Compiled at: 2019-11-20 15:09:06
# Size of source mod 2**32: 5040 bytes
from xml.etree import ElementTree

def main():
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    configdict = ConvertXmlToDict('config.xml')
    pp.pprint(configdict)
    print(configdict['settings']['color'])
    configdict['settings']['color'] = 'red'
    print(configdict.settings.color)
    configdict.settings.color = 'red'
    root = ConvertDictToXml(configdict)
    tree = ElementTree.ElementTree(root)
    tree.write('config.new.xml')


class XmlDictObject(dict):
    __doc__ = '\n    Adds object like functionality to the standard dictionary.\n    '

    def __init__(self, initdict=None):
        if initdict is None:
            initdict = {}
        dict.__init__(self, initdict)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def __str__(self):
        if '_text' in self:
            return self.__getitem__('_text')
        else:
            return ''

    @staticmethod
    def Wrap(x):
        """
        Static method to wrap a dictionary recursively as an XmlDictObject
        """
        if isinstance(x, dict):
            return XmlDictObject((k, XmlDictObject.Wrap(v)) for k, v in x.items())
        else:
            if isinstance(x, list):
                return [XmlDictObject.Wrap(v) for v in x]
            return x

    @staticmethod
    def _UnWrap(x):
        if isinstance(x, dict):
            return dict((k, XmlDictObject._UnWrap(v)) for k, v in x.items())
        else:
            if isinstance(x, list):
                return [XmlDictObject._UnWrap(v) for v in x]
            return x

    def UnWrap(self):
        """
        Recursively converts an XmlDictObject to a standard dictionary and returns the result.
        """
        return XmlDictObject._UnWrap(self)


def _ConvertDictToXmlRecurse(parent, dictitem):
    if not not isinstance(dictitem, type([])):
        raise AssertionError
    else:
        if isinstance(dictitem, dict):
            for tag, child in dictitem.items():
                if str(tag) == '_text':
                    parent.text = str(child)
                elif isinstance(child, type([])):
                    for listchild in child:
                        elem = ElementTree.Element(tag)
                        parent.append(elem)
                        _ConvertDictToXmlRecurse(elem, listchild)

                else:
                    elem = ElementTree.Element(tag)
                    parent.append(elem)
                    _ConvertDictToXmlRecurse(elem, child)

        else:
            parent.text = str(dictitem)


def ConvertDictToXml(xmldict):
    """
    Converts a dictionary to an XML ElementTree Element 
    """
    roottag = list(xmldict.keys())[0]
    root = ElementTree.Element(roottag)
    _ConvertDictToXmlRecurse(root, xmldict[roottag])
    return root


def _ConvertXmlToDictRecurse(node, dictclass):
    nodedict = dictclass()
    if len(list(node.items())) > 0:
        nodedict.update(dict(list(node.items())))
    else:
        for child in node:
            newitem = _ConvertXmlToDictRecurse(child, dictclass)
            if child.tag in nodedict:
                if isinstance(nodedict[child.tag], type([])):
                    nodedict[child.tag].append(newitem)
                else:
                    nodedict[child.tag] = [
                     nodedict[child.tag], newitem]
            else:
                nodedict[child.tag] = newitem

        if node.text is None:
            text = ''
        else:
            text = node.text.strip()
        if len(nodedict) > 0:
            if len(text) > 0:
                nodedict['_text'] = text
        else:
            nodedict = text
    return nodedict


def ConvertXmlToDict(root, dictclass=XmlDictObject):
    """
    Converts an XML file or ElementTree Element to a dictionary
    """
    if isinstance(root, type('')):
        root = ElementTree.parse(root).getroot()
    else:
        if not isinstance(root, ElementTree.Element):
            raise TypeError('Expected ElementTree.Element or file path string')
    return dictclass({root.tag: _ConvertXmlToDictRecurse(root, dictclass)})


if __name__ == '__main__':
    main()