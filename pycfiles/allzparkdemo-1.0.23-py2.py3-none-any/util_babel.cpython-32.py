# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/support/babel/util_babel.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on May 3, 2012\n\n@package ally utilities\n@copyright 2012 Sourcefabric o.p.s.\n@license http: // www.gnu.org / licenses / gpl - 3.0.txt\n@author: Mugur Rus\n\nContains Babel utils\n'
from functools import reduce
from babel.messages.catalog import Message

def msgId(msg):
    """
    Returns the message identifier used to retrieve the message from the
    catalog. This is be different from the id attribute when the message
    has plural forms.

    @param msg: Message
        The message for which to return the identifier
    @return: string
        The message identifier
    """
    assert isinstance(msg, Message), 'Invalid message %s' % msg
    if not isinstance(msg.id, (list, tuple)):
        return msg.id
    return msg.id[0]


def isMsgTranslated(msg):
    """
    Returns true if the message has partial or full translation.
    @param msg: Message
        The message for which to return the identifier
    @return: bool
    """
    assert isinstance(msg, Message), 'Invalid message %s' % msg
    if isinstance(msg.string, (list, tuple)):
        return not reduce(lambda empty, elem: empty and not elem, msg.string, True)
    else:
        return bool(msg.string)


def copyTranslation(src, dst):
    """
    Copy the translation from the source message to the destination message.

    @param src: Message
        The message from which to copy the translation
    @param dst: Message
        The message to which to copy the translation
    @return: Message
        The destination message
    """
    assert isinstance(src, Message), 'Invalid message %s' % src
    assert isinstance(dst, Message), 'Invalid message %s' % dst
    if type(src.string) == type(dst.string) or dst.string is None or isinstance(src.string, (list, tuple)):
        dst.string = src.string
    else:
        if isinstance(dst.string, list):
            dst[0] = src.string
        elif isinstance(dst.string, tuple):
            string = [tr for tr in dst.string]
            string[0] = src.string
            dst.string = tuple(string)
    return dst


def fixBabelCatalogAddBug(msg, numPlurals):
    """
    The Babel catalog does not set the translation strings properly when the
    message has plural form. Regardless of the number of plurals, when adding
    a new message only two strings are set for the translation. E.g.: for
    Romanian the num_plurals catalog attribute is 3 but the translation
    strings is a tuple of 2: ('', ''). This issue is fixed though when writing
    the PO file - the PO file contains the proper number of plurals. So when
    comparing a message from a generated catalog to a message from a catalog
    read from a PO file the result is false even though they have the same
    partial translation.
    @param msg: Message
        Message to fix
    @param numPlurals: int
        The number of plurals from the catalog this message belongs to
    """
    assert isinstance(msg, Message), 'Invalid message %s' % msg
    if isinstance(msg.id, (list, tuple)):
        if not msg.string or isinstance(msg.string, str):
            string = msg.string
            msg.string = ['' for x in range(numPlurals)]
            msg.string[0] = string
            msg.string = tuple(msg.string)
        elif isinstance(msg.string, (list, tuple)) and len(msg.string) != numPlurals:
            string = []
            for x in range(0, numPlurals):
                if len(msg.string) > x:
                    string.append(msg.string[x])
                else:
                    string.append('')

            msg.string = tuple(string)