# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/xslt/xslt.py
# Compiled at: 2017-04-03 18:58:57
import os, imp, glob

def load(modname):
    try:
        file, path, descr = imp.find_module(modname, [''])
    except ImportError:
        try:
            file, path, descr = imp.find_module(modname, [
             os.path.dirname(__file__)])
        except ImportError:
            raise ValueError("Xslt '%s' not found" % modname)

    mod = imp.load_module(modname, file, path, descr)
    file.close()
    o = mod.Xslt()
    return o


def get_deplists():
    """
    Return the dependency list to check for each XSLT plugin. The returned
    list also gives the available plugins.
    """
    ps = glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
    selfmod = os.path.splitext(os.path.basename(__file__))[0]
    ps = [ os.path.splitext(os.path.basename(p))[0] for p in ps ]
    if selfmod in ps:
        ps.remove(selfmod)
    if '__init__' in ps:
        ps.remove('__init__')
    deplists = []
    for p in ps:
        try:
            x = load(p)
            deplists.append((p, x.get_deplist()))
        except:
            pass

    return deplists