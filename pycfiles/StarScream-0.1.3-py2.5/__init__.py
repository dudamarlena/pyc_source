# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\starscreamlib\__init__.py
# Compiled at: 2008-05-10 08:19:20
import sys, os, os.path as op
from pkg_resources import resource_string
from handout import build_handout
from slides import build_slides

def copy_css_files(dest):
    """Copy all the CSS files into the specified directory"""
    for f in ['handout', 'slide', 'syntax']:
        cssfile = f + '.css'
        copy_file(cssfile, dest)


def copy_script_files(dest):
    """Copy all the JS files into a ``scripts`` directory inside the
    specified directory. Create the ``scripts`` directory if necessary."""
    scriptDir = op.join(dest, 'scripts')
    if not op.exists(scriptDir):
        os.mkdir(scriptDir)
    for f in ['jquery.dimensions', 'jquery.gradient', 'jquery', 'scripts']:
        jsfile = f + '.js'
        copy_file('scripts/' + jsfile, dest)


def copy_file(name, dest):
    """Write the contents of ``name`` (a file in this module) to the
    directory ``dest``"""
    destFile = op.join(dest, name)
    if op.exists(destFile):
        return
    print name
    fout = open(destFile, 'wb')
    fout.write(resource_string(__name__, name))
    fout.close()