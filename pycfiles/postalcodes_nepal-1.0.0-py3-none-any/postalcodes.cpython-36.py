# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/biplov/Desktop/postalcodes_nepal/postalcodes_nepal/postalcodes.py
# Compiled at: 2020-03-19 01:08:25
# Size of source mod 2**32: 2128 bytes
import json, pkg_resources
my_data = pkg_resources.resource_filename(__name__, 'dataset/postalcodes.json')
with open(my_data) as (f):
    NepalData = json.load(f)

def validate(postal_code):
    postal_code = str(postal_code)
    for dict in NepalData:
        for po_info in dict['data']:
            if po_info['Postal Code'] == postal_code:
                return True

    return False


def postal_code(city):
    city = str(city)
    city = city.capitalize()
    for dict in NepalData:
        for po_info in dict['data']:
            if po_info['Post Office'] == city:
                return po_info['Postal Code']


def city_po_info(city):
    city = str(city)
    city = city.capitalize()
    for dict in NepalData:
        for po_info in dict['data']:
            if po_info['Post Office'] == city:
                city_po_info = {'District':dict['District'],  'Post Office':po_info['Post Office'], 
                 'Postal Code':po_info['Postal Code'], 
                 'Post Office Type':po_info['Post Office Type']}
                return city_po_info


def postalcode_to_city(postal_code):
    postal_code = str(postal_code)
    for dict in NepalData:
        for po_info in dict['data']:
            if po_info['Postal Code'] == postal_code:
                return po_info['Post Office']


def postalcode_info(postal_code):
    postal_code = str(postal_code)
    for dict in NepalData:
        for po_info in dict['data']:
            if po_info['Postal Code'] == postal_code:
                city_po_info = {'District':dict['District'],  'Post Office':po_info['Post Office'], 
                 'Postal Code':po_info['Postal Code'], 
                 'Post Office Type':po_info['Post Office Type']}
                return city_po_info


def district_data(district):
    district = str(district)
    district = district.capitalize()
    district_po_data = []
    for dict in NepalData:
        if dict['District'] == district:
            for po_info in dict['data']:
                district_po_data.append((po_info['Post Office'], po_info['Postal Code']))

            return district_po_data


def country_data():
    country_po_data = []
    for dict in NepalData:
        for po_info in dict['data']:
            country_po_data.append((po_info['Post Office'], po_info['Postal Code']))

    return country_po_data