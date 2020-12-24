# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/build/generate_Makemm.py
# Compiled at: 2013-12-08 21:45:16


def main():
    import sys
    project = sys.argv[1]
    path = sys.argv[0]
    render(path, project)


def render(path, project):
    import os
    d = {'project': project}
    import packages
    packageInfoTable = getattr(packages, 'packageInfoTable', None)
    if packageInfoTable:
        table = packages.packageInfoTable
        dirs = []
        for name in packages.packageNames:
            info = table[name]
            dirs.append(info['path'])
            continue

    else:
        from ..packages.factories.fromPyPackage import factory
        pkgs = factory(packages)
        pkgs = pkgs.getAll()
        dirs = [ p.name for p in pkgs ]
    dirs = ('').join([ '\t%s \\\n' % dir for dir in dirs ])
    d['directories'] = dirs
    pwd = os.path.abspath(__file__)
    pwd = os.path.dirname(pwd)
    fmtstr = open(os.path.join(pwd, 'Make.mm.template')).read()
    s = fmtstr % d
    f = os.path.join(path, 'Make.mm')
    open(f, 'w').write(s)
    return


if __name__ == '__main__':
    main()
__id__ = '$Id$'