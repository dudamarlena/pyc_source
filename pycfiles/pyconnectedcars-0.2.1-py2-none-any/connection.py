# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyconnectedcars/connection.py
# Compiled at: 2018-02-17 14:29:09
import calendar, datetime
from urllib.parse import urlencode
from urllib.request import Request, build_opener
from urllib.error import HTTPError
import json
from connectedcars.Exceptions import ConnectedCarsException

class Connection(object):
    """Connection to Tesla Motors API"""

    def __init__(self, email, password):
        """Initialize connection object"""
        self.user_agent = 'okhttp/3.6.0'
        self.baseurl = 'https://skoda.connectedcars.dk/'
        self.api = '/api/graphql'
        self._query = '\n    mutation RootMutationType($email: String, $password: String) {\n      user: login(email: $email, password: $password) {\n        ...userFields\n      }\n    }\n  \n\n\n    fragment userFields on User {\n      \n  id,\n  firstname,\n  lastname,\n  mobile,\n  email,\n  lang,\n  onboardingFinished,\n  token,\n  cars {\n    id,\n    vin,\n    locationName,\n    name,\n    lat,\n    long,\n    fuelLevel,\n    fuelLevelLiter,\n    fuelLevelUpdatedAt,\n    lockedState,\n    lockedStateUpdatedAt,\n    systemsAreOk,\n    oilLevelIsOk,\n    tirePressureIsOk,\n    batteryChargeIsOk,\n    odometer,\n    imageFilename,\n    updatedAt,\n    service {\n      nextServiceInKm,\n      nextServiceInDays\n    },\n    licensePlates {\n      id,\n      licensePlate,\n      createdAt\n    },\n    lamps(listLampStates: true, source: USER) {\n      type,\n      color,\n      frequency,\n      enabled,\n      source,\n      time\n    },\n    incidents(status: ON, dismissed: false, limit: 1000) {\n      id,\n      rule,\n      system {\n        key,\n        headerDanish,\n        headerEnglish,\n        nameDanish,\n        nameEnglish\n      },\n      recommendation {\n        key,\n        descriptionEnglish,\n        descriptionDanish\n      },\n      startTime,\n      context {\n        ... on CarIncidentServiceReminderContext {\n          serviceDate\n        }\n      }\n    }\n  },\n  workshop {\n    id,\n    dealernumber,\n    dealername,\n    phone,\n    bookingurl\n  }\n\n    }\n  '
        self.auth_vars = {'email': email, 
           'password': password}

    def get_data(self):
        """Utility command to get data from API"""
        payload = {'query': self._query, 
           'variables': self.auth_vars}
        return self.post(json.dumps(payload))

    def post(self, data={}, baseurl=''):
        """Utility command to post data to API"""
        headers = {'Content-Type': 'application/json', 
           'User-Agent': self.user_agent}
        return self.__open(self.api, headers=headers, data=data, baseurl=baseurl)

    def __open(self, url, headers={}, data=None, baseurl=''):
        """Raw urlopen command"""
        if not baseurl:
            baseurl = self.baseurl
        req = Request('%s%s' % (baseurl, url), headers=headers)
        try:
            req.data = urlencode(data).encode('utf-8')
        except TypeError:
            pass

        opener = build_opener()
        try:
            resp = opener.open(req)
            charset = resp.info().get('charset', 'utf-8')
            data = json.loads(resp.read().decode(charset))
            opener.close()
            return data
        except HTTPError as e:
            if e.code == 408:
                return False
            raise ConnectedCarsException(e.code)