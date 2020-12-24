# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\genxmlif\xmliftest.py
# Compiled at: 2008-08-08 10:15:38
import genxmlif
from genxmlif.xmlifODict import odict
xmlIf = genxmlif.chooseXmlIf(genxmlif.XMLIF_ELEMENTTREE)
xmlTree = xmlIf.createXmlTree(None, 'testTree', {'rootAttr1': 'RootAttr1'})
xmlRootNode = xmlTree.getRootNode()
myDict = odict((('childTag1', '123'), ('childTag2', '123')))
xmlRootNode.appendChild('childTag', myDict)
xmlRootNode.appendChild('childTag', {'childTag1': '123456', 'childTag2': '123456'})
xmlRootNode.appendChild('childTag', {'childTag1': '123456789', 'childTag3': '1234', 'childTag2': '123456789'})
xmlRootNode.appendChild('childTag', {'childTag1': '1', 'childTag2': '1'})
print xmlTree.printTree(prettyPrint=1)
print xmlTree
print xmlTree.getRootNode()