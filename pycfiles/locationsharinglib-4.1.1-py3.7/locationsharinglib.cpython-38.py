# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/Personal_to_cleanup/python/locationsharinglib/locationsharinglib/locationsharinglib.py
# Compiled at: 2020-04-07 02:48:27
# Size of source mod 2**32: 13391 bytes
"""
Main code for locationsharinglib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from __future__ import unicode_literals
import json, logging, pickle, warnings
from dataclasses import dataclass
from datetime import datetime
import pytz
from cachetools import TTLCache, cached
from requests import Session
from .locationsharinglibexceptions import InvalidCookies, InvalidData
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-12-24'
__copyright__ = 'Copyright 2017, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos', 'Michaël Arnauts', 'Amy Nagle',
 'Jeremy Wiebe', 'Chris Helming']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'locationsharinglib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())
STATE_CACHING_SECONDS = 30
STATE_CACHE = TTLCache(maxsize=1, ttl=STATE_CACHING_SECONDS)
ACCOUNT_URL = 'https://myaccount.google.com/?hl=en'

@dataclass
class Cookie:
    __doc__ = 'Models a cookie.'
    domain: str
    flag: bool
    path: str
    secure: bool
    expiry: int
    name: str
    value: str

    def to_dict--- This code section failed: ---

 L.  90         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'Cookie.to_dict.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_CONST               ('domain', 'name', 'value', 'path')
               12  GET_ITER         
               14  CALL_FUNCTION_1       1  ''
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class Service:
    __doc__ = 'An object modeling the service to retrieve locations.'

    def __init__(self, cookies_file=None, authenticating_account='unknown@gmail.com'):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self.email = authenticating_account
        self._session = self._validate_cookie(cookies_file or '')

    def _validate_cookie(self, cookies_file):
        session = self._get_authenticated_session(cookies_file)
        response = session.get(ACCOUNT_URL)
        self._logger.debug('Getting personal account page and its cookies...\n %s', response.content)
        response = session.get(ACCOUNT_URL)
        self._logger.debug('Validating access to personal account...')
        if response.history:
            message = 'The cookies provided do not provide a valid session, could not reach personal account page.Please create another cookie file and try again.'
            raise InvalidCookies(message)
        return session

    def _get_authenticated_session(self, cookies_file):
        session = Session()
        try:
            cfile = open(cookies_file, 'rb')
        except FileNotFoundError:
            message = 'Could not open cookies file, either file does not exist or no read access.'
            raise InvalidCookies(message)
        else:
            try:
                session.cookies.update(pickle.load(cfile))
                self._logger.debug('Successfully loaded pickled cookie!')
                warnings.warn('Pickled cookie format is going to be deprecated in a future version, please start using a text base cookie file!')
            except (pickle.UnpicklingError, KeyError, AttributeError, EOFError, ValueError):
                self._logger.debug('Trying to load text based cookies.')
                session = self._load_text_cookies(session, cfile)
            else:
                cfile.close()
                return session

    def _load_text_cookies(self, session, cookies_file):
        try:
            text = cookies_file.read().decode('utf-8')
            cookies = [Cookie(*line.strip().split()) for line in text.splitlines() if not line.strip().startswith('#') if line]
            for cookie in cookies:
                (session.cookies.set)(**cookie.to_dict())

        except Exception:
            self._logger.exception('Things broke...')
            message = 'Could not properly load cookie text file.'
            raise InvalidCookies(message)
        else:
            return session

    @cached(STATE_CACHE)
    def _get_data(self):
        payload = {'authuser':0,  'hl':'en', 
         'gl':'us', 
         'pb':'!1m7!8m6!1m3!1i14!2i8413!3i5385!2i6!3x4095!2m3!1e0!2sm!3i407105169!3m7!2sen!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e1!5m4!1e4!8m2!1e0!1e1!6m9!1e12!2i2!26m1!4b1!30m1!1f1.3953487873077393!39b1!44e1!50e0!23i4111425'}
        url = 'https://www.google.com/maps/rpc/locationsharing/read'
        response = self._session.get(url, params=payload, verify=True)
        self._logger.debug(response.text)
        if response.ok:
            try:
                data = json.loads(response.text.split("'", 1)[1])
            except (ValueError, IndexError, TypeError):
                self._logger.exception('Unable to parse response :%s', response.text)
                data = ['']

        else:
            self._logger.warning('Received response code:%s', response.status_code)
            data = ['']
        return data

    def get_shared_people(self):
        """Retrieves all people that share their location with this account."""
        people = []
        output = self._get_data()
        self._logger.debug(output)
        shared_entries = output[0] or []
        for info in shared_entries:
            try:
                people.append(Person(info))
            except InvalidData:
                self._logger.debug('Missing location or other info, dropping person with info: %s', info)

        else:
            return people

    def get_authenticated_person--- This code section failed: ---

 L. 189         0  SETUP_FINALLY        84  'to 84'

 L. 190         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _get_data
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'output'

 L. 191        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _logger
               14  LOAD_METHOD              debug
               16  LOAD_FAST                'output'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 192        22  LOAD_GLOBAL              Person

 L. 193        24  LOAD_FAST                'self'
               26  LOAD_ATTR                email

 L. 194        28  LOAD_FAST                'output'
               30  LOAD_CONST               9
               32  BINARY_SUBSCR    
               34  LOAD_CONST               1
               36  BINARY_SUBSCR    

 L. 195        38  LOAD_CONST               None

 L. 196        40  LOAD_CONST               None

 L. 197        42  LOAD_CONST               None

 L. 198        44  LOAD_CONST               None

 L. 200        46  LOAD_CONST               None

 L. 201        48  LOAD_CONST               None

 L. 202        50  LOAD_FAST                'self'
               52  LOAD_ATTR                email

 L. 203        54  LOAD_FAST                'self'
               56  LOAD_ATTR                email

 L. 199        58  BUILD_LIST_4          4 

 L. 205        60  LOAD_CONST               None

 L. 206        62  LOAD_CONST               None

 L. 207        64  LOAD_CONST               None

 L. 208        66  LOAD_CONST               None

 L. 209        68  LOAD_CONST               None

 L. 210        70  LOAD_CONST               None

 L. 211        72  LOAD_CONST               None

 L. 192        74  BUILD_LIST_14        14 
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'person'
               80  POP_BLOCK        
               82  JUMP_FORWARD        124  'to 124'
             84_0  COME_FROM_FINALLY     0  '0'

 L. 213        84  DUP_TOP          
               86  LOAD_GLOBAL              IndexError
               88  LOAD_GLOBAL              TypeError
               90  LOAD_GLOBAL              InvalidData
               92  BUILD_TUPLE_3         3 
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   122  'to 122'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 214       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _logger
              108  LOAD_METHOD              debug
              110  LOAD_STR                 'Missing essential info, cannot instantiate authenticated person'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 215       116  POP_EXCEPT       
              118  LOAD_CONST               None
              120  RETURN_VALUE     
            122_0  COME_FROM            96  '96'
              122  END_FINALLY      
            124_0  COME_FROM            82  '82'

 L. 216       124  LOAD_FAST                'person'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 118

    def get_all_people(self):
        """Retrieves all people sharing their location."""
        people = self.get_shared_people() + [self.get_authenticated_person()]
        return filter(None, people)

    def get_person_by_nickname(self, nickname):
        """Retrieves a person by nickname."""
        return next((person for person in self.get_all_people() if person.nickname.lower() == nickname.lower()), None)

    def get_person_by_full_name(self, name):
        """Retrieves a person by full name."""
        return next((person for person in self.get_all_people() if person.full_name.lower() == name.lower()), None)

    def get_coordinates_by_nickname(self, nickname):
        """Retrieves a person's coordinates by nickname."""
        person = self.get_person_by_nickname(nickname)
        if not person:
            return ('', '')
        return (
         person.latitude, person.longitude)

    def get_coordinates_by_full_name(self, name):
        """Retrieves a person's coordinates by full name."""
        person = self.get_person_by_full_name(name)
        if not person:
            return ('', '')
        return (
         person.latitude, person.longitude)


class Person:
    __doc__ = 'A person sharing its location as coordinates.'

    def __init__(self, data):
        logger_name = '{base}.{suffix}'.format(base=LOGGER_BASENAME, suffix=(self.__class__.__name__))
        self._logger = logging.getLogger(logger_name)
        self._id = None
        self._picture_url = None
        self._full_name = None
        self._nickname = None
        self._latitude = None
        self._longitude = None
        self._timestamp = None
        self._accuracy = None
        self._address = None
        self._country_code = None
        self._charging = None
        self._battery_level = None
        self._populate(data)

    def _populate(self, data):
        try:
            self._id = data[6][0]
            self._picture_url = data[6][1]
            self._full_name = data[6][2]
            self._nickname = data[6][3]
            self._latitude = data[1][1][2]
            self._longitude = data[1][1][1]
            self._timestamp = data[1][2]
            self._accuracy = data[1][3]
            self._address = data[1][4]
            self._country_code = data[1][6]
            try:
                self._charging = data[13][0]
            except (IndexError, TypeError):
                self._charging = None
            else:
                try:
                    self._battery_level = data[13][1]
                except (IndexError, TypeError):
                    self._battery_level = None

        except (IndexError, TypeError):
            self._logger.debug(data)
            raise InvalidData

    def __str__(self):
        text = ('Full name        :{}'.format(self.full_name),
         'Nickname         :{}'.format(self.nickname),
         'Current location :{}'.format(self.address),
         'Latitude         :{}'.format(self.latitude),
         'Longitude        :{}'.format(self.longitude),
         'Datetime         :{}'.format(self.datetime),
         'Charging         :{}'.format(self.charging),
         'Battery %        :{}'.format(self.battery_level),
         'Accuracy         :{}'.format(self._accuracy))
        return '\n'.join(text)

    @property
    def id(self):
        """The internal google id of the account."""
        return self._id or self.full_name

    @property
    def picture_url(self):
        """The url of the person's avatar."""
        return self._picture_url

    @property
    def full_name(self):
        """The full name of the user as set in google."""
        return self._full_name

    @property
    def nickname(self):
        """The nickname as set in google."""
        return self._nickname

    @property
    def latitude(self):
        """The latitude of the person's current location."""
        return self._latitude

    @property
    def longitude(self):
        """The longitude of the person's current location."""
        return self._longitude

    @property
    def timestamp(self):
        """The timestamp of the location retrieval."""
        return self._timestamp

    @property
    def datetime(self):
        """A datetime representation of the location retrieval."""
        return datetime.fromtimestamp((int(self.timestamp) / 1000), tz=(pytz.utc))

    @property
    def address(self):
        """The address as reported by google for the current location."""
        return self._address

    @property
    def country_code(self):
        """The location's country code."""
        return self._country_code

    @property
    def accuracy(self):
        """The accuracy of the gps."""
        return self._accuracy

    @property
    def charging(self):
        """Whether or not the user's device is charging."""
        return bool(self._charging)

    @property
    def battery_level(self):
        """The battery level of the user's device."""
        return self._battery_level