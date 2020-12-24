# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/bandit/job.py
# Compiled at: 2017-01-27 17:18:38
import json, os, sys

class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


class Metadata(Map):
    """
    Metadata that can be stored for your job.
    """

    def __setitem__(self, key, value):
        try:
            json.dumps(key)
            json.dumps(value)
        except Exception as e:
            raise Exception(e)

        super(Metadata, self).__setitem__(key, value)
        self._write_metadata(self)

    def __delitem__(self, key):
        super(Metadata, self).__delitem__(key)
        self._write_metadata(self)

    def _write_metadata(self, data):
        try:
            json.dumps(data)
        except Exception as e:
            raise Exception('data is not json serializable: %s' % str(e))

        if not os.path.exists('/job/metadata/metadata.json'):
            sys.stderr.write(json.dumps(data, indent=2) + '\n')
            return
        with open('/job/metadata/metadata.json', 'wb') as (f):
            json.dump(data, f)

    def _get_metadata(self):
        if not os.path.exists('/job/metadata/metadata.json'):
            return {}
        with open('/job/metadata/metadata.json', 'rb') as (f):
            return json.load(f)