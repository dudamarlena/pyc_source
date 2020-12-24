# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cs/prj/quantumcore/src/quantumcore.contenttypes/quantumcore/contenttypes/registry.py
# Compiled at: 2010-04-21 06:56:32
import tempfile, os, pymagic, globs

class MIMETypesRegistry(object):
    """the main class for the mimetype registry. It holds globs and magic detectors 
    and is able to check a file for it's content type"""

    def __init__(self, cachefile=None):
        """initialize the registry by loading all data files"""
        self.globs = globs.GlobRegistry()
        self.globs.read()
        if cachefile is None:
            cachedir = tempfile.mkdtemp()
            cachefile = os.path.join(cachedir, 'magic')
        self.magic = pymagic.Magic(None, cachefile)
        return

    def classify(self, filename=None, data=None, force_magic=False, default='application/octet-stream'):
        """check a file by filename and or data for the correct type. If ``force_magic`` is ``True`` then even in the case
        the filename produced only one mimetype the magic detection will be done nevertheless. ``data`` should only be the
        beginning of the file, e.g. 4096 bytes."""
        filename_types = []
        data_type = None
        if filename is not None:
            filename_types = self.globs.match(filename, [])
            if len(filename_types) == 1 and not force_magic:
                return filename_types[0]
            if data is None and filename_types == []:
                return default
            if data is None:
                return filename_types[0]
        if data is not None:
            data_type = self.magic.classify(data)
        if data_type is not None:
            return data_type
        elif filename_types != []:
            return filename_types[0]
        return default