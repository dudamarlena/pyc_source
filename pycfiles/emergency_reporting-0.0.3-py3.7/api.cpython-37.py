# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emergency_reporting/api.py
# Compiled at: 2020-05-02 18:50:45
# Size of source mod 2**32: 8695 bytes
from urllib.parse import urljoin
import requests
from .excpetion import WebCallException
from .util import BASE_URL

class API:

    def __init__(self, name, path, subscription):
        self.base = BASE_URL
        self.name = name
        self.path = path
        self.subscription = subscription

    def url(self):
        return urljoin(self.base, self.path)

    def make_call(self, path, params, retry=1):
        limit = 5
        headers = {'Ocp-Apim-Subscription-Key':self.subscription.Auth.primary_key, 
         'Authorization':self.subscription.Auth.token.access_token}
        url = urljoin(self.url(), path)
        response = requests.get(url, params=params, headers=headers)
        if not response.ok:
            if retry <= limit:
                if response.status_code == 401:
                    self.subscription.Auth.get_token()
                retry += 1
                return self.make_call(path, params, retry)
        return response

    def retrieve(self, path, params, json_key):
        response = self.make_call(path, params)
        if response.ok:
            return response.json()[json_key]
        raise WebCallException(response.status_code)


class AgenyIncidentsApi(API):

    def __init__(self, subscription):
        super().__init__('Ageny Incidents', 'agencyincidents/', subscription=subscription)

    def get_incidents(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'incidents'
        json_key = 'incidents'
        return self.retrieve(path, kwargs, json_key)

    def get_exposures(self, incident_id, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = f"incidents/{incident_id}/exposures"
        json_key = 'exposures'
        return self.retrieve(path, kwargs, json_key)

    def get_all_exposures(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'incidents/exposures'
        json_key = 'exposures'
        return self.retrieve(path, kwargs, json_key)

    def get_exposure_crew_members(self, exposureID, **kwargs):
        path = f"exposures/{exposureID}/crewmembers"
        json_key = 'crewMembers'
        return self.retrieve(path, kwargs, json_key)

    def get_all_exposure_crew_members(self, **kwargs):
        path = 'exposures/crewmembers'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['crewMembers']
        raise WebCallException(response.status_code)

    def get_crew_memeber_roles(self, exposure_user_id, **kwargs):
        path = f"crewmembers/{exposure_user_id}/roles"
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['roles']
        raise WebCallException(response.status_code)

    def get_exposure_location(self, exposureID, **kwargs):
        path = f"exposures/{exposureID}/location"
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['exposureLocation']
        raise WebCallException

    def get_all_exposure_locations(self, **kwargs):
        path = 'exposures/location'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['exposureLocations']
        raise WebCallException

    def get_all_exposure_naratives(self, **kwargs):
        path = 'exposures/narratives'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['narratives']
        raise WebCallException

    def get_all_exposure_apparatuses(self, **kwargs):
        path = 'exposures/apparatuses'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['exposureApparatuses']
        raise WebCallException


class AgencyApparatusApi(API):

    def __init__(self, subscription):
        super().__init__('Ageny Apparatus', 'agencyapparatus/', subscription=subscription)

    def get_apparatuses(self, **kwargs):
        path = 'apparatus'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['apparatus']
        raise WebCallException


class AgencyUsersApi(API):

    def __init__(self, subscription):
        super().__init__('Ageny Users', 'agencyusers/', subscription)

    def get_users(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'users'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['users']
        raise WebCallException(response.status_code)


class AgencyStationsApi(API):

    def __init__(self, subscription):
        super().__init__('Ageny Stations', 'agencystations/', subscription)

    def get_stations(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'stations'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['stations']
        raise WebCallException(response.status_code)


class AgencyClassesApi(API):

    def __init__(self, subscription):
        super().__init__('Ageny Classes', 'agencyclasses/', subscription)

    def get_classes(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['classes']
        raise WebCallException(response.status_code)

    def get_all_classes_students(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes/students'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['students']
        raise WebCallException(response.status_code)

    def get_all_classes_instructors(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes/instructors'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['instructors']
        raise WebCallException(response.status_code)

    def get_all_agency_code_categories(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes/agencycodecategories'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['agencyCodeCategories']
        raise WebCallException(response.status_code)

    def get_all_agency_codes(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes/agencycodes'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['agencyCodes']
        raise WebCallException(response.status_code)

    def get_all_classes_categories(self, **kwargs):
        """
        kwargs are parsed as the get params. Valid args are:-
        rowVersion, limit, offset, filter, orderby
        """
        path = 'classes/categories'
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['categories']
        raise WebCallException(response.status_code)

    def get_class_category(self, categoryID, **kwargs):
        path = f"classes/categories/{categoryID}"
        response = self.make_call(path, kwargs)
        if response.ok:
            return response.json()['category']
        raise WebCallException