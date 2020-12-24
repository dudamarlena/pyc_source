# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/PY3/CONJUGAR_/conjugar/araq.py
# Compiled at: 2018-11-27 23:12:38
# Size of source mod 2**32: 2116 bytes
import re, elist.elist as elel, estring.estring as eses

def creat_or_from_sarr(sarr):
    regex_str = elel.join(sarr, '|')
    return re.compile(regex_str)


def search_gen(regex, s, *args):
    args = list(args)
    arrlen = args.__len__()
    if arrlen == 0:
        start = 0
        end = s.__len__()
    else:
        if arrlen == 1:
            start = args[0]
            end = s.__len__()
        else:
            start = args[0]
            end = args[1]
    cur = start
    while True:
        m = regex.search(s, cur)
        if m:
            if m.start() < end:
                cur = m.end()
            yield m
        else:
            return


def find_all_spans(regex, s):
    rslt = []
    g = search_gen(regex, s)
    for each in g:
        ele = (
         each.start(), each.end())
        rslt.append(ele)

    return rslt


def regex_split(regex, s):
    spans = find_all_spans(regex, s)
    arr = eses.get_substr_arr_via_spans(s, spans)
    return arr


def de_cond_and_engine(ele, *args):
    args = list(args)
    conds = args[0]
    lngth = conds.__len__()
    if args.__len__() > 1:
        funcs = args[1]
        if isinstance(funcs, list):
            pass
        else:
            func = funcs
            funcs = elel.init(func, lngth)
    else:
        func = lambda ele, cond: ele in cond
        funcs = elel.init(lngth, func)
    for i in range(0, lngth):
        each = conds[i]
        tmp = funcs[i](each, ele)
        if tmp:
            pass
        else:
            return False

    return True


def de_cond_or_engine(ele, *args):
    args = list(args)
    conds = args[0]
    lngth = conds.__len__()
    if args.__len__() > 1:
        funcs = args[1]
        if isinstance(funcs, list):
            pass
        else:
            func = funcs
            funcs = elel.init(func, lngth)
    else:
        func = lambda ele, cond: ele in cond
        funcs = elel.init(lngth, func)
    for i in range(0, lngth):
        each = conds[i]
        tmp = funcs[i](each, ele)
        if tmp:
            return True

    return False