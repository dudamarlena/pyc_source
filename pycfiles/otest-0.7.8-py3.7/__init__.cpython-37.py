# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/__init__.py
# Compiled at: 2019-05-24 02:43:07
# Size of source mod 2**32: 6817 bytes
"""
    otest
    ~~~~~~~~~~

    Basic functionality needed by OAuth2, OIDC and UMA test tools
    :copyright: (c) 2016 by Roland Hedberg.
    :license: APACHE 2.0, see LICENSE for more details.
"""
from __future__ import print_function
import json, logging, time, traceback, requests, sys
from subprocess import Popen, PIPE
from oic.oauth2 import HttpError
from otest.events import EV_END
__author__ = 'roland'
__version__ = '0.7.8'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2019 Roland Hedberg'
LOCAL_PATH = 'export/'
END_TAG = '==== END ===='
CRYPTSUPPORT = {'none':'n',  'signing':'s',  'encryption':'e'}

class AATestError(Exception):
    pass


class FatalError(AATestError):
    pass


class Break(AATestError):
    pass


class Unknown(AATestError):
    pass


class ConfigurationError(AATestError):
    pass


class NotSupported(AATestError):
    pass


class RequirementsNotMet(AATestError):
    pass


class CheckError(AATestError):
    pass


class OperationError(AATestError):
    pass


class ConditionError(FatalError):
    pass


def as_bytes(s):
    """
    Convert an unicode string to bytes.
    :param s: Unicode / bytes string
    :return: bytes string
    """
    try:
        s = s.encode('utf-8', 'replace')
    except (AttributeError, UnicodeDecodeError):
        pass

    return s


def as_unicode(b):
    """
    Convert a byte string to a unicode string
    :param b: byte string
    :return: unicode string
    """
    try:
        b = b.decode()
    except (AttributeError, UnicodeDecodeError):
        pass

    return b


def start_script(path, wdir='', *args):
    if not path.startswith('/'):
        popen_args = [
         './' + path]
    else:
        popen_args = [
         path]
    popen_args.extend(args)
    if wdir:
        return Popen(popen_args, stdout=PIPE, stderr=PIPE, cwd=wdir)
    return Popen(popen_args, stdout=PIPE, stderr=PIPE)


def stop_script_by_name(name):
    import subprocess, signal, os
    p = subprocess.Popen(['ps', '-A'], stdout=(subprocess.PIPE))
    out, err = p.communicate()
    for line in out.splitlines():
        if name in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def stop_script_by_pid(pid):
    import signal, os
    os.kill(pid, signal.SIGKILL)


def get_page(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.text
    raise HttpError(resp.status_code)


def exception_trace(tag, exc, log=None):
    message = (traceback.format_exception)(*sys.exc_info())
    if log:
        if isinstance(exc, Exception):
            log.error('[%s] ExcList: %s' % (tag, ''.join(message)))
        log.error('[%s] Exception: %s' % (tag, exc))
    else:
        if isinstance(exc, Exception):
            print(('[%s] ExcList: %s' % (tag, ''.join(message))), file=(sys.stderr))
        try:
            print(('[%s] Exception: %s' % (tag, exc)), file=(sys.stderr))
        except UnicodeEncodeError:
            print(('[%s] Exception: %s' % (
             tag, exc.message.encode('utf-8', 'replace'))),
              file=(sys.stderr))

        return message


class ContextFilter(logging.Filter):
    __doc__ = '\n    This is a filter which injects time laps information into the log.\n    '

    def start(self):
        self.start = time.time()

    def filter(self, record):
        record.delta = time.time() - self.start
        return True


def jlog(logger, typ, item):
    func = getattr(logger, typ)
    func(json.dumps(item, indent=2, sort_keys=True))


def resp2json(resp):
    return {'message':resp.message, 
     'status':resp.status,  'headers':resp.headers}


from otest.operation import Operation

class Done(Operation):

    def run(self, *args, **kwargs):
        self.conv.events.store(EV_END, '')