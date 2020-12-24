# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lambadalib/prelaunch.py
# Compiled at: 2017-04-24 15:46:12
# Size of source mod 2**32: 855 bytes
import ast, sys, importlib, imp
from lambadalib import functionproxy
from lambadalib import cmdline

def main_unused(name):
    fileobj, path, description = imp.find_module(name)
    if description[2] != imp.PY_SOURCE:
        raise ImportError('no source file found')
    modcode = fileobj.read()
    d = {}
    tree = ast.parse(modcode)
    for item in tree.body:
        if isinstance(item, ast.Import):
            modname = item.names[0].name
            mod = importlib.import_module(modname)
            d[modname] = mod

    functionproxy.scan(d)
    code = compile(modcode, path, 'exec')
    module = imp.new_module(name)
    exec(code, module.__dict__)
    sys.modules[name] = module


def prename_unused():
    modname = sys.argv[1]
    if modname.endswith('.py'):
        modname = modname[:-3]
    main(modname)


if __name__ == '__main__':
    cmdline.execute()