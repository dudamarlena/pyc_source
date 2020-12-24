# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/json.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.json\n    ~~~~~~~~~~~~~~~~\n\n    This file does not directly provide JSON dumping/parsing methods\n    but imports the required methods from various JSON parsers.\n\n    Currently supported:\n\n    * simplejson: http://undefined.org/python/#simple_json\n    * python-json: http://cheeseshop.python.org/pypi/python-json\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from datetime import datetime, tzinfo
from pocoo.exceptions import PocooRuntimeError
__all__ = [
 'dump', 'load', 'dumps', 'loads', 'parse_jsonrpc_request', 'dump_datetime', 'parse_datetime']
try:
    from simplejson import dump, load, dumps, loads
except ImportError:
    try:
        _json = __import__('json')
        _ = (_json.JsonReader, _json.JsonWriter)
    except (ImportError, AttributeError):
        raise PocooRuntimeError('No supported JSON library is installed! Please install either simplejson or python-json.')
    else:

        def dump(obj, fileobj):
            """Serialize ``obj`` to the file object ``fileobj``."""
            fileobj.write(_json.write(obj))


        def load(fileobj):
            """Load serialized data form the file object ``fileobj``."""
            return _json.read(fileobj.read())


        def dumps(obj):
            """Return ``obj`` serialized as a string."""
            return _json.write(obj)


        def loads(s):
            """Load serialized data from the string ``s``."""
            return _json.read(s)


def parse_jsonrpc_request(data):
    """
    Give the method a string and it will return all information required
    so that you can call an exported method according to jsonrpc 1.1

    :return: (method, args, kwargs, id)
    """
    try:
        request = loads(data)
    except:
        raise ValueError('malformed json')

    if not isinstance(request, dict):
        raise ValueError('invalid request')
    if float(request.get('version', '1.0')) < 1.1:
        raise ValueError('jsonrpc 1.1 request required')
    if 'method' not in request or 'params' not in request:
        raise ValueError('method or parameters not given')
    method = request['method']
    params = request['params']
    if isinstance(params, list):
        args = tuple(params)
        kwargs = {}
    elif isinstance(params, dict):
        args = {}
        kwargs = {}
        for (key, value) in params.iteritems():
            if key.isdigit():
                args[int(key)] = value
            else:
                kwargs[key] = value

        try:
            args = tuple((args[idx] for idx in xrange(len(args))))
        except IndexError:
            raise ValueError('invalid parameter definition')

    id = request.get('id')
    return (
     method, args, kwargs, id)


def dump_datetime(d):
    """Creates a string for the datetime object a javascript
    function can parse. You just need to pass the resuling string
    on the client to ``new Date()``."""
    return d.strftime('%m %d %Y %H:%M:%S UTC')


def parse_datetime(d):
    """Takes a javascript dateformat (``new Date().toGMTString()``)
    string and returns a valid datetime object."""
    try:
        (_, day, month, year, time, _) = d.split()
        (hours, minutes, seconds) = time.split(':')
        return datetime(int(year), [
         'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Dec'].index(month) + 1, int(day), int(hours), int(minutes), int(seconds))
    except ValueError:
        raise ValueError('not a valid date string')