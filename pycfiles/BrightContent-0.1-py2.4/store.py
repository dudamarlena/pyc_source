# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/brightcontent/core/store.py
# Compiled at: 2006-08-22 02:42:40
import os, cStringIO, glob, threading, amara, datetime
from amara import binderytools
from brightcontent.util import fixup_namespaces, quick_xml_scan
ATOM10_NS = 'http://www.w3.org/2005/Atom'
XHTML1_NS = 'http://www.w3.org/1999/xhtml'
ENCODING = 'UTF-8'
DUMMY_URI = 'urn:x-brightcontent:dummy'
COMMON_PREFIXES = {'atom': ATOM10_NS, 'xh': XHTML1_NS}
DEFAULT_LANG = 'en'
STORE_XML_FILE = 'store.xml'

class repository:
    """
    The Bright Content Atom Store repository
    This is the core Atom capability, with Python API
    For APP access, plug in the brightcontent.core.store.app
    WSGI middleware (which is vaporware at present :-) )
    """
    __module__ = __name__

    def get_entries(self, limit=-1, lower_date=None, upper_date=None, slug=None):
        raise NotImplementedError

    def assemble_feed(self, entries, stream=None):
        atom = amara.create_document('feed', ATOM10_NS, attributes={'xml:lang': 'en'})
        storedoc = amara.parse(self.store_xml_file, prefixes=COMMON_PREFIXES)
        for element in storedoc.feed.xml_children:
            atom.feed.xml_append(element)

        for entry in entries:
            atom.feed.xml_append_fragment(entry)

        fixup_namespaces(atom)
        if stream:
            atom.xml(indent='yes', stream=stream)
            return stream
        else:
            buffer = cStringIO.StringIO()
            atom.xml(indent='yes', stream=buffer)
            return buffer.getvalue()


class flatfile_repository(repository):
    """
    Flat file implementation of the repository
    """
    __module__ = __name__

    def __init__(self, storedir):
        self.storedir = storedir
        self.store_xml_file = os.path.join(storedir, STORE_XML_FILE)

    def get_entries(self, offset=0, limit=-1, lower_date=None, upper_date=None, slug=None):
        filenames = glob.glob(os.path.join(self.storedir, '*'))
        filenames = [ fn for fn in filenames if not fn.endswith(STORE_XML_FILE) ]
        entries = []
        offseted = 0
        for fn in filenames:
            updated = quick_xml_scan(fn, 'atom:updated', prefixes=COMMON_PREFIXES)
            date = amara.binderytools.parse_isodate(updated)
            if not (lower_date and date < lower_date or upper_date and date > upper_date):
                if slug and os.path.splitext(os.path.split(fn)[1])[0] == slug:
                    continue
                entry = open(fn, 'r').read()
                if offseted >= offset:
                    entries.append(entry)
                else:
                    offseted += 1
                if limit != -1 and len(entries) >= limit:
                    break

        return entries


if __name__ == '__main__':
    import sys
    from dateutil.relativedelta import *
    from dateutil.tz import tzlocal
    store = flatfile_repository('/tmp/atomstore')
    now = datetime.datetime.now(tzlocal())
    try:
        limit = int(sys.argv[1])
    except IndexError:
        limit = -1
    else:
        try:
            start = int(sys.argv[2])
            upper = now + relativedelta(days=-start)
        except IndexError:
            upper = None
        else:
            try:
                end = int(sys.argv[3])
                lower = now + relativedelta(days=-end)
            except IndexError:
                lower = None
            else:
                try:
                    slug = sys.argv[4]
                except IndexError:
                    slug = None
                else:
                    entries = store.get_entries(limit, lower_date=lower, upper_date=upper, slug=slug)
                    print store.assemble_feed(entries)