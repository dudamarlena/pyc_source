# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/core.py
# Compiled at: 2019-03-19 08:11:10
# Size of source mod 2**32: 4825 bytes
from http import HTTPStatus
from json import JSONDecodeError
import requests
from .errors import OneSignalAPIError
from .utils import merge_dicts

class OneSignalCallResult:

    def __init__(self, response):
        self.status_code = response.status_code
        self.is_error = self.status_code != HTTPStatus.OK
        try:
            json = response.json()
        except JSONDecodeError:
            json = {'errors': 'Failed to decode JSON in OneSignalClient.'}

        self.errors = json.get('errors') if (self.is_error or 'errors' in json.keys()) else None
        self.body = json


class OneSignalClient:
    __doc__ = 'Connects all the functions and methods to the OneSignal API\n\n    Central class that is used to interact with the OneSignal API\n    by passing notification classes into the methods.\n\n    Attributes:\n        app_id: OneSignal app id\n        rest_api_key: secret OneSignal rest api key\n    '
    base_api_url = 'https://onesignal.com/api/v1/'

    def __init__(self, app_id, rest_api_key):
        """Inits OneSignal with connection details"""
        self.app_id = app_id
        self.rest_api_key = rest_api_key
        self.session = requests.session()

    def request(self, method, endpoint, json={}):
        """Sends a request to the OneSignal API

        Args:
            method: HTTP request method
            endpoint: api endpoint
            json: request data

        Returns:
            A dict of the api response

        Raises:
            OneSignalAPIError: OneSignal API request was not successful
        """
        response = self.session.request(method,
          '{api_url}{endpoint}'.format(api_url=(self.base_api_url), endpoint=endpoint),
          json=json,
          headers={'Authorization': 'Basic {key}'.format(key=(self.rest_api_key))})
        if response.status_code != HTTPStatus.OK:
            try:
                raise OneSignalAPIError(response.json())
            except JSONDecodeError:
                raise OneSignalAPIError({'errors': 'Status code "{}" returned.'.format(response.status_code)})

        return response

    def send(self, notification):
        """Send a notification

        Attributes:
            notification: instance of a *Notification class

        Returns:
            A dict of the API response
        """
        if isinstance(self.app_id, str):
            app_id_obj = {'app_id': self.app_id}
        else:
            if isinstance(self.app_id, list):
                app_id_obj = {'app_ids': [self.app_id]}
        data = merge_dicts(notification.get_data(), app_id_obj)
        return OneSignalCallResult(self.request('post', 'notifications', json=data))

    def cancel(self, notification):
        """Cancel a notification

        Attributes:
            notification: instance of a *Notification class or notification id

        Returns:
            A dict of the API response
        """
        if isinstance(notification, str):
            notification_id = notification
        else:
            if not notification.id:
                raise ValueError('The notification was propably not sent yet')
            notification_id = notification.id
        return OneSignalCallResult(self.request('delete', 'notifications/{notification_id}?app_id={app_id}'.format(notification_id=notification_id, app_id=(self.app_id))))

    def details(self, notification):
        """Get details about a notification

        Attributes:
            notification: instance of a *Notification class or notification id

        Returns:
            A dict of the API response
        """
        if isinstance(notification, str):
            notification_id = notification
        else:
            if not notification.id:
                raise ValueError('The notification was propably not sent yet')
            notification_id = notification.id
        response = self.request('get', 'notifications/{notification_id}?app_id={app_id}'.format(notification_id=notification_id, app_id=(self.app_id)))
        result = {}
        for key in response.keys():
            result[self.to_underscore(key)] = response[key]

        return result

    def to_underscore(self, var):
        """Converts camelCase to underscore

        Attributes:
            var: name of variable in camelCase
        """
        result = ''
        for letter in var:
            if letter == letter.lower():
                result += letter
            else:
                result += '_' + letter.lower()

        return result