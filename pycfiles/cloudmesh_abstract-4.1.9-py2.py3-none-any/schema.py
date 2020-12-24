# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/cloudmesh/rest/schema.py
# Compiled at: 2017-04-12 13:00:41
from __future__ import print_function
from ruamel import yaml
import os
from os.path import splitext, exists
import glob
from cloudmesh.common.Shell import Shell
import json
from cloudmesh.common.util import writefile
from cloudmesh.common.Shell import Shell

class ConvertSpec(object):

    def __init__(self, infile, outfile, indent=2):
        if '.py' in outfile:
            print('... converting', infile, '->', outfile)
            r = Shell.execute('evegenie', [infile])
            print(r)
        elif '.yml' in infile and '.json' in outfile:
            element = yaml.safe_load(open(infile))
            print('... writing to', outfile)
            writefile(outfile, json.dumps(element, indent=indent))
        else:
            print('conversion not yet supported')