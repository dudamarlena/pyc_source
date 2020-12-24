# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/scripts/combine_sheets.py
# Compiled at: 2018-02-11 11:26:27
# Size of source mod 2**32: 3496 bytes
import csv, collections
MAIN_PATH = 'django_geo_db/data/us-cities-and-zips.csv'
COUNTY_PATH = 'django_geo_db/data/us_zip_codes_states.csv'
OUT_FILE = 'django_geo_db/data/us-data-final.csv'

def combine():
    all_entries = {}
    all_entries_by_state_name = {}
    print('Reading first file')
    with open(MAIN_PATH, 'r') as (inFile):
        reader = csv.reader(inFile)
        is_first = True
        for line in reader:
            if is_first:
                is_first = False
                continue
                entry = [
                 line[0],
                 line[1],
                 line[2],
                 line[3],
                 line[4],
                 line[5],
                 line[6]]
                state = entry[2]
                city = entry[1]
                if state not in all_entries_by_state_name:
                    all_entries_by_state_name[state] = {}
                if city not in all_entries_by_state_name[state]:
                    all_entries_by_state_name[state][city] = entry
                zip = int(entry[0])
                all_entries[zip] = entry

    print('Reading second file')
    with open(COUNTY_PATH, 'r') as (inFile):
        reader = csv.reader(inFile)
        is_first = True
        for line in reader:
            if is_first:
                is_first = False
                continue
                zipcode = int(line[0])
                county = line[5]
                state = line[4]
                city = line[3]
                lat = line[1]
                if not lat:
                    pass
            else:
                if city == 'Apo' or city == 'Fpo':
                    pass
                else:
                    if zipcode == '40129':
                        pass
                    else:
                        if city == 'Migrate' and state == 'KY':
                            pass
                        else:
                            if city == 'Mc Lean':
                                city = 'McLean'
                            if not state == 'GU':
                                if not state == 'PW':
                                    if not state == 'FM':
                                        if not state == 'MP':
                                            if state == 'MH':
                                                pass
                                            else:
                                                if zipcode not in all_entries:
                                                    if city == 'East Boston':
                                                        city = 'Boston'
                                                    if city == 'North Waltham':
                                                        city = 'Waltham'
                                                    try:
                                                        another_version = all_entries_by_state_name[state][city]
                                                    except Exception as e:
                                                        print(state)
                                                        print(city)
                                                        raise e

                                                    lat = another_version[3]
                                                    lon = another_version[4]
                                                    time = another_version[5]
                                                    dst = another_version[6]
                                                    print('{0} - {1}, {2} was not found. Adding.'.format(zipcode, city, state))
                                                    all_entries[zipcode] = [
                                                     zipcode, city, state, lat, lon, time, dst]
                                                all_entries[zipcode].insert(3, county)

    print('Writing Results')
    all_entries_in_order = collections.OrderedDict()
    all_zips = sorted([int(key) for key in all_entries.keys()])
    for zip in all_zips:
        all_entries_in_order[zip] = all_entries[zip]

    with open(OUT_FILE, 'w') as (outFile):
        writer = csv.writer(outFile)
        writer.writerow(['zip', 'city', 'state', 'county', 'latitude', 'longitude', 'timezone', 'dst'])
        for zip, entry in all_entries_in_order.items():
            if len(entry) != 8:
                pass
            else:
                writer.writerow(entry)

    print('Done')


combine()