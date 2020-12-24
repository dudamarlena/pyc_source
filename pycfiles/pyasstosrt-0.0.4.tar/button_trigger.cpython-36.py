# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/trigger/button_trigger.py
# Compiled at: 2018-01-07 13:01:17
# Size of source mod 2**32: 877 bytes
import os, subprocess, RPi.GPIO as GPIO, time, logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')

class ButtonTrigger:

    def __init__(self, trigger_pin):
        self.trigger_pin = trigger_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((self.trigger_pin), (GPIO.IN), pull_up_down=(GPIO.PUD_DOWN))
        self.trigger_event = False

    def __on_event(self, arg):
        self.trigger_event = True

    def start(self, stop_callback):
        logger.info('waiting for GPIO %d rising...' % self.trigger_pin)
        GPIO.add_event_detect(self.trigger_pin, GPIO.RISING, self._ButtonTrigger__on_event)
        while stop_callback():
            if self.trigger_event:
                break
            time.sleep(0.1)

        GPIO.remove_event_detect(self.trigger_pin)
        GPIO.cleanup(self.trigger_pin)
        return self.trigger_event