# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martin/Documents/privatespace/pyconnectedcars/pyconnectedcars/controller.py
# Compiled at: 2018-02-17 19:55:59
# Size of source mod 2**32: 1881 bytes
import time
from multiprocessing import RLock
from pyconnectedcars.connection import Connection
from pyconnectedcars.Fuel import Fuel
from pyconnectedcars.Lock import Lock
from pyconnectedcars.BinarySensor import SystemsAreOkSensor, OilLevelIsOkSensor, TirePressureIsOkSensor, BatteryChargeIsOkSensor
from pyconnectedcars.GPS import GPS, Odometer

class Controller:

    def __init__(self, email, password, update_interval, baseurl=''):
        self._Controller__connection = Connection(email, password, baseurl)
        self._Controller__vehicles = []
        self.update_interval = update_interval
        self._Controller__car = {}
        self._Controller__last_update_time = 0
        self._Controller__lock = RLock()
        self.update()
        for car_id, car in self._Controller__car.items():
            self._Controller__vehicles.append(Fuel(car, self))
            self._Controller__vehicles.append(Lock(car, self))
            self._Controller__vehicles.append(GPS(car, self))
            self._Controller__vehicles.append(Odometer(car, self))
            self._Controller__vehicles.append(SystemsAreOkSensor(car, self))
            self._Controller__vehicles.append(OilLevelIsOkSensor(car, self))
            self._Controller__vehicles.append(TirePressureIsOkSensor(car, self))
            self._Controller__vehicles.append(BatteryChargeIsOkSensor(car, self))

    def get(self):
        self._Controller__last_update_time = time.time()
        return self._Controller__connection.get_data()

    def list_vehicles(self):
        return self._Controller__vehicles

    def update(self):
        cur_time = time.time()
        with self._Controller__lock:
            if cur_time - self._Controller__last_update_time > self.update_interval:
                data = self.get()
                if data:
                    if data['data']:
                        for car_data in data['data']['user']['cars']:
                            self._Controller__car[car_data['id']] = car_data

                else:
                    self._Controller__car = {}

    def get_car_params(self, car_id):
        return self._Controller__car[car_id]