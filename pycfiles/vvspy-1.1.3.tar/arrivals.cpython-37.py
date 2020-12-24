# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\arrivals.py
# Compiled at: 2019-12-09 14:13:30
# Size of source mod 2**32: 4536 bytes
from typing import List, Union
from datetime import datetime
import requests, json, traceback
from .obj import Arrival
_API_URL = 'http://www3.vvs.de/vvs/widget/XML_DM_REQUEST?'

def get_arrivals(station_id: Union[(str, int)], check_time: datetime=None, limit: int=100, debug: bool=False, request_params: dict=None, **kwargs) -> Union[(List[Arrival], None)]:
    """

    Returns: List[:class:`vvspy.obj.Arrival`]
    Returns none on webrequest errors.

    Examples
    --------
    Basic usage:

    .. code-block:: python

        results = vvspy.get_arrivals("5006115", limit=3)  # Stuttgart main station

    Set proxy for request:

    .. code-block:: python

        proxies = {}  # see https://stackoverflow.com/a/8287752/9850709
        results = vvspy.get_arrivals("5006115", request_params={"proxies": proxies})

    Parameters
    ----------
        station_id Union[:class:`int`, :class:`str`]
            Station you want to get arrivals from.
            See csv on root of repository to get your id.
        check_time Optional[:class:`datetime.datetime`]
            Time you want to check.
            default datetime.now()
        limit Optional[:class:`int`]
            Limit request/result on this integer.
            default 100
        debug Optional[:class:`bool`]
            Get advanced debug prints on failed web requests
            default False
        request_params Optional[:class:`dict`]
            params parsed to the api request (e.g. proxies)
            default {}
        kwargs Optional[:class:`dict`]
            Check arrivals.py to see all available kwargs.
    """
    if not check_time:
        check_time = datetime.now()
    else:
        if request_params is None:
            request_params = dict()
        params = {'locationServerActive':kwargs.get('locationServerActive', 1),  'lsShowTrainsExplicit':kwargs.get('lsShowTrainsExplicit', 1), 
         'stateless':kwargs.get('stateless', 1), 
         'language':kwargs.get('language', 'de'), 
         'SpEncId':kwargs.get('SpEncId', 0), 
         'anySigWhenPerfectNoOtherMatches':kwargs.get('anySigWhenPerfectNoOtherMatches', 1), 
         'limit':limit, 
         'depArr':'arrival', 
         'type_dm':kwargs.get('type_dm', 'any'), 
         'anyObjFilter_dm':kwargs.get('anyObjFilter_dm', 2), 
         'deleteAssignedStops':kwargs.get('deleteAssignedStops', 1), 
         'name_dm':station_id, 
         'mode':kwargs.get('mode', 'direct'), 
         'dmLineSelectionAll':kwargs.get('dmLineSelectionAll', 1), 
         'useRealtime':kwargs.get('useRealtime', 1), 
         'outputFormat':kwargs.get('outputFormat', 'json'), 
         'coordOutputFormat':kwargs.get('coordOutputFormat', 'WGS84[DD.ddddd]'), 
         'itdDateTimeDepArr':'arr', 
         'itdDateYear':check_time.strftime('%Y'), 
         'itdDateMonth':check_time.strftime('%m'), 
         'itdDateDay':check_time.strftime('%d'), 
         'itdTimeHour':check_time.strftime('%H'), 
         'itdTimeMinute':check_time.strftime('%M'), 
         'itdTripDateTimeDepArr':'arr'}
        try:
            r = (requests.get)(_API_URL, **{**request_params, **{'params': params}})
        except ConnectionError as e:
            try:
                print('ConnectionError')
                traceback.print_exc()
                return
            finally:
                e = None
                del e

    if r.status_code != 200:
        if debug:
            print('Error in API request')
            print(f"Request: {r.status_code}")
            print((f"{r.text}"))
        return
    try:
        r.encoding = 'UTF-8'
        return _parse_response(r.json())
    except json.decoder.JSONDecodeError:
        if debug:
            print('Error in API request')
            print('Received invalid json')
            print(f"Request: {r.status_code}")
            print((f"{r.text}"))
        return


def _parse_response(result: dict) -> List[Union[Arrival]]:
    parsed_response = []
    if not (result and 'arrivalList' not in result or result['arrivalList']):
        return []
        if isinstance(result['arrivalList'], dict):
            parsed_response.append(Arrival(**result['arrivalList']['arrival']))
        else:
            if isinstance(result['arrivalList'], list):
                for arrival in result['arrivalList']:
                    parsed_response.append(Arrival(**arrival))

    return parsed_response