# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compare_for_testing/compare.py
# Compiled at: 2019-10-11 07:35:28
# Size of source mod 2**32: 2585 bytes
from collections.abc import Iterator
from itertools import zip_longest
from typing import Union

class CompareJson:
    start_index = 0
    accuracy = 3

    @staticmethod
    def is_instance(v_iter, v_type):
        return all(map(lambda t: isinstance(t, v_type), v_iter))

    @staticmethod
    def _strip_values(v_in, v_out):
        if isinstance(v_out, str):
            v_out = v_out.strip()
        if isinstance(v_in, str):
            v_in = v_in.strip()
        return (v_in, v_out)

    def _compare_array(self, v_in, v_out, mismatch_items):
        for key, value in enumerate((zip_longest(v_in, v_out)), start=(self.start_index)):
            result = (CompareJson())(*value)
            if result:
                mismatch_items[key] = result

    def _compare_number(self, v_in, v_out):
        return round(v_in, self.accuracy) != round(v_out, self.accuracy)

    @staticmethod
    def _is_equal(v_in, v_out):
        return any((
         v_in == v_out,
         v_in == '!not_empty' and v_out != 'нет в ответе' and v_out,
         v_in == '!empty' and not v_out))

    @staticmethod
    def _compare_dict(v_in, v_out, mismatch_items):
        for key, value_in in v_in.items():
            result = CompareJson()(value_in, v_out.get(key, 'Поля %r нет в ответе' % key))
            if result:
                mismatch_items[key] = result

    def __call__(self, v_in, v_out) -> Union[(None, dict)]:
        v_in, v_out = self._strip_values(v_in, v_out)
        mismatch_items = dict()
        if self._is_equal(v_in, v_out):
            pass
        elif self.is_instance((v_in, v_out), (list, tuple, Iterator)):
            self._compare_array(v_in, v_out, mismatch_items)
        elif isinstance(v_in, set):
            if v_in.symmetric_difference(v_out):
                return self.formation_error(list(v_in), v_out)
            elif self.is_instance((v_in, v_out), (int, float)) and self._compare_number(v_in, v_out):
                return self.formation_error(v_in, v_out)
            if self.is_instance((v_in, v_out), dict):
                self._compare_dict(v_in, v_out, mismatch_items)
        else:
            return self.formation_error(v_in, v_out)
        return mismatch_items

    @staticmethod
    def formation_error(v_in, v_out):
        return {'Хотели':v_in, 
         'Получили':v_out}


compare = CompareJson()