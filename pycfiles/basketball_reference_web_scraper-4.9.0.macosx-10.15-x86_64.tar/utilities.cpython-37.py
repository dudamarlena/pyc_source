# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaebradley/.virtualenvs/basketball_reference_web_scraper/lib/python3.7/site-packages/basketball_reference_web_scraper/utilities.py
# Compiled at: 2020-01-10 17:57:04
# Size of source mod 2**32: 450 bytes


def str_to_int(value, default=int(0)):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return default


def str_to_float(value, default=float(0)):
    stripped_value = value.strip()
    try:
        return float(stripped_value)
    except ValueError:
        return default


def merge_two_dicts(first, second):
    combined = first.copy()
    combined.update(second)
    return combined