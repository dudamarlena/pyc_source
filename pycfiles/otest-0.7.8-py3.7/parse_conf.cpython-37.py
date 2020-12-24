# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/rp/parse_conf.py
# Compiled at: 2016-10-24 10:04:08
# Size of source mod 2**32: 1730 bytes
import json
from otest import Unknown
__author__ = 'roland'

def translate(spec, func_factories):
    asp = {}
    for key, args in spec.items():
        _fnc = None
        for fact in func_factories:
            try:
                _fnc = fact(key)
            except Exception:
                pass
            else:
                break

        if not _fnc:
            raise Unknown('Check {}'.format(key))
        asp[_fnc] = args

    return asp


COPY = [
 'descr']

def parse_json_conf(cnf_file, cls_factories, chk_factories, func_factories):
    """

    :param cnf_file:
    :param cls_factories:
    :param chk_factory:
    :return:
    """
    stream = open(cnf_file, 'r')
    js = json.load(stream)
    stream.close()
    res = {}
    for tid, spec in js.items():
        ops = {}
        for oper, asse in spec.items():
            if oper == 'setup':
                if asse:
                    ops['setup'] = translate(asse, func_factories)
                else:
                    ops['setup'] = {}
            elif oper in COPY:
                ops[oper] = asse
            else:
                _cls = ''
                for fact in cls_factories:
                    try:
                        _cls = fact(oper)
                    except Exception:
                        pass
                    else:
                        break

                if not _cls:
                    raise Unknown('Operation {}'.format(oper))
                ops[_cls.__name__] = {'assert': {}}
            if 'assert' in asse and asse['assert'] is not None:
                ops[_cls.__name__]['assert'] = translate(asse['assert'], chk_factories)

        res[tid] = ops

    return res