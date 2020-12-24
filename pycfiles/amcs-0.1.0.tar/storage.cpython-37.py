# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/storage.py
# Compiled at: 2020-01-12 12:29:08
# Size of source mod 2**32: 2410 bytes
import re
from .utils import to_unit, percent
_USED = '.UsedBytes'
_TOTAL = '.TotalBytes'

def _express_as(value, unit):
    try:
        return to_unit(value, unit)
    except (TypeError, ValueError):
        return (
         'unknown', unit)


class Storage(object):

    @property
    def storage_device_info(self):
        ret = self.command('storageDevice.cgi?action=getDeviceAllInfo')
        return ret.content.decode('utf-8')

    @property
    def storage_device_names(self):
        ret = self.command('storageDevice.cgi?action=factory.getCollect')
        return ret.content.decode('utf-8')

    def _get_storage_values(self, *params):
        info = self.storage_device_info
        ret = []
        for param in params:
            try:
                ret.append(re.search('.{}=([0-9.]+)'.format(param), info).group(1))
            except AttributeError:
                ret.append(None)

        if len(params) == 1:
            return ret[0]
        return ret

    @property
    def storage_used(self):
        return _express_as(self._get_storage_values(_USED), 'GB')

    @property
    def storage_total(self):
        return _express_as(self._get_storage_values(_TOTAL), 'GB')

    @property
    def storage_used_percent(self):
        used, total = self._get_storage_values(_USED, _TOTAL)
        try:
            return percent(used, total)
        except (TypeError, ValueError, ZeroDivisionError):
            return 'unknown'

    @property
    def storage_all(self):
        used, total = self._get_storage_values(_USED, _TOTAL)
        try:
            used_percent = percent(used, total)
        except (TypeError, ValueError, ZeroDivisionError):
            used_percent = 'unknown'

        return {'used_percent':used_percent, 
         'used':_express_as(used, 'GB'), 
         'total':_express_as(total, 'GB')}