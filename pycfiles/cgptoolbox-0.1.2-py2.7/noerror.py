# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\examples\noerror.py
# Compiled at: 2013-01-25 10:22:40
import sys, os, shutil, tempfile, importlib
dir = tempfile.mkdtemp().replace('\\', '/')
pkg = [ ('{}/pkg{}').format(dir, i) for i in (0, 1) ]
os.makedirs(pkg[0])
sys.path.append(dir)
os.makedirs(pkg[1])
for i in (0, 1):
    with open(os.path.join(pkg[i], '__init__.py'), 'w') as (f):
        f.write('"""__init__ file required for package directory."""')
    with open(os.path.join(pkg[i], ('module{}.py').format(i)), 'w') as (f):
        f.write(('print "Importing module{} from {}"').format(i, pkg[i]))
    print 'hello'
    importlib.import_module(('pkg{}.module{}').format(i, i), ('pkg{}').format(i))

shutil.rmtree(dir)