# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\workspace\test01\xmind2.0\xxmind\file\xmind-sdk-python-master\xmind\core\notes.py
# Compiled at: 2018-11-13 07:00:38
"""
    xmind.core.notes
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
__author__ = 'aiqi@xmind.net <Woody Ai>'
from . import const
from .mixin import TopicMixinElement

class NotesElement(TopicMixinElement):
    TAG_NAME = const.TAG_NOTES

    def __init__(self, node=None, ownerTopic=None):
        super(NotesElement, self).__init__(node, ownerTopic)

    def getContent(self, format=const.PLAIN_FORMAT_NOTE):
        """ Get notes content

        :parma format:  specified returned content format, plain text
                        by default.
        """
        content = self.getFirstChildNodeByTagName(format)
        if not content:
            return
        if format is const.PLAIN_FORMAT_NOTE:
            content = PlainNotes(node=content, ownerTopic=self.getOwnerTopic())
        else:
            raise Exception('Only support plain text notes right now')
        return content.getTextContent()


class _NoteContentElement(TopicMixinElement):

    def __init__(self, node=None, ownerTopic=None):
        super(_NoteContentElement, self).__init__(node, ownerTopic)

    def getFormat(self):
        return self.getImplementation().tagName


class PlainNotes(_NoteContentElement):
    """ Plain text notes

    :param content: utf8 plain text.
    :param node:    `xml.dom.Element` object`
    :param ownerTopic:  `xmind.core.topic.TopicElement` object

    """
    TAG_NAME = const.PLAIN_FORMAT_NOTE

    def __init__(self, content=None, node=None, ownerTopic=None):
        super(PlainNotes, self).__init__(node, ownerTopic)
        if content is not None:
            self.setTextContent(content)
        return

    def setContent(self, content):
        self.setTextContent(content)


def main():
    pass


if __name__ == '__main__':
    main()