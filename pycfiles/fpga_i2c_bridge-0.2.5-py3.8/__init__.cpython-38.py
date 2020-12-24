# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_i2c_bridge/__init__.py
# Compiled at: 2020-04-15 04:29:35
# Size of source mod 2**32: 9542 bytes
"""I2C Bridge API. Provides an interface for the FPGA smart home bridge."""
import threading
from time import sleep
from typing import List, Dict, Union
from fpga_i2c_bridge.appliance import I2CGenericBinary, I2CDimmer, I2CRGBDimmer, I2CShutter, I2CAppliance, I2CApplianceType, UnknownDeviceTypeError, InvalidStateError
from fpga_i2c_bridge.sensor import I2CSensor, I2CSensorType, I2CBinarySensor, I2CShutterControlSensor, I2CCycleButtonSensor
from fpga_i2c_bridge.net.error import I2CException, I2CNoSuchDeviceException
from fpga_i2c_bridge.net.packet import I2CApplianceStateResponse, I2CInputEventResponse
from fpga_i2c_bridge.util import Logger

class I2CBridge:
    __doc__ = 'Represents a FPGA smart home bridge.'

    def __init__(self, i2c_dummy=False, i2c_dummy_appliances: List[int]=None, i2c_dummy_sensors: List[int]=None, i2c_bus=1, i2c_addr=62):
        """The I2C hardware bus to be used."""
        self.bus = i2c_bus
        self.addr = i2c_addr
        if i2c_dummy:
            from fpga_i2c_bridge.i2c_dummy import I2CDummy
            self.i2c = I2CDummy(appliance_types=(i2c_dummy_appliances or [4, 3, 2, 1]), sensor_types=(i2c_dummy_sensors or [5, 4, 3, 2, 1]),
              error_ratio=0.002)
        else:
            from fpga_i2c_bridge.i2c import I2CBusReal
            self.i2c = I2CBusReal(bus=i2c_bus, addr=i2c_addr)
        self.logger = Logger.get_logger(self)
        self.version = None
        self._num_appliances = 0
        self._num_sensors = 0
        self._query_status()
        self.appliances = {}
        self.sensors = {}
        self._query_devices()
        self.is_polling = False
        self.poll_update_callbacks = {}
        self.poll_delay = 0.5
        self.poll_thread = threading.Thread(target=(self._poll_loop), daemon=True)
        self.poll_thread.start()
        self.poll_fail_delay = 2

    def _query_status(self) -> None:
        """Queries status and number of devices from the FPGA."""
        info = self.i2c.get_fpga_status()
        self.logger.info('FPGA Version %08x, %d appliances, %d sensors' % (
         info.version, info.num_appliances, info.num_sensors))
        self.version = info.version
        self._num_appliances = info.num_appliances
        self._num_sensors = info.num_sensors

    def _query_devices(self) -> None:
        """
        Queries all devices from the FPGA. Device objects are created accordingly and stored inside the devices and
        inputs fields.
        """
        self.logger.info('Scanning for appliances...')
        self.appliances = {}
        try:
            for i in range(self._num_appliances):
                try:
                    dev_type = self.i2c.get_appliance_type(i).device_type
                    try:
                        self.appliances[i] = I2CAppliance.create(bridge=self, device_id=i, device_type=(I2CApplianceType(dev_type)))
                        self.logger.info('Device %02x is a %s' % (i, self.appliances[i]))
                        self.appliances[i].update_state(self.i2c.get_appliance_state(i).device_state)
                    except UnknownDeviceTypeError as e:
                        try:
                            self.logger.error(f"Couldn't set up device ID {i}: {e}")
                        finally:
                            e = None
                            del e

                except I2CNoSuchDeviceException as e:
                    try:
                        self.logger.info(f"Appliance ID {e.device_id} does not exist, skipping")
                        self.appliances[i] = None
                    finally:
                        e = None
                        del e

        except I2CException as e:
            try:
                self.logger.warn('I2C error while scanning for devices: %s' % e)
            finally:
                e = None
                del e

        else:
            self.logger.info('Found %d appliances' % sum((d is not None for d in self.appliances.values())))
            self.logger.info('Scanning for sensors...')
            self.sensors = {}
            try:
                for i in range(self._num_sensors):
                    try:
                        input_type = self.i2c.get_sensor_type(i).sensor_type
                        try:
                            self.sensors[i] = I2CSensor.create(bridge=self, sensor_id=i, sensor_type=(I2CSensorType(input_type)))
                        except UnknownDeviceTypeError as e:
                            try:
                                self.logger.info(f"Couldn't set up Input ID {i}: {e}")
                            finally:
                                e = None
                                del e

                    except I2CNoSuchDeviceException as e:
                        try:
                            self.logger.info(f"Sensor ID {e.device_id} does not exist, skipping")
                            self.sensors[i] = None
                        finally:
                            e = None
                            del e

            except I2CException as e:
                try:
                    self.logger.warn(f"I2C error while scanning for inputs: {e}")
                finally:
                    e = None
                    del e

            else:
                self.logger.info('Found %d sensors' % sum((d is not None for d in self.sensors.values())))

    def poll(self) -> None:
        """
        Performs a manual poll request on the FPGA. For any incoming events, the appropriate registered callback
        handlers are called.
        """
        for event in self.i2c.poll():
            try:
                if isinstance(event, I2CApplianceStateResponse):
                    try:
                        self.appliances[event.device_id].update_state(event.device_state)
                        for func in self.poll_update_callbacks.values():
                            func(self.appliances[event.device_id])

                    except (ValueError, InvalidStateError) as e:
                        try:
                            self.logger.warning(f"Malformed state update event data, ignoring: {e}")
                        finally:
                            e = None
                            del e

                else:
                    if isinstance(event, I2CInputEventResponse):
                        try:
                            self.sensors[event.sensor_id].on_input(event.sensor_data)
                        except ValueError as e:
                            try:
                                self.logger.warning(f"Malformed event data, ignoring: {e}")
                            finally:
                                e = None
                                del e

            except I2CException as e:
                try:
                    self.logger.error(f"Failed to forward event: {e}")
                finally:
                    e = None
                    del e

    def register_update(self):
        """
        Decorator that registers the following function as a global callback handler for State Update events.
        The callback function must take two parameters: the device that caused the event and the raw state data.
        :return: Decorator for function.
        """

        def decorator(function):

            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                return result

            self.poll_update_callbacks[function.__name__] = wrapper

        return decorator

    def start_polling(self, delay: float=0.5) -> None:
        """
        Starts automatic polling of the FPGA.
        :param delay: Polling frequency.
        """
        self.poll_delay = delay
        if self.is_polling:
            return
        self.logger.info('Starting auto-polling')
        self.is_polling = True

    def stop_polling(self) -> None:
        """
        Stops automatic polling of the FPGA.
        """
        if not self.is_polling:
            return
        self.logger.info('Stopping auto-polling')
        self.is_polling = False

    def _poll_loop(self) -> None:
        self.logger.info('Starting polling thread')
        try:
            while True:
                try:
                    if self.is_polling:
                        self.poll()
                    sleep(self.poll_delay)
                    self.poll_fail_delay = 1
                except I2CException as e:
                    try:
                        self.logger.warn(f"Communication failure: {e}")
                        self.logger.info(f"Attempting to resume polling in {self.poll_fail_delay}s")
                        sleep(self.poll_fail_delay)
                        self.poll_fail_delay = min(self.poll_fail_delay + 2, 30)
                    finally:
                        e = None
                        del e

        except (KeyboardInterrupt, SystemExit):
            self.logger.info('Polling thread: Received exit signal')
        else:
            self.logger.info('Closing polling thread')

    def reset(self) -> None:
        """
        Sends a reset signal to the FPGA.
        """
        was_polling = False
        if self.is_polling:
            was_polling = True
            self.stop_polling()
        self.i2c.reset_fpga()
        self._query_devices()
        if was_polling:
            self.start_polling()

    def send_state--- This code section failed: ---

 L. 233         0  SETUP_FINALLY        22  'to 22'

 L. 234         2  LOAD_FAST                'self'
                4  LOAD_ATTR                i2c
                6  LOAD_METHOD              set_appliance_state
                8  LOAD_FAST                'device_id'
               10  LOAD_FAST                'new_state'
               12  CALL_METHOD_2         2  ''
               14  POP_TOP          

 L. 235        16  POP_BLOCK        
               18  LOAD_CONST               True
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L. 236        22  DUP_TOP          
               24  LOAD_GLOBAL              I2CException
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    76  'to 76'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        64  'to 64'

 L. 237        38  LOAD_FAST                'self'
               40  LOAD_ATTR                logger
               42  LOAD_METHOD              warn
               44  LOAD_STR                 'Sending device state failed: %s'
               46  LOAD_FAST                'e'
               48  BINARY_MODULO    
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

 L. 238        54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         64  'to 64'
               60  LOAD_CONST               False
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM_FINALLY    36  '36'
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  END_FINALLY      
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            28  '28'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'

Parse error at or near `RETURN_VALUE' instruction at offset 20

    def __str__(self) -> str:
        return 'FPGA Bridge @ I2C Bus %d, Addr 0x%02x' % (self.bus, self.addr)