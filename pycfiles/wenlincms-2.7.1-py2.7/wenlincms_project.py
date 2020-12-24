# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/bin/wenlincms_project.py
# Compiled at: 2016-05-20 23:41:38
from __future__ import unicode_literals
import os
from distutils.dir_util import copy_tree
from optparse import OptionParser
from wenlincms.utils.importing import path_for_import

def create_project():
    u"""
    复制 project_template 到当前目录
    """
    parser = OptionParser(usage=b'usage: %prog [options] project_name')
    parser.add_option(b'-a', b'--alternate', dest=b'alt', metavar=b'PACKAGE', help=b'Alternate package to use, containing a project_template')
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error(b'project_name must be specified')
    project_name = args[0]
    if project_name.startswith(b'-'):
        parser.error(b"project_name cannot start with '-'")
    project_path = os.path.join(os.getcwd(), project_name)
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error(b"'%s' conflicts with the name of an existing Python module and cannot be used as a project name. Please try another name." % project_name)

    packages = [
     b'wenlincms']
    if options.alt:
        packages.append(options.alt)
    for package_name in packages:
        try:
            __import__(package_name)
        except ImportError:
            parser.error(b"Could not import package '%s'" % package_name)

    for package_name in packages:
        package_path = path_for_import(package_name)
        copy_tree(os.path.join(package_path, b'project_template'), project_path)

    for root, dirs, files in os.walk(project_path, False):
        for f in files:
            try:
                if f.endswith(b'.pyc'):
                    os.remove(os.path.join(root, f))
            except:
                pass


if __name__ == b'__main__':
    create_project()