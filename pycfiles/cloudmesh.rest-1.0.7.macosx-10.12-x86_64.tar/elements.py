# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/ENV2/lib/python2.7/site-packages/cloudmesh/rest/elements.py
# Compiled at: 2017-04-12 13:00:41
from __future__ import print_function
import glob, json

class Elements(object):

    def __init__(self, directory, filename):
        import yaml, os.path
        settings = {}
        try:
            os.remove(filename)
        except Exception as e:
            pass

        if '.yaml' in filename:
            for file in glob.glob(os.path.join(directory, '*.yml')):
                with open(file) as (fd):
                    d = yaml.load(fd)
                    settings.update(d)

        elif 'json' in filename:
            for file in glob.glob(os.path.join(directory, '*.json')):
                print('... reading', file)
                with open(file) as (fd):
                    d = json.load(fd)
                    settings.update(d)

        else:
            print('converrsion not supported')
            return
        with open(filename, 'w') as (fd):
            json.dump(settings, fd, indent=4)
        return