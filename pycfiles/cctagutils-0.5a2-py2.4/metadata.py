# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cctagutils/metadata.py
# Compiled at: 2007-03-15 10:29:40
"""Dispatch to lookup the correct metadata handler for a given file.  Relies
on entry points defined by this package and others to find the correct
handler.  If an appropriate handler is not found for a given file extension,
falls back to XMP extraction.
"""
__id__ = '$Id: metadata.py 712 2007-02-20 18:07:32Z nyergler $'
__version__ = '$Revision: 712 $'
__copyright__ = '(c) 2004-2007, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'
import pkg_resources
from cctagutils.handler.xmp import XmpMetadata

def metadata(filename):
    """Returns the appropriate instance for the detected filetype of
    [filename].  The returned instance will be a subclass of the
    AudioMetadata class."""
    ext = filename.split('.')[(-1)].lower()
    handlers = pkg_resources.iter_entry_points('cctagutils.handler', ext)
    try:
        h = handlers.next()
        return h.load()(filename)
    except StopIteration, e:
        return XmpMetadata(filename)


open = metadata