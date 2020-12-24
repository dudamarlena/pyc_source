# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tamell/code/pyteslaapi/pyteslaapi/vehicle.py
# Compiled at: 2018-11-02 20:45:38
# Size of source mod 2**32: 7965 bytes
from exceptions import TeslaException
from climate import Climate
from drive import Drive
from charge import Charge
from gui_settings import GuiSettings
import logging, time
_LOGGER = logging.getLogger(__name__)

class Vehicle:
    UPDATES = [
     'vehicle_state', 'drive_state', 'charge_state', 'climate_state', 'gui_settings']
    STATE_VENT = 'vent'
    STATE_CLOSE = 'close'

    def __init__(self, client, data):
        self._Vehicle__id = data['id']
        self._vehicle_id = data['vehicle_id']
        self._Vehicle__vin = data['vin']
        self._Vehicle__state = data['state']
        self._Vehicle__name = data['display_name']
        self._Vehicle__client = client
        self._Vehicle__vehicle_data = None
        self._drive_data = None
        self._charge_data = None
        self._climate_data = None
        self._gui_settings_data = None
        self._Vehicle__climate = Climate(self)
        self._Vehicle__drive = Drive(self)
        self._Vehicle__charge = Charge(self)
        self._Vehicle__gui_settings = GuiSettings(self)

    def __update_state(self, data):
        self._Vehicle__state = data['state']
        self._Vehicle__name = data['display_name']

    def update_vehicle(self):
        vehicles = self._Vehicle__client.get('vehicles')
        for v in vehicles:
            if v['id'] == self._Vehicle__id:
                self._Vehicle__update_state(v)

    def update(self):
        for update in self.UPDATES:
            try:
                data = self._Vehicle__client.get('vehicles/{}/data_request/{}'.format(self.id, update))
                if update == 'vehicle_state':
                    _LOGGER.debug(data)
                    self._Vehicle__vehicle_data = data
                else:
                    if update == 'drive_state':
                        self._drive_data = data
                    else:
                        if update == 'charge_state':
                            self._charge_data = data
                        else:
                            if update == 'climate_state':
                                self._climate_data = data
                            else:
                                if update == 'gui_settings':
                                    self._gui_settings_data = data
                                else:
                                    _LOGGER.debug('Unknown update of {} found'.format(update))
            except TeslaException as ex:
                try:
                    _LOGGER.error('Updating Tesla {} resulted in an error {} - {}'.format(update, ex.code, ex.message))
                finally:
                    ex = None
                    del ex

    def __set_sunroof_state(self, state):
        return self._Vehicle__client.command(self.id, 'sun_roof_control', {'state': state})

    def send_command(self, command_name, data={}):
        return self._Vehicle__client.command(self.id, command_name, data)

    def vent_sunroof(self):
        return self._Vehicle__set_sunroof_state(self.STATE_VENT)

    def close_sunroof(self):
        return self._Vehicle__set_sunroof_state(self.STATE_CLOSE)

    def open_sunroof(self, percentage):
        return self.send_command('sun_roof_control', {'percent': percentage})

    def flash_lights(self):
        return self.send_command('flash_lights')

    def honk_horn(self):
        return self.send_command('honk_horn')

    def unlock_doors(self):
        return self.send_command('door_unlock')

    def lock_doors(self):
        return self.send_command('door_lock')

    def valet_mode_off(self, pin=None):
        return self.send_command('set_valet_mode', {'on':False, 
         'pin':pin})

    def valet_mode_on(self, pin=None):
        return self.send_command('set_valet_mode', {'on':True, 
         'pin':pin})

    def reset_valet_pin(self, pin=None):
        return self.send_command('reset_valet_pin')

    def open_trunk(self, pin=None):
        return self.send_command('trunk_open', {'which_trunk': 'rear'})

    def open_frunk(self, pin=None):
        return self.send_command('trunk_open', {'which_trunk': 'front'})

    def remote_state(self, pin=None):
        return self.send_command('remote_start_drive', {'password': self._Vehicle__client._password})

    @property
    def climate(self):
        return self._Vehicle__climate

    @property
    def drive(self):
        return self._Vehicle__drive

    @property
    def charge(self):
        return self._Vehicle__charge

    @property
    def gui_settings(self):
        return self._Vehicle__gui_settings

    def wake_up(self):
        data = self._Vehicle__client.post('vehicles/{}/wake_up'.format(self.id))
        retry = 0
        while data['state'] == 'offline' and retry <= 5:
            _LOGGER.debug('Vehicle still not awake trying again')
            retry += 1
            time.sleep(retry * 2.5)
            data = self._Vehicle__client.post('vehicles/{}/wake_up'.format(self.id))

        if retry == 6:
            return False
        return data

    @property
    def id(self):
        return self._Vehicle__id

    @property
    def name(self):
        if self._Vehicle__name:
            return self._Vehicle__name
        return 'Tesla Model {} {}'.format(str(self._Vehicle__vin[3]).upper(), str(self._Vehicle__vin))

    @property
    def vin(self):
        return self._Vehicle__vin

    @property
    def state(self):
        return self._Vehicle__state

    @property
    def api_version(self):
        return self._Vehicle__vehicle_data['api_version']

    @property
    def autopark_state_v2(self):
        return self._Vehicle__vehicle_data['autopark_state_v2']

    @property
    def autopark_style(self):
        return self._Vehicle__vehicle_data['autopark_style']

    @property
    def calendar_supported(self):
        return self._Vehicle__vehicle_data['calendar_supported']

    @property
    def car_version(self):
        return self._Vehicle__vehicle_data['car_version']

    @property
    def center_display_state(self):
        return self._Vehicle__vehicle_data['center_display_state']

    @property
    def df(self):
        return self._Vehicle__vehicle_data['df']

    @property
    def dr(self):
        return self._Vehicle__vehicle_data['dr']

    @property
    def ft(self):
        return self._Vehicle__vehicle_data['ft']

    @property
    def homelink_nearby(self):
        return self._Vehicle__vehicle_data['homelink_nearby']

    @property
    def is_user_present(self):
        return self._Vehicle__vehicle_data['is_user_present']

    @property
    def last_autopark_eror(self):
        return self._Vehicle__vehicle_data['last_autopark_eror']

    @property
    def locked(self):
        return self._Vehicle__vehicle_data['locked']

    @property
    def media_state(self):
        return self._Vehicle__vehicle_data['media_state']

    @property
    def notifications_supported(self):
        return self._Vehicle__vehicle_data['notifications_supported']

    @property
    def odometer(self):
        return self._Vehicle__vehicle_data['odometer']

    @property
    def parsed_calendar_supported(self):
        return self._Vehicle__vehicle_data['parsed_calendar_supported']

    @property
    def pf(self):
        return self._Vehicle__vehicle_data['pf']

    @property
    def pr(self):
        return self._Vehicle__vehicle_data['pr']

    @property
    def remote_start(self):
        return self._Vehicle__vehicle_data['remote_start']

    @property
    def remote_start_supported(self):
        return self._Vehicle__vehicle_data['remote_start_supported']

    @property
    def rt(self):
        return self._Vehicle__vehicle_data['rt']

    @property
    def software_update(self):
        return self._Vehicle__vehicle_data['software_update']

    @property
    def speed_limit_mode(self):
        return self._Vehicle__vehicle_data['speed_limit_mode']

    @property
    def sun_roof_percent_open(self):
        return self._Vehicle__vehicle_data['sun_roof_percent_open']

    @property
    def sun_roof_state(self):
        return self._Vehicle__vehicle_data['sun_roof_state']

    @property
    def timestamp(self):
        return self._Vehicle__vehicle_data['timestamp']

    @property
    def valet_mode(self):
        return self._Vehicle__vehicle_data['valet_mode']

    @property
    def vehicle_name(self):
        return self._Vehicle__vehicle_data['vehicle_name']