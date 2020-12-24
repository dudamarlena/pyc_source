# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Programming/python/joy2mouse/joy2mouselib/__init__.py
# Compiled at: 2011-06-08 13:58:03
import joystick, mouse, keyboard, profiles, mousethread, sys, gobject
__NAME__ = 'joy2mouse'
__VERSION__ = 0.1
__AUTHOR__ = 'Daniel Nögel'

class App(object):

    def __init__(self, options):
        self.device = profiles.config.config.get('device', '/dev/input/js0')
        self.divisor = float(profiles.config.config.get('divisor', 20000))
        self.pointermode = profiles.config.config.get('pointermode', 'True').lower().strip().startswith('t')
        if options.profile:
            self.read_profiles(options.profile)
        else:
            print 'No profile selected'
            print 'use -p to select one from .joy2mouse'
            print
            self.default_profile()
        self.mouse = mouse.Mouse()
        self.keyboard = keyboard.Keyboard()
        self.joystick = joystick.Joystick(self.device)
        self.mousethread = mousethread.MouseThread(self.pointermode)
        self.mousethread.start()
        if self.watch_axis:
            self.joystick.connect('axis', self.axis_event)
        if self.mappings != {}:
            self.joystick.connect('button', self.button_event)

    def default_profile(self):
        self.mappings = {}
        self.watch_axis = [ i for i in range(0, 6) ]
        for i in range(0, 5):
            self.mappings[i] = (
             'mouse', i + 1)

    def read_profiles(self, profile):
        config = profiles.config.config
        if profile not in config:
            print ("ERROR: Profile '{0}' not found").format(profile)
            sys.exit(1)
        self.device = config[profile].get('device', self.device)
        self.divisor = float(config[profile].get('divisor', self.divisor))
        self.pointermode = config[profile].get('pointermode', str(self.pointermode)).lower().strip().startswith('t')
        if 'axis' in config[profile]:
            self.watch_axis = [ int(i) for i in config[profile]['axis'].strip().split() ]
        else:
            self.watch_axis = None
        self.mappings = {}
        for i in range(0, 100):
            if str(i) in config[profile]:
                if 'mouse' in config[profile][str(i)].strip():
                    self.mappings[i] = (
                     'mouse', int(config[profile][str(i)].replace('mouse', '').strip()))
                else:
                    self.mappings[i] = (
                     'key', config[profile][str(i)].strip())

        print self.mappings
        return

    def button_event(self, signal, number, value, init):
        if init:
            return
        if number not in self.mappings:
            return
        mode = self.mappings[number][0]
        if mode == 'mouse':
            if value == 1:
                self.mouse.press(self.mappings[number][1])
            elif value == 0:
                self.mouse.release(self.mappings[number][1])
        elif value == 1:
            self.keyboard.press_key(self.mappings[number][1])
        elif value == 0:
            self.keyboard.release_key(self.mappings[number][1])

    def axis_event(self, signal, number, value, init):
        if init:
            return
        if number not in self.watch_axis:
            return
        if number % 2 == 0 and value != 0:
            self.mousethread.x = value / self.divisor
        elif number % 2 != 0 and value != 0:
            self.mousethread.y = value / self.divisor
        elif number % 2 == 0 and value == 0:
            self.mousethread.x = 0
        elif number % 2 != 0 and value == 0:
            self.mousethread.y = 0