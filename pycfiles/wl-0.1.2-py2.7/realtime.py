# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\realtime.py
# Compiled at: 2017-11-03 09:14:33
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.0'
__date__ = b'2017-11-03'
from flotils import Loadable
from flotils.loadable import load_json
from floscraper import WebScraper
from requests.compat import urljoin
from dateutil.parser import parse as dt_parse
from .errors import RequestException, ProtocolViolation
from .models import Request
from .models.realtime import RTResponse, Monitor, Stop, Line, Departure
from .utils import to_utc

class WLRealtime(Loadable):
    """ Wienerlinien realtime API """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(WLRealtime, self).__init__(settings)
        self.api_key = settings[b'api_key']
        self.base_url = b'https://www.wienerlinien.at/ogd_realtime/'
        self.session = WebScraper(settings.get(b'web', {}))
        return

    def _parse_datetime(self, dt_str):
        """
        Parse datetime string to object

        :param dt_str: Datetime string to parse
        :type dt_str: str | unicode
        :return: Naive datetime in utc
        :rtype: None | datetime.datetime
        """
        if not dt_str:
            return None
        else:
            return to_utc(dt_parse(dt_str))

    def _is_present(self, element, field, required=False, type=None, exception_msg=None):
        present = field in element
        if not exception_msg:
            exception_msg = (b"field '{}' is required").format(field)
        if not present and required:
            self.debug(element)
            raise ProtocolViolation(exception_msg)
        return present

    def _get_field(self, element, field, required=False, type=None, exception_msg=None):
        """
        Get field on element

        :param element:
        :type element: dict[str | unicode, T]
        :param field:
        :type field: str | unicode
        :param required:
        :type required: bool
        :param type:
        :type type:
        :param exception_msg:
        :type exception_msg: str | unicode | None
        :return:
        :rtype: T
        """
        present = field in element
        if not exception_msg:
            exception_msg = (b"field '{}' is required").format(field)
        if not present:
            if required:
                self.debug(element)
                raise ProtocolViolation(exception_msg)
            return None
        return element[field]

    def _parse_stop(self, stop):
        """

        :param stop:
        :type stop: dict
        :return:
        :rtype: wl.models.realtime.Stop
        """
        if not stop:
            return None
        else:
            res = Stop()
            res.stop_type = self._get_field(stop, b'type', True)
            self._is_present(stop, b'geometry', True)
            try:
                res.location = {b'type': self._get_field(stop[b'geometry'], b'type', True), b'lat': self._get_field(stop[b'geometry'], b'coordinates', True)[0], 
                   b'lng': self._get_field(stop[b'geometry'], b'coordinates', True)[1]}
            except IndexError:
                raise ProtocolViolation(b'No lat/lng')

            self._is_present(stop, b'properties', True)
            self._is_present(stop[b'properties'], b'name', True)
            res.title = self._get_field(stop[b'properties'], b'title', True)
            res.municipality = self._get_field(stop[b'properties'], b'municipality', True)
            res.municipality_id = self._get_field(stop[b'properties'], b'municipalityId', True)
            res.type = self._get_field(stop[b'properties'], b'type', True)
            res.gate = self._get_field(stop[b'properties'], b'gate')
            self._is_present(stop[b'properties'], b'attributes', True)
            res.rbl = self._get_field(stop[b'properties'][b'attributes'], b'rbl', True)
            return res

    def _parse_departure(self, departure):
        """

        :param departure:
        :type departure: dict
        :return:
        :rtype: wl.models.realtime.Departure
        """
        res = Departure()
        self._is_present(departure, b'departureTime', True)
        res.planned = self._parse_datetime(self._get_field(departure[b'departureTime'], b'timePlanned', True))
        res.real = self._parse_datetime(self._get_field(departure[b'departureTime'], b'timeReal'))
        res.countdown = self._get_field(departure[b'departureTime'], b'countdown', True)
        vehicle = departure.get(b'vehicle')
        if vehicle:
            res.vehicle = {b'name': self._get_field(vehicle, b'name', True), b'direction': self._get_field(vehicle, b'direction', True), 
               b'direction_id': self._get_field(vehicle, b'richtungsId', True), 
               b'barrier_free': self._get_field(vehicle, b'barrierFree', True), 
               b'realtime_supported': self._get_field(vehicle, b'realtimeSupported', True), 
               b'traffic_jam': self._get_field(vehicle, b'trafficjam', True), 
               b'type': self._get_field(vehicle, b'type', True)}
        return res

    def _parse_line(self, line):
        """

        :param line:
        :type line: dict
        :return:
        :rtype: wl.models.realtime.Line
        """
        res = Line()
        res.name = self._get_field(line, b'name', True)
        res.towards = self._get_field(line, b'towards', True)
        res.direction = self._get_field(line, b'direction', True)
        res.direction_id = self._get_field(line, b'richtungsId', True)
        res.barrier_free = self._get_field(line, b'barrierFree')
        res.realtime_supported = self._get_field(line, b'realtimeSupported')
        res.traffic_jam = self._get_field(line, b'trafficjam')
        res.type = self._get_field(line, b'type', True)
        res.id = self._get_field(line, b'lineId')
        self._is_present(line, b'departures', True)
        deps = line[b'departures'].get(b'departure')
        if deps:
            res.departures = []
            for dep in deps:
                res.departures.append(self._parse_departure(dep))

        else:
            res.departures = deps
        return res

    def _parse_lines(self, lines):
        """

        :param line:
        :type line: None | list[dict]
        :return:
        :rtype: None | list[wl.models.realtime.Line]
        """
        if not lines:
            return lines
        res = []
        for line in lines:
            res.append(self._parse_line(line))

        return res

    def _parse_monitor(self, monitor):
        """

        :param monitor:
        :type monitor: dict
        :return:
        :rtype: wl.models.realtime.Model
        """
        res = Monitor()
        res.stop = self._parse_stop(self._get_field(monitor, b'locationStop', True))
        res.lines = self._parse_lines(self._get_field(monitor, b'lines'))
        return res

    def _parse_monitors(self, monitors):
        """

        :param monitors:
        :type monitors: None | list[dict]
        :return:
        :rtype: None | list[wl.models.realtime.Model]
        """
        if not monitors:
            return monitors
        res = []
        for mon in monitors:
            res.append(self._parse_monitor(mon))

        return res

    def _parse_response(self, data):
        res = RTResponse()
        json = load_json(data)
        res.raw = json
        if not json:
            raise Exception(b'Empty response')
        if not isinstance(json, dict):
            raise ProtocolViolation(b'Expected object')
        msg = json.get(b'message')
        if not msg or not isinstance(msg, dict):
            raise ProtocolViolation(b'Expected object')
        res.message_code = msg.get(b'messageCode')
        res.message_value = msg.get(b'value')
        if res.message_value is None or res.message_code is None:
            raise ProtocolViolation(b'Value or Code unset')
        server_time = msg.get(b'serverTime')
        if server_time:
            res.server_time = self._parse_datetime(server_time)
        data = json.get(b'data')
        if not data:
            self.warning(b'No data')
            return res
        else:
            res.monitors = self._parse_monitors(data.get(b'monitors'))
            return res

    def _make_req(self, url_part, req):
        """

        :param url_part: What service of realtime api to use
        :type url_part: str | unicode
        :param req:
        :type req: wl.models.Request
        :return: Parsed response
        :rtype: wl.models.RTResponse
        """
        url = urljoin(self.base_url, url_part)
        params = req.params
        if isinstance(params, dict):
            params = dict(params)
            params.setdefault(b'sender', self.api_key)
        else:
            if isinstance(params, list):
                params = list(params)
                if not [ a for a in params if a[0] == b'sender' ]:
                    params.append((b'sender', self.api_key))
            else:
                self.warning(b'Unknown parameters - cannot add api key')
            try:
                resp = self.session.get(url, params=params)
            except:
                self.exception((b'Failed to load on {}:\n{}').format(url, params))
                raise RequestException(b'Request failed')

            if not resp.html:
                self.error((b'No data {}:\n{}').format(url, params))
                raise RequestException(b'Empty response')
            try:
                res = self._parse_response(resp.html)
            except:
                self.exception((b'Failed to parse {}:\n{}').format(url, params))
                raise RequestException(b'Parse failed')

        return res

    def _parse_traffic(self, data):
        """

        :param data:
        :type data: dict
        :return:
        :rtype:
        """
        self.debug(b'()')
        for cat in data.get(b'trafficInfoCategoryGroups', []):
            if self._is_present(cat, b'id', True):
                pass
            if self._is_present(cat, b'name', True):
                continue

        for cat in data.get(b'trafficInfoCategories', []):
            if self._is_present(cat, b'id', True):
                pass
            if self._is_present(cat, b'refTrafficInfoCategoryGroupId', True):
                pass
            if self._is_present(cat, b'name', True):
                pass
            if self._is_present(cat, b'trafficInfoNameList', True):
                pass
            if self._is_present(cat, b'title', True):
                continue

        for info in data.get(b'trafficInfos', []):
            if self._is_present(info, b'refTrafficInfoCategoryId', True):
                pass
            if self._is_present(info, b'name', True):
                pass
            if self._is_present(info, b'priority'):
                pass
            if self._is_present(info, b'owner'):
                pass
            if self._is_present(info, b'title', True):
                pass
            if self._is_present(info, b'description', True):
                pass
            if self._is_present(info, b'relatedLines'):
                pass
            if self._is_present(info, b'relatedStops'):
                pass
            if self._is_present(info, b'time'):
                if self._is_present(info, b'start'):
                    pass
                if self._is_present(info, b'end'):
                    pass
                if self._is_present(info, b'resume'):
                    pass
            if self._is_present(info, b'attributes'):
                if self._is_present(info[b'attributes'], b'status'):
                    pass
                if self._is_present(info[b'attributes'], b'station'):
                    pass
                if self._is_present(info[b'attributes'], b'location'):
                    pass
                if self._is_present(info[b'attributes'], b'reason'):
                    pass
                if self._is_present(info[b'attributes'], b'towards'):
                    pass
                if self._is_present(info[b'attributes'], b'relatedLines'):
                    pass
                if self._is_present(info[b'attributes'], b'relatedStops'):
                    pass

    def _parse_news(self, data):
        """

        :param data:
        :type data: dict
        :return:
        :rtype:
        """
        self.debug(b'()')
        if self._is_present(data, b'poiCategoryGroups', True):
            for cat in data[b'poiCategoryGroups']:
                if self._is_present(cat, b'id', True):
                    pass
                if self._is_present(cat, b'name', True):
                    continue

        if self._is_present(data, b'poiCategories', True):
            for cat in data[b'poiCategoryGroups']:
                if self._is_present(cat, b'id', True):
                    pass
                if self._is_present(cat, b'refPoiCategoryGroupId', True):
                    pass
                if self._is_present(cat, b'name', True):
                    pass
                if self._is_present(cat, b'trafficInfoNameList', True):
                    pass
                if self._is_present(cat, b'title', True):
                    continue

        for info in data.get(b'pois', []):
            if self._is_present(info, b'refPoiCategoryId', True):
                pass
            if self._is_present(info, b'name', True):
                pass
            if self._is_present(info, b'title', True):
                pass
            if self._is_present(info, b'subtitle'):
                pass
            if self._is_present(info, b'description', True):
                pass
            if self._is_present(info, b'relatedStops'):
                pass
            if self._is_present(info, b'relatedLines'):
                pass
            if self._is_present(info, b'time', True):
                if self._is_present(info, b'start', True):
                    pass
                if self._is_present(info, b'end', True):
                    pass
            if self._is_present(info, b'attributes'):
                if self._is_present(info[b'attributes'], b'status'):
                    pass
                if self._is_present(info[b'attributes'], b'station'):
                    pass
                if self._is_present(info[b'attributes'], b'location'):
                    pass
                if self._is_present(info[b'attributes'], b'towards'):
                    pass
                if self._is_present(info[b'attributes'], b'relatedLines'):
                    pass
                if self._is_present(info[b'attributes'], b'relatedStops'):
                    pass
                if self._is_present(info[b'attributes'], b'ausVon'):
                    pass
                if self._is_present(info[b'attributes'], b'ausBis'):
                    pass
                if self._is_present(info[b'attributes'], b'rbls'):
                    pass

    def monitor(self, rbls, traffic_info=None):
        """
        Get departure monitor for stop

        :param rbls: One or more rbls
        :type rbls: str | unicode | list[str | unicode]
        :param traffic_info: One or more of
            'stoerunglang', 'stoerungkurz', 'aufzugsinfo'
        :type traffic_info: str | unicode | list[str | unicode]
        :return: Monitor information
        :rtype:
        """
        if not isinstance(rbls, list):
            rbls = [
             rbls]
        req = Request()
        req.params = [ (b'rbl', rbl) for rbl in rbls ]
        if traffic_info:
            if not isinstance(traffic_info):
                traffic_info = [
                 traffic_info]
            req.params.extend([ (b'activateTrafficInfo', t) for t in traffic_info ])
        resp = self._make_req(b'monitor', req)
        if resp.message_code != RTResponse.CODE_OK:
            raise RequestException((b'Error response {} ({})').format(resp.message_code, resp.message_value))
        if resp.monitors is None:
            raise RequestException(b'No monitors parsed')
        return resp