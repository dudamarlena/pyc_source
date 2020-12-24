# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/stripogram/__init__.py
# Compiled at: 2008-11-27 09:36:34
from html2text import HTML2Text
from html2safehtml import HTML2SafeHTML

def html2text(s, ignore_tags=(), indent_width=4, page_width=80):
    ignore_tags = [ t.lower() for t in ignore_tags ]
    parser = HTML2Text(ignore_tags, indent_width, page_width)
    parser.feed(s)
    parser.close()
    parser.generate()
    return parser.result


def html2safehtml(s, valid_tags=('b', 'a', 'i', 'br', 'p')):
    valid_tags = [ t.lower() for t in valid_tags ]
    parser = HTML2SafeHTML(valid_tags)
    parser.feed(s)
    parser.close()
    parser.cleanup()
    return parser.result


try:
    from AccessControl import ModuleSecurityInfo
except ImportError:
    pass
else:
    ModuleSecurityInfo('Products.stripogram').declareObjectPublic()
    ModuleSecurityInfo('Products.stripogram').declarePublic('html2text', 'html2safehtml')