# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/common.py
# Compiled at: 2017-01-14 03:18:28
# Size of source mod 2**32: 2041 bytes
import logging
from otest.events import EV_OPERATION
from otest.summation import assert_summation
from otest.verify import Verify

def setup_logger(log, log_file_name='tt.log'):
    hdlr = logging.FileHandler(log_file_name)
    base_formatter = logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
    hdlr.setFormatter(base_formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)


def make_list(flows, profile, map_prof, **kw_args):
    f_names = list(flows.keys())
    f_names.sort()
    flow_names = []
    for k in kw_args['order']:
        k += '-'
        l = [z for z in f_names if z.startswith(k)]
        flow_names.extend(l)

    res = []
    if profile:
        sprofile = profile.split('.')
    else:
        sprofile = []
    for tid in flow_names:
        _flow = flows[tid]
        if map_prof(sprofile, _flow['profile'].split('.')):
            res.append(tid)

    return res


def make_entity(**kw_args):
    raise NotImplemented()


def run_flow(profiles, conv, test_id, conf, profile, chk_factory, index=0):
    print('==' + test_id)
    conv.test_id = test_id
    conv.conf = conf
    if index >= len(conv.flow['sequence']):
        return
    conv.index = index
    for item in conv.flow['sequence'][index:]:
        if isinstance(item, tuple):
            cls, funcs = item
        else:
            cls = item
            funcs = {}
        _oper = cls(conv=conv, profile=profile, test_id=test_id, conf=conf,
          funcs=funcs,
          chk_factory=chk_factory)
        conv.operation = _oper
        conv.events.store(EV_OPERATION, (cls.__name__), sender='run_flow')
        _oper.setup(profiles.PROFILEMAP)
        _oper()
        conv.index += 1

    try:
        if conv.flow['tests']:
            _ver = Verify(chk_factory, conv)
            _ver.test_sequence(conv.flow['tests'])
    except KeyError:
        pass
    except Exception as err:
        try:
            raise
        finally:
            err = None
            del err

    info = assert_summation(conv, test_id)
    return info