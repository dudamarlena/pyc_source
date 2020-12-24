# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\wl\routing.py
# Compiled at: 2017-11-15 21:37:42
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
import datetime
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from flotils import Loadable
from floscraper import WebScraper
from requests.compat import urljoin
from dateutil.parser import parse as dt_parse
from .models.routing import ItdRequest, ItdResponse, ItdDMResponse, Line, Departure, Stop
from .errors import RequestException
from .utils import local_to_utc, utc_to_local

class WLRouting(Loadable):
    """ Wienerlinien routing API """

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(WLRouting, self).__init__(settings)
        self.base_url = b'https://www.wienerlinien.at/ogd_routing/'
        self.session = WebScraper(settings.get(b'web', {}))
        return

    def _parse_datetime_st(self, st):
        if not st:
            return st
        return local_to_utc(dt_parse(st))

    def _parse_response(self, data):
        """

        :param data:
        :type data:
        :return:
        :rtype: wl.models.routing.ItdResponse
        """
        try:
            root = etree.fromstring(data)
        except ValueError:
            root = etree.fromstring(data.encode(b'utf-8'), parser=etree.XMLParser(encoding=b'utf-8'))

        if root is None or root.tag != b'itdRequest':
            raise ValueError(b'Wrong root tag')
        res = ItdResponse()
        attr = {}
        if root.attrib:
            attr = root.attrib
        if b'serverID' in attr:
            res.server_id = attr[b'serverID']
        if b'version' in attr:
            res.version = attr[b'version']
        if b'language' in attr:
            res.language = attr[b'language']
        if b'lengthUnit' in attr:
            res.length_unit = attr[b'lengthUnit']
        if b'sessionID' in attr:
            res.session_id = attr[b'sessionID']
        if b'client' in attr:
            res.client = attr[b'client']
        if b'virtDir' in attr:
            res.virt_dir = attr[b'virtDir']
        if b'clientIP' in attr:
            res.client_ip = attr[b'clientIP']
        if b'now' in attr:
            res.now = self._parse_datetime_st(attr[b'now'])
        if b'nowWD' in attr:
            res.now_wd = attr[b'nowWD']
        res.children = list(root)
        return res

    def _make_req(self, url_part, req):
        """

        :param url_part: What service of routing api to use
        :type url_part: str | unicode
        :param req:
        :type req: wl.models.routing.ItdRequest
        :return: Response root element
        :rtype: wl.models.routing.ItdResponse
        """
        url = urljoin(self.base_url, url_part)
        try:
            resp = self.session.get(url, params=req.to_get_params())
        except:
            self.exception((b'Failed to load on {}:\n{}').format(url, req.to_get_params()))
            raise RequestException(b'Request failed')

        try:
            if resp.html and resp.html.startswith(b'<!DOCTYPE HTML'):
                raise RequestException(b'API send plain html')
            data = resp.raw
            if not data:
                self.warning(b'Defaulting to decoded response')
                data = resp.html
            res = self._parse_response(data)
        except:
            self.exception((b'Failed to parse {}:\n{}').format(url, req.to_get_params()))
            raise RequestException(b'Parse failed')

        return res

    def _parse_line(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: wl.models.routing.Line
        """
        if root.tag != b'itdServingLine':
            raise ValueError((b'Expected line - {}').format(root.tag))
        line_dict = root.attrib
        for ele in root:
            if ele.tag == b'motDivaParams':
                line_dict[b'network'] = ele.attrib.get(b'network')
                line_dict[b'line'] = ele.attrib.get(b'line')
            elif ele.tag == b'itdRouteDescText':
                line_dict[b'description'] = ele.text

        return Line.from_dict(line_dict)

    def _parse_lines(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: list[wl.models.routing.Line]
        """
        if root.tag != b'itdServingLines':
            raise ValueError((b'Expected lines - {}').format(root.tag))
        lines = []
        for ele in root:
            lines.append(self._parse_line(ele))

        return lines

    def _parse_datetime_itd(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: datetime.datetime
        """
        if root.tag != b'itdDateTime':
            raise ValueError((b'Expected datetime - {}').format(root.tag))
        d = root.find(b'itdDate')
        t = root.find(b'itdTime')
        dt_dict = {}
        if d is None:
            raise ValueError(b'Expected date')
        if t is None:
            raise ValueError(b'Expected time')
        dt_dict.update(d.attrib)
        dt_dict.update(t.attrib)
        del dt_dict[b'weekday']
        dt_dict = {key:int(value) for key, value in dt_dict.items() if value if value}
        return local_to_utc(datetime.datetime(**dt_dict))

    def _parse_departure(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: wl.models.routing.Depature
        """
        if root.tag != b'itdDeparture':
            raise ValueError((b'Expected departure - {}').format(root.tag))
        d = root.attrib
        d.update({b'stop_id': d[b'stopID'], 
           b'stop_name': d[b'stopName'], 
           b'platform_name': d[b'platformName']})
        res = Departure.from_dict(d)
        for ele in root:
            if ele.tag == b'itdServingLine':
                res.line = self._parse_line(ele)
            elif ele.tag == b'itdDateTime':
                res.datetime = self._parse_datetime_itd(ele)
            else:
                self.debug((b'{}').format(ele.tag))

        return res

    def _parse_departures(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: list[wl.models.routing.Depature]
        """
        if root.tag != b'itdDepartureList':
            raise ValueError((b'Expected departures - {}').format(root.tag))
        deps = []
        for ele in root:
            deps.append(self._parse_departure(ele))

        return deps

    def _parse_stop(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: wl.models.routing.Stop
        """
        if root.tag != b'itdOdvAssignedStop':
            raise ValueError((b'Expected stop - {}').format(root.tag))
        d = root.attrib
        d.update({b'stop_id': d[b'stopID'], 
           b'distance_time': d[b'distanceTime']})
        res = Stop.from_dict(d)
        res.name = root.text
        return res

    def _parse_stops(self, root):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :return:
        :rtype: list[wl.models.routing.Stop]
        """
        if root.tag != b'itdOdvAssignedStops':
            raise ValueError((b'Expected stops - {}').format(root.tag))
        stops = []
        for ele in root:
            stops.append(self._parse_stop(ele))

        return stops

    def _parse_odv_name_elem(self, root):
        if root.tag != b'odvNameElem':
            raise ValueError((b'Expected odv name elem - {}').format(root.tag))
        res = Stop()
        res.stop_id = root.attrib.get(b'id', root.attrib.get(b'stopID'))
        res.name = root.text
        return res

    def _parse_odv_name(self, root):
        if root.tag != b'itdOdvName':
            raise ValueError((b'Expected odv name - {}').format(root.tag))
        stops = []
        for ele in root:
            if ele.tag == b'odvNameElem':
                stops.append(self._parse_odv_name_elem(ele))

        return stops

    def _parse_itd_odv(self, root, res):
        """

        :param root:
        :type root: xml.etree.ElementTree.Element
        :param res:
        :type res: wl.models.routing.ItdDMResponse
        :return:
        :rtype: wl.models.routing.ItdDMResponse
        """
        if root.tag != b'itdOdv':
            raise ValueError((b'Expected odv - {}').format(root.tag))
        xml_stops = root.find(b'itdOdvAssignedStops')
        if xml_stops is not None:
            res.stops = self._parse_stops(xml_stops)
        else:
            xml_names = root.find(b'itdOdvName')
            res.stops = self._parse_odv_name(xml_names)
        return res

    def _parse_response_dm(self, resp):
        """

        :param resp:
        :type resp: wl.models.routing.ItdResponse
        :return:
        :rtype: wl.models.routing.ItdDMResponse
        """
        if not resp.children or len(resp.children) != 0:
            ValueError(b'Invalid Subtype')
        mon = resp.children[0]
        if mon.tag != b'itdDepartureMonitorRequest':
            ValueError((b'Exepected departure monitor - {}').format(mon.tag))
        res = ItdDMResponse.from_dict(resp.to_dict())
        res.children = None
        res.request_id = mon.get(b'requestID')
        for ele in mon:
            if ele.tag == b'itdServingLines':
                res.lines = self._parse_lines(ele)
            elif ele.tag == b'itdDateTime':
                res.datetime = self._parse_datetime_itd(ele)
            elif ele.tag == b'itdDepartureList':
                res.departures = self._parse_departures(ele)
            elif ele.tag == b'itdOdv':
                self._parse_itd_odv(ele, res)

        return res

    def _make_req_dm(self, req):
        """

        :param req:
        :type req: wl.models.routing.ItdRequest
        :return:
        :rtype: wl.models.routing.ItdDMResponse
        """
        itd_resp = self._make_req(b'XML_DM_REQUEST', req)
        return self._parse_response_dm(itd_resp)

    def dm_search(self, location, dt=None, limit=40):
        req = ItdRequest()
        req.session_id = 0
        req.params.update({b'locationServerActive': 1, 
           b'lsShowTrainsExplicit': 1, 
           b'type_dm': b'any', 
           b'name_dm': location, 
           b'limit': limit})
        if dt:
            dt = utc_to_local(dt)
            req.params[b'itdDate'] = dt.strftime(b'%Y%m%d')
            req.params[b'itdTime'] = dt.strftime(b'%H%M')
        res = self._make_req_dm(req)
        return res

    def dm_select(self, resp, lines=None, dt=None, stops=None, limit=40):
        req = ItdRequest.from_dict(resp.to_dict())
        req.params = []
        if stops:
            req.params.append(('type_dm', 'stopID'))
            for stop_id in stops:
                req.params.append((b'name_dm', stop_id))

        if lines is None:
            req.params.append(('dmLineSelectionAll', 1))
        else:
            req.params = []
            for line in lines:
                if isinstance(line, Line):
                    req.params.append((b'dmLineSelection', line.index))
                else:
                    req.params.append((b'dmLineSelection', line))

        if dt:
            dt = utc_to_local(dt)
            req.params.append((b'itdDate', dt.strftime(b'%Y%m%d')))
            req.params.append((b'itdTime', dt.strftime(b'%H%M')))
        req.params.append((b'limit', limit))
        res = self._make_req_dm(req)
        return res

    def dm_search_select(self, location, dt=None, limit=40):
        req = ItdRequest()
        req.session_id = 0
        req.params.update({b'locationServerActive': 1, 
           b'lsShowTrainsExplicit': 1, 
           b'type_dm': b'any', 
           b'name_dm': location, 
           b'limit': limit, 
           b'dmLineSelectionAll': 1})
        if dt:
            dt = utc_to_local(dt)
            req.params[b'itdDate'] = dt.strftime(b'%Y%m%d')
            req.params[b'itdTime'] = dt.strftime(b'%H%M')
        res = self._make_req_dm(req)
        return res