# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Bureau\educat_irsensor\irsensors\irsensors\irsensorset.py
# Compiled at: 2019-09-23 20:18:57
# Size of source mod 2**32: 9112 bytes
from time import sleep
from threading import Thread
from serial import Serial
from irsensors.irsensor import IRSensor

class IRSensorSet(Thread):
    __doc__ = 'This class represent the IR sensor set.\n\n\tThis class is a thread, it means that the run method will be executed in parallel to the main program as soon as the start method is call in the main program.\n\n\tAttributes:\n\t\tTHREAD_ATTRIBUTES is a tuple of attribute\'s name that need to be modifie for the thread to run well.\n\t\t_sensor is the serial connection USB with the physical sensor.\n\t\t_sensors is the list of IR sensor contents in the physical sensor.\n\t\t_listening is the control variable for knowing if the thread is launched or not.\n\n\t\tmain method :\n\t\t\tlisten(self) :\n\t\t\t\tThis method is call by the run method, itself called by the start method as explain before. The user needs to launche the start method to access sensor\'s data.\n\t\t\t\tThis method reads data from the physical sensor throught the _sensor attribute. After a little process on the data, give it to the right IRSensor in the attribute _sensors list.\n\n\t\tother methods :\n\t\t\t__len__(self): Give the number of sensor in the sensor set.\n\t\t\trun(self):\n\t\t\t\tThis method is executed in parallel to the main programm as soon as the main program call the start method.\n\t\t\t\tFirstly, check if the thread is not already launched, then update the _listening attribute, open the serial connection, write "1" for the physical sensor to start sending data and launche the listen method in a while loop as long as the _listening attribute is True.\n\t\t\t\tFinally, when the _listening attribute changes from True to False, stop to launche the listen method, write "0" for the physical sensor to stop sending data and close the serial connection USB.\n\t\t\tstop(self): Change the _listening attribute\'s value from True to False to stop the loop in the run method.\n\t\t\t__repr__(self): Return a str which indicates the class of the object and the value of his attributes.\n\t\t\t__str__(self): Return a str which indicates the distance of each IRSensor in the _sensor list, in the same order as their ID was given in the constructor.\n\n\t'
    THREAD_ATTRIBUTES = ('_target', '_name', '_args', '_kwargs', '_daemonic', '_ident',
                         '_tstate_lock', '_started', '_is_stopped', '_initialized',
                         '_stderr', '_verbose', '_stopped', '_block')

    def __init__(self, port, id_sensors=[
 0, 1, 2, 3], baud=9600, time_out=1, nb_values_history=10):
        """Constructor of the IRSensorSet class.

                Create the serial connection USB.
                Create the list of IRSensor.
                Set the _listening attribute to False.

                """
        Thread.__init__(self)
        object.__setattr__(self, '_sensor', Serial(port, baud,
          timeout=time_out))
        getattr(self, '_sensor').close()
        sensors = []
        for i in range(len(id_sensors)):
            sensors.append(IRSensor(id=(id_sensors[i]),
              nb_values=nb_values_history))

        object.__setattr__(self, '_sensors', sensors)
        object.__setattr__(self, '_listening', False)

    def __getattr__(self, attribute_name):
        """Raise an AttributeError when the user tries to access an attribute that does not exist."""
        raise AttributeError("'IRSensorSet' object has no attribute " + attribute_name)

    def __setattr__(self, attribute_name, attribute_value):
        """Apart from some attributes for the thread to run well, raise an TypeError when the user tries to modifie an attribute's value.

                The varaiables which names are in the THREAD_ATTRIBUTE tuple should not be modified by the outside.

                """
        if attribute_name in IRSensorSet.THREAD_ATTRIBUTES:
            object.__setattr__(self, attribute_name, attribute_value)
            return
        raise TypeError("'IRSensorSet' object does not support attribute assignment (attributeName -> " + attribute_name + ', attributeValue -> ' + str(attribute_value) + ')')

    def __delattr__(self, attribute_name):
        """Raise an TypeError when the user tries to delete an attribute."""
        raise TypeError("'IRSensorSet' object does not support attribute deletion (attributeName -> " + attribute_name + ')')

    def __getitem__(self, item_name):
        """aise an AttributeError when the user tries to access an attribute as item."""
        if item_name in ('sensor', 'sensors', 'listening'):
            raise TypeError("'IRSensorSet' object does not support item reading (attributeName -> " + item_name + ')')
        raise KeyError("'IRSensorSet' has no item " + item_name)

    def __setitem__(self, item_name, item_value):
        """Raise an TypeError when the user tries to modifie the value of an attribute as item."""
        raise TypeError("'IRSensorSet' object does not support item assignment (attributeName -> " + item_name + ', attributeValue -> ' + str(item_value) + ')')

    def __delitem__(self, item_name):
        """Raise an TypeError when the user tries to delete an attribute as items."""
        raise TypeError("'IRSensorSet' object does not support item deletion (attributeName -> " + item_name + ')')

    def __len__(self):
        """Return the lenght of the _sensors list.

                Give the number of sensors.

                """
        return len(getattr(self, '_sensors'))

    def run(self):
        """Launche the thread.

                If the thread is already running, do not do anything.
                If the thread is not already running, open the serial connection USB, write "1" for the physical sensor to start sending data and launche the listen method in a while loop as long as the _listening attribute is True.
                Finally, when the _listening attribute changes from True to False, stop to launche the listen method and stop the while loop, write "0" for the physical sensor to stop sending data and close the serial connection USB.

                """
        if not getattr(self, '_listening'):
            object.__setattr__(self, '_listening', True)
            serial_usb = getattr(self, '_sensor')
            serial_usb.open()
            serial_usb.write(b'1')
            while getattr(self, '_listening'):
                self.listen()

            serial_usb.write(b'0')
            serial_usb.close()

    def listen(self):
        r"""Main part of the thread : Read the data from USB connection and give it to the right sensor.

                Read one line of data from the physical sensor. The expected from of the line of data is b"ID,Error_Code,Distance,.........,
". What is between the third and the fourth comma does not matter.
                Decode, split and remove the 
 at the end of the data.
                Simplify the ID. /!\ As the simplification take on count only one digit, it will make some problems if the id is greater or equal to 10.
                Convert the error code from string to int.
                Convert the distance from string to float.
                Search the good IRSensor in the _sensor attribute list and give it data throught the write method.

                """
        data_tmp = getattr(self, '_sensor').readline()
        data_tmp = data_tmp.decode().split(',')[:-1]
        data_tmp[0] = int(data_tmp[0][(-1)])
        data_tmp[1] = int(data_tmp[1])
        data_tmp[2] = float(data_tmp[2])
        for sensor in getattr(self, '_sensors'):
            if sensor['ID'] == data_tmp[0]:
                sensor.write(id=(data_tmp[0]),
                  error=(data_tmp[1]),
                  distance=(data_tmp[2]))

    def stop(self):
        """Stop the thread."""
        if getattr(self, '_listening'):
            object.__setattr__(self, '_listening', False)

    def __repr__(self):
        """Return a str which indicates the class of the object and the value of his attributes."""
        serial_usb = getattr(self, '_sensor')
        return '<Class = IRSensorSet, port = ' + serial_usb.port + ', Baudrate = ' + str(serial_usb.baudrate) + ', TimeOut = ' + str(serial_usb.timeout) + ', NbSensors = ' + str(len(self)) + ', listening = ' + str(getattr(self, '_listening')) + '>'

    def __str__(self):
        """Return a str which contains the distance from each sensor.

                1 column = 1 sensor. Distance is in cm and the value can be up to 10m excluded.

                """
        str_data = ''
        for i in range(len(self)):
            distance = getattr(self, '_sensors')[i]['distance'] / 10
            str_data += '%5.1f' % distance + '\t'

        return str_data

    def __del__(self):
        """Destructor of the IRSensorSet class."""
        self.stop()


__all__ = [
 'IRSensorSet']
if __name__ == '__main__':
    test = IRSensorSet('COM22')
    try:
        try:
            test.start()
            print(repr(test), '\n', str(test), '\n')
            while True:
                print(test)
                sleep(0.1)

        except KeyboardInterrupt:
            pass

    finally:
        test.stop()
        del test