# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/find_package.py
# Compiled at: 2017-12-04 07:19:32
import os, setuptools

def smart_find_packages(package_list):
    """Run find_packages the way we intend."""
    packages = []
    for pkg in package_list.strip().split('\n'):
        pkg_path = pkg.replace('.', os.path.sep)
        packages.append(pkg)
        packages.extend([ '%s.%s' % (pkg, f) for f in setuptools.find_packages(pkg_path)
                        ])

    return ('\n').join(set(packages))