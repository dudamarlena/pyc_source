# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/xml/xml_tool.py
# Compiled at: 2019-12-17 01:13:16
# Size of source mod 2**32: 1199 bytes
from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.file.file_tool import FileTool
import xml.etree.ElementTree as ET

class XMLTool:

    @classmethod
    def down(cls, root, tags):
        node = root
        for tag in tags:
            node = node.find(tag)
            if not node:
                return node

        return node

    @classmethod
    def down2text(cls, root, tags):
        node = root
        for tag in tags:
            node = node.find(tag)
            if not node:
                return node

        return node.text

    @classmethod
    def down2uniq(cls, root, tags):
        node = root
        for tag in tags:
            children = node.findall(tag)
            if not children:
                return
                node = l_singleton2obj(children)

        return node

    @classmethod
    def x2text(cls, node):
        return node.text

    @classmethod
    def filepath2xml(cls, filepath):
        utf8 = FileTool.filepath2utf8(filepath)
        return cls.utf82xml(utf8)

    @classmethod
    def utf82xml(cls, utf8):
        return ET.fromstring(utf8)

    @classmethod
    def xml2j_xml(cls, xml):
        return {node.tag:node.text for node in xml}