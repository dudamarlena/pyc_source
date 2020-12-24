# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/ropetools.py
# Compiled at: 2013-11-12 16:48:22
"""
Created on Thu Oct 10 21:17:46 2013

@author: user
"""
import pdb, sys, os, rope
from pprint import pprint as pp
import rope.base.project
from rope.base import libutils
myproject = rope.base.project.Project(os.getcwd())
myresource = libutils.path_to_resource(myproject, 'textools.py')
from rope.refactor.extract import ExtractVariable
from rope import refactor