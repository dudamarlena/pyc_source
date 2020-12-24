# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/routes.py
# Compiled at: 2011-11-24 04:30:49
import re, urllib, pypoly

class Route(object):
    _regex_parse = re.compile('{([^}]+)}')

    def __init__(self, name, route, defaults={}, types={}, requirements={}, action=None, controller=None):
        self._action = action
        self.controller = controller
        self._defaults = defaults
        self._types = types
        self._param_names = []
        self._requirements = {}
        self.name = name
        reg = route
        tpl = route
        for a in self._regex_parse.findall(route):
            (name, sep, param) = a.partition(':')
            if param == '':
                param = '[^/]+'
            reg = reg.replace('{' + a + '}', '(?P<%s>%s)' % (name, param))
            tpl = tpl.replace('{' + a + '}', '%(' + name + ')s')
            self._param_names.append(name)

        for (n, v) in requirements.items():
            t = type(v)
            if t == str or t == unicode:
                self._requirements[n] = re.compile('^' + v + '$')
            else:
                self._requirements[n] = v

        pypoly.log.debug("Creating Route with regex '%s' and template '%s'" % (
         reg,
         tpl))
        self._regex_match = re.compile('^' + reg + '$')
        self._tpl = tpl

    def generate(self, action=None, values={}):
        if action != None and self._action != None and self._action != action:
            return
        else:
            for name in self._param_names:
                if name in ('action', ):
                    continue
                if name not in values and name not in self._defaults:
                    return

            if action == None:
                action = self._action
            values_url = {}
            params = {}
            for (name, value) in values.items():
                if name not in self._param_names:
                    params[name] = value
                else:
                    values_url[name] = value

            if 'action' in self._param_names:
                values_url['action'] = action
            ret = self._tpl % values_url
            baseurl = pypoly.config.get('server.baseurl')
            if baseurl[(-1)] == '/':
                baseurl = baseurl[:-1]
            if ret[0] == '/':
                ret = ret[1:]
            ret = ('/').join([baseurl, ret])
            if len(params) == 0:
                return ret
            return ret + '?' + urllib.urlencode(params)

    def match(self, url):
        m = self._regex_match.match(url)
        if not m:
            return
        else:
            res = m.groupdict()
            params = self._defaults.copy()
            for (n, v) in res.items():
                if n == 'controller':
                    continue
                if n in self._requirements:
                    m = self._requirements[n].match(v)
                    if not m:
                        return
                if n in self._types:
                    try:
                        params[n] = self._types[n](v)
                    except Exception, inst:
                        pypoly.log.debug(str(inst))
                        return

                else:
                    params[n] = v

            action = params.pop('action', self._action)
            if action == None:
                return
            return {'action': action, 
               'controller': self.controller, 
               'params': params}


if __name__ == '__main__':
    import doctest
    doctest.testmod()