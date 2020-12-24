# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/backend/webcam.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 3895 bytes
import logging
from gi.repository import GObject, GUdev
logger = logging.getLogger('Webcam')

class Webcam(GObject.GObject):
    __doc__ = 'docstring for Webcam.'
    __gsignals__ = {'webcam-change': (GObject.SIGNAL_RUN_LAST,
                       None,
                       ())}

    def __init__(self):
        super(Webcam, self).__init__()
        self.device_list = {}
        self.has_webcam = False
        logger.debug('Initializing webcam support.')
        try:
            self.udev_client = GUdev.Client.new(subsystems=['video4linux'])
            self.udev_client.connect('uevent', self.watch)
        except:
            logger.warning('Unable to initialize webcam support.')

        self.detect()

    def watch(self, client, action, device):
        logger.debug('Webcam device list: {}'.format(self.device_list))
        logger.debug('Webcam change detected: {}'.format(action))
        if action == 'add':
            try:
                c_name = device.get_property('ID_V4L_PRODUCT')
                c_devname = device.get_property('DEVNAME')
                if (c_devname, c_name) not in self.device_list:
                    self.device_list.append((c_devname, c_name))
                    logger.debug('New webcam found: {}'.format(c_name))
                else:
                    logger.warning('Duplicate cam detected!? {} {}'.format(c_devname, c_name))
            except Exception as e:
                try:
                    logger.debug('Unable to register new webcam. {}'.format(e.str))
                finally:
                    e = None
                    del e

        else:
            if action == 'remove':
                try:
                    c_name = device.get_property('ID_V4L_PRODUCT')
                    c_devname = device.get_property('DEVNAME')
                    logger.debug('Removing webcam {}'.format(c_name))
                    for cam in self.device_list:
                        if c_devname == cam[0]:
                            self.device_list.remove(cam)
                            logger.debug('Removed webcam {}'.format(c_name))

                except Exception as e:
                    try:
                        logger.debug('Unable to de-register a webcam. {}'.format(e.str))
                    finally:
                        e = None
                        del e

            else:
                logger.debug('Unknown UDEV action {}.'.format(action))
        self.emit('webcam-change')

    def detect(self):
        self.device_list = []
        cams = self.udev_client.query_by_subsystem(subsystem='video4linux')
        if cams:
            for c in cams:
                c_name = c.get_property('ID_V4L_PRODUCT')
                c_devname = c.get_property('DEVNAME')
                logger.debug('  Webcam found: {0}'.format(c_name))
                self.device_list.append((c_devname, c_name))

        else:
            logger.info('Webcam not detected.')
        if self.device_list:
            self.has_webcam = True
        return self.device_list

    def get_device_file(self, num):
        try:
            return self.device_list[num][2]
        except:
            return