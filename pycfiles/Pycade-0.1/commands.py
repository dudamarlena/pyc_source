# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cabig/cacore/generate/commands.py
# Compiled at: 2010-06-24 14:29:32
__doc__ = ' \ncaPyGen API Generation\n'
__author__ = 'Konrad Rokicki'
__date__ = '$Date$'
__version__ = '$Revision$'
import sys, os
from ZSI.generate.commands import wsdl2py
from distutils import dir_util, file_util
import cacore2python
NS_INIT = ("__import__('pkg_resources').declare_namespace(__name__)", )

def cacore2py():
    try:
        sys.path.insert(0, '.')
        import settings
    except ImportError:
        sys.stderr.write("Error: Can't find settings.py\n")
        sys.exit(1)

    print 'Cleaning output directory', settings.OUTPUT_DIR
    try:
        dir_util.remove_tree(settings.OUTPUT_DIR)
    except OSError:
        pass

    r = [
     settings.OUTPUT_DIR] + settings.ROOT_PACKAGE.split('.')
    outputDir = os.path.join(*r)
    dir_util.mkpath(settings.OUTPUT_DIR)
    print 'Generating Python API from', settings.WSDL_FILE
    for p in [ settings.ROOT_PACKAGE + '.' + v for v in settings.PACKAGE_MAPPING.values() ]:
        prefix = settings.OUTPUT_DIR
        for d in p.split('.')[:-1]:
            prefix = os.path.join(prefix, d)
            dir_util.mkpath(prefix)
            contents = ''
            if d == 'cabig':
                contents = NS_INIT
            file_util.write_file(os.path.join(prefix, '__init__.py'), contents)

    args = [
     '-lbo', outputDir, settings.WSDL_FILE]
    wsdl2py(args)
    sys.path.insert(0, outputDir)
    fileName = [ f for f in os.listdir(outputDir) if f.endswith('_client.py') ][0]
    moduleName = fileName.replace('.py', '')
    module = __import__(moduleName)
    cacore2python.generate(module, settings, outputDir)
    print 'API generation completed'


if __name__ == '__main__':
    cacore2py()