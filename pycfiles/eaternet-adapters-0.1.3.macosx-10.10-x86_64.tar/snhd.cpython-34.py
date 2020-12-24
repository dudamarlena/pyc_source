# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/adapters/agencies/snhd.py
# Compiled at: 2015-05-15 15:11:21
# Size of source mod 2**32: 4362 bytes
"""An adapter for the Southern Nevada Health District (Las Vegas).

Example: Print all the Las Vegas business names
--------------------------------------------------

    >>> from eaternet.adapters.agencies.snhd import Snhd
    >>>
    >>> agency = Snhd()
    >>> for biz in agency.businesses():
    >>>     if biz.city == 'Las Vegas':
    >>>         print(biz.name)

The SNHD makes their restaurant inspection data available via a zip
file for download. The file contains several Mysql tables converted
to CSV. And so, this is an example for how to code adapters for other
agencies which publish their data in a similar way.

This code downloads the latest zip file, extracts it, parses the csv,
and provides iterators of Data Transfer Objects:
Businesses, Inspections, Violations, and ViolationKinds. (These are
specified in the ``eaternet.adapters.framework`` package.)

SNHD's CSV format seems to be non-standard, e.g. using the double-quote
character in fields without escaping it. We need to find out what their
quote character actually is. In the meantime, the files can be parsed by
setting the quote character to something else that doesn't appear in the
text, such as a pipe symbol.

See http://southernnevadahealthdistrict.org/restaurants/inspect-downloads.php
    The SNHD Developer information page
See ``eaternet.adapters.framework`` The Framework package

"""
import csv, os
from eaternet.adapters.agencies import snhd_constants
from eaternet.adapters.framework import util
from eaternet.adapters.framework.abstract_adapter import AbstractAdapter, BusinessData, InspectionData, ViolationData, ViolationKindData

class Snhd(AbstractAdapter):

    def __init__(self):
        self._zip_dir = None

    def businesses(self):
        """Return an iterable yielding BusinessData objects."""
        return self._lazy_iterator(csv_file='restaurant_establishments.csv', factory_function=business_dto)

    def inspections(self):
        """Return an iterable yielding InspectionData objects."""
        return self._lazy_iterator(csv_file='restaurant_inspections.csv', factory_function=inspection_dto)

    def violations(self):
        """Return an iterable yielding ViolationData objects."""
        return self._lazy_iterator(csv_file='restaurant_inspection_violations.csv', factory_function=violation_dto)

    def violation_kinds(self):
        """Return an iterable yielding ViolationKindData objects."""
        return self._lazy_iterator(csv_file='restaurant_violations.csv', factory_function=violation_kind_dto)

    @util.memoize
    def _lazy_iterator(self, csv_file, factory_function):
        """Return an iterator over Data Transfer Objects"""
        headers = snhd_constants.CSV_SCHEMA[csv_file]['headers']
        f = open(os.path.join(self.zip_directory(), csv_file))
        csv_reader = csv.DictReader(f, fieldnames=headers, delimiter=snhd_constants.COLUMN_SEPARATOR, quotechar=snhd_constants.QUOTE_CHARACTER)
        next(csv_reader)
        return map(factory_function, csv_reader)

    @util.memoize
    def zip_directory(self):
        return util.download_and_extract(snhd_constants.DOWNLOAD_URL)


def business_dto(csv_row):
    return BusinessData(name=csv_row['restaurant_name'], address=csv_row['address'], city=csv_row['city_name'], zipcode=csv_row['zip_code'], orig_key=csv_row['permit_number'])


def inspection_dto(csv_row):
    return InspectionData(orig_key=csv_row['serial_number'], business_orig_key=csv_row['permit_number'], score=csv_row['inspection_grade'], date=csv_row['inspection_date'])


def violation_dto(csv_row):
    return ViolationData(orig_key=csv_row['inspection_violation_id'], inspection_id=csv_row['inspection_id'], violation_kind_id=csv_row['inspection_violation'])


def violation_kind_dto(csv_row):
    return ViolationKindData(orig_key=csv_row['violation_id'], code=csv_row['violation_code'], demerits=csv_row['violation_demerits'], description=csv_row['violation_description'])