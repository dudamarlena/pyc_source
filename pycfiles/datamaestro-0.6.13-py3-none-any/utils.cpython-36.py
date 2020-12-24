# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/datamaestro/utils.py
# Compiled at: 2020-02-25 07:34:23
# Size of source mod 2**32: 2425 bytes
import logging, os, os.path as op, json
from pathlib import PosixPath, Path

def rm_rf(d):
    logging.debug('Removing directory %s' % d)
    for path in (op.join(d, f) for f in os.listdir(d)):
        if op.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)

    os.rmdir(d)


class TemporaryDirectory:

    def __init__(self, path: Path):
        self.delete = True
        self.path = path

    def __enter__(self):
        logging.debug('Creating directory %s', self.path)
        self.path.mkdir(parents=True, exist_ok=True)
        return self

    def __exit__(self, type, value, traceback):
        if self.delete:
            rm_rf(self.path)


class CachedFile:
    __doc__ = 'Represents a downloaded file that has been cached'

    def __init__(self, path, keep=False):
        self.path = path
        self.keep = keep

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if not self.keep:
                self.path.unlink()
        except Exception as e:
            logging.warning('Could not delete cached file %s [%s]', self.path, e)


def deprecated(message, f):
    from inspect import getframeinfo, stack

    def wrapped(*args, **kwargs):
        caller = getframeinfo(stack()[1][0])
        logging.warning('called at %s:%d - %s' % (caller.filename, caller.lineno, message))
        return f(*args, **kwargs)

    return wrapped


class JsonContext:
    pass


class BaseJSONEncoder(json.JSONEncoder):

    def __init__(self):
        super().__init__()
        self.context = JsonContext()

    def default(self, o):
        return {key:value for key, value in o.__dict__.items() if not key.startswith('__') if not key.startswith('__')}


class JsonEncoder(BaseJSONEncoder):
    __doc__ = 'Default JSON encoder'

    def default(self, o):
        if isinstance(o, PosixPath):
            return str(o.resolve())
        else:
            return super().default(o)


class XPMEncoder(BaseJSONEncoder):
    __doc__ = 'Experimaestro encoder'

    def default(self, o):
        if isinstance(o, PosixPath):
            return {'$type':'path',  '$value':str(o.resolve())}
        else:
            if hasattr(o.__class__, '__datamaestro__'):
                m = super().default(o)
                m['$type'] = o.__class__.__datamaestro__.id
                return m
            return super().default(o)