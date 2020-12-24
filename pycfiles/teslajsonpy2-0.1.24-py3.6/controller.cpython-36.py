# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/controller.py
# Compiled at: 2018-06-14 16:08:19
# Size of source mod 2**32: 4427 bytes
import time
from multiprocessing import RLock
from teslajsonpy2.connection import Connection
from teslajsonpy2.BatterySensor import Battery, Range
from teslajsonpy2.Lock import Lock
from teslajsonpy2.Climate import Climate, TempSensor
from teslajsonpy2.BinarySensor import ParkingSensor, ChargerConnectionSensor
from teslajsonpy2.Charger import ChargerSwitch, RangeSwitch
from teslajsonpy2.GPS import GPS, Odometer
from teslajsonpy2.Trunk import FrontTrunk, RearTrunk

class Controller:

    def __init__(self, email, password, update_interval):
        self._Controller__connection = Connection(email, password)
        self._Controller__vehicles = []
        self.update_interval = update_interval
        self._Controller__climate = {}
        self._Controller__charging = {}
        self._Controller__state = {}
        self._Controller__driving = {}
        self._Controller__gui = {}
        self._Controller__vehicle = {}
        self._Controller__last_update_time = {}
        self._Controller__update = {}
        self._Controller__lock = RLock()
        cars = self._Controller__connection.get('vehicles')['response']
        for car in cars:
            self._Controller__last_update_time[car['id']] = 0
            self._Controller__update[car['id']] = True
            self.update(car['id'])
            self._Controller__vehicles.append(Climate(car, self))
            self._Controller__vehicles.append(Battery(car, self))
            self._Controller__vehicles.append(Range(car, self))
            self._Controller__vehicles.append(TempSensor(car, self))
            self._Controller__vehicles.append(Lock(car, self))
            self._Controller__vehicles.append(ChargerConnectionSensor(car, self))
            self._Controller__vehicles.append(ChargerSwitch(car, self))
            self._Controller__vehicles.append(RangeSwitch(car, self))
            self._Controller__vehicles.append(ParkingSensor(car, self))
            self._Controller__vehicles.append(GPS(car, self))
            self._Controller__vehicles.append(Odometer(car, self))
            self._Controller__vehicles.append(FrontTrunk(car, self))
            self._Controller__vehicles.append(RearTrunk(car, self))

    def post(self, vehicle_id, command, data={}):
        return self._Controller__connection.post('vehicles/%i/%s' % (vehicle_id, command), data)

    def get(self, vehicle_id, command):
        return self._Controller__connection.get('vehicles/%i/%s' % (vehicle_id, command))

    def data_request(self, vehicle_id, name):
        return self.get(vehicle_id, 'data_request/%s' % name)['response']

    def command(self, vehicle_id, name, data={}):
        return self.post(vehicle_id, 'command/%s' % name, data)

    def list_vehicles(self):
        return self._Controller__vehicles

    def wake_up(self, vehicle_id):
        self.post(vehicle_id, 'wake_up')

    def update(self, car_id):
        cur_time = time.time()
        with self._Controller__lock:
            if self._Controller__update[car_id] and cur_time - self._Controller__last_update_time[car_id] > self.update_interval:
                self.wake_up(car_id)
                data = self.get(car_id, 'data')
                if data:
                    if data['response']:
                        self._Controller__climate[car_id] = data['response']['climate_state']
                        self._Controller__charging[car_id] = data['response']['charge_state']
                        self._Controller__state[car_id] = data['response']['vehicle_state']
                        self._Controller__driving[car_id] = data['response']['drive_state']
                        self._Controller__gui[car_id] = data['response']['gui_settings']
                        self._Controller__last_update_time[car_id] = time.time()
                        self._Controller__vehicle[car_id] = data['response']['vehicle_state']
                else:
                    self._Controller__climate[car_id] = False
                    self._Controller__charging[car_id] = False
                    self._Controller__state[car_id] = False
                    self._Controller__driving[car_id] = False
                    self._Controller__gui[car_id] = False
                    self._Controller__vehicle[car_id] = False

    def get_climate_params(self, car_id):
        return self._Controller__climate[car_id]

    def get_charging_params(self, car_id):
        return self._Controller__charging[car_id]

    def get_state_params(self, car_id):
        return self._Controller__state[car_id]

    def get_drive_params(self, car_id):
        return self._Controller__driving[car_id]

    def get_gui_params(self, car_id):
        return self._Controller__gui[car_id]

    def get_vehicle_params(self, car_id):
        return self._Controller__vehicle[car_id]

    def get_updates(self, car_id=None):
        if car_id is not None:
            return self._Controller__update[car_id]
        else:
            return self._Controller__update

    def set_updates(self, car_id, value):
        self._Controller__update[car_id] = value