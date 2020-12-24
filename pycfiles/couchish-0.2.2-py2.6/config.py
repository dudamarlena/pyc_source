# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/couchish/config.py
# Compiled at: 2009-07-23 14:02:24
"""
Couchish configuration.
"""
from couchish.couchish_jsonbuilder import get_views

class Config(object):

    def __init__(self, types, views):
        self.types = types
        self.views = views
        self.viewdata = get_views(types, views)

    @classmethod
    def from_yaml(cls, types, views):
        """
        Load config from a set of YAML config files.
        """
        import yaml
        types = dict((name, yaml.load(file(filename))) for (name, filename) in types.iteritems())
        for (name, value) in types.items():
            if not value.get('metadata', {}).get('views', {}).get('all'):
                value.setdefault('metadata', {}).setdefault('views', {})['all'] = '%s/all' % name

        views = yaml.load(file(views))
        return cls(types, views)