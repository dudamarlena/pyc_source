# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/raumfeldHandler.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import json, re, subprocess, sys, syslog
from pprint import pprint
from xml.dom import minidom
import hashlib
from pyfeld.renderer import Renderer
from pyfeld.discoverByHttp import DiscoverByHttp
from pyfeld.errorPrint import err_print
from pyfeld.getRaumfeld import RaumfeldDeviceSettings, HostDevice
from pyfeld.raumfeldZone import RaumfeldZone
from pyfeld.room import Room
from pyfeld.upnpCommand import UpnpCommand
from pyfeld.upnpService import UpnpService
from pyfeld.upnpsoap import UpnpSoap
from pyfeld.xmlHelper import XmlHelper
from pyfeld.settings import Settings

class MediaDevice():

    def __init__(self, udn, location, server_type, name=b''):
        self.udn = udn
        self.location = location
        self.type = server_type
        self.name = name


class RaumfeldHandler():
    active_zones = []
    new_zones = []
    media_servers = set()
    config_device = set()
    raumfeld_device = set()
    media_renderers = set()

    def __init__(self):
        self.events_count = 0
        self.verbose = False
        self.zone_hash = b''
        self.found_protocol_ip = None
        self.notify_callback = None
        return

    def set_notify_callback(self, cb):
        self.notify_callback = cb

    def set_active_zones(self, zones, zone_hash):
        RaumfeldHandler.active_zones = zones
        self.zone_hash = zone_hash
        self.__save_quick_access()

    def find_zone_for_room(self, room_name):
        index = 0
        try:
            for index in range(0, len(RaumfeldHandler.active_zones)):
                for room in RaumfeldHandler.active_zones[index].rooms:
                    if room.name == room_name:
                        return index

        except Exception as e:
            err_print((b'find_zone_for_room error: {0}').format(e))

        return index

    def get_request_zone(self, param_dictionary):
        if b'hasroom' in param_dictionary:
            return self.find_zone_for_room(param_dictionary[b'hasroom'][0])
        if b'room' in param_dictionary:
            return self.find_zone_for_room(param_dictionary[b'room'][0])
        if b'zoneindex' in param_dictionary:
            return int(param_dictionary[b'zoneindex'][0])
        err_print(b'error request zone')

    def set(self, cmd, param_dictionary):
        result = dict()
        try:
            index = self.get_request_zone(param_dictionary)
            print b'set ' + cmd
            print b'zone index:' + str(index)
            result[b'set'] = cmd
            result[b'zoneindex'] = str(index)
            if cmd == b'volume':
                RaumfeldHandler.active_zones[index].set_volume(param_dictionary[b'value'][0])
        except Exception as e:
            result[b'error'] = (b'set error {0}').format(e)
            err_print((b'set  error {0}').format(e))

        return result

    def get_last_media(self, param_dictionary):
        index = self.get_request_zone(param_dictionary)
        return RaumfeldHandler.active_zones[index].media

    def set_media(self, media, param_dictionary):
        index = self.get_request_zone(param_dictionary)
        RaumfeldHandler.active_zones[index].set_media(media)

    def get(self, cmd, param_dictionary):
        result = dict()
        try:
            index = self.get_request_zone(param_dictionary)
            result[b'get'] = cmd
            result[b'zoneindex'] = str(index)
            zone = RaumfeldHandler.active_zones[index]
            result[b'isplaying'] = zone.is_playing()
            if cmd == b'volume':
                zone.update_volumes()
                result[b'volume'] = str(zone.volume)
            if cmd == b'position':
                zone.update_position_info()
                result.update(zone.position)
            if cmd == b'media':
                zone.update_media()
                result.update(zone.media)
            if cmd == b'runstate':
                pass
        except Exception as e:
            result[b'error'] = (b'get error cmd={0} {1}').format(cmd, e)
            err_print((b'get error cmd={0} {1}').format(cmd, e))

        return result

    def do(self, cmd, param_dictionary):
        result = dict()
        try:
            index = self.get_request_zone(param_dictionary)
            print b'do ' + cmd
            print b'zone index:' + str(index)
            result[b'do'] = cmd
            result[b'zoneindex'] = str(index)
            if cmd == b'pause':
                RaumfeldHandler.active_zones[index].pause()
            elif cmd == b'stop':
                RaumfeldHandler.active_zones[index].stop()
            elif cmd == b'play':
                RaumfeldHandler.active_zones[index].play()
            elif cmd in ('prev', 'previous'):
                RaumfeldHandler.active_zones[index].previous()
            elif cmd == b'next':
                RaumfeldHandler.active_zones[index].next()
            elif cmd == b'seek':
                RaumfeldHandler.active_zones[index].seek(param_dictionary[b'value'][0])
            elif cmd == b'seekback':
                RaumfeldHandler.active_zones[index].seek_backward(10)
            elif cmd == b'seekfwd':
                RaumfeldHandler.active_zones[index].seek_forward(10)
            elif cmd == b'fade':
                RaumfeldHandler.active_zones[index].set_fade(param_dictionary[b'vs'][0], param_dictionary[b've'][0], param_dictionary[b't'][0])
            elif cmd == b'loop':
                RaumfeldHandler.active_zones[index].set_loop(param_dictionary[b'cuein'][0], param_dictionary[b'cueout'][0])
            elif cmd == b'stoploop':
                RaumfeldHandler.active_zones[index].terminate_loop = True
        except Exception as e:
            err_print((b'set action error {0}').format(e))

        return result

    def get_network_location_by_udn(self, udn, xmlListDevices):
        if udn is None:
            return
        else:
            devices = xmlListDevices.getElementsByTagName(b'device')
            try:
                for device in devices:
                    if device.getAttribute(b'udn') == udn:
                        location = device.getAttribute(b'location')
                        return location

            except Exception as e:
                err_print((b'Error in regex find:{0}').format(e))

            return

    def parse_other_devices_in_zone_raumfeld(self, xmlListDevices, zone_udn, zone):
        zone_obj = RaumfeldZone(zone_udn)
        rooms = zone.getElementsByTagName(b'room')
        for room in rooms:
            room_udn = room.getAttribute(b'udn')
            element = room.getElementsByTagName(b'renderer')
            for el in element:
                room_renderer_udn = el.getAttribute(b'udn')
                location = self.get_network_location_by_udn(room_renderer_udn, xmlListDevices)
                room_obj = Room(room_udn, room_renderer_udn, room.attributes[b'name'].value, location)
                room_obj.set_upnp_service(location)
                zone_obj.add_room(room_obj)

        zone_obj.set_soap_host(self.get_network_location_by_udn(zone_udn, xmlListDevices))
        return zone_obj

    def parse_rooms_in_zone_raumfeld(self, xmlListDevices, zone_udn, zone):
        zone_obj = RaumfeldZone(zone_udn)
        rooms = zone.getElementsByTagName(b'room')
        for room in rooms:
            room_udn = room.getAttribute(b'udn')
            element = room.getElementsByTagName(b'renderer')
            renderers = []
            for el in element:
                room_renderer_udn = el.getAttribute(b'udn')
                location = self.get_network_location_by_udn(room_renderer_udn, xmlListDevices)
                renderer = Renderer(room_renderer_udn, el.getAttribute(b'name'), location)
                RaumfeldHandler.renderers.append(renderer)
                renderers.append(renderer)

            room_obj = Room(room_udn, renderers, room.attributes[b'name'].value, location)
            room_obj.set_upnp_service(location)
            zone_obj.add_room(room_obj)

        zone_obj.set_soap_host(self.get_network_location_by_udn(zone_udn, xmlListDevices))
        return zone_obj

    def parse_devices_in_zone_raumfeld(self, xmlListDevices):
        RaumfeldHandler.media_servers = set()
        RaumfeldHandler.config_device = set()
        RaumfeldHandler.raumfeld_device = set()
        RaumfeldHandler.media_renderers = set()
        devices = xmlListDevices.getElementsByTagName(b'device')
        for device in devices:
            if device.getAttribute(b'type') == b'urn:schemas-upnp-org:device:MediaServer:1':
                if device.childNodes[0].nodeValue == b'Raumfeld MediaServer':
                    location = device.getAttribute(b'location')
                    udn = device.getAttribute(b'udn')
                    type = device.getAttribute(b'type')
                    host_path = re.match(b'(http://.*)/', location)
                    name = device.firstChild.nodeValue
                    if self.verbose:
                        print (
                         b'Media server: ', host_path.group(1))
                    found_device = MediaDevice(udn, host_path.group(1), type, name)
                    found_device.upnp_service = self.get_zone_services(xmlListDevices, udn)
                    RaumfeldHandler.media_servers.add(found_device)
            if device.getAttribute(b'type') == b'urn:schemas-raumfeld-com:device:ConfigDevice:1':
                if device.childNodes[0].nodeValue == b'Raumfeld ConfigDevice':
                    location = device.getAttribute(b'location')
                    udn = device.getAttribute(b'udn')
                    type = device.getAttribute(b'type')
                    host_path = re.match(b'(http://.*)/', location)
                    if self.verbose:
                        print (
                         b'Raumfeld ConfigDevice: ', host_path.group(1))
                    name = device.firstChild.nodeValue
                    found_device = MediaDevice(udn, host_path.group(1), type, name)
                    found_device.upnp_service = self.get_zone_services(xmlListDevices, udn)
                    RaumfeldHandler.config_device.add(found_device)
            if device.getAttribute(b'type') == b'urn:schemas-upnp-org:device:MediaRenderer:1':
                location = device.getAttribute(b'location')
                udn = device.getAttribute(b'udn')
                type = device.getAttribute(b'type')
                name = device.firstChild.nodeValue
                host_path = re.match(b'(http://.*)/', location)
                if self.verbose:
                    print (
                     b'Media renderer: ', host_path.group(1))
                found_device = MediaDevice(udn, host_path.group(1), type, name)
                found_device.upnp_service = self.get_zone_services(xmlListDevices, udn)
                RaumfeldHandler.media_renderers.add(found_device)
            if device.getAttribute(b'type') == b'urn:schemas-raumfeld-com:device:RaumfeldDevice:1':
                if b'Device' in device.childNodes[0].nodeValue:
                    location = device.getAttribute(b'location')
                    udn = device.getAttribute(b'udn')
                    type = device.getAttribute(b'type')
                    name = device.firstChild.nodeValue
                    host_path = re.match(b'(http://.*)/', location)
                    if self.verbose:
                        print (
                         b'Raumfeld Device: ', host_path.group(1))
                    found_device = MediaDevice(udn, host_path.group(1), type, name)
                    found_device.upnp_service = self.get_zone_services(xmlListDevices, udn)
                    RaumfeldHandler.raumfeld_device.add(found_device)

    def get_zone_services(self, xmlListDevices, udn):
        devices = xmlListDevices.getElementsByTagName(b'device')
        try:
            for device in devices:
                if device.getAttribute(b'udn') == udn:
                    location = device.getAttribute(b'location')
                    upnp_service = UpnpService()
                    upnp_service.set_location(location)
                    return upnp_service

        except Exception as e:
            err_print((b'Error in regex find:{0}').format(e))

        return

    def check_for_zone(self, ip):
        try:
            xml_headers, xml_data = UpnpSoap.get(ip + b':47365/getZones')
            xml_headers_devices, xml_data_devices = UpnpSoap.get(ip + b':47365/listDevices')
            if xml_data is not False:
                active_zones = []
                xml_root = minidom.parseString(xml_data)
                xml_root_devices = minidom.parseString(xml_data_devices)
                self.parse_devices_in_zone_raumfeld(xml_root_devices)
                zones = xml_root.getElementsByTagName(b'zone')
                RaumfeldHandler.renderers = list()
                for zone in zones:
                    try:
                        udn_id = zone.attributes[b'udn'].value
                        zone_obj = self.parse_rooms_in_zone_raumfeld(xml_root_devices, udn_id, zone)
                        zone_obj.services = self.get_zone_services(xml_root_devices, udn_id)
                        active_zones.append(zone_obj)
                    except Exception as e:
                        err_print((b'Warning: error on reading zone:{0}').format(e))

                try:
                    elements = xml_root.getElementsByTagName(b'unassignedRooms')
                    if len(elements) > 0:
                        unassigned = elements[0]
                        zone_obj = self.parse_rooms_in_zone_raumfeld(xml_root_devices, None, unassigned)
                        zone_obj.services = None
                        active_zones.append(zone_obj)
                except Exception as e:
                    err_print((b'Info: parsing unassignedRooms:{0}').format(e))

                return active_zones
            return
        except Exception as e:
            err_print((b'error on reading zones skipping:{0}').format(e))

        return

    @staticmethod
    def hash_zone(zones):
        zone_hash = []
        for zone in zones:
            zone_hash.append(zone.get_control_hash())

        zone_hash.sort()
        return hashlib.md5(str(zone_hash).encode()).hexdigest()

    def reprocess(self):
        try:
            if self.found_protocol_ip is None:
                self.found_protocol_ip = self.__get_host_ip_from_local()
            HostDevice.set(self.found_protocol_ip)
            if self.found_protocol_ip is not None:
                zones = self.check_for_zone(b'http://' + self.found_protocol_ip)
                current_zone_hash = RaumfeldHandler.hash_zone(zones)
                if current_zone_hash != self.zone_hash:
                    HostDevice.set(self.found_protocol_ip)
                    self.set_active_zones(zones, current_zone_hash)
                return True
        except Exception as e:
            err_print(b'reprocess: ' + str(e))

        return False

    def process_batch(self, lines, with_protocol):
        try:
            if with_protocol:
                manyips = re.findall(b'(https?://.*):', lines.decode(b'UTF-8'))
            else:
                manyips = re.findall(b'([0-9]+[.][0-9]+[.][0-9]+[.][0-9]+)', lines.decode(b'UTF-8'))
            new_zones = []
            ips = set(manyips)
            for ip in ips:
                protocol_ip = ip
                if not with_protocol:
                    protocol_ip = b'http://' + ip
                zones = self.check_for_zone(protocol_ip)
                if zones is not None:
                    self.found_protocol_ip = ip
                    new_zones.extend(zones)

            zone_hash = RaumfeldHandler.hash_zone(self.active_zones)
            self.set_active_zones(new_zones, zone_hash)
        except Exception as e:
            err_print(b'process_batch: command failed:' + str(e))

        return

    def search_gssdp_service(self, service):
        if self.verbose:
            print b'searching'
        command = b'gssdp-discover -n 3 | grep -A 1 ' + service
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            print b'search_gssdp_service: command failed:' + str(e)
            syslog.syslog(b'command failed:' + str(e))

        lines = b''
        while True:
            nextline = process.stdout.readline()
            if len(nextline) == 0 and process.poll() != None:
                break
            lines += nextline

        self.process_batch(lines, True)
        exitCode = process.returncode
        if self.verbose:
            print b'searching done'
        return exitCode

    def nmap_fallback(self):
        db = DiscoverByHttp()
        self.found_protocol_ip = db.found_IP()
        if self.found_protocol_ip is None:
            print b'No host found: switched on? available in raumfeld app? Crashed?'
            exit(1)
        self.reprocess()
        return

    def search_nmap_range(self, iprange):
        lines = self.nmap_fallback()
        if lines is not None:
            self.process_batch(lines, False)
        return 0

    def play_zone(self, name):
        for zone in self.active_zones:
            try:
                if zone.udn:
                    if zone.udn == name:
                        zone.play()
                        return
            except Exception as e:
                err_print(b'Error: command failed:' + str(e))

    def publish_state(self):
        string_state = self.get_state()
        print str(string_state.encode(b'utf-8'))

    def get_active_zones(self):
        return RaumfeldHandler.active_zones

    def get_zones_as_dict(self, verbosity=1):
        values = []
        index = 0
        for zone in RaumfeldHandler.active_zones:
            zone_dict = dict()
            try:
                if zone.udn:
                    zone.get_zone_stuff()
                if verbosity == 1:
                    zone_dict[b'index'] = str(index)
                zone_dict[b'media'] = zone.media
                zone_dict[b'host'] = str(zone.soap_host)
                zone_dict[b'name'] = zone.get_friendly_name()
                room_list = []
                for room in zone.rooms:
                    room_list.append([room.get_name(), room.get_udn()])

                room_list.sort()
                zone_dict[b'rooms'] = room_list
                zone_dict[b'udn'] = str(zone.udn)
                zone_dict[b'position'] = zone.position
                zone_dict[b'transport'] = zone.transport
                zone_dict[b'volume'] = zone.volume
                index += 1
            except Exception as e:
                pass

            values.append(zone_dict)

        values.sort(key=lambda k: k[b'name'])
        return values

    def get_all_rooms(self):
        room_list = dict()
        for zone in RaumfeldHandler.active_zones:
            try:
                for room in zone.rooms:
                    room_list.append({b'zone': zone.udn, b'room': room})

            except Exception as e:
                pass

        return room_list

    def get_current_media(self, param_dictionary):
        try:
            index = self.get_request_zone(param_dictionary)
            RaumfeldHandler.active_zones[index].update_media()
            return RaumfeldHandler.active_zones[index].media
        except Exception as e:
            err_print((b'error get_current_media {0}').format(e))

    def get_state(self):
        resstr = b'current state'
        try:
            zones = self.get_zones_as_dict(1)
            for zone in zones:
                try:
                    resstr += b'\nZone #' + zone[b'index'] + b': ' + zone[b'name']
                    resstr += b'\n      udn = ' + zone[b'udn']
                    resstr += b'\n     host = ' + zone[b'host']
                    resstr += b'\n  Room(s) : '
                    for room in zone[b'rooms']:
                        resstr += b'\n          '
                        resstr += room[0]
                        resstr += b':' + room[1]

                    resstr += b'\n   Volume = ' + str(zone[b'volume'])
                except Exception as e:
                    resstr += b'\nError: command failed:' + str(e)

                resstr += b'\n'

            for item in RaumfeldHandler.media_servers:
                resstr += b'Mediaserver = ' + str(item.location) + b'\n'

            resstr += b'zone hash:' + self.zone_hash + b'\n'
            return resstr
        except Exception as e:
            err_print((b'get_state error {0}').format(e))

        return resstr

    def find_udn(self, udn):
        for zone in self.get_active_zones():
            try:
                if zone.udn == udn:
                    result_list = dict({b'type': b'zone', b'obj': zone})
                    return result_list
                for room in zone.rooms:
                    for renderer in room.get_renderer_list():
                        if renderer.get_udn() == udn:
                            result_list = dict({b'type': b'room_renderer', b'obj': room})
                            return result_list
                        if room.get_udn() == udn:
                            result_list = dict({b'type': b'room', b'obj': room})
                            return result_list

            except:
                pass

        return

    def set_subscription_values(self, udn, xml_lastchange):
        state_var_items = XmlHelper.xml_extract_dict_by_val(xml_lastchange, [
         b'TransportState',
         b'AVTransportURIMetaData',
         b'AVTransportURI',
         b'CurrentPlayMode',
         b'CurrentTransportActions',
         b'CurrentTrack',
         b'CurrentTrackURI',
         b'CurrentTrackMetaData',
         b'CurrentTrackDuration',
         b'TransportStatus',
         b'TransportState',
         b'Mute',
         b'Volume'])
        if len(state_var_items):
            result = self.find_udn(udn)
            if result[b'type'] in ('room', 'room_renderer', 'zone'):
                result[b'obj'].set_event_update(udn, state_var_items)
            self.events_count += 1
            if self.notify_callback is not None:
                self.notify_callback(self)
        return

    def browse_media(self, path):
        for server in self.media_servers:
            try:
                uc = UpnpCommand(server.location)
                res = uc.browsechildren(path)
                if res is None:
                    pass
                else:
                    return res
            except:
                pass

        return

    def browse_info(self, path):
        for server in self.media_servers:
            uc = UpnpCommand(server.location)
            return uc.browse(path)

    def __save_quick_access(self):
        values = dict()
        media_server_list = list()
        device_list = list()
        for renderer in self.renderers:
            device_dict = dict()
            try:
                device_dict[b'udn'] = str(renderer.udn)
                device_dict[b'location'] = str(renderer.location)
                device_dict[b'name'] = str(renderer.name)
            except Exception as e:
                pass

            device_list.append(device_dict)

        values[b'renderer'] = device_list
        device_list = list()
        for renderer in self.media_renderers:
            device_dict = dict()
            try:
                device_dict[b'udn'] = str(renderer.udn)
                device_dict[b'location'] = str(renderer.location)
                device_dict[b'type'] = str(renderer.type)
                device_dict[b'name'] = str(renderer.name)
            except Exception as e:
                pass

            device_list.append(device_dict)

        values[b'mediarenderer'] = device_list
        configdevice_list = list()
        for config_device in self.config_device:
            device_dict = dict()
            try:
                device_dict[b'udn'] = str(config_device.udn)
                device_dict[b'location'] = str(config_device.location)
                device_dict[b'type'] = str(config_device.type)
                device_dict[b'name'] = str(config_device.name)
            except Exception as e:
                pass

            configdevice_list.append(device_dict)

        values[b'configdevice'] = configdevice_list
        for server in self.media_servers:
            mserver_dict = dict()
            mserver_dict[b'udn'] = server.udn
            mserver_dict[b'type'] = server.type
            mserver_dict[b'location'] = server.location
            mserver_dict[b'services'] = server.upnp_service.services_list
            mserver_dict[b'name'] = str(server.name)
            media_server_list.append(mserver_dict)

        values[b'mediaserver'] = media_server_list
        values[b'host'] = str(self.found_protocol_ip)
        zone_list = list()
        for zone in RaumfeldHandler.active_zones:
            zone_dict = dict()
            try:
                zone_dict[b'host'] = str(zone.soap_host)
                zone_dict[b'name'] = zone.get_friendly_name()
                try:
                    zone_dict[b'services'] = zone.services.services_list
                except Exception as e:
                    pass

                room_list = []
                for room in zone.rooms:
                    room_config = dict()
                    room_config[b'name'] = room.get_name()
                    room_config[b'location'] = room.get_location()
                    room_config[b'udn'] = room.get_udn()
                    room_renderer = []
                    for renderer in room.get_renderer_list():
                        renderer_dict = dict()
                        renderer_dict[b'name'] = renderer.get_name()
                        renderer_dict[b'location'] = renderer.get_location()
                        renderer_dict[b'udn'] = renderer.get_udn()
                        room_renderer.append(renderer_dict)

                    room_config[b'room_renderers'] = room_renderer
                    room_list.append(room_config)

                zone_dict[b'rooms'] = room_list
                zone_dict[b'udn'] = str(zone.udn)
            except Exception as e:
                print (b'Error creating quickaccess object: {0}').format(e)

            zone_list.append(zone_dict)

        values[b'zones'] = zone_list
        device_list = list()
        for device in RaumfeldHandler.raumfeld_device:
            device_dict = dict()
            try:
                device_dict[b'udn'] = str(device.udn)
                device_dict[b'location'] = str(device.location)
                device_dict[b'type'] = str(device.type)
                device_dict[b'name'] = str(device.name)
            except Exception as e:
                pass

            device_list.append(device_dict)

        values[b'devices'] = device_list
        with open(Settings.home_directory() + b'/data.json', b'w') as (f):
            json.dump(values, f, ensure_ascii=True, sort_keys=True, indent=4)

    @staticmethod
    def __get_host_ip_from_local():
        try:
            s = open(Settings.home_directory() + b'/data.json', b'r').read()
            quick_access = json.loads(s)
            return quick_access[b'host']
        except Exception as err:
            err_print((b'get_host_ip_from_local error: {0}').format(err))

        return


def main(argv):
    if len(sys.argv) < 2:
        err_print(b'missing ip')
        sys.exit(2)
    host = sys.argv[1]
    zone = RaumfeldHandler()
    zone.process_batch(bytearray(host, b'UTF-8'), False)
    print zone.get_state()


if __name__ == b'__main__':
    main(sys.argv)