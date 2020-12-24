# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reporters_db/utils.py
# Compiled at: 2020-02-28 18:07:21
import datetime, json
from collections import OrderedDict

def suck_out_variations_only(reporters):
    """Builds a dictionary of variations to canonical reporters.

    The dictionary takes the form of:
        {
         "A. 2d": ["A.2d"],
         ...
         "P.R.": ["Pen. & W.", "P.R.R.", "P."],
        }

    In other words, it's a dictionary that maps each variation to a list of
    reporters that it could be possibly referring to.
    """
    variations_out = {}
    for reporter_key, data_list in reporters.items():
        for data in data_list:
            for variation_key, variation_value in data['variations'].items():
                try:
                    variations_list = variations_out[variation_key]
                    if variation_value not in variations_list:
                        variations_list.append(variation_value)
                except KeyError:
                    variations_out[variation_key] = [
                     variation_value]

    return variations_out


def suck_out_editions(reporters):
    """Builds a dictionary mapping edition keys to their root name.

    The dictionary takes the form of:
        {
         "A.":   "A.",
         "A.2d": "A.",
         "A.3d": "A.",
         "A.D.": "A.D.",
         ...
        }

    In other words, this lets you go from an edition match to its parent key.
    """
    editions_out = {}
    for reporter_key, data_list in reporters.items():
        for data in data_list:
            for edition_key, edition_value in data['editions'].items():
                try:
                    editions_out[edition_key]
                except KeyError:
                    editions_out[edition_key] = reporter_key

    return editions_out


def names_to_abbreviations(reporters):
    """Build a dict mapping names to their variations

    Something like:

        {
            "Atlantic Reporter": ['A.', 'A.2d'],
        }

    Note that the abbreviations are sorted by start date.
    """
    names = {}
    for reporter_key, data_list in reporters.items():
        for data in data_list:
            abbrevs = data['editions'].keys()
            sort_func = lambda x: str(data['editions'][x]['start']) + x
            abbrevs = sorted(abbrevs, key=sort_func)
            names[data['name']] = abbrevs

    sorted_names = OrderedDict(sorted(names.items(), key=lambda t: t[0]))
    return sorted_names


def print_json_with_dates(obj):
    date_handler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) else None
    print json.dumps(obj, default=date_handler, sort_keys=True)