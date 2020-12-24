# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cs/prj/quantumcore/src/quantumcore.contenttypes/quantumcore/contenttypes/globs.py
# Compiled at: 2010-04-21 06:17:08
import pkg_resources, re, fnmatch
EXT_RE = re.compile('(\\.\\w+)')

class GlobRegistry(object):
    """a registry for storing and detecting glob patterns"""

    def __init__(self):
        """initialize glob registry"""
        self.extensions = {}
        self.cs_extensions = {}
        self.cs_globs = []
        self.globs = []
        self.max_extension_length = 3

    def read(self):
        """read the default glob file and create the mapping"""
        fp = pkg_resources.resource_stream(__name__, 'data/sharedmime/globs2')
        max_extension_length = 0
        while True:
            line = fp.readline()
            if not line:
                break
            if line.startswith('#'):
                continue
            line = line[:-1]
            parts = line.split(':')
            (prio, mimetype, pattern) = parts[:3]
            flags = ''
            if len(parts) > 3:
                flags = parts[3]
            if pattern.startswith('*.'):
                ext = pattern[1:]
                if 'cs' in flags:
                    self.cs_extensions.setdefault(ext, []).append(mimetype)
                else:
                    self.extensions.setdefault(ext.lower(), []).append(mimetype)
                max_extension_length = max(max_extension_length, len(ext.split('.')))
            else:
                e = fnmatch.translate(pattern)
                if 'cs' in flags:
                    self.cs_globs.append((re.compile(e), mimetype))
                else:
                    self.globs.append((re.compile(e, re.I), mimetype))

        self.max_extension_length = max_extension_length

    def cut_extension(self, filename):
        """finds extensions of the filename and returns a list with found ones
        sorted by length, longest first. max_extension_length will define the 
        maximum length it searches for. This is computed on reading the glob file
        in read().
        
        Example::
            >>> gr.cut_extension("filename.tar.gz")
            ['.tar.gz', '.gz']        
        """
        exts = EXT_RE.findall(filename)
        result = []
        for i in range(min(len(exts), self.max_extension_length), 0, -1):
            ext = ('').join(exts[-i:])
            result.append(ext)

        return result

    def match(self, filename, default=None):
        """try to match a filename to a list of mimetypes. If this is your only
        method of matching you can give a ``default`` mimetype. Otherwise ``None``
        will be returned in case no match was found.
        
        Matching will be done from the longest to shortest pattern which"""
        cs_match_exts = self.cut_extension(filename)
        for m in cs_match_exts:
            if self.cs_extensions.has_key(m):
                return self.cs_extensions[m]

        match_exts = self.cut_extension(filename.lower())
        for m in match_exts:
            if self.extensions.has_key(m):
                return self.extensions[m]

        res = set()
        for (regexp, mimetype) in self.cs_globs:
            if regexp.match(filename) is not None:
                res.add(mimetype)

        if len(res) > 0:
            return list(res)
        for (regexp, mimetype) in self.globs:
            if regexp.match(filename) is not None:
                res.add(mimetype)

        if len(res) > 0:
            return list(res)
        return default