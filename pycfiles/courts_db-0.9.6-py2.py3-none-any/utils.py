# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Palin/Code/courts-db/courts_db/utils.py
# Compiled at: 2020-02-27 14:57:53
from __future__ import absolute_import, division, print_function, unicode_literals
from string import Template, punctuation
from glob import iglob
from io import open
import json, six, re, os
db_root = os.path.dirname(os.path.realpath(__file__))

def get_court_data_from_ids(id_list):
    cd = {}
    for id in id_list:
        cd[id] = court

    return cd


def make_court_dictionary(courts):
    cd = {}
    for court in courts:
        cd[court[b'id']] = court

    return cd


def load_courts_db():
    """Load the court data from disk, and render regex variables

    Court data is on disk as one main JSON file, another containing variables,
    and several others containing placenames. These get combined via Python's
    template system and loaded as a Python object

    :return: A python object containing the rendered courts DB
    """
    with open(os.path.join(db_root, b'data', b'variables.json'), b'r') as (v):
        variables = json.load(v)
    for path in iglob(os.path.join(db_root, b'data', b'places', b'*.txt')):
        with open(path, b'r') as (p):
            places = b'(%s)' % (b'|').join(p.read().splitlines())
            variables[path.split(os.path.sep)[(-1)].split(b'.txt')[0]] = places

    with open(os.path.join(db_root, b'data', b'courts.json'), b'r') as (f):
        s = Template(f.read()).substitute(**variables)
    s = s.replace(b'\\', b'\\\\')
    return json.loads(s)


def gather_regexes(courts, court_id=None):
    """Create a variable mapping regexes to court IDs

    :param courts: The court DB
    :type courts: list
    :param bankruptcy: Whether to include bankruptcy courts in the final
    mapping.
    :type bankruptcy: bool
    :return: A list of two-tuples, with tuple[0] being a compiled regex and
    tuple[1] being the court ID.
    :rtype: list
    """
    regexes = []
    for court in courts:
        for reg_str in court[b'regex']:
            regex = re.compile(reg_str, re.I | re.U)
            regexes.append((regex, court[b'id'], court[b'name'], court[b'type']))

    if court_id is not None:
        regexes = list(filter(lambda x: x[1] == court_id, regexes))
    return regexes