# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/devices.py
# Compiled at: 2016-06-13 14:11:03
"""
Devices interface.
"""
import urllib
from vsmclient import base

class Device(base.Resource):
    """A device is a disk on server for osd as data or journal."""

    def __repr__(self):
        return '<Device: %s>' % self.id


class DeviceManager(base.ManagerWithFind):
    """
    Manage :class:`Device` resources.
    """
    resource_class = Device

    def get(self, device_id):
        """
        Get a device.

        :param device_id: The ID of the device.
        :rtype: :class:`Device`
        """
        return self._get('/devices/%s' % device_id, 'device')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all devices.

        :rtype: list of :class:`Device`
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/devices%s%s' % (detail, query_string), 'devices')
        return ret

    def get_available_disks(self, search_opts=None):
        """
        Get a list of available disks
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        resp, body = self.api.client.get('/devices/get_available_disks%s' % query_string)
        body = body.get('available_disks')
        result_mode = search_opts.get('result_mode')
        if result_mode == 'get_disks':
            return {'disks': body}
        else:
            ret = {'ret': 1}
            message = []
            paths = search_opts.get('path')
            disks = []
            for disk in body:
                disk_name = disk.get('disk_name', '')
                by_path = disk.get('by_path', '')
                by_uuid = disk.get('by_uuid', '')
                if disk_name:
                    disks.append(disk_name)
                if by_path:
                    disks.append(by_path)
                if by_uuid:
                    disks.append(by_uuid)

            if paths:
                unaviable_paths = [ path for path in paths if path not in disks ]
                if unaviable_paths:
                    message.append('There is no %s ' % (',').join(unaviable_paths))
            if message:
                ret = {'ret': 0, 'message': ('.').join(message)}
            return ret

    def get_smart_info(self, search_opts=None):
        """
        Get a dict of smart info
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        resp, body = self.api.client.get('/devices/get_smart_info%s' % query_string)
        smart_info = body.get('smart_info')
        return smart_info