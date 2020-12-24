# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/ublox_lara_r2/ublox_lara_r2.py
# Compiled at: 2018-06-21 23:09:48
import os, sys, thread, serial, time, RPi.GPIO as GPIO

class Ublox_lara_r2:

    def __init__(self, port='/dev/ttyAMA0', baudrate=115200):
        self.cmd_done = False
        self.power_pin = 29
        self.reset_pin = 31
        self.keep_receive_alive = True
        self.debug = True
        self.response = ''
        self.comm = serial.Serial(port, baudrate)

    def __del__(self):
        self.disabel_rtscts()
        self.cmd_done = True
        self.keep_receive_alive = False

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.setup(self.reset_pin, GPIO.OUT)
        GPIO.output(self.power_pin, False)
        GPIO.output(self.reset_pin, False)
        self.enable_rtscts()
        self.start_receive_handle()

    def enable_rtscts(self):
        os.system('rpirtscts on')
        if self.debug:
            print 'rts cts on'

    def disabel_rtscts(self):
        os.system('rpirtscts off')
        if self.debug:
            print 'rts cts off'

    def pwr_key_trigger(self):
        GPIO.output(self.power_pin, True)
        time.sleep(1.0)
        GPIO.output(self.power_pin, False)

    def handle_receive(self):
        while True == self.keep_receive_alive:
            if self.comm.readable():
                line = self.comm.readline()
                self.response += line
                if self.debug:
                    print '<' + line,

    def start_receive_handle(self):
        thread.start_new_thread(self.handle_receive, ())

    def send(self, cmd):
        self.response = ''
        self.comm.write(cmd)
        if self.debug:
            print '\r\n>' + cmd

    def sendAT(self, cmd, response=None, timeout=1):
        self.cmd_done = False
        self.response = ''
        attempts = timeout
        while not self.cmd_done and attempts >= 0:
            self.comm.write(cmd)
            if self.debug:
                print '\r\n>' + cmd,
            time.sleep(0.5)
            if None != response:
                if self.response.find(response) >= 0:
                    self.cmd_done = True
            elif None == response:
                self.cmd_done = True
            attempts = attempts - 1
            time.sleep(0.5)

        return attempts >= 0

    def getRSSI(self):
        rssi = ''
        self.sendAT('AT+CSQ\r\n', 'OK\r\n')
        if self.response != '':
            parts = self.response.split('\r\n')
            for part in parts:
                parse_index = part.find('+CSQ: ')
                if parse_index is not -1:
                    rssi = part[6:].split(',')[0]
                    break

        return rssi

    def reset_power(self):
        self.debug = False
        print 'waking up...',
        sys.stdout.flush()
        if not self.sendAT('AT\r\n', 'OK\r\n'):
            self.pwr_key_trigger()
            while not self.sendAT('AT\r\n', 'OK\r\n'):
                print '...',
                sys.stdout.flush()

            print '\r\n'
        self.debug = True