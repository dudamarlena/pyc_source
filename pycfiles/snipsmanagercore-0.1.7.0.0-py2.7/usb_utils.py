# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/usb_utils.py
# Compiled at: 2018-01-05 06:03:47
""" USB utilities. """
from __future__ import absolute_import
import os, re, subprocess, usb.core, usb.util

class USB:

    class Device:
        unknown, respeaker, conexant = range(3)

    @staticmethod
    def get_boards():
        try:
            all_devices = usb.core.find(find_all=True)
        except Exception as e:
            if str(e) != 'No backend available':
                raise
            return USB.Device.unknown

        if not all_devices:
            return USB.Device.unknown
        for board in all_devices:
            try:
                devices = board.product.lower()
                if devices.find('respeaker') >= 0:
                    return USB.Device.respeaker
                if devices.find('conexant') >= 0:
                    return USB.Device.conexant
            except Exception as e:
                continue

        return USB.Device.unknown

    @staticmethod
    def get_usb_led_device():
        devices = USB.lsusb()
        if not devices:
            return None
        else:
            devices = devices.lower()
            if devices.find('respeaker') >= 0:
                return USB.Device.respeaker
            if devices.find('conexant') >= 0:
                return USB.Device.conexant
            return USB.Device.unknown

    @staticmethod
    def lsusb():
        FNULL = open(os.devnull, 'w')
        try:
            return subprocess.check_output(['lsusb'])
        except:
            try:
                return subprocess.check_output(['system_profiler', 'SPUSBDataType'])
            except:
                return

        return