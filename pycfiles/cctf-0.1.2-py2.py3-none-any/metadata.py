# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cctagutils/metadata.py
# Compiled at: 2007-03-15 10:29:40
__doc__ = 'Dispatch to lookup the correct metadata handler for a given file.  Relies\non entry points defined by this package and others to find the correct\nhandler.  If an appropriate handler is not found for a given file extension,\nfalls back to XMP extraction.\n'
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