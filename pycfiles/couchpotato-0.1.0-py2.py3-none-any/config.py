# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/config.py
# Compiled at: 2009-07-23 14:02:24
__doc__ = '\nCouchish configuration.\n'
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