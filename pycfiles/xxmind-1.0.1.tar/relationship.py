# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2.0\xxmind\file\xmind-sdk-python-master\xmind\core\relationship.py
# Compiled at: 2018-11-13 07:00:38
"""
    xmind.core.relationship
    ~~~~~~~~~~~~~~~~~~~

    :copyright:
    :license:
"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
from . import const
from .mixin import WorkbookMixinElement
from .topic import TopicElement
from .title import TitleElement

class RelationshipElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_RELATIONSHIP

    def __init__(self, node=None, ownerWorkbook=None):
        super(RelationshipElement, self).__init__(node, ownerWorkbook)
        self.addIdAttribute(const.ATTR_ID)

    def _get_title(self):
        return self.getFirstChildNodeByTagName(const.TAG_TITLE)

    def _find_end_point(self, id):
        owner_workbook = self.getOwnerWorkbook()
        if owner_workbook is None:
            return
        else:
            end_point = owner_workbook.getElementById(id)
            if end_point is None:
                return
            if end_point.tagName == const.TAG_TOPIC:
                return TopicElement(end_point, owner_workbook)
            return

    def getEnd1ID(self):
        return self.getAttribute(const.ATTR_END1)

    def setEnd1ID(self, id):
        self.setAttribute(const.ATTR_END1, id)
        self.updateModifiedTime()

    def getEnd2ID(self):
        return self.getAttribute(const.ATTR_END2)

    def setEnd2ID(self, id):
        self.setAttribute(const.ATTR_END2, id)
        self.updateModifiedTime()

    def getEnd1(self, end1_id):
        return self._find_end_point(end1_id)

    def getEnd2(self, end2_id):
        return self._find_end_point(end2_id)

    def getTitle(self):
        title = self._get_title()
        if title:
            title = TitleElement(title, self.getOwnerWorkbook())
            return title.getTextContent()

    def setTitle(self, text):
        _title = self._get_title()
        title = TitleElement(_title, self.getOwnerWorkbook())
        title.setTextContent(text)
        if _title is None:
            self.appendChild(title)
        self.updateModifiedTime()
        return


class RelationshipsElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_RELATIONSHIPS

    def __init__(self, node=None, ownerWorkbook=None):
        super(RelationshipsElement, self).__init__(node, ownerWorkbook)


def main():
    pass


if __name__ == '__main__':
    main()