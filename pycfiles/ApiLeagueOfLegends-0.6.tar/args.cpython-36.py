# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jojo/.virtualenvs/apikit/lib/python3.6/site-packages/apikit/args.py
# Compiled at: 2018-08-06 13:02:15
# Size of source mod 2**32: 1014 bytes
from flask import request
from werkzeug.exceptions import NotFound
BOOL_TRUISH = [
 'true', '1', 'yes', 'y', 't']

def arg_bool(name, default=False):
    """ Fetch a query argument, as a boolean. """
    v = request.args.get(name, '')
    if not len(v):
        return default
    else:
        return v in BOOL_TRUISH


def arg_int(name, default=None):
    """ Fetch a query argument, as an integer. """
    try:
        v = request.args.get(name)
        return int(v)
    except (ValueError, TypeError):
        return default


def get_limit(default=50, field='limit'):
    """ Get a limit argument. """
    return max(0, min(1000, arg_int(field, default=default)))


def get_offset(default=0, field='offset'):
    """ Get an offset argument. """
    return max(0, arg_int(field, default=default))


def obj_or_404(obj):
    if obj is None:
        raise NotFound()
    return obj


def request_data():
    data = request.get_json(silent=True)
    if data is None:
        data = dict(request.form.items())
    return data