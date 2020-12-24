# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/SRMspinanalysis/get_data.py
# Compiled at: 2018-05-29 14:01:25
from bs4 import BeautifulSoup
import urllib2, numpy as np, re

class SolidRocketMotor(object):
    """Solid rocket motors use solid propllant to produce thrust.

    Attributes
    ----------
    motor_name : Name of motor
    motor_diameter : Diameter of motor [mm]
    motor_length : Length of motor [mm]
    motor_delays : Delays of motor
    motor_propellant_weight : Mass of propellant [kg]
    motor_total_weight : Mass of propellant and casing [kg]
    motor_manufacturer : Manufacturer of the motor
    motor_time_data : Time vector for thrust curve [s]
    motor_thrust_data : Thrust vector time profile [N]
    motor_number_of_grains : Number of propllant grains in motor
    
    """

    def __init__(self, url):
        """Initializes the solid rocket motor with information from a desired
        thrustcurve.org url.
        """
        motor_header_line, motor_time_data, motor_thrust_data = extract_RASP_data(url)
        self.motor_name = motor_header_line[0]
        self.motor_diameter = motor_header_line[1]
        self.motor_length = motor_header_line[2]
        self.motor_delays = motor_header_line[3]
        self.motor_propellant_weight = motor_header_line[4]
        self.motor_total_weight = motor_header_line[5]
        self.motor_manufacturer = motor_header_line[6]
        self.motor_time_data = motor_time_data
        self.motor_thrust_data = motor_thrust_data
        self.motor_number_of_grains = 1.0

    def add_delay(self, delay):
        """ Adds a time delay for ignition for a solid rocket motor. Time delay is in seconds.
        """
        self.motor_time_data += delay

    def compute_thrust_per_grain(self):
        """ Computes the thrust per grain. This is used for motors that are
            manufactured as multiple grains. Assign SolidRocketMotor.motor_number_of_grains
            a value before using this function.
        """
        return self.motor_thrust_data / self.motor_number_of_grains


def extract_RASP_data(url):
    """Provide this function with a RASP engine url from thrustcurve.org to
    retrieve thrust data and other important motor information via
    html parsing using BeautifulSoup.
    
    Args:
        url (str): URL from thrustcurve.org containing RASP engine data.

    Returns:
        motor_header_line (list): List of strings containing motor information.
        motor_time_data (np.array()): Time vector for thrust data.
        motor_thrust_data (np.array()): Thrust time profile for a particular motor.

    """
    response = urllib2.urlopen(url)
    raw_html = response.read()
    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    RASP_raw_data = ('').join(parsed_html.find('textarea').get_text()).split('\n')
    RASP_raw_data = [ re.sub('\r', '', line) for line in RASP_raw_data ]
    RASP_raw_data = [ line.lstrip() for line in RASP_raw_data ]
    RASP_raw_data = [ re.sub(' +', ' ', line) for line in RASP_raw_data ]
    RASP_raw_data = [ line for line in RASP_raw_data if not is_comment(line) ]
    if RASP_raw_data[(-1)] == '':
        RASP_raw_data = RASP_raw_data[:-1]
    motor_header_line = RASP_raw_data[0].split(' ')
    RASP_raw_thrust_time_data = [ line.split(' ') for line in RASP_raw_data[1:] ]
    motor_time_data = np.zeros(len(RASP_raw_thrust_time_data) + 1)
    motor_thrust_data = np.zeros(len(RASP_raw_thrust_time_data) + 1)
    for index, data_point in enumerate(RASP_raw_thrust_time_data, 1):
        motor_time_data[index] = float(data_point[0])
        motor_thrust_data[index] = float(data_point[1])

    return (
     motor_header_line, motor_time_data, motor_thrust_data)


def is_comment(line):
    """This function simply checks to see if a line in a RASP file is a comment. 
    Comments begin with a ';' character.

    Args:
        line (str): Line from html text.

    Returns:
        bool: Whether or not a line is a comment.

    """
    return line.startswith(';')