# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/filecatalog/xhtmlizer.py
# Compiled at: 2008-06-17 19:10:19
"""
File Catalog XHTMLizer
======================

Create an XHTML document from a directory tree file.

:copyright: 2006-2008 Jochen Kupperschmidt
:license: GNU General Public License, version 2; see LICENSE for details
"""
from cgi import escape
import os.path, sys
from filecatalog import io

def create_xhtml(data, title):
    yield '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n  <head>\n    <title>%s</title>\n  </head>\n  <body>\n    <h1>%s</h1>\n    <ul>' % (title, title)
    for line in append_list_items([data], 3):
        yield line

    yield '    </ul>\n  </body>\n</html>'


def append_list_items(items, level):
    """Recursively append items to the list."""
    if not isinstance(items, list):
        raise StandardError('Invalid data.')
    for item in items:
        if isinstance(item, dict):
            for key in item.iterkeys():
                yield indent('<li class="folder">' + escape(key), level)
                yield indent('<ul>', level + 1)
                for line in append_list_items(item[key], level + 2):
                    yield line

                yield indent('</ul>', level + 1)
                yield indent('</li>', level)

        else:
            yield indent('<li>%s</li>' % escape(item), level)


def indent(string, level):
    return '  ' * level + string


def main(filename):
    """Load tree, then build and output XHTML."""
    data = io.load_file(filename)
    print ('\n').join(create_xhtml(data, filename))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s <data file>' % os.path.basename(sys.argv[0])
        sys.exit(2)
    main(sys.argv[1])