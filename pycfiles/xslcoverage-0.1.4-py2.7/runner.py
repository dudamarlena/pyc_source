# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xslcover/runner.py
# Compiled at: 2016-11-26 11:29:20
import os, imp, glob
plugin_subdir = 'runners'

def load(modname, subdir=''):
    global plugin_subdir
    try:
        file_, path, descr = imp.find_module(modname, [''])
    except ImportError:
        try:
            subdir = subdir or plugin_subdir
            plugin_dir = os.path.join(os.path.dirname(__file__), subdir)
            file_, path, descr = imp.find_module(modname, [plugin_dir])
        except ImportError:
            raise ValueError("Trace Runner '%s' not found" % modname)

    mod = imp.load_module(modname, file_, path, descr)
    if file_:
        file_.close()
    return mod


def load_runner(modname, subdir=''):
    mod = load(modname, subdir=subdir)
    o = mod.TraceRunner()
    return o


def load_parser(modname, subdir=''):
    mod = load(modname, subdir=subdir)
    o = mod.TraceParser()
    return o


def get_plugins(subdir=''):
    """
    Return the list of the default available plugins stored in 'runners'
    """
    subdir = subdir or plugin_subdir
    plugin_dir = os.path.join(os.path.dirname(__file__), subdir)
    ps = glob.glob(os.path.join(plugin_dir, '*.py'))
    ps = [ os.path.splitext(os.path.basename(p))[0] for p in ps ]
    if '__init__' in ps:
        ps.remove('__init__')
    modlists = []
    for p in ps:
        try:
            x = load(p, subdir=subdir)
            modlists.append(p)
        except Exception as e:
            print e

    return modlists