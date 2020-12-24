# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/web/helpers.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 528 bytes


def create_url_for_helper(name, *parts, **defaults):

    def url_for_helper(self, *args, absolute=False, **kwargs):
        params = dict(defaults)
        params.update(kwargs)
        _parts = params.pop('parts', {})
        _parts.update(dict(zip(parts, map(str, args))))
        if _parts:
            params['parts'] = _parts
        url = self.request.app.router[name].url(**params)
        if absolute:
            return self.make_url_absolute(url)
        return url

    url_for_helper.__name__ = 'url_for_' + name
    return url_for_helper