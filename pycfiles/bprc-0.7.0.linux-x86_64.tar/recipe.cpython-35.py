# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/recipe.py
# Compiled at: 2016-08-20 13:14:45
# Size of source mod 2**32: 10426 bytes
"""
This module implements all the class types required to represent the YAML recipe in memory.
"""
import os, sys
from itertools import chain
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import logging, collections
from bprc.utils import vlog, errlog, verboseprint

class Headers(collections.MutableMapping):
    __doc__ = 'A collection of HTTP request or response headers'

    def __init__(self, headers):
        self._headers = dict((k.lower(), v) for k, v in headers.items())

    def __getitem__(self, key):
        lkey = key.lower()
        return self._headers[lkey]

    def __setitem__(self, key, value):
        lkey = key.lower()
        self._headers[lkey] = value

    def __delitem__(self, key):
        lkey = key.lower()
        del self._headers[lkey]

    def __iter__(self):
        return iter(self._headers)

    def __len__(self):
        return len(self._headers)


class Body(collections.MutableMapping):
    __doc__ = 'A collection of parameters in an HTTP request or response body'

    def __init__(self, body):
        self._body = body

    def __getitem__(self, key):
        return self._body[key]

    def __setitem__(self, key, value):
        self._body[key] = value

    def __delitem__(self, key):
        del self._body[key]

    def __iter__(self):
        return iter(self._body)

    def __len__(self):
        return len(self._body)


class QueryString(collections.MutableMapping):
    __doc__ = 'An collection of parameters passed on an HTTP Querystring, used for passing URL parameters'

    def __init__(self, querystring):
        self._querystring = querystring

    def __getitem__(self, key):
        return self._querystring[key]

    def __setitem__(self, key, value):
        self._querystring[key] = value

    def __delitem__(self, key):
        del self._querystring[key]

    def __iter__(self):
        return iter(self._querystring)

    def __len__(self):
        return len(self._querystring)


class Options(collections.MutableMapping):
    __doc__ = 'An collection of parameters passed options into a step'

    def __init__(self, options):
        if options is not None:
            self._options = options
        else:
            self._options = {}

    def __getitem__(self, key):
        return self._options[key]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __delitem__(self, key):
        del self._options[key]

    def __iter__(self):
        return iter(self._options)

    def __len__(self):
        return len(self._options)

    def __str__(self):
        outstr = ''
        for key, value in sorted(self._options.items()):
            outstr += key + ': ' + str(value) + ', '

        return outstr


class Response:
    __doc__ = 'An HTTP Response, part of a step'

    def __init__(self, *, code, headers, body):
        self.code = code
        self.headers = Headers(headers)
        self.body = Body(body)


class Request:
    __doc__ = 'An HTTP Request, part of a step'

    def __init__(self, *, headers, querystring, body):
        self.headers = Headers(headers)
        self.querystring = QueryString(querystring)
        self.body = Body(body)


class Step:
    __doc__ = 'Defines a Step in the Recipe - a specific URL and its properties'

    def __init__(self, *, name, URL, httpmethod, request, response, options):
        self.name = name
        self.URL = URL
        self.httpmethod = httpmethod
        self.options = Options(options)
        for part in ['headers', 'body', 'querystring']:
            try:
                logging.debug(request[part])
            except KeyError as ke:
                vlog('No request ' + part + ' values passed into step ' + self.name)
                request.update({part: {}})
            except TypeError as te:
                vlog('No request ' + part + ' object passed into step ' + self.name)
                request = {}
                request.update({part: {}})

        self.request = Request(headers=request['headers'], querystring=request['querystring'], body=request['body'])
        for part in ['headers', 'body']:
            try:
                logging.debug(response[part])
            except KeyError as ke:
                vlog('No response ' + part + ' values passed into step ' + self.name)
                response.update({part: {}})
            except TypeError as te:
                vlog('No response ' + part + ' object passed into step ' + self.name)
                response = {}
                response.update({part: {}})

        try:
            logging.debug(response['code'])
        except KeyError as ke:
            vlog('No response code values passed into step ' + self.name)
            response.update({'code': ''})

        self.response = Response(code=response['code'], headers=response['headers'], body=response['body'])


class Recipe:
    __doc__ = 'Defines the Recipe class, which holds a list of URLs to process'

    def __init__(self, dmap):
        if 'recipe' not in dmap:
            errlog("No 'recipe' found in YAML input. Aborting", KeyError("Missing 'recipe'"))
            raise KeyError
        if not isinstance(dmap['recipe'], list):
            errlog("Could not find any 'steps' in the recipe", TypeError("Missing 'step'"))
            raise TypeError
        self.steps = []
        for i, item in enumerate(dmap['recipe']):
            vlog('Parsing recipe step ' + str(i))
            try:
                logging.debug('Recipe: Name =' + str(dmap['recipe'][i]['name']))
            except KeyError as ke:
                vlog("No step name set. Setting name to 'Step " + str(i) + "'")
                dmap['recipe'][i].update({'name': 'Step: ' + str(i)})

            try:
                logging.debug('Recipe: Options =' + str(dmap['recipe'][i]['options']))
            except KeyError as ke:
                vlog('No step options passed. Creating empty options opbject for this step.')
                dmap['recipe'][i].update({'options': {}})

            try:
                logging.debug('Recipe: URL =' + str(dmap['recipe'][i]['URL']))
            except KeyError as ke:
                errlog('No URL set in step ' + str(i) + '. Aborting...', ke)
                raise KeyError

            try:
                logging.debug('Recipe: HTTPMethod =' + str(dmap['recipe'][i]['httpmethod']))
            except KeyError as ke:
                vlog('No HTTPMethod set. Defaulting to GET')
                dmap['recipe'][i].update({'httpmethod': 'GET'})

            try:
                logging.debug('Recipe: Request =' + str(dmap['recipe'][i]['request']))
            except KeyError as ke:
                vlog('No request set. Creating an empty request object with headers, body and querystring')
                dmap['recipe'][i].update({'request': {'body': {}, 'querystring': {}, 'headers': {}}})

            try:
                logging.debug('Recipe: Response =' + str(dmap['recipe'][i]['response']))
            except KeyError as ke:
                vlog('No response set. Creating an empty response object with headers, body and response code')
                dmap['recipe'][i].update({'response': {'body': {}, 'code': '', 'headers': {}}})

            vlog('Creating recipe step object id=' + str(i) + '...')
            self.steps.append(Step(name=dmap['recipe'][i]['name'], URL=dmap['recipe'][i]['URL'], httpmethod=dmap['recipe'][i]['httpmethod'], request=dmap['recipe'][i]['request'], response=dmap['recipe'][i]['response'], options=dmap['recipe'][i]['options']))
            vlog('Parsed recipe step ' + str(i) + ' (' + dmap['recipe'][i]['name'] + ') ok...')

    def __str__(self):
        ret_str = ''
        for s in self.steps:
            ret_str += 'Step= ' + str(s)

        return ret_str