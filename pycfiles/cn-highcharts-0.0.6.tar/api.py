# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/craterdome/work/cn_api_python/lib/python2.7/site-packages/cn_api_python/api.py
# Compiled at: 2012-02-07 14:44:50
import slumber, urllib2

def _field_schema(base_url, plural):
    url = base_url + plural + '/schema/'
    json = slumber.serialize.JsonSerializer()
    response = urllib2.urlopen(url)
    html = response.read()
    return lambda : json.loads(html)


def _list_field(api, plural):
    return lambda **kwargs: getattr(api, plural).get(**kwargs)


def _create_field(api, plural):
    return lambda info_dict: getattr(api, plural).post(info_dict)


def _get_field(api, plural):
    return lambda id: getattr(api, plural).__call__(id).get()


def _update_field(api, plural):
    return lambda id, info_dict: getattr(api, plural).__call__(id).put(info_dict)


class CharityAPI:

    def __init__(self, api_token=None, version='v1', api_location='http://cnapi.tivixlabs.com/api/'):
        if api_token:
            raise Error('This has not been implemented yet')
        self.base_url = api_location + version + '/'
        self.api = slumber.API(self.base_url)
        fields = {'category': 'categories', 
           'cause': 'causes', 
           'celebrity': 'celebrities', 
           'organization': 'organizations', 
           'celebrity_relationship': 'celebrity_relationships', 
           'celebrity_org': 'celebrity_orgs', 
           'country_region': 'country_regions', 
           'country': 'countries', 
           'country_org': 'country_orgs', 
           'orgs_rating': 'orgs_ratings'}
        for single, plural in fields.items():
            setattr(self, single + '_schema', _field_schema(self.base_url, plural))
            setattr(self, 'list_' + plural, _list_field(self.api, plural))
            setattr(self, 'get_' + single, _get_field(self.api, plural))