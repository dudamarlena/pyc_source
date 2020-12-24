# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/benoit/Dev/vigilance-meteo/src/vigilancemeteo/department_weather_alert.py
# Compiled at: 2019-04-15 12:19:39
# Size of source mod 2**32: 8091 bytes
"""Implement a class for Météofrance weather alerts for a department"""
from vigilancemeteo import VigilanceMeteoError, VigilanceMeteoFranceProxy
from vigilancemeteo.constants import EQUIVALENCE_75, VALID_DEPARTMENT_LIST

class DepartmentWeatherAlert(object):
    __doc__ = "A Class to descripe French departments weather alerts.\n\n    Data are fetch on vigilance.meteofrance.com website.\n\n    Public attributes  from DepartmentWeatherAlert class\n    - department_color: return the overall criticity color for the department\n    - additional_info_URL: return the URL to access more information about\n      department weather alerts from the MétéoFrance website.\n    - bulletin_date: return latest bulletin update date & time with timezone\n    - department: Get or set the department number corresponding to the area\n      watched.\n    - alerts_list: return the list of all alert types.\n\n    Methods from DepartmentWeatherAlert class:\n    - update_department_status(): update alerts list by feching latest info from\n      MétéoFrance forcast.\n    - summary_message(format): return a string with textual synthesis of the\n      active alerts in department. According to value of 'format' parameter,\n      the string return change: 'text' (default) or 'html'\n    "

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
        try:
            self._alerts_list = self._viglance_MF_proxy.get_alert_list(self.department)
        except VigilanceMeteoError:
            self._alerts_list = {}

    def __repr__(self):
        """"instance representation"""
        alerts_list_ordonnee = ''
        for key in sorted(self.alerts_list.keys()):
            alerts_list_ordonnee = alerts_list_ordonnee + "'{}': '{}', ".format(key, self.alerts_list[key])

        return "DepartmentWeatherAlert: \n - department: '{}'\n - bulletin_date: '{}'\n - alerts_list: {{{}}}".format(self._department, self.bulletin_date, alerts_list_ordonnee[:-2])

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
                elif self.alerts_list:
                    if all(alert == 'Vert' for alert in self.alerts_list.values()):
                        synthesis = 'Vert'
                else:
                    synthesis = None
        return synthesis

    @property
    def additional_info_URL(self):
        """Get the link to have additional info about alerts in department.

        Return the vigilance.meteofrance.com URL to get additinonal details
        about active alerts in the department.
        """
        return 'http://vigilance.meteofrance.com/Bulletin_sans.html?a=dept{}&b=1&c='.format(self._department)

    def summary_message(self, msg_format='text'):
        """Get synthesis text message to have the list of the active alerts.
        
        msg_format parameter can be 'text' or 'html'.
        """
        if msg_format == 'text':
            if self.department_color == 'Vert':
                message = 'Aucune alerte météo en cours.'
            else:
                if self.department_color is None:
                    message = "Impossible de récupérer l'information."
                else:
                    message = 'Alerte météo {} en cours :'.format(self.department_color)
                    for type_risque in sorted(self.alerts_list.keys()):
                        if self.alerts_list[type_risque] != 'Vert':
                            message = message + '\n - {}: {}'.format(type_risque, self.alerts_list[type_risque])

        else:
            if msg_format == 'html':
                if self.department_color == 'Vert':
                    message = '<p>Aucune alerte météo en cours.</p>'
                else:
                    if self.department_color is None:
                        message = "<p>Impossible de récupérer l'information.</p>"
                    else:
                        message = '<p>Alerte météo {} en cours :</p><ul>'.format(self.department_color)
                        for type_risque in sorted(self.alerts_list.keys()):
                            if self.alerts_list[type_risque] != 'Vert':
                                message = message + '<li>{}: {}</li>'.format(type_risque, self.alerts_list[type_risque])

                        message = message + '</ul>'
            else:
                raise ValueError("msg_format of summary_message() only method accept 'text' or 'html' values. Used value: {}".format(msg_format))
        return message

    @property
    def bulletin_date(self):
        """Accessor and setter for bulletin update date"""
        return self._viglance_MF_proxy.bulletin_date

    @property
    def alerts_list(self):
        """Accessor and setter for weather alerts list"""
        return self._alerts_list

    @property
    def department(self):
        """Accessor for area code linked to the weather report"""
        return self._department

    @property
    def proxy(self):
        """Accessor for proxy used by the class"""
        return self._viglance_MF_proxy

    @department.setter
    def department(self, department):
        """Setter with consitency check on the are code value.

        Departemnt variable should be a 2 chararcters string. In the source XML
        file, the 92, 93 and 95 departments do not exist. In this case we have
        to use the 75 department instead.
        This setter will call the update_department_status() method systematicaly.
        """
        if department not in VALID_DEPARTMENT_LIST:
            raise ValueError("Department parameter have to be a 2 characters stringbetween '01' and '95' or '2A' or '2B' or '99'.Used value: {}".format(department))
        validated_department = department
        if department in EQUIVALENCE_75:
            validated_department = '75'
        self._department = validated_department
        self.update_department_status()