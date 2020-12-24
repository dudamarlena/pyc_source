# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/getRaumfeld.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import hashlib, socket, requests, json, sys, xml.etree.ElementTree as ET, subprocess
from time import sleep

class HostDevice:
    __raumfeld_host_device = None

    @staticmethod
    def set(ip):
        HostDevice.__raumfeld_host_device = RaumfeldDeviceSettings(ip)

    @staticmethod
    def get():
        return HostDevice.__raumfeld_host_device


class RaumfeldDeviceSettings:
    local_ip = b''

    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.model = b'unknown'
        self.modelName = b'unknown'
        self.modelNumber = b'unknown'
        self.modelImageURL = b'unknown'
        self.isAccessPoint = b'unknown'
        self.isSetupInProgress = b'unknown'
        self.deviceId = b'unknown'
        self.state = b'unknown'
        self.ssid = b'unknown'
        self.renderer_uuid = b'unknown'
        self.version = b'unknown'
        self.valid = False

    def set_verbose(self):
        self.verbose = True

    def retrieve_device_settings(self):
        self.get_local_ip_address()
        json_result = self.get_hostdata(b'device')
        if json_result is None:
            return
        else:
            print json_result.text
            self.valid = True
            try:
                json_dict = json.loads(json_result.text)
                self.model = json_dict[b'model']
                self.modelName = json_dict[b'modelName']
                self.modelNumber = json_dict[b'modelNumber']
                self.modelImageURL = json_dict[b'modelImageURL']
                self.isAccessPoint = json_dict[b'isAccessPoint']
                if b'isSetupInProgress' in json_dict:
                    self.isSetupInProgress = json_dict[b'isSetupInProgress']
                else:
                    self.isSetupInProgress = b'NA'
                headers = json_result.headers
                self.deviceId = headers[b'x-deviceid']
                result = self.get_hostdata(b'deviceConfiguration')
                if result is not None:
                    json_dict = json.loads(result.text)
                    if b'state' in json_dict:
                        self.state = json_dict[b'state']
                    else:
                        self.state = b'NA'
            except Exception as err:
                print (b'RaumfeldDeviceSettings.retrieve_device_settings Exception: {0}').format(err)
                return

            self.get_zones()
            self.get_media_servers()
            print self.get_info_str()
            return

    def get_info_str(self):
        res = b'Model:        ' + self.modelName
        res += b'\nDeviceId:     ' + self.deviceId
        res += b'\nState:        ' + self.state
        res += b'\n'
        return res

    def create_auth_key(self):
        hash = hashlib.sha256()
        hash.update(bytes(self.server_ip, b'UTF-8'))
        hash.update(b'$392G3hJ7Dl3qZ4')
        hash.update(bytes(self.local_ip, b'UTF-8'))
        hash_result = hash.hexdigest()
        return hash_result

    @staticmethod
    def get_local_ip_address():
        if RaumfeldDeviceSettings.local_ip != b'':
            return RaumfeldDeviceSettings.local_ip
        else:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                res = s.getsockname()[0]
                RaumfeldDeviceSettings.local_ip = res
                print b'Local IP address:' + res
                return res
            except Exception as err:
                print (b'Exception get_local_ip_address: {0}').format(err)
                return

            return

    @staticmethod
    def force_local_ip_address(ip):
        RaumfeldDeviceSettings.local_ip = ip

    def get_media_servers(self):
        try:
            requests.packages.urllib3.disable_warnings()
            url = b'http://' + self.server_ip + b':47365/getMediaServers'
            print url
            r = requests.get(url)
            root = ET.fromstring(r.content)
            for child in root:
                print (
                 b'+', child.tag, child.get(b'name'), child.get(b'udn'))

            return r
        except Exception as err:
            print (b'Exception get_media_servers: {0}').format(err)
            return

        return

    def create_zone_with_rooms(self, rooms):
        try:
            requests.packages.urllib3.disable_warnings()
            url = b'http://' + self.server_ip + b':47365/'
            if len(rooms) == 1:
                url += b'connectRoomToZone?'
                url += b'roomUDN='
                for item in rooms:
                    url += item
                    break

            else:
                url += b'connectRoomsToZone?'
                url += b'roomUDNs='
                for item in rooms:
                    url += item + b','

                url = url[:-1]
            r = requests.get(url)
            return r
        except Exception as err:
            print (b'Exception create_zone_with_rooms: {0}').format(err)
            return

        return

    def add_rooms_to_zone(self, zone_udn, rooms):
        try:
            requests.packages.urllib3.disable_warnings()
            url = b'http://' + self.server_ip + b':47365/connectRoomsToZone?'
            url += b'zoneUDN=' + zone_udn
            url += b'&roomUDNs='
            for item in rooms:
                url += item + b','

            url = url[:-1]
            print url
            r = requests.get(url)
            return r
        except Exception as err:
            print (b'Exception create_zone_with_rooms: {0}').format(err)

        return

    def set_room_standby(self, uuid, state):
        if state == b'on':
            cmd = b'enterManualStandby'
        else:
            if state == b'off':
                cmd = b'leaveStandby'
            elif state == b'auto':
                cmd = b'enterAutomaticStandby'
            else:
                raise b'standby with unknown state called (use on|off|auto)'
            try:
                requests.packages.urllib3.disable_warnings()
                url = b'http://' + self.server_ip + b':47365/' + cmd + b'?'
                url += b'&roomUDN=' + uuid
                r = requests.get(url)
                return r
            except Exception as err:
                print (b'Exception create_zone_with_rooms: {0}').format(err)

        return

    def drop_room(self, room_udn):
        try:
            requests.packages.urllib3.disable_warnings()
            url = b'http://' + self.server_ip + b':47365/dropRoomJob?'
            url += b'&roomUDN=' + room_udn
            r = requests.get(url)
            return r
        except Exception as err:
            print (b'Exception create_zone_with_rooms: {0}').format(err)
            return

        return

    def get_zones(self):
        try:
            requests.packages.urllib3.disable_warnings()
            url = b'http://' + self.server_ip + b':47365/getZones'
            print url
            r = requests.get(url)
            root = ET.fromstring(r.content)
            for atype in root.findall(b'zones'):
                for child in atype:
                    print (child.tag, child.get(b'udn'))
                    for room in child:
                        print (
                         b'+', room.tag, room.get(b'name'), room.get(b'udn'))
                        for renderer in room:
                            print (
                             b'  +', renderer.tag, renderer.get(b'name'), renderer.get(b'udn'))

            return r
        except Exception as err:
            print (b'Exception get_zones: {0}').format(err)
            return

        return

    def get_hostdata(self, what):
        try:
            requests.packages.urllib3.disable_warnings()
            headers = {b'Content-Type': b'application/json', b'X-AuthKey': self.create_auth_key()}
            url = b'https://' + self.server_ip + b':48366/raumfeldSetup/v1/' + what
            print url
            r = requests.get(url, headers=headers, verify=False)
            return r
        except Exception as err:
            print (b'Exception get_hostdata: {0}').format(err)
            return

        return

    def get_host_id(self):
        return self.host_id


if __name__ == b'__main__':
    if len(sys.argv) == 1:
        print b'usage: ' + sys.argv[0] + b' <raumfeld-device ip>'
        sys.exit(2)
    ds = RaumfeldDeviceSettings(sys.argv[1])
    ds.set_verbose()
    ds.retrieve_device_settings()