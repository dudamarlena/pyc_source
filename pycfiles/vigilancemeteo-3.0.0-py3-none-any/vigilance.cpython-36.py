# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benoit/Dev/vigilance-meteo/vigilancemeteo/vigilance.py
# Compiled at: 2019-03-26 19:22:53
# Size of source mod 2**32: 14129 bytes
"""Implement a class for Météofrance weather alerts """
import sys, re
from datetime import datetime
from lxml import etree
from pytz import timezone
from vigilancemeteo.constants import ALERT_COLOR_LIST, VALID_DEPARTMENT_LIST
if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

class VigilanceMeteoFranceProxy(object):
    __doc__ = 'Class to manage the download of the data sources from MeteoFrance website.'
    URL_VIGILANCE_METEO_XML = 'http://vigilance.meteofrance.com/data/NXFR33_LFPW_.xml'
    URL_VIGILANCE_METEO_CHECKSUM = 'http://vigilance.meteofrance.com/data/vigilance_controle.txt'
    ALERT_TYPE_LIST = [
     'Vent violent', 'Pluie-innodation', 'Orages',
     'Inondation', 'Neige-verglas', 'Canicule',
     'Grand-froid', 'Avalanches', 'Vagues-submersion']
    COASTAL_DEPARTMENT_LIST = [
     '06', '11', '13', '14', '17', '22', '29', '2A', '2B', '30', '33', '34',
     '35', '40', '44', '50', '56', '59', '62', '64', '66', '76', '80', '83',
     '85']

    def __init__(self):
        """Class instance constructor."""
        self._xml_tree = None
        self._latest_check_date = None
        self._latest_checksum_value = None
        self._bulletin_date = None

    def _get_new_checksum(self):
        """Return the checksum of the data source on MétéoFrance website"""
        if self._latest_check_date is None or (datetime.now() - self._latest_check_date).seconds > 60:
            self._latest_check_date = datetime.now()
            text = urlopen(VigilanceMeteoFranceProxy.URL_VIGILANCE_METEO_CHECKSUM).read().decode('utf-8')
            checksum = re.search('\\n(.+?)\\s', text)
            if checksum:
                return checksum.group(1)
        else:
            return self._latest_checksum_value

    def update_data(self):
        """Download an update of the XML data source only if needed"""
        current_checksum = self._get_new_checksum
        if current_checksum != self._latest_checksum_value:
            self._latest_checksum_value = current_checksum
            self._xml_tree = etree.parse(VigilanceMeteoFranceProxy.URL_VIGILANCE_METEO_XML)
            string_date = self._xml_tree.xpath('/CV/EV')[0].get('dateinsert')
            annee = int(string_date[0:4])
            mois = int(string_date[4:6])
            jour = int(string_date[6:8])
            heure = int(string_date[8:10])
            minute = int(string_date[10:12])
            seconde = int(string_date[12:14])
            paris_timezone = timezone('Europe/Paris')
            self._bulletin_date = paris_timezone.localize(datetime(annee, mois, jour, heure, minute, seconde))

    def get_alert_list(self, department):
        """Return the list and status of the alerts for a given department."""
        self.update_data()
        alerts_list = {}
        for alert_type in VigilanceMeteoFranceProxy.ALERT_TYPE_LIST:
            alerts_list[alert_type] = 'Vert'

        department_alerts = self.xml_tree.xpath("/CV/DV[attribute::dep='" + department + "']")
        if department in VigilanceMeteoFranceProxy.COASTAL_DEPARTMENT_LIST:
            department_alerts.extend(self.xml_tree.xpath("/CV/DV[attribute::dep='" + department + "10']"))
        for alerts_group in department_alerts:
            color = int(alerts_group.get('coul'))
            for active_alert in list(alerts_group):
                alert_type = int(active_alert.get('val'))
                alerts_list[VigilanceMeteoFranceProxy.ALERT_TYPE_LIST[(alert_type - 1)]] = ALERT_COLOR_LIST[(color - 1)]

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


class ZoneAlerte(object):
    __doc__ = "A Class to descripe French departments weather alerts.\n\n    Data are fetch ont vigilance.meteofrance.com website.\n\n    Private attributes from ZoneAlerte class:\n    - _department: The department watched\n    - _alerts_list: A dictionary with all the alerts. Keys for alert type and\n      value for criticity (by color).\n\n    Methods from ZoneAlerte class:\n    - mise_a_jour_etat(): update alerts list by feching latest info from\n      MétéoFrance forcast.\n    - message_de_synthese(format): return a string with textual synthesis\n      of the active alerts in department. According to value of 'format'\n      parameter, the string return change: 'text' (default) or 'html'\n\n    Public attributes  from ZoneAlerte class\n    - department_color: return the overall criticity color for the department\n    - url_pour_en_savoir_plus: return the URL to access more information about\n      department weather alerts from the MétéoFrance website.\n    - bulletin_date: return latest bulletin update date & time with timezone\n    - departement: Get or set the departement number corresponding to the area\n      watched.\n    - alerts_list: return the list of active alerts\n\n    Example:\n    >>>import vigilancemeteo\n    >>>zone = vigilancemeteo.ZoneAlerte('92')\n    >>>zone.department_color\n    'Vert'\n    >>>zone.urlPourEnSavoirPlus\n    'http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept75&b=1&c='\n    >>>zone.message_de_synthese\n    'Aucune alerte en cours.'\n    "

    def __init__(self, department, vmf_proxy=None):
        """Class instance constructor.

        2 arguments expected:
         - The department (Required) number as a 2 character String. Can be between 01 and 95,
           2A, 2B or 99 (for Andorre).
         - a VigilanceMeteoFranceProxy object (Optional) to manage de communication with the
           Météo France online source.
        """
        self._alerts_list = {}
        self._department = None
        if vmf_proxy is not None:
            self._viglance_MF_proxy = vmf_proxy
        else:
            self._viglance_MF_proxy = VigilanceMeteoFranceProxy()
        self.department = department

    def update_department_status(self):
        """Fetch active weather alerts for the department.

        get the alert color for the 9 different types on the Météo France
        website and update the variable 'alerts_list'.
        """
        self._alerts_list = self._viglance_MF_proxy.get_alert_list(self.department)

    def __repr__(self):
        """"instance representation"""
        alerts_list_ordonnee = ''
        for key in sorted(self.alerts_list.keys()):
            alerts_list_ordonnee = alerts_list_ordonnee + "'{}': '{}', ".format(key, self.alerts_list[key])

        return "ZoneAlerte: \n - departement: '{}'\n - bulletin_date: '{}'\n - alerts_list: {{{}}}".format(self._department, self.bulletin_date, alerts_list_ordonnee[:-2])

    @property
    def department_color(self):
        """Get the department color.

        It's the color of the most critical alert.
        """
        if any(alert == 'Rouge' for alert in self.alerts_list.values()):
            synthesis = 'Rouge'
        else:
            if any(alert == 'Orange' for alert in self.alerts_list.values()):
                synthesis = 'Orange'
            else:
                if any(alert == 'Jaune' for alert in self.alerts_list.values()):
                    synthesis = 'Jaune'
                else:
                    if all(alert == 'Vert' for alert in self.alerts_list.values()):
                        synthesis = 'Vert'
                    else:
                        synthesis = None
        return synthesis

    @property
    def url_pour_en_savoir_plus(self):
        """Get the link to have additional info about alerts in department.

        Return the vigilance.meteofrance.com URL to get additinonal details
        about active alerts in the department.
        """
        return 'http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept{}&b=1&c='.format(self._department)

    def message_de_synthese(self, msg_format='text'):
        """Get synthesis text message to have the list of the active alerts."""
        if self.department_color == 'Vert':
            if msg_format == 'text':
                message = 'Aucune alerte météo en cours.'
            elif msg_format == 'html':
                message = '<p>Aucune alerte météo en cours.</p>'
        else:
            if self.department_color is None:
                if msg_format == 'text':
                    message = "Impossible de récupérer l'information"
                if msg_format == 'html':
                    message = "<p>Impossible de récupérer l'infmation</p>"
            else:
                if msg_format == 'text':
                    message = 'Alerte météo {} en cours :'.format(self.department_color)
                    for type_risque in sorted(self.alerts_list.keys()):
                        if self.alerts_list[type_risque] != 'Vert':
                            message = message + '\n - {}: {}'.format(type_risque, self.alerts_list[type_risque])

                else:
                    if msg_format == 'html':
                        message = '<p>Alerte météo {} en cours :</p><ul>'.format(self.department_color)
                        for type_risque in sorted(self.alerts_list.keys()):
                            if self.alerts_list[type_risque] != 'Vert':
                                message = message + '<li>{}: {}</li>'.format(type_risque, self.alerts_list[type_risque])

                        message = message + '</ul>'
        return message

    @property
    def bulletin_date(self):
        """Accessor and setter for Update date"""
        return self._viglance_MF_proxy.bulletin_date

    @property
    def alerts_list(self):
        """Accessor and setter for weather alerts list"""
        return self._alerts_list

    @property
    def department(self):
        """Accessor for area code linked to the weather report"""
        return self._department

    @department.setter
    def department(self, department):
        """Setter with consitency check on the are code value.

        Departemnt variable should be a 2 chararcters string. In the source XML
        file, the 92, 93 and 95 departments do not exist. In this case we have
        to use the 75 department instead.
        This setter will call the mise_a_jour_etat() method systematicaly.
        """
        if department not in VALID_DEPARTMENT_LIST:
            raise ValueError("Departement parameter have to be a 2 characters stringbetween '01' and '95' or '2A' or '2B' or '99'.Used value: {}".format(department))
        equivalence75 = [
         '92', '93', '94']
        validated_department = department
        if department in equivalence75:
            validated_department = '75'
        self._department = validated_department
        self.update_department_status()