# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/connection.py
# Compiled at: 2018-02-18 18:15:37
# Size of source mod 2**32: 3263 bytes
from urllib.request import Request, build_opener
import json
from pyconnectedcars.Exceptions import ConnectedCarsException

class Connection(object):
    """Connection"""

    def __init__(self, email, password, baseurl=''):
        """Initialize connection object"""
        self.user_agent = 'okhttp/3.6.0'
        self.baseurl = baseurl
        if not self.baseurl:
            self.baseurl = 'https://skoda.connectedcars.dk'
        self.api = '/api/graphql'
        self._query = '\n    mutation RootMutationType($email: String, $password: String) {\n      user: login(email: $email, password: $password) {\n        ...userFields\n      }\n    }\n  \n\n\n    fragment userFields on User {\n      \n  id,\n  firstname,\n  lastname,\n  mobile,\n  email,\n  lang,\n  onboardingFinished,\n  token,\n  cars {\n    id,\n    vin,\n    locationName,\n    name,\n    lat,\n    long,\n    fuelLevel,\n    fuelLevelLiter,\n    fuelLevelUpdatedAt,\n    lockedState,\n    lockedStateUpdatedAt,\n    systemsAreOk,\n    oilLevelIsOk,\n    tirePressureIsOk,\n    batteryChargeIsOk,\n    odometer,\n    imageFilename,\n    updatedAt,\n    service {\n      nextServiceInKm,\n      nextServiceInDays\n    },\n    licensePlates {\n      id,\n      licensePlate,\n      createdAt\n    },\n    lamps(listLampStates: true, source: USER) {\n      type,\n      color,\n      frequency,\n      enabled,\n      source,\n      time\n    },\n    incidents(status: ON, dismissed: false, limit: 1000) {\n      id,\n      rule,\n      system {\n        key,\n        headerDanish,\n        headerEnglish,\n        nameDanish,\n        nameEnglish\n      },\n      recommendation {\n        key,\n        descriptionEnglish,\n        descriptionDanish\n      },\n      startTime,\n      context {\n        ... on CarIncidentServiceReminderContext {\n          serviceDate\n        }\n      }\n    }\n  },\n  workshop {\n    id,\n    dealernumber,\n    dealername,\n    phone,\n    bookingurl\n  }\n\n    }\n  '
        self.auth_vars = {'email':email, 
         'password':password}

    def get_data(self):
        """Utility command to get data from API"""
        payload = {'query':self._query, 
         'variables':self.auth_vars}
        return self.post(json.dumps(payload))

    def post(self, data=''):
        """Utility command to post data to API"""
        headers = {'Content-Type':'application/json', 
         'User-Agent':self.user_agent}
        return self._Connection__open((self.api),
          headers=headers, req_data=data)

    def __open(self, url, headers={}, req_data=None):
        """Raw urlopen command"""
        req = Request(('%s%s' % (self.baseurl, url)),
          data=(req_data.encode('utf8')),
          headers=headers)
        opener = build_opener()
        resp = opener.open(req)
        charset = resp.info().get('charset', 'utf-8')
        data = json.loads(resp.read().decode(charset))
        opener.close()
        if data.get('errors'):
            raise ConnectedCarsException(data['errors'][0]['message'], data['errors'])
        return data