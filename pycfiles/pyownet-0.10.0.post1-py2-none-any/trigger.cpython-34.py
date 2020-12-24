# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/alertapi30/trigger.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 5593 bytes
from pyowm.utils import timeformatutils
from pyowm.alertapi30.enums import AlertChannelsEnum

class Trigger:
    """Trigger"""

    def __init__(self, start_after_millis, end_after_millis, conditions, area, alerts=None, alert_channels=None, id=None):
        assert start_after_millis is not None
        assert end_after_millis is not None
        assert isinstance(start_after_millis, int)
        assert isinstance(end_after_millis, int)
        if start_after_millis > end_after_millis:
            raise ValueError('Error: trigger start time must precede trigger end time')
        self.start_after_millis = start_after_millis
        self.end_after_millis = end_after_millis
        assert conditions is not None
        if len(conditions) == 0:
            raise ValueError('A trigger must contain at least one condition: you provided none')
        self.conditions = conditions
        assert area is not None
        if len(area) == 0:
            raise ValueError('The area for a trigger must contain at least one geoJSON type: you provided none')
        self.area = area
        if alerts is None or len(alerts) == 0:
            self.alerts = list()
        else:
            self.alerts = alerts
        if alert_channels is None or len(alert_channels) == 0:
            self.alert_channels = [
             AlertChannelsEnum.OWM_API_POLLING]
        else:
            self.alert_channels = alert_channels
        self.id = id

    def get_alerts(self):
        """
        Returns all of the alerts for this `Trigger`
        :return: a list of `Alert` objects
        """
        return self.alerts

    def get_alert(self, alert_id):
        """
        Returns the `Alert` of this `Trigger` having the specified ID
        :param alert_id: str, the ID of the alert
        :return: `Alert` instance
        """
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert

    def get_alerts_since(self, timestamp):
        """
        Returns all the `Alert` objects of this `Trigger` that were fired since the specified timestamp.
        :param timestamp: time object representing the point in time since when alerts have to be fetched
        :type timestamp: int, ``datetime.datetime`` or ISO8601-formatted string
        :return: list of `Alert` instances
        """
        unix_timestamp = timeformatutils.to_UNIXtime(timestamp)
        result = []
        for alert in self.alerts:
            if alert.last_update >= unix_timestamp:
                result.append(alert)
                continue

        return result

    def get_alerts_on(self, weather_param):
        """
        Returns all the `Alert` objects of this `Trigger` that refer to the specified weather parameter (eg. 'temp',
        'pressure', etc.). The allowed weather params are the ones enumerated by class
        `pyowm.alertapi30.enums.WeatherParametersEnum`
        :param weather_param: str, values in `pyowm.alertapi30.enums.WeatherParametersEnum`
        :return: list of `Alert` instances
        """
        result = []
        for alert in self.alerts:
            for met_condition in alert.met_conditions:
                if met_condition['condition'].weather_param == weather_param:
                    result.append(alert)
                    break

        return result

    def __repr__(self):
        return '<%s.%s - id=%s, start_after_mills=%s, end_after_mills=%s, alerts=%s>' % (
         __name__,
         self.__class__.__name__,
         self.id if self.id is not None else 'None',
         self.start_after_millis,
         self.end_after_millis,
         str(len(self.alerts)))