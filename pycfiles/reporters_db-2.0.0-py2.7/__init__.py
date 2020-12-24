# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reporters_db/__init__.py
# Compiled at: 2020-02-28 18:07:21
import datetime, json, os, six
from .utils import suck_out_editions, names_to_abbreviations, suck_out_variations_only

def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, six.string_types):
            try:
                dct[k] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
            except:
                pass

    return dct


db_root = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(db_root, 'data', 'reporters.json')) as (f):
    REPORTERS = json.load(f, object_hook=datetime_parser)
with open(os.path.join(db_root, 'data', 'state_abbreviations.json')) as (f):
    STATE_ABBREVIATIONS = json.load(f)
with open(os.path.join(db_root, 'data', 'case_name_abbreviations.json')) as (f):
    CASE_NAME_ABBREVIATIONS = json.load(f)
VARIATIONS_ONLY = suck_out_variations_only(REPORTERS)
EDITIONS = suck_out_editions(REPORTERS)
NAMES_TO_EDITIONS = names_to_abbreviations(REPORTERS)