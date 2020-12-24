# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/fits_align/core.py
# Compiled at: 2018-08-23 04:21:41
# Size of source mod 2**32: 13825 bytes
from __future__ import print_function
import json, keyring, getpass, warnings
from datetime import datetime
import astropy.units as u, astropy.coordinates as coord, astropy.io.votable as votable
from astropy.table import Table
from astropy.io import fits
from astropy import log
from ..query import BaseQuery, QueryWithLogin
from ..utils import commons
from ..utils import prepend_docstr_nosections
from ..utils import async_to_sync
from ..utils import system_tools
from . import conf

@async_to_sync
class LcoClass(QueryWithLogin):
    URL = conf.server
    TIMEOUT = conf.timeout
    FRAMES_URL = conf.frames
    DTYPES = ['i', 'S39', 'S230', 'i', 'S19', 'S16', 'S20', 'S3', 'S4', 'f', 'S2', 'i']
    DATA_NAMES = ['id', 'filename', 'url', 'RLEVEL', 'DATE_OBS', 'PROPID', 'OBJECT', 'SITEID', 'TELID', 'EXPTIME', 'FILTER', 'REQNUM']
    TOKEN = None

    def query_object_async(self, object_name, start='', end='', rlevel='', get_query_payload=False, cache=True):
        """
        This method is for services that can parse object names. Otherwise
        use :meth:`astroquery.lco.LcoClass.query_region`.
        Put a brief description of what the class does here.

        Parameters
        ----------
        object_name : str
            name of the identifier to query.
        get_query_payload : bool, optional
            This should default to False. When set to `True` the method
            should return the HTTP request parameters as a dict.
        start: str, optional
            Default is `None`. When set this must be in iso E8601Dw.d datestamp format
            YYYY-MM-DD HH:MM
        end: str, optional
            Default is `None`. When set this must be in iso E8601Dw.d datestamp format
            YYYY-MM-DD HH:MM
        rlevel: str, optional
            Pipeline reduction level of the data. Default is `None`, and will
            return all data products. Options are  0 (Raw), 11 (Quicklook), 91 (Final reduced).
        Returns
        -------
        response : `requests.Response`
            Returns an astropy Table with results. See below for table headers
            id - ID of each Frame
            filename - Name of Frame file
            url - Download URL
            RLEVEL - 0 (Raw), 11 (Quicklook), 91 (Final reduced).
            DATE_OBS - Observation data
            PROPID - LCO proposal code
            OBJECT - Object Name
            SITEID - LCO 3-letter site ID of where observation was made
            TELID - LCO 4-letter telescope ID of where observation was made
            EXPTIME - Exposure time in seconds
            FILTER - Filter name
            REQNUM - LCO ID of the observing request which originated this frame

        Examples
        --------
        # from astroquery.lco import Lco
        # Lco.login(username='jdowland')
        # Lco.query_object_async('M15', start='2016-01-01 00:00', end='2017-02-01 00:00')

        """
        kwargs = {'object_name':object_name, 
         'start':start, 
         'end':end, 
         'rlevel':rlevel}
        request_payload = (self._args_to_payload)(**kwargs)
        if get_query_payload:
            return request_payload
        else:
            return self._parse_response(request_payload, cache)

    def query_region_async(self, coordinates, start='', end='', rlevel='', get_query_payload=False, cache=True):
        """
        Queries a region around the specified coordinates.

        Parameters
        ----------
        coordinates : str or `astropy.coordinates`.
            coordinates around which to query
        get_query_payload : bool, optional
            Just return the dict of HTTP request parameters.
        verbose : bool, optional
            Display VOTable warnings or not.

        Returns
        -------
        response : `requests.Response`
            Returns an astropy Table with results. See below for table headers
            id - ID of each Frame
            filename - Name of Frame file
            url - Download URL
            RLEVEL - 0 (Raw), 11 (Quicklook), 91 (Final reduced).
            DATE_OBS - Observation data
            PROPID - LCO proposal code
            OBJECT - Object Name
            SITEID - LCO 3-letter site ID of where observation was made
            TELID - LCO 4-letter telescope ID of where observation was made
            EXPTIME - Exposure time in seconds
            FILTER - Filter name
            REQNUM - LCO ID of the observing request which originated this frame

        Examples
        --------
        # from astroquery.lco import Lco
        # Lco.login(username='jdowland')
        # Lco.query_region_async('00h42m44.330s +41d16m07.50s', start='2016-01-01 00:00', end='2017-02-01 00:00')
        """
        kwargs = {'coordinates':coordinates, 
         'start':start, 
         'end':end, 
         'rlevel':rlevel}
        request_payload = (self._args_to_payload)(**kwargs)
        if get_query_payload:
            return request_payload
        else:
            return self._parse_response(request_payload, cache)

    def _args_to_payload(self, *args, **kwargs):
        request_payload = dict()
        request_payload['OBSTYPE'] = 'EXPOSE'
        if kwargs.get('start', ''):
            request_payload['start'] = validate_datetime(kwargs['start'])
        if kwargs.get('end', ''):
            request_payload['end'] = validate_datetime(kwargs['end'])
        if kwargs.get('rlevel', ''):
            request_payload['rlevel'] = validate_rlevel(kwargs['rlevel'])
        if kwargs.get('coordinates', ''):
            request_payload['coordinates'] = validate_coordinates(kwargs['coordinates'])
        else:
            if kwargs.get('object_name', ''):
                request_payload['OBJECT'] = kwargs['object_name']
        return request_payload

    def _login(self, username=None, store_password=False, reenter_password=False):
        """
        Login to the LCO Archive.

        Parameters
        ----------
        username : str, optional
            Username to the Las Cumbres Observatory archive. If not given, it should be
            specified in the config file.
        store_password : bool, optional
            Stores the password securely in your keyring. Default is False.
        reenter_password : bool, optional
            Asks for the password even if it is already stored in the
            keyring. This is the way to overwrite an already stored password
            on the keyring. Default is False.
        """
        if username is None:
            if self.USERNAME == '':
                raise LoginError('If you do not pass a username to login(), you should configure a default one!')
            else:
                username = self.USERNAME
        else:
            if reenter_password is False:
                password_from_keyring = keyring.get_password('astroquery:archive-api.lco.global', username)
            else:
                password_from_keyring = None
            if password_from_keyring is None:
                if system_tools.in_ipynb():
                    log.warning('You may be using an ipython notebook: the password form will appear in your terminal.')
                password = getpass.getpass('{0}, enter your Las Cumbres Observatory password:\n'.format(username))
            else:
                password = password_from_keyring
            log.info('Authenticating {0} with lco.global...'.format(username))
            login_response = self._request('POST', (conf.get_token), cache=False,
              data={'username':username,  'password':password})
            if login_response.status_code == 200:
                log.info('Authentication successful!')
                token = json.loads(login_response.content)
                self.TOKEN = token['token']
            else:
                log.exception('Authentication failed!')
            token = None
        if token:
            if password_from_keyring is None:
                if store_password:
                    keyring.set_password('astroquery:archive-api.lco.global', username, password)

    def _parse_result(self, response, verbose=False):
        if not verbose:
            commons.suppress_vo_warnings()
        log.info(len(self.DTYPES), len(self.DATA_NAMES))
        t = Table(names=(self.DATA_NAMES), dtype=(self.DTYPES))
        if response['count'] > 0:
            try:
                for line in response['results']:
                    filtered_line = {key:line[key] for key in self.DATA_NAMES}
                    t.add_row(filtered_line)

            except ValueError:
                pass

        return t

    def _parse_response(self, request_payload, cache):
        if not self.TOKEN:
            warnings.warn('You have not authenticated and will only get results for non-proprietary data')
            headers = None
        else:
            headers = {'Authorization': 'Token ' + self.TOKEN}
        response = self._request('GET', (self.FRAMES_URL), params=request_payload, timeout=(self.TIMEOUT),
          cache=cache,
          headers=headers)
        if response.status_code == 200:
            resp = json.loads(response.content)
            return self._parse_result(resp)
        else:
            log.exception('Failed!')
            return False


Lco = LcoClass()

def validate_datetime(input):
    format_string = '%Y-%m-%d %H:%M'
    try:
        datetime.strptime(input, format_string)
        return input
    except ValueError:
        warning.warning('Input {} is not in format {} - ignoring input'.format(input, format_string))
        return ''


def validate_rlevel(input):
    excepted_vals = ['0', '00', '11', '91']
    if str(input) in excepted_vals:
        return input
    else:
        warning.warning('Input {} is not one of {} - ignoring'.format(input, ','.join(excepted_vals)))
        return ''


def validate_coordinates(coordinates):
    c = commons.parse_coordinates(coordinates)
    if c.frame.name == 'galactic':
        coords = 'POINT({} {})'.format(c.icrs.ra.degree, c.icrs.dec.degree)
    else:
        ra, dec = commons.coord_to_radec(c)
        coords = 'POINT({} {})'.format(ra, dec)
    return coords