# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reporters_db/make_csv.py
# Compiled at: 2020-02-28 18:07:21
"""This will take the reporters json file and flatten it into a CSV."""
import csv
from reporters_db import REPORTERS
FIELDNAMES = [
 'citation', 'name', 'publisher', 'cite_type', 'edition1', 'edition2',
 'edition3', 'edition4', 'edition5', 'edition6', 'start_e1', 'start_e2',
 'start_e3', 'start_e4', 'start_e5', 'start_e6', 'end_e1', 'end_e2',
 'end_e3', 'end_e4', 'end_e5', 'end_e6', 'mlz_jurisdictions', 'variations',
 'href', 'notes']

def make_editions_dict(editions):
    """Take a reporter editions dict and flatten it, returning a dict for
    use in the DictWriter.
    """
    d = {}
    nums = [
     '1', '2', '3', '4', '5', '6']
    num_counter = 0
    for k, date_dict in editions.items():
        d['edition%s' % nums[num_counter]] = k
        if date_dict['start'] is not None:
            d['start_e%s' % nums[num_counter]] = date_dict['start'].isoformat()
        if date_dict['end'] is not None:
            d['end_e%s' % nums[num_counter]] = date_dict['end'].isoformat()
        num_counter += 1

    return d


def make_csv():
    with open('reporters.csv', 'w') as (f):
        out = csv.DictWriter(f, fieldnames=FIELDNAMES)
        out.writeheader()
        for cite, reporter_list in REPORTERS.items():
            print 'Adding: %s' % cite
            for reporter in reporter_list:
                d = make_editions_dict(reporter['editions'])
                d['citation'] = cite
                d['name'] = reporter['name']
                d['publisher'] = reporter.get('publisher', '')
                d['cite_type'] = reporter['cite_type']
                d['mlz_jurisdictions'] = (', ').join(reporter['mlz_jurisdiction'])
                d['variations'] = (', ').join(reporter['variations'].keys())
                d['href'] = reporter.get('href', '')
                d['notes'] = reporter.get('notes', '')
                out.writerow(d)


if __name__ == '__main__':
    make_csv()