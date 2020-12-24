# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/csv/csv_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 1640 bytes
import csv
from nose.tools import assert_greater_equal
from foxylib.tools.collections.collections_tool import iter2singleton, merge_dicts, vwrite_no_duplicate_key

class CSVTool:

    @classmethod
    def filepath2str_ll(cls, filepath):
        with open(filepath, 'r', encoding='utf-8') as (f):
            r = csv.reader(f)
            l = list(r)
        return l

    @classmethod
    def lines2str_ll(cls, lines):
        r = csv.reader(lines)
        l = list(r)
        return l

    @classmethod
    def str_ll2h_list(cls, str_ll):
        assert_greater_equal(len(str_ll), 1)
        m = iter2singleton(map(len, str_ll))
        key_list = str_ll[0]
        h_list = [merge_dicts([{key_list[j]: l[j]} for j in range(m)],
          vwrite=vwrite_no_duplicate_key) for l in str_ll[1:]]
        return h_list

    @classmethod
    def strs_iter2fileptr(cls, str_list_iter, file_pointer):
        writer = csv.writer(file_pointer, quoting=(csv.QUOTE_MINIMAL))
        for l in str_list_iter:
            writer.writerow(l)

    @classmethod
    def strs_iter2file(cls, str_list_iter, filepath):
        with open(filepath, 'w', newline='') as (f):
            cls.strs_iter2fileptr(str_list_iter, f)

    @classmethod
    def utf8s_iter2file(cls, utf8_list_iter, filepath):
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as (f):
            cls.strs_iter2fileptr(utf8_list_iter, f)