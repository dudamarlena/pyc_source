# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/adapters/agencies/snhd_constants.py
# Compiled at: 2015-05-15 15:11:21
# Size of source mod 2**32: 1772 bytes
DOWNLOAD_URL = 'http://southernnevadahealthdistrict.org/restaurants/download/restaurants.zip'
COLUMN_SEPARATOR = ';'
QUOTE_CHARACTER = '|'
CSV_SCHEMA = {'restaurant_inspections.csv': {'headers': [
                                            'serial_number',
                                            'permit_number',
                                            'inspection_date',
                                            'inspection_time',
                                            'employee_id',
                                            'inspection_type_id',
                                            'inspection_demerits',
                                            'inspection_grade',
                                            'permit_status',
                                            'inspection_result',
                                            'violations',
                                            'record_updated']}, 
 'restaurant_establishments.csv': {'headers': [
                                               'permit_number',
                                               'facility_id',
                                               'PE',
                                               'restaurant_name',
                                               'location_name',
                                               'address',
                                               'latitude',
                                               'longitude',
                                               'city_id',
                                               'city_name',
                                               'zip_code',
                                               'nciaa',
                                               'plan_review',
                                               'record_status',
                                               'current_grade',
                                               'current_demerits',
                                               'date_current',
                                               'previous_grade',
                                               'date_previous']}, 
 'restaurant_inspection_violations.csv': {'headers': [
                                                      'inspection_violation_id',
                                                      'inspection_id',
                                                      'inspection_violation']}, 
 'restaurant_violations.csv': {'headers': [
                                           'violation_id',
                                           'violation_code',
                                           'violation_sort',
                                           'violation_demerits',
                                           'violation_description']}}