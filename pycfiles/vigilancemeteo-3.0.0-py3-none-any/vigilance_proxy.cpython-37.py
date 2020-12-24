# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benoit/Dev/vigilance-meteo/src/vigilancemeteo/vigilance_proxy.py
# Compiled at: 2019-04-14 13:05:36
# Size of source mod 2**32: 9707 bytes
"""Implement a class to communicate with Météofrance weather alerts website."""
import re, sys
from datetime import datetime
from lxml import etree
from pytz import timezone
from vigilancemeteo.constants import ALERT_COLOR_LIST, ALERT_TYPE_LIST, COASTAL_DEPARTMENT_LIST, UPDATE_STATUS_CHECKSUM_CACHED_60S, UPDATE_STATUS_CHECKSUM_UPDATED, UPDATE_STATUS_ERROR_AND_BULLETIN_EXPIRED, UPDATE_STATUS_ERROR_BUT_PREVIOUS_BULLETIN_VALID, UPDATE_STATUS_SAME_CHECKSUM, UPDATE_STATUS_XML_UPDATED, VALID_DEPARTMENT_LIST
if sys.version_info < (3, 0):
    from urllib2 import urlopen, URLError
else:
    from urllib.request import urlopen, URLError

class VigilanceMeteoError(Exception):
    __doc__ = 'Error class, used when fetching or parsing vigilance.meteofrance.com website.'


class VigilanceMeteoFranceProxy(object):
    __doc__ = 'Class to manage the download of the data sources from MeteoFrance website.\n    \n    Data are fetch on vigilance.meteofrance.com website.\n    \n    Public attributes:\n    - xml_tree = XML representation of the weather alert bulletin\n    - bulletin_date = Date of the bulletin (with timezone)\n    - checksum = Checksum of the weather alert bulletin\n    - status = current status of the proxy (possible value in constant.py)\n\n    Public Methods:\n    - update_date(): Check if new information are available and download them if any.\n    - get_alert_list(department): of a given department return the list of the alerts.\n \n    Private attributes:\n    - _xml_tree = XML representation of the weather alert bulletin\n    - _bulletin_date = Date of the bulletin (with timezone)\n    - _latest_check_date = Date of the latest check if new bulletin is available\n    - _latest_checksum_value = Checksum of the weather alert bulletin\n    '
    URL_VIGILANCE_METEO_XML = 'http://vigilance.meteofrance.com/data/NXFR33_LFPW_.xml'
    URL_VIGILANCE_METEO_CHECKSUM = 'http://vigilance.meteofrance.com/data/vigilance_controle.txt'

    def __init__(self):
        """Class instance constructor."""
        self._xml_tree = None
        self._latest_check_date = None
        self._latest_checksum_value = None
        self._bulletin_date = None
        self._proxy_status = None

    def _get_new_checksum(self):
        """Return the checksum of the data source on MétéoFrance website.
        
        The checksum allows high frequency requests and downloads data only if 
        new information are published.
        If the data source is unvailabe, return the previous checksum if bulletin
        validity date is still not reached. If the bulletin has expired, raise
        an VigilanceMeteoError error."""
        if self._latest_check_date is None or (datetime.now() - self._latest_check_date).total_seconds() > 60:
            try:
                text = urlopen(self.URL_VIGILANCE_METEO_CHECKSUM).read().decode('utf-8')
            except URLError:
                if self.bulletin_date is not None:
                    if (timezone('UTC').localize(datetime.utcnow()) - self.bulletin_date).days < 1:
                        self._proxy_status = UPDATE_STATUS_ERROR_BUT_PREVIOUS_BULLETIN_VALID
                        return self._latest_checksum_value
                self._proxy_status = UPDATE_STATUS_ERROR_AND_BULLETIN_EXPIRED
                raise VigilanceMeteoError("Error: 'vigilance_controle.txt' unreachable and weather alert bulletin has expired")
            else:
                self._latest_check_date = datetime.now()
                checksum = re.search('\\n(.+?)\\s', text)
                self._proxy_status = UPDATE_STATUS_CHECKSUM_UPDATED
                return checksum.group(1)
        else:
            self._proxy_status = UPDATE_STATUS_CHECKSUM_CACHED_60S
            return self._latest_checksum_value

    def update_data(self):
        """Downloads an updates of the XML data source only if needed.
        
        The methods checks before if the checksum has changed on the website. If
        yes, XML data source is updated.
        """
        current_checksum = self._get_new_checksum()
        if current_checksum != self._latest_checksum_value:
            self._latest_checksum_value = current_checksum
            try:
                self._xml_tree = etree.parse(self.URL_VIGILANCE_METEO_XML)
            except (OSError, IOError):
                if self.bulletin_date is not None and (timezone('UTC').localize(datetime.utcnow()) - self.bulletin_date).days < 1:
                    self._proxy_status = UPDATE_STATUS_ERROR_BUT_PREVIOUS_BULLETIN_VALID
                else:
                    self._proxy_status = UPDATE_STATUS_ERROR_AND_BULLETIN_EXPIRED
                    self._latest_check_date = None
                    raise VigilanceMeteoError("Error: 'NXFR33_LFPX_.xml' unreachable and weather alert bulletin has expired")
            else:
                string_date = self._xml_tree.xpath('/CV/EV')[0].get('dateinsert')
                annee = int(string_date[0:4])
                mois = int(string_date[4:6])
                jour = int(string_date[6:8])
                heure = int(string_date[8:10])
                minute = int(string_date[10:12])
                seconde = int(string_date[12:14])
                paris_timezone = timezone('Europe/Paris')
                self._bulletin_date = paris_timezone.localize(datetime(annee, mois, jour, heure, minute, seconde))
                self._proxy_status = UPDATE_STATUS_XML_UPDATED
        else:
            if self._proxy_status == UPDATE_STATUS_CHECKSUM_UPDATED:
                self._proxy_status = UPDATE_STATUS_SAME_CHECKSUM

    def get_alert_list(self, department):
        """Return the list and status of the alerts for a given department.
        
        For all alert types, a status (Vert, Jaune, Orange, Rouge) is returned.
        """
        self.update_data()
        alerts_list = {}
        for alert_type in ALERT_TYPE_LIST:
            alerts_list[alert_type] = 'Vert'

        department_alerts = self.xml_tree.xpath("/CV/DV[attribute::dep='" + department + "']")
        if department in COASTAL_DEPARTMENT_LIST:
            department_alerts.extend(self.xml_tree.xpath("/CV/DV[attribute::dep='" + department + "10']"))
        for alerts_group in department_alerts:
            color = int(alerts_group.get('coul'))
            for active_alert in list(alerts_group):
                alert_type = int(active_alert.get('val'))
                alerts_list[ALERT_TYPE_LIST[(alert_type - 1)]] = ALERT_COLOR_LIST[(color - 1)]

        return alerts_list

    @property
    def xml_tree(self):
        """Getter of xml_tree attribute."""
        return self._xml_tree

    @property
    def checksum(self):
        """Getter for _latest_checksum_value"""
        return self._latest_checksum_value

    @property
    def bulletin_date(self):
        """Getter for _bulletin_date"""
        return self._bulletin_date

    @property
    def status(self):
        """ Getter for _proxy_status"""
        return self._proxy_status