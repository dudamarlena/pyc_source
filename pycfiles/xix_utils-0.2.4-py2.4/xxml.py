# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/xxml.py
# Compiled at: 2006-03-02 13:59:00
"""xml utilities.
"""
import lxml.etree as xmllib
from xix.utils.interfaces import IDiffFactory
from xix.utils.diff import AbstractDiff, PrettyDiff
from xix.utils.diff import NonSequentialDiffFactory, DictionaryDiffFactory
from xix.utils.comp.interface import implements
import warnings
__author__ = 'Drew Smathers'
__contact__ = 'drew.smathers@gmail.com'
__version__ = '$Revision$'[11:-2]
__license__ = 'MIT'
warnings.warn('xxml module is pre-alpha/unstable.')

class XmlTreeDiff(AbstractDiff):
    """Contains missing, same and added list of XmlElementDiff 
    instances
    """
    __module__ = __name__


class XmlElementDiff(AbstractDiff):
    """Contains attributeDiff and XmlTreeDiff for recursive diffing.
    """
    __module__ = __name__
    attrDiff = None
    xmlTreeDiff = None


class XmlDiffFactory:
    """Expose semantic differences between two xml trees.
    """
    __module__ = __name__
    implements(IDiffFactory)
    elmDiffFactory = NonSequentialDiffFactory()
    attrDiffFactory = DictionaryDiffFactory()

    def diff(self, tree1, tree2, check_order=False):
        """Return diff object representing Differences between tree1
        and tree2.  

        @param tree1: xml tree 1
        @param tree2: xml tree 2
        @param check_order: consider the order of elements in the tree.
        """
        if not check_order:
            return self.__diff_noorder_root(tree1, tree2)
        return self.__diff_ordercounts(tree1, tree2)

    def __diff_noorder(self, elms1, elms2):
        pass

    def __diff_noorder_root(self, tree1, tree2):
        same, missing, added = [], [], []
        root1 = tree1.getroot()
        root2 = tree2.getroot()
        attrDiff = None
        if root1.tag != root2.tag:
            missing.append(root1.tag)
            added.append(root2.tag)
            return AstractDiff([], missing, added)
        else:
            attrDiff = attrDiffFactory.diff(root1.attrib, root2.attrib)
        elmDiff = XmlElementDiff()
        elmDiff.attrDiff = attrDiff
        return

    def __diff_ordercounts(self, tree1, tree2):
        raise NotImplementedError('checking xml trees with order is not implemented')