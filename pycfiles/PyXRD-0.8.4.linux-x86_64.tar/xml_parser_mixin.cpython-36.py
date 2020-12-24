# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xml_parser_mixin.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1649 bytes
try:
    from lxml import ET
except ImportError:
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        try:
            import xml.etree.ElementTree as ET
        except ImportError:
            try:
                import cElementTree as ET
            except ImportError:
                try:
                    import elementtree.ElementTree as ET
                except ImportError:
                    print('Failed to import ElementTree from any known place')

class XMLParserMixin(object):
    __doc__ = '\n        XML Parser Mixin class\n    '

    @classmethod
    def get_xml_for_string(cls, s):
        """ Returns a tuple containing the XML tree and root objects """
        root = ET.fromstring(s)
        return (ET.ElementTree(element=root), root)

    @classmethod
    def get_xml_for_file(cls, f):
        """ Returns a tuple containing the XML tree and root objects """
        tree = ET.parse(f)
        return (tree, tree.getroot())

    @classmethod
    def get_val(cls, root, path, attrib, default=None):
        """ Returns the attribute `attrib` from the first element found in
        `root` using the given `path`or default if not found """
        element = root.find(path)
        if element is not None:
            return element.get(attrib)
        else:
            return default