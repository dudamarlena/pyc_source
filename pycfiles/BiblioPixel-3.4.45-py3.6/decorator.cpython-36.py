# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/rest/decorator.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2062 bytes
import flask, functools, traceback, urllib
from .. import editor
NO_PROJECT_ERROR = 'No Project is currently loaded'
BAD_ADDRESS_ERROR = 'Bad address {address}'
BAD_GETTER_ERROR = "Couldn't get address {address}"
BAD_SETTER_ERROR = "Couldn't set value {value} at address {address}"

def single(method):
    """Decorator for RestServer methods that take a single address"""

    @functools.wraps(method)
    def single(self, address, value=None):
        address = urllib.parse.unquote_plus(address)
        try:
            error = NO_PROJECT_ERROR
            if not self.project:
                raise ValueError
            error = BAD_ADDRESS_ERROR
            ed = editor.Editor(address, self.project)
            if value is None:
                error = BAD_GETTER_ERROR
                result = method(self, ed)
            else:
                error = BAD_SETTER_ERROR
                result = method(self, ed, value)
            result = {'value': result}
        except Exception as e:
            traceback.print_exc()
            msg = '%s\n%s' % ((error.format)(**locals()), e)
            result = {'error': msg}

        return flask.jsonify(result)

    return single


def multi(method):
    """Decorator for RestServer methods that take multiple addresses"""

    @functools.wraps(method)
    def multi(self, address=''):
        values = flask.request.values
        address = urllib.parse.unquote_plus(address)
        if address:
            if values:
                if not address.endswith('.'):
                    address += '.'
        result = {}
        for a in values or '':
            try:
                if not self.project:
                    raise ValueError('No Project is currently loaded')
                ed = editor.Editor(address + a, self.project)
                result[address + a] = {'value': method(self, ed, a)}
            except:
                if self.project:
                    traceback.print_exc()
                result[address + a] = {'error': 'Could not multi addr %s' % a}

        return flask.jsonify(result)

    return multi