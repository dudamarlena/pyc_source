# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/verify.py
# Compiled at: 2017-04-17 13:34:47
# Size of source mod 2**32: 3327 bytes
import logging, sys, traceback
from otest import Break
from otest import ConditionError
from otest import exception_trace
from otest.check import CRITICAL
from otest.check import INTERACTION
from otest.events import EV_ASSERTION
from otest.events import EV_CONDITION
from otest.events import EV_FAULT
__author__ = 'roland'
logger = logging.getLogger(__name__)
LABELS = {'cid':'WHERE', 
 'status':'STATUS',  'http_status':'HTTP STATUS', 
 'message':'INFO'}

class MissingTest(Exception):
    pass


class Verify(object):

    def __init__(self, check_factory, conv, cls_name=''):
        self.check_factory = check_factory
        self.ignore_check = []
        self.exception = None
        self.conv = conv
        self.cls_name = cls_name

    def check_severity(self, stat):
        if stat.status in [CRITICAL, INTERACTION]:
            for attr, label in LABELS.items():
                try:
                    _val = getattr(stat, attr)
                except AttributeError:
                    pass
                else:
                    if _val:
                        self.conv.events.store(EV_FAULT, '{label}: {val}'.format(val=_val, label=label))

            try:
                if not stat.mti:
                    raise Break(stat.message)
                else:
                    raise ConditionError(stat.message)
            except KeyError:
                pass

    def do_check(self, test, **kwargs):
        logger.debug('do_check({}, {})'.format(test, kwargs))
        if isinstance(test, str):
            try:
                chk = (self.check_factory(test))(**kwargs)
            except TypeError:
                raise MissingTest(test)

        else:
            chk = test(**kwargs)
        if chk.__class__.__name__ not in self.ignore_check:
            self.conv.events.store(EV_ASSERTION, chk.__class__.__name__)
            try:
                stat = chk(self.conv)
            except Exception as err:
                try:
                    exception_trace('do_check', err, logger)
                    raise
                finally:
                    err = None
                    del err

            else:
                if self.cls_name:
                    stat.context = self.cls_name
                self.conv.events.store(EV_CONDITION, stat, sender=(self.__class__))
                self.check_severity(stat)

    def err_check(self, test, err=None, bryt=True):
        if err:
            self.exception = err
        chk = self.check_factory(test)()
        chk(self, self.conv.events.last_item(EV_CONDITION))
        if bryt:
            e = ConditionError('%s' % err)
            e.trace = ''.join((traceback.format_exception)(*sys.exc_info()))
            raise e

    def test_sequence(self, sequence):
        if isinstance(sequence, dict):
            for test, kwargs in list(sequence.items()):
                if not kwargs:
                    self.do_check(test)
                else:
                    (self.do_check)(test, **kwargs)

        else:
            for test in sequence:
                if isinstance(test, tuple):
                    test, kwargs = test
                    kwargs = kwargs or {}
                else:
                    kwargs = {}
                (self.do_check)(test, **kwargs)

        return True