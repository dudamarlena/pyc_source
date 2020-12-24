# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/path_builder.py
# Compiled at: 2015-08-31 22:18:13
import inspect, re, string

class PathBuilder(object):

    class PathTemplate(string.Template):
        delimiter = ':'

    @classmethod
    def build(cls, obj, params, path_template):
        path = path_template
        if hasattr(obj, 'api_attributes') and not inspect.isclass(obj):
            attributes = obj.api_attributes()
            path = PathBuilder.PathTemplate(path).safe_substitute(**attributes)
        if not params:
            params = {}
        path = PathBuilder.PathTemplate(path).safe_substitute(**params)
        remaining = [ m.start() for m in re.finditer(':', path) ]
        if len(remaining):
            raise ValueError('The template path (%s) can not be properly created from the provided object and params.' % path)
        return path