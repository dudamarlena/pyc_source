# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\makerst.py
# Compiled at: 2019-11-20 14:39:19
# Size of source mod 2**32: 2448 bytes
"""
makerst - make a bunch of autodoc rst files
===================================================
"""
import os.path, glob

def main():
    """
    make a bunch of autodoc rst files
    """
    srcpath = './doc/source'
    if not os.path.exists(srcpath):
        srcpath = './doc'
        if not os.path.exists(srcpath):
            print('Could not find ./doc/source or ./doc.  Exiting')
            return
    created = []
    for f in glob.glob('*.py'):
        modname = os.path.splitext(f)[0]
        if modname in ('__init__', 'setup', 'version'):
            pass
        else:
            rstfname = '.'.join([modname, 'rst'])
            fullrstpath = os.path.join(srcpath, rstfname)
            if os.path.exists(fullrstpath):
                pass
            else:
                RST = open(fullrstpath, 'w')
                RST.write('.. automodule:: {0}\n'.format(modname))
                RST.write('    :members:\n')
                RST.close()


if __name__ == '__main__':
    main()