# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/standalonetemplate.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 3130 bytes
sources = '\n@SOURCES@'
import sys, base64, zlib

class DictImporter(object):

    def __init__(self, sources):
        self.sources = sources

    def find_module(self, fullname, path=None):
        if fullname == 'argparse':
            if sys.version_info >= (2, 7):
                return
        else:
            if fullname in self.sources:
                return self
            if fullname + '.__init__' in self.sources:
                return self

    def load_module(self, fullname):
        from types import ModuleType
        try:
            s = self.sources[fullname]
            is_pkg = False
        except KeyError:
            s = self.sources[(fullname + '.__init__')]
            is_pkg = True

        co = compile(s, fullname, 'exec')
        module = sys.modules.setdefault(fullname, ModuleType(fullname))
        module.__file__ = '%s/%s' % (__file__, fullname)
        module.__loader__ = self
        if is_pkg:
            module.__path__ = [
             fullname]
        do_exec(co, module.__dict__)
        return sys.modules[fullname]

    def get_source(self, name):
        res = self.sources.get(name)
        if res is None:
            res = self.sources.get(name + '.__init__')
        return res


if __name__ == '__main__':
    if sys.version_info >= (3, 0):
        exec('def do_exec(co, loc): exec(co, loc)\n')
        import pickle
        sources = sources.encode('ascii')
        sources = pickle.loads(zlib.decompress(base64.decodebytes(sources)))
    else:
        import cPickle as pickle
        exec('def do_exec(co, loc): exec co in loc\n')
        sources = pickle.loads(zlib.decompress(base64.decodestring(sources)))
    importer = DictImporter(sources)
    sys.meta_path.insert(0, importer)
    entry = '@ENTRY@'
    do_exec(entry, locals())