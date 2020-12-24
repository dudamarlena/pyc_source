# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\models\helpers.py
# Compiled at: 2017-01-30 05:55:29
# Size of source mod 2**32: 732 bytes
from difflib import HtmlDiff
differ = HtmlDiff()

def delta_field_dictionaries(new, old):
    differences = {}
    for key in set(new.keys()) | set(old.keys()):
        new_value = new.get(key)
        old_value = old.get(key)
        if new_value != old_value:
            differences[key] = {'new': new_value, 
             'old': old_value}

    return differences


def difference_table(new, old):
    deltas = delta_field_dictionaries(new.field_dict, old.field_dict)
    html = ''
    for key in deltas:
        html += differ.make_table(deltas[key]['old'].split('\n'), deltas[key]['new'].split('\n'), 'old', 'new')

    return html