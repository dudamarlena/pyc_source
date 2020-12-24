# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\file\xmind-sdk-python-master\xmind\core\notes.py
# Compiled at: 2019-07-01 23:22:26
# Size of source mod 2**32: 1817 bytes
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
        elif format is const.PLAIN_FORMAT_NOTE:
            content = PlainNotes(node=content, ownerTopic=(self.getOwnerTopic()))
        else:
            raise Exception('Only support plain text notes right now')
        return content.getTextContent()


class _NoteContentElement(TopicMixinElement):

    def __init__(self, node=None, ownerTopic=None):
        super(_NoteContentElement, self).__init__(node, ownerTopic)

    def getFormat(self):
        return self.getImplementation().tagName


class PlainNotes(_NoteContentElement):
    __doc__ = ' Plain text notes\n\n    :param content: utf8 plain text.\n    :param node:    `xml.dom.Element` object`\n    :param ownerTopic:  `xmind.core.topic.TopicElement` object\n\n    '
    TAG_NAME = const.PLAIN_FORMAT_NOTE

    def __init__(self, content=None, node=None, ownerTopic=None):
        super(PlainNotes, self).__init__(node, ownerTopic)
        if content is not None:
            self.setTextContent(content)

    def setContent(self, content):
        self.setTextContent(content)


def main():
    pass


if __name__ == '__main__':
    main()