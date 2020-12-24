# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/__init__.py
# Compiled at: 2013-12-08 21:45:16
"""
sub-packages:

* build: find out dependencies, create .tools, and build
* installers: installers for dependent software packages
* envvars: environment variable manipulations
* paths: utilities to find out installation paths of software packages
* scripts: provide methods that can be used as the 'main' method of useful scripts

"""

def make_tarball(directory):
    """make a tarball of the given directory tree.
    
    make_tarball( "/a/b/c/hello" ) --> hello.tgz
    """
    import os
    name = os.path.basename(directory)
    tarball = '%s.tgz' % name
    import tarfile
    f = tarfile.open(tarball, 'w:gz')
    f.add(directory, name)
    del f
    return tarball


__id__ = '$Id$'