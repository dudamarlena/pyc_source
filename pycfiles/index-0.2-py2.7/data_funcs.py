# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\lib\data_funcs.py
# Compiled at: 2013-09-15 13:30:49
from __future__ import division, absolute_import, print_function, unicode_literals
import re, logging
from .backwardcompat import *

def get_list(val):
    if val == None:
        return []
    else:
        if isinstance(val, (list, tuple)):
            return val
        else:
            return [
             val]

        return []


def get_str_sequence(sequence_str):
    str_sequence = []
    sequence_list = sequence_str.split(b',')
    for i in sequence_list:
        if i:
            i = i.strip()
            str_sequence.append(i)

    return str_sequence


def get_int_sequence(sequence_str, from_list=None):
    from_len = None if from_list == None else len(from_list)
    int_sequence = []
    str_sequence = get_str_sequence(sequence_str)
    for i in str_sequence:
        nosequence = True
        if i.isdigit():
            if not i == b'0':
                i = int(i) - 1
                if i not in int_sequence:
                    int_sequence.append(i)
                nosequence = False
        else:
            res = re.match(b'^(\\d*)-(\\d*):?(\\d*)$', i)
            if res:
                start, stop, step = res.group(1, 2, 3)
                start = int(start) - 1 if start else 0
                stop = int(stop) if stop else from_len
                step = int(step) if step else 1
            else:
                res = re.match(b'^(\\d*):(-?\\d*):?(\\d*)$', i)
                if res:
                    start, stop, step = res.group(1, 2, 3)
                    start = int(start) if start else 0
                    stop = int(stop) + 1 if stop else from_len
                    step = int(step) if step else 1
                    if stop <= 0:
                        if from_len == None:
                            raise ValueError(b'Impossible to calculate the count of array! Array is not defined!')
                        stop = from_len - stop - 1
            if res:
                if stop == None:
                    raise ValueError(b'Impossible to calculate the count of array! Array is not defined!')
                for i in range(start, stop, step):
                    if i not in int_sequence:
                        int_sequence.append(i)

                nosequence = False
        if nosequence:
            raise ValueError((b"Wrong expression: '{0}'").format(i))

    int_sequence.sort()
    return int_sequence


def filter_list(from_list, filter):
    if filter == None:
        return from_list
    else:
        new_list = []
        if isinstance(filter, string_types):
            res = re.match(b'^\\[(.*)\\]$', filter)
            if res:
                filter = res.group(1)
                index_list = get_int_sequence(filter, from_list)
                from_len = len(from_list) - 1
                for i in index_list:
                    if i <= from_len:
                        new_list.append(from_list[i])
                    else:
                        logging.warning((b'Недопустимый индекс: {0}').format(i + 1))
                        break

            res = re.match(b'^\\((.*)\\)$', filter)
            if res:
                filter = res.group(1)
                names_list = get_str_sequence(filter)
                for name in names_list:
                    if name in from_list:
                        new_list.append(name)
                    else:
                        logging.warning((b'Недопустимое значение: {0}').format(name))

            res = re.match(b'^/(.*)/$', filter)
            if res:
                filter = res.group(1)
                pattern = re.compile(filter)
                for i in from_list:
                    if pattern.match(i):
                        new_list.append(i)

            if filter in from_list:
                new_list.append(filter)
        elif isinstance(filter, list):
            for name in filter:
                if name in from_list:
                    new_list.append(name)
                else:
                    logging.warning((b'Недопустимое значение: {0}').format(name))

        return new_list


def filter_match(name, filter, index=None):
    if filter == None:
        return True
    else:
        if isinstance(filter, string_types):
            res = re.match(b'^\\[(.*)\\]$', filter)
            if res:
                filter = res.group(1)
                index_list = get_int_sequence(filter)
                if index == None:
                    assert None, b'index required!'
                    return False
                return index in index_list
            res = re.match(b'^\\((.*)\\)$', filter)
            if res:
                filter = res.group(1)
                names_list = get_str_sequence(filter)
                return name in names_list
            res = re.match(b'^/(.*)/$', filter)
            if res:
                filter = res.group(1)
                if re.match(filter, name):
                    return True
                return False
        elif isinstance(filter, list):
            return name in filter
        return