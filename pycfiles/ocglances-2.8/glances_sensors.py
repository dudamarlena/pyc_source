# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Téléchargements/ocglances/tmp/ocglances/plugins/glances_sensors.py
# Compiled at: 2017-02-11 10:25:25
"""Sensors plugin."""
try:
    import sensors
except ImportError:
    pass

from ocglances.logger import logger
from ocglances.plugins.glances_batpercent import Plugin as BatPercentPlugin
from ocglances.plugins.glances_hddtemp import Plugin as HddTempPlugin
from ocglances.plugins.glances_plugin import GlancesPlugin
SENSOR_TEMP_UNIT = 'C'
SENSOR_FAN_UNIT = 'rpm'

def to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 1.8 + 32


class Plugin(GlancesPlugin):
    """Glances sensors plugin.

    The stats list includes both sensors and hard disks stats, if any.
    The sensors are already grouped by chip type and then sorted by name.
    The hard disks are already sorted by name.
    """

    def __init__(self, args=None):
        """Init the plugin."""
        super(Plugin, self).__init__(args=args)
        self.glancesgrabsensors = GlancesGrabSensors()
        self.hddtemp_plugin = HddTempPlugin(args=args)
        self.batpercent_plugin = BatPercentPlugin(args=args)
        self.display_curse = True
        self.reset()

    def get_key(self):
        """Return the key of the list."""
        return 'label'

    def reset(self):
        """Reset/init the stats."""
        self.stats = []

    @GlancesPlugin._check_decorator
    @GlancesPlugin._log_result_decorator
    def update(self):
        """Update sensors stats using the input method."""
        self.reset()
        if self.input_method == 'local':
            self.stats = []
            try:
                temperature = self.__set_type(self.glancesgrabsensors.get('temperature_core'), 'temperature_core')
            except Exception as e:
                logger.error('Cannot grab sensors temperatures (%s)' % e)
            else:
                self.stats.extend(temperature)

            try:
                fan_speed = self.__set_type(self.glancesgrabsensors.get('fan_speed'), 'fan_speed')
            except Exception as e:
                logger.error('Cannot grab FAN speed (%s)' % e)
            else:
                self.stats.extend(fan_speed)

            try:
                hddtemp = self.__set_type(self.hddtemp_plugin.update(), 'temperature_hdd')
            except Exception as e:
                logger.error('Cannot grab HDD temperature (%s)' % e)
            else:
                self.stats.extend(hddtemp)

            try:
                batpercent = self.__set_type(self.batpercent_plugin.update(), 'battery')
            except Exception as e:
                logger.error('Cannot grab battery percent (%s)' % e)
            else:
                self.stats.extend(batpercent)

        elif self.input_method == 'snmp':
            pass
        return self.stats

    def __set_type(self, stats, sensor_type):
        """Set the plugin type.

        4 types of stats is possible in the sensors plugin:
        - Core temperature: 'temperature_core'
        - Fan speed: 'fan_speed'
        - HDD temperature: 'temperature_hdd'
        - Battery capacity: 'battery'
        """
        for i in stats:
            i.update({'type': sensor_type})
            i.update({'key': self.get_key()})

        return stats

    def update_views(self):
        """Update stats views."""
        super(Plugin, self).update_views()
        for i in self.stats:
            if not i['value']:
                continue
            if i['type'] == 'battery':
                self.views[i[self.get_key()]]['value']['decoration'] = self.get_alert(100 - i['value'], header=i['type'])
            else:
                self.views[i[self.get_key()]]['value']['decoration'] = self.get_alert(i['value'], header=i['type'])

    def msg_curse(self, args=None):
        """Return the dict to display in the curse interface."""
        ret = []
        if not self.stats or args.disable_sensors:
            return ret
        msg = ('{:18}').format('SENSORS')
        ret.append(self.curse_add_line(msg, 'TITLE'))
        for i in self.stats:
            if i['type'] == 'battery' and i['value'] == []:
                continue
            ret.append(self.curse_new_line())
            label = self.has_alias(i['label'].lower())
            if label is None:
                label = i['label']
            if i['type'] != 'fan_speed':
                msg = ('{:15}').format(label[:15])
            else:
                msg = ('{:13}').format(label[:13])
            ret.append(self.curse_add_line(msg))
            if i['value'] in ('ERR', 'SLP', 'UNK', 'NOS'):
                msg = ('{:>8}').format(i['value'])
                ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='value', option='decoration')))
            else:
                if args.fahrenheit and i['type'] != 'battery' and i['type'] != 'fan_speed':
                    value = to_fahrenheit(i['value'])
                    unit = 'F'
                else:
                    value = i['value']
                    unit = i['unit']
                try:
                    msg = ('{:>7.0f}{}').format(value, unit)
                    ret.append(self.curse_add_line(msg, self.get_views(item=i[self.get_key()], key='value', option='decoration')))
                except (TypeError, ValueError):
                    pass

        return ret


class GlancesGrabSensors(object):
    """Get sensors stats using the py3sensors library."""

    def __init__(self):
        """Init sensors stats."""
        try:
            sensors.init()
        except Exception:
            self.initok = False
        else:
            self.initok = True

        self.reset()

    def reset(self):
        """Reset/init the stats."""
        self.sensors_list = []

    def __update__(self):
        """Update the stats."""
        self.reset()
        if self.initok:
            for chip in sensors.iter_detected_chips():
                for feature in chip:
                    sensors_current = {}
                    if feature.name.startswith('temp'):
                        sensors_current['unit'] = SENSOR_TEMP_UNIT
                    elif feature.name.startswith('fan'):
                        sensors_current['unit'] = SENSOR_FAN_UNIT
                    if sensors_current:
                        try:
                            sensors_current['label'] = feature.label
                            sensors_current['value'] = int(feature.get_value())
                        except Exception as e:
                            logger.debug('Cannot grab sensor stat (%s)' % e)
                        else:
                            self.sensors_list.append(sensors_current)

        return self.sensors_list

    def get(self, sensor_type='temperature_core'):
        """Get sensors list."""
        self.__update__()
        if sensor_type == 'temperature_core':
            ret = [ s for s in self.sensors_list if s['unit'] == SENSOR_TEMP_UNIT ]
        elif sensor_type == 'fan_speed':
            ret = [ s for s in self.sensors_list if s['unit'] == SENSOR_FAN_UNIT ]
        else:
            logger.debug('Unknown sensor type %s' % sensor_type)
            ret = []
        return ret

    def quit(self):
        """End of connection."""
        if self.initok:
            sensors.cleanup()