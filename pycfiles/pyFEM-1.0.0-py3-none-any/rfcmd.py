# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyfeld/rfcmd.py
# Compiled at: 2018-03-27 07:51:39
from __future__ import unicode_literals
version = b'0.9.29'
import json, subprocess, sys, urllib, urllib3
try:
    from texttable import Texttable
except:
    pass

from requests.utils import quote
from time import sleep
from pyfeld.settings import Settings
from pyfeld.upnpCommand import UpnpCommand
from pyfeld.getRaumfeld import RaumfeldDeviceSettings
from pyfeld.raumfeldHandler import RaumfeldHandler
from pyfeld.didlInfo import DidlInfo

class InfoList():

    def __init__(self, sortItem, others):
        self.sortItem = sortItem
        self.others = others

    def get_list(self):
        return self.sortItem + self.others


class RfCmd():
    rfConfig = dict()
    raumfeld_host_device = None

    @staticmethod
    def get_raumfeld_infrastructure():
        try:
            s = open(Settings.home_directory() + b'/data.json', b'r').read()
            RfCmd.rfConfig = json.loads(s)
            for zone in RfCmd.rfConfig[b'zones']:
                if b'rooms' not in zone:
                    zone[b'rooms'] = None
                if b'udn' not in zone:
                    zone[b'udn'] = None

            RfCmd.raumfeld_host_device = RaumfeldDeviceSettings(RfCmd.rfConfig[b'host'])
        except Exception as err:
            print (b'get_raumfeld_infrastructure: Exception: {0}').format(err)
            return

        return

    @staticmethod
    def get_renderer_udn(renderer_name):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                for room in zone[b'rooms']:
                    for renderer in room[b'room_renderers']:
                        if renderer[b'name'] == renderer_name:
                            return renderer[b'udn']

        return

    @staticmethod
    def get_udn_from_renderer_by_room(room_name):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                for room in zone[b'rooms']:
                    if room[b'name'] == room_name:
                        for renderer in room[b'room_renderers']:
                            return renderer[b'udn']

        return

    @staticmethod
    def get_room_udn(room_name):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                for room in zone[b'rooms']:
                    if room[b'name'] == room_name:
                        return room[b'udn']

        return

    @staticmethod
    def get_room_zone_index(room_name):
        index = 0
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                for room in zone[b'rooms']:
                    if room[b'name'] == room_name:
                        return index

            index += 1

        return -1

    @staticmethod
    def build_dlna_play_container(udn, server_type, path):
        s = b'dlna-playcontainer://' + quote(udn)
        s += b'?'
        s += b'sid=' + quote(server_type)
        s += b'&cid=' + quote(path)
        s += b'&md=0'
        return s

    @staticmethod
    def build_dlna_play_single(udn, server_type, path):
        s = b'dlna-playsingle://' + quote(udn)
        s += b'?'
        s += b'sid=' + quote(server_type)
        s += b'&iid=' + quote(path)
        return s

    @staticmethod
    def is_unassigned_room(roomName):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                if zone[b'name'] == b'unassigned room':
                    for room in zone[b'rooms']:
                        if roomName == room[b'name']:
                            return True

        return False

    @staticmethod
    def get_unassigned_rooms(verbose, format):
        result = b''
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                if zone[b'name'] == b'unassigned room':
                    for room in zone[b'rooms']:
                        result += room[b'name'] + b'\n'

        return result

    @staticmethod
    def get_renderer(verbose, format):
        result = b''
        for renderer in RfCmd.rfConfig[b'renderer']:
            if verbose == 2:
                result += renderer[b'location'] + b'\t'
            if verbose == 1:
                result += RfCmd.get_pure_ip(renderer[b'location']) + b'\t'
            result += renderer[b'name'] + b'\n'

        return result

    @staticmethod
    def get_pure_ip(url):
        loc = urllib3.util.parse_url(url)
        return loc.hostname

    @staticmethod
    def map_ip_to_friendly_name(ip):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                for room in zone[b'rooms']:
                    if RfCmd.get_pure_ip(room[b'location']) == ip:
                        return room[b'name']
                    for renderer in room[b'room_renderers']:
                        if RfCmd.get_pure_ip(renderer[b'location']) == ip:
                            return renderer[b'name']

        return

    @staticmethod
    def map_udn_to_friendly_name(udn):
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                if zone[b'udn'] == udn:
                    return [b'Zone', zone[b'name']]
                for room in zone[b'rooms']:
                    if room[b'udn'] == udn:
                        return [b'Room', room[b'name']]
                    for renderer in room[b'room_renderers']:
                        if renderer[b'udn'] == udn:
                            return [b'Renderer', renderer[b'name']]

        return

    @staticmethod
    def get_device_name_by_ip(ip):
        for device in RfCmd.rfConfig[b'renderer']:
            ip_l = urllib3.util.parse_url(device[b'location'])
            if ip == ip_l.host:
                return device[b'name']

        return b'N/A'

    @staticmethod
    def get_device_ips(verbose, format):
        result = b''
        ip_list = []
        host_is_set = False
        for device in RfCmd.rfConfig[b'devices']:
            ip_l = urllib3.util.parse_url(device[b'location'])
            if ip_l.host == RfCmd.rfConfig[b'host']:
                ip_list.append(InfoList(ip_l.host, str(RfCmd.map_ip_to_friendly_name(ip_l.host)) + b' <host>'))
                host_is_set = True
            else:
                ip_list.append(InfoList(ip_l.host, str(RfCmd.map_ip_to_friendly_name(ip_l.host))))

        if not host_is_set:
            ip_list.append(InfoList(RfCmd.rfConfig[b'host'], b'<host>'))
        ip_list.sort(key=lambda x: x.sortItem, reverse=False)
        if format == b'json':
            return json.dumps(ip_list) + b'\n'
        f_list = []
        for ip in ip_list:
            if ip.sortItem not in f_list:
                f_list.append(ip.sortItem)

        if format == b'list':
            return f_list
        if verbose:
            for item in ip_list:
                result += item.sortItem + b'\t' + item.others + b'\n'

        else:
            for ip in f_list:
                result += ip + b'\n'

        return result

    @staticmethod
    def get_device_location_by_udn(udn):
        for zone in RfCmd.rfConfig[b'zones']:
            for room in zone[b'rooms']:
                for renderer in room[b'room_renderers']:
                    if renderer[b'udn'] == udn:
                        loc = urllib3.util.parse_url(renderer[b'location'])
                        return loc.netloc

                if room is not None:
                    if room[b'udn'] == udn:
                        loc = urllib3.util.parse_url(room[b'location'])
                        return loc.netloc

        return

    @staticmethod
    def get_rooms(verbose, format):
        result = b''
        room_list = []
        for zone in RfCmd.rfConfig[b'zones']:
            for room in zone[b'rooms']:
                if room is not None:
                    room_name = room[b'name']
                    if verbose:
                        room_name += b':' + room[b'location']
                    room_list.append(room_name)

        room_list.sort()
        if format == b'json':
            result += b'['
            cnt = 0
            for r in room_list:
                result += b'"' + r + b'",'
                cnt += 1

            if cnt != 0:
                result = result[:-1] + b']\n'
            else:
                result = b'[]\n'
        else:
            if format == b'dict':
                return room_list
            for r in room_list:
                result += r + b'\n'

        return result

    @staticmethod
    def get_didl_extract(didl_result, format=b'plain'):
        didlinfo = DidlInfo(didl_result, True)
        items = didlinfo.get_items()
        if format == b'json':
            return json.dumps(items, sort_keys=True, indent=2)
        if format == b'dict':
            return items
        result = b''
        result += items[b'artist'] + b'\n'
        result += items[b'title'] + b'\n'
        result += items[b'album'] + b'\n'
        result += items[b'resSampleFrequency'] + b'\n'
        result += items[b'resSourceType'] + b'\n'
        result += items[b'resBitrate'] + b'\n'
        result += items[b'rfsourceID'] + b'\n'
        return result

    @staticmethod
    def get_room_info(uc, udn):
        result = uc.get_room_volume(udn)

    @staticmethod
    def get_specific_zoneinfo(uc, format):
        results = uc.get_position_info()
        if format == b'json':
            result = b'{ "AbsTime" : '
            if b'AbsTime' in results:
                result += b'"' + results[b'AbsTime'] + b'",\n'
            else:
                result += b'"",\n'
            result += b'"TrackDuration" : '
            if b'TrackDuration' in results:
                result += b'"' + results[b'TrackDuration'] + b'",\n'
            else:
                result += b'"",\n'
            result += b'"TrackMetaData" : '
            if b'TrackMetaData' in results:
                result += RfCmd.get_didl_extract(results[b'TrackMetaData'], format)
            result += b'}'
            return result
        else:
            result = b''
            if b'AbsTime' in results:
                result += results[b'AbsTime'] + b'\n'
            else:
                result += b'\n'
            if b'TrackDuration' in results:
                result += results[b'TrackDuration'] + b'\n'
            else:
                result += b'\n'
            if b'TrackMetaData' in results:
                result += RfCmd.get_didl_extract(results[b'TrackMetaData'])
            return result

    @staticmethod
    def get_info(verbose, format, zero_index=True):
        if format == b'json':
            return json.dumps(RfCmd.rfConfig, sort_keys=True, indent=2) + b'\n'
        else:
            if format == b'text':
                i = 0
                if not zero_index:
                    i += 1
                result = b''
                for zone in RfCmd.rfConfig[b'zones']:
                    result += (b'Zone #{0}: {1}; ').format(i, zone[b'name'])
                    if zone[b'rooms'] is None:
                        result += b'unassigned: '
                        for room in zone[b'rooms']:
                            result += (b'{0} ').format(room[b'name'])

                    i += 1

            else:
                i = 0
                if not zero_index:
                    i += 1
                result = b''
                for media_server in RfCmd.rfConfig[b'mediaserver']:
                    if verbose >= 1:
                        result += (b'Mediaserver #{0} : {1}\n').format(i, media_server[b'udn'])
                    else:
                        result += (b'Mediaserver #{0}\n').format(i)
                    i += 1

                i = 0
                if not zero_index:
                    i += 1
                for zone in RfCmd.rfConfig[b'zones']:
                    if verbose == 2:
                        result += (b'Zone #{0} : {1} : {2} -> {3}\n').format(i, zone[b'name'], str(zone[b'udn']), zone[b'host'])
                    elif verbose == 1:
                        result += (b'Zone #{0} : {1} : {2}\n').format(i, zone[b'name'], str(zone[b'udn']))
                    else:
                        result += (b'Zone #{0} : {1}\n').format(i, zone[b'name'])
                    if zone[b'rooms'] is not None:
                        for room in zone[b'rooms']:
                            if verbose == 2:
                                result += (b"\tRoom '{0}' : {1} -> {2}\n").format(room[b'name'], room[b'udn'], room[b'location'])
                            else:
                                if verbose == 1:
                                    result += (b"\tRoom '{0}' : {1}\n").format(room[b'name'], room[b'udn'])
                                else:
                                    result += (b"\tRoom '{0}'\n").format(room[b'name'])
                                for renderer in room[b'room_renderers']:
                                    if verbose == 2:
                                        result += (b"\t\tRenderer '{0}' : {1} -> {2}\n").format(renderer[b'name'], renderer[b'udn'], renderer[b'location'])
                                    elif verbose == 1:
                                        result += (b"\t\tRenderer '{0}' : {1}\n").format(renderer[b'name'], renderer[b'udn'])
                                    else:
                                        result += (b"\t\tRenderer '{0}'\n").format(renderer[b'name'])

                        i += 1

            return result

    @staticmethod
    def get_play_info(verbose, format):
        result = b''
        maxsize = 10
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                if len(zone[b'name']) > maxsize:
                    maxsize = len(zone[b'name'])

        maxsize += 2
        result_list = list()
        header_list = [b'Zone', b'Vol', b'Track', b'Length', b'Pos', b'Src', b'BR', b'Src', b'Track title', b'Track Info']
        result_list.append(header_list)
        for zone in RfCmd.rfConfig[b'zones']:
            if zone[b'rooms'] is not None:
                single_result = list()
                if zone[b'host'] == b'None':
                    single_result.append(zone[b'name'])
                    for i in range(len(header_list) - 1):
                        single_result.append(b'-')

                else:
                    uc = UpnpCommand(zone[b'host'])
                    single_result.append(zone[b'name'])
                    single_result.append(uc.get_volume())
                    results = uc.get_position_info()
                    single_result.append(str(results[b'Track']))
                    single_result.append(str(results[b'TrackDuration']))
                    single_result.append(str(results[b'AbsTime']))
                    if b'DIDL-Lite' in results[b'TrackMetaData']:
                        didlinfo = DidlInfo(results[b'TrackMetaData'], True).get_items()
                        single_result.append(didlinfo[b'resSourceType'])
                        single_result.append(didlinfo[b'resBitrate'])
                        single_result.append(didlinfo[b'resSourceName'])
                        single_result.append(didlinfo[b'title'])
                    else:
                        single_result.append(b'-')
                        single_result.append(b'-')
                        single_result.append(b'-')
                        single_result.append(b'-')
                    media_info = uc.get_media_info()
                    try:
                        if b'CurrentURIMetaData' in media_info:
                            didlinfo = DidlInfo(media_info[b'CurrentURIMetaData']).get_items()
                            media = didlinfo[b'title']
                            single_result.append(media)
                    except:
                        single_result.append(b'-')

                result_list.append(single_result)
                if len(zone[b'rooms']):
                    header_list = [
                     b'Room/Renderer', b'Vol', b'Mute', b'Balance', b'Eq Low', b'Eq Mid', b'Eq High', b'', b'', b'']
                    result_list.append(header_list)
                    for room in zone[b'rooms']:
                        single_result = list()
                        single_result.append(b'> ' + room[b'name'])
                        udn = RfCmd.get_room_udn(room[b'name'])
                        location = RfCmd.get_device_location_by_udn(udn)
                        urc = UpnpCommand(location)
                        result = uc.get_room_volume(udn)
                        single_result.append(result)
                        result = uc.get_room_mute(udn)
                        single_result.append(result)
                        result = urc.get_balance()
                        if result == b'':
                            result = b'-'
                        single_result.append(result)
                        result = urc.get_filter(b'list')
                        single_result.append(result[b'LowDB'])
                        single_result.append(result[b'MidDB'])
                        single_result.append(result[b'HighDB'])
                        single_result.append(b'')
                        single_result.append(b'')
                        single_result.append(b'')
                        result_list.append(single_result)

            if format == b'json':
                result = json.dumps(result_list, sort_keys=True, indent=2) + b'\n'
        else:
            t = Texttable(250)
            t.add_rows(result_list)
            result = t.draw() + b'\n'

        return result

    @staticmethod
    def get_zone_info(format):
        result = b''
        if format == b'json':
            result = json.dumps(RfCmd.rfConfig[b'zones'], sort_keys=True, indent=2) + b'\n'
        else:
            for zone in RfCmd.rfConfig[b'zones']:
                if zone[b'rooms'] is not None:
                    if zone[b'name'] != b'unassigned room':
                        result += zone[b'name']
                        result += b'\n'

        return result

    @staticmethod
    def timecode_to_seconds(tc):
        components = tc.split(b':')
        return int(components[0]) * 3600 + int(components[1]) * 60 + int(components[2])

    @staticmethod
    def wait_operation(uc, condition):
        while True:
            result = uc.get_volume()
            volume = int(result[b'CurrentVolume'])
            results = uc.get_position_info()
            try:
                didlinfo = DidlInfo(results[b'TrackMetaData'])
                items = didlinfo.get_items()
                title = items[b'title']
                artist = items[b'artist']
            except:
                pass

            track = -1
            if b'Track' in results:
                track = int(results[b'Track'])
            duration = -1
            if b'TrackDuration' in results:
                duration = RfCmd.timecode_to_seconds(results[b'TrackDuration'])
            position = -1
            if b'AbsTime' in results:
                position = RfCmd.timecode_to_seconds(results[b'AbsTime'])
            eval_result = eval(condition)
            if eval_result:
                break
            sleep(1)

        return condition

    @staticmethod
    def fade_operation(uc, time, volume_start, volume_end):
        t = 0
        while t < time:
            volume_now = volume_start + (volume_end - volume_start) * t / time
            uc.set_volume(volume_now)
            sleep(1)
            t += 1

        uc.set_volume(volume_end)
        return b'done'

    @staticmethod
    def discover():
        zones_handler = RaumfeldHandler()
        if not zones_handler.reprocess():
            local_ip = RaumfeldDeviceSettings.get_local_ip_address()
            zones_handler.search_nmap_range(local_ip + b'/24')
            zones_handler.publish_state()
        RfCmd.get_raumfeld_infrastructure()

    @staticmethod
    def find_renderer(name):
        for renderer in RfCmd.rfConfig[b'renderer']:
            if name == renderer[b'name']:
                return RfCmd.get_pure_ip(renderer[b'location'])

        return

    @staticmethod
    def find_device(name):
        if name in b'<host>':
            return RfCmd.rfConfig[b'host']
        else:
            for device in RfCmd.rfConfig[b'devices']:
                ip_l = urllib3.util.parse_url(device[b'location'])
                if str(RfCmd.map_ip_to_friendly_name(ip_l.host)) == name:
                    return ip_l.host

            return


def usage(argv):
    print b'Usage: ' + argv[0] + b' [OPTIONS] [COMMAND] {args}'
    print b'Version: ' + version
    print b'OPTIONS: '
    print b'  -j,--json                 Use json as output format, default is plain text lines'
    print b'  -u,--udn  udn             Specify room by udn rather by name'
    print b"  -d,--discover             Discover again (will be fast if host didn't change)"
    print b'     --zonebyudn #          Specify zone by udn'
    print b'  -z,--zone #               Specify zone index (use info to get a list), default 0 = first'
    print b'  -r,--zonewithroom name    Specify zone index by using room name'
    print b'  -s,--renderer name        Specify renderer by using renderer name'
    print b'  -e,--device name          specify device by name, special case is <host> as name'
    print b'  -m,--mediaserver #        Specify media server, default 0 = first'
    print b'  -v,--verbose              Increase verbosity (use twice for more)'
    print b'     --force-local-ip IP    force local ip to a certain address (useful with multiple net cards)'
    print b'COMMANDS: (some commands return xml)'
    print b'  browse path               Browse for media append /* for recursive'
    print b"  play browseitem           Play item in zone i.e. play '0/My Music/Albums/TheAlbumTitle'"
    print b"  playuri URI               Play external URI in zone i.e. play 'http://localhost/your.mp3'"
    print b'  stop|prev|next            Control currently playing items in zone'
    print b'  resume|pause              Control currently playing items in zone'
    print b'  volume #                  Set volume of zone'
    print b'  getvolume                 Get volume of zone'
    print b'  roomvolume room  #        Set volume of room'
    print b'  roomgetvolume room        Get volume of room'
    print b'  roomgeteq room            Get equalizer settings of device'
    print b'  mute #                    Set mute state'
    print b'  getmute                   Get mute state of zone'
    print b'  roommute room #           Mute room'
    print b'  roomgetmute room          Get mute state of room'
    print b'  roomgeteq room            Get equalizer settings of device'
    print b'  roomseteq room L M H      Set equalizer device Low Mid High range is -1536 to 1536'
    print b'  position                  Get position info of zone'
    print b'  seek #                    Seek to a specific position'
    print b'  standby state {room(s)}   Set a room into standby state=on/off/auto'
    print b'  roomgetsetting room value Get special setting of soundbar/deck:'
    print b'                             Audio Mode: Stereo, Arena, Theater, Voice'
    print b'                             Source Select: TV_ARC, OpticalIn, LineIn, Raumfeld'
    print b'                             TV Source Select, TV_ARC, OpticalIn, LineIn'
    print b'                             Subwoofer Playback Volume: -10 ... 10'
    print b'                             Subwoofer X-Over: 80Hz, 100Hz, 120Hz, 140Hz'
    print b'                             Night Mode Switch'
    print b'  roomsetsetting room value #  Set special setting of soundbar/deck'
    print b'INFOS: (return lists of easily parsable text/json)'
    print b'  host                      print host ip'
    print b'  rooms                     Show list of rooms ordererd alphabetically'
    print b'  deviceips                 Show list of devices (rooms/host) ip address (verbose shows name)'
    print b'  renderer                  Show list of renderer names (verbose shows ip)'
    print b'  unassignedrooms           Show list of unassigned rooms'
    print b'  zoneinfo                  Show info on zone'
    print b'  zones                     Show list of zones, unassigned room is skipped'
    print b'  info                      Show list of zones, rooms and renderers'
    print b'  status                    Show list of status of renderers'
    print b'  playinfo                  Show playing info of renderers'
    print b'#MACRO OPERATIONS'
    print b'  wait condition            wait for condition (expression) [volume, position, duration, title, artist] i.e. volume < 5 or position==120 '
    print b'  fade time vols vole       fade volume from vols to vole in time seconds '
    print b'#ZONE MANAGEMENT (will automatically discover after operating)'
    print b'  createzone {room(s)}      create zone with list of rooms (space seperated)'
    print b'  addtozone {room(s)}       add rooms to existing zone'
    print b"  drop {room(s)}            drop rooms from it's zone"
    print b'#SSH '
    print b'  ssh {command...}          send command to given device, device is determined by --renderer or --device'


sshcmd = b'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@'
scpcmd = b'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '

def retrieve(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return 0

    lines = b''
    while True:
        nextline = process.stdout.readline()
        if len(nextline) == 0 and process.poll() != None:
            break
        lines += nextline.decode(b'utf-8')

    return lines


def single_device_command(ip, cmd):
    cmd = sshcmd + ip + b' ' + cmd
    print (b'running cmd on device {0}: {1}').format(ip, cmd)
    lines = retrieve(cmd)
    print (b'result from {0}').format(ip)
    return lines


def run_main():
    argv = list()
    for arg in sys.argv:
        argv.append(arg)

    verbose = 0
    if len(argv) < 2:
        usage(argv)
        sys.exit(2)
    target_device = None
    zoneIndex = -1
    mediaIndex = 0
    room = b''
    device_format = b'named'
    format = b'plain'
    arg_pos = 1
    RfCmd.get_raumfeld_infrastructure()
    while argv[arg_pos].startswith(b'-'):
        if argv[arg_pos].startswith(b'--'):
            option = argv[arg_pos][2:]
        else:
            option = argv[arg_pos]
        arg_pos += 1
        if option == b'verbose' or option == b'-v':
            verbose += 1
        elif option == b'-vv':
            verbose += 2
        elif option == b'force-local-ip':
            RaumfeldDeviceSettings.force_local_ip_address(argv[arg_pos])
            arg_pos += 1
        elif option == b'user-agent':
            UpnpCommand.overwrite_user_agent(argv[arg_pos])
            arg_pos += 1
        elif option == b'help' or option == b'-h':
            usage(argv)
            sys.exit(2)
        elif option == b'renderer' or option == b'-s':
            target_device = RfCmd.find_renderer(argv[arg_pos])
            arg_pos += 1
        elif option == b'device' or option == b'-e':
            target_device = RfCmd.find_device(argv[arg_pos])
            arg_pos += 1
        elif option == b'udn' or option == b'-u':
            device_format = b'udn'
        elif option == b'json' or option == b'-j':
            format = b'json'
        elif option == b'discover' or option == b'-d':
            RfCmd.discover()
            uc = UpnpCommand(RfCmd.rfConfig[b'zones'][zoneIndex][b'host'])
            if arg_pos == len(argv):
                print b'done'
                sys.exit(0)
        elif option == b'zonebyudn':
            found = False
            for index, zone in enumerate(RfCmd.rfConfig[b'zones']):
                if argv[arg_pos] == zone[b'udn']:
                    zoneIndex = index
                    uc = UpnpCommand(RfCmd.rfConfig[b'zones'][zoneIndex][b'host'])
                    found = True

            if not found:
                print (b'Zoneudn {0} not found').format(argv[arg_pos])
                sys.exit(-1)
            arg_pos += 1
        elif option == b'zone' or option == b'-z':
            zoneIndex = int(argv[arg_pos])
            uc = UpnpCommand(RfCmd.rfConfig[b'zones'][zoneIndex][b'host'])
            arg_pos += 1
        elif option == b'zonewithroom' or option == b'-r':
            roomName = argv[arg_pos]
            zoneIndex = RfCmd.get_room_zone_index(roomName)
            if verbose:
                print (
                 b'Room found in zone ', zoneIndex)
            if zoneIndex == -1:
                print (b"ERROR: room with name '{0}' not found").format(roomName)
                print b'Available rooms are to be found here:\n' + RfCmd.get_info(verbose)
                exit(-1)
            if RfCmd.is_unassigned_room(roomName):
                print b'error: room is unassigned: ' + roomName
                exit(-1)
            uc = UpnpCommand(RfCmd.rfConfig[b'zones'][zoneIndex][b'host'])
            arg_pos += 1
        elif option == b'mediaserver' or option == b'-m':
            mediaIndex = int(argv[arg_pos])
            arg_pos += 1
        else:
            print (b'unknown option --{0}').format(option)
            usage(argv)
            sys.exit(2)

    if zoneIndex == -1:
        zoneIndex = 0
        uc = UpnpCommand(RfCmd.rfConfig[b'zones'][0][b'host'])
    uc_media = UpnpCommand(RfCmd.rfConfig[b'mediaserver'][mediaIndex][b'location'])
    operation = argv[arg_pos]
    arg_pos += 1
    result = None
    if operation == b'play':
        udn = RfCmd.rfConfig[b'mediaserver'][mediaIndex][b'udn']
        transport_data = dict()
        browseresult = uc_media.browsechildren(argv[arg_pos])
        if browseresult is None:
            browseresult = uc_media.browse(argv[arg_pos])
            transport_data[b'CurrentURI'] = RfCmd.build_dlna_play_single(udn, b'urn:upnp-org:serviceId:ContentDirectory', argv[arg_pos])
        else:
            transport_data[b'CurrentURI'] = RfCmd.build_dlna_play_container(udn, b'urn:upnp-org:serviceId:ContentDirectory', argv[arg_pos])
        print (
         b'URI', argv[arg_pos], transport_data[b'CurrentURI'])
        transport_data[b'CurrentURIMetaData'] = b'<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"><container></container></DIDL-Lite>'
        uc.set_transport_uri(transport_data)
        result = b'ok'
    elif operation == b'playuri':
        transport_data = dict()
        transport_data[b'CurrentURI'] = argv[arg_pos]
        print (b'URI', argv[arg_pos], transport_data[b'CurrentURI'])
        transport_data[b'CurrentURIMetaData'] = b'<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" \n            xmlns:dc="http://purl.org/dc/elements/1.1/" \n            xmlns:dlna="urn:schemas-dlna-org:metadata-1-0/" \n            xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" \n            xmlns:raumfeld="urn:schemas-raumfeld-com:meta-data/raumfeld"\n            lang="en"\n            >\n                <item parentID="RadioTeufel" id="RadioTeufel/1" restricted="1">\n                <res bitrate="192" protocolInfo="http-get:*:audio/x-mpegurl:*">' + transport_data[b'CurrentURI'] + b'</res>\n                <raumfeld:name>radio</raumfeld:name>\n                <upnp:class>ContentSection</upnp:class>\n                <raumfeld:section>RadioTime</raumfeld:section>\n                <dc:title>Audio Broadcast</dc:title>\n                <upnp:album>Elegant Girl</upnp:album>\n                <upnp:artist>Audio Broadcast</upnp:artist>\n                <upnp:genre>Classic</upnp:genre>\n                <dc:creator>us</dc:creator>\n                <upnp:originalTrackNumber>1</upnp:originalTrackNumber>\n                <dc:date>1977-01-01</dc:date>\n                </item>\n            </DIDL-Lite>'
        uc.set_transport_uri(transport_data)
        result = b'ok'
    elif operation == b'resume':
        result = uc.play()
    elif operation == b'pause':
        result = uc.pause()
    elif operation == b'stop':
        result = uc.stop()
    elif operation == b'next':
        result = uc.next()
    elif operation == b'prev':
        result = uc.previous()
    elif operation == b'roomgetinfo':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        result = RfCmd.get_room_info(uc, udn)
    elif operation == b'volume' or operation == b'setvolume':
        if device_format == b'udn':
            for renderer in RfCmd.rfConfig[b'renderer']:
                if renderer[b'udn'] == argv[arg_pos]:
                    host = urllib3.util.parse_url(renderer[b'location'])
                    uc = UpnpCommand(host.netloc)

            arg_pos += 1
            result = uc.set_volume_by_udn(argv[arg_pos])
        else:
            result = uc.set_volume(argv[arg_pos])
    elif operation == b'getvolume':
        if device_format == b'udn':
            for renderer in RfCmd.rfConfig[b'renderer']:
                if renderer[b'udn'] == argv[arg_pos]:
                    host = urllib3.util.parse_url(renderer[b'location'])
                    uc = UpnpCommand(host.netloc)

            result = uc.get_volume_by_udn(format)
        else:
            result = uc.get_volume(format)
    elif operation == b'roomgetvolume':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        result = uc.get_room_volume(udn)
    elif operation == b'roomsetvolume' or operation == b'roomvolume':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        arg_pos += 1
        result = uc.set_room_volume(udn, argv[arg_pos])
    elif operation == b'mute' or operation == b'setmute':
        result = uc.set_mute(argv[arg_pos])
    elif operation == b'getmute':
        result = uc.get_mute(format)
    elif operation == b'roomgetsetting':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        arg_pos += 1
        moniker = argv[arg_pos]
        if moniker == b'all':
            result = b''
            for i in [b'Audio Mode', b'Source Select', b'TV Source Select', b'Subwoofer Playback Volume', b'Subwoofer X-Over', b'Night Mode Switch']:
                result += urc.get_setting(i, format)

        else:
            result = urc.get_setting(moniker, format)
    elif operation == b'roomsetsetting':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        arg_pos += 1
        result = urc.set_setting(argv[arg_pos], argv[(arg_pos + 1)])
    elif operation == b'roomgetmute':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        result = uc.get_room_mute(udn)
    elif operation == b'roomsetmute':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        arg_pos += 1
        result = uc.set_room_mute(udn, argv[arg_pos])
    elif operation == b'roomgeteq':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        result = urc.get_filter(format)
    elif operation == b'roomseteq':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        result = urc.set_filter(argv[(arg_pos + 1)], argv[(arg_pos + 2)], argv[(arg_pos + 3)])
    elif operation == b'roomgetbalance':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        result = urc.get_balance(format)
    elif operation == b'roomsetbalance':
        if device_format == b'udn':
            udn = argv[arg_pos]
        else:
            udn = RfCmd.get_room_udn(argv[arg_pos])
        location = RfCmd.get_device_location_by_udn(udn)
        urc = UpnpCommand(location)
        result = urc.set_balance(argv[(arg_pos + 1)])
    elif operation == b'standby':
        state = argv[arg_pos]
        arg_pos += 1
        while arg_pos < len(argv):
            udn = RfCmd.get_room_udn(argv[arg_pos])
            if udn is None:
                print b'unknown room ' + argv[arg_pos]
            else:
                RfCmd.raumfeld_host_device.set_room_standby(str(udn), state)
            arg_pos += 1

    elif operation == b'position':
        results = uc.get_position_info()
        if format == b'json':
            return json.dumps(results, sort_keys=True, indent=2) + b'\n'
        result = b''
        if b'TrackDuration' in results:
            result += str(results[b'TrackDuration'])
        result += b'\n'
        if b'AbsTime' in results:
            result += str(results[b'AbsTime'])
        result += b'\n'
    elif operation == b'seek':
        result = uc.seek(argv[arg_pos])
    elif operation == b'wait':
        result = RfCmd.wait_operation(uc, argv[arg_pos])
    elif operation == b'fade':
        result = RfCmd.fade_operation(uc, int(argv[arg_pos]), int(argv[(arg_pos + 1)]), int(argv[(arg_pos + 2)]))
    elif operation == b'createzone':
        rooms = set()
        result = b'zone creation adding rooms:\n'
        while arg_pos < len(argv):
            if device_format == b'udn':
                udn = argv[arg_pos]
            else:
                udn = RfCmd.get_room_udn(argv[arg_pos])
            result += (b"{0}'\n").format(str(udn))
            rooms.add(str(udn))
            arg_pos += 1
            RfCmd.raumfeld_host_device.create_zone_with_rooms(rooms)

        sleep(2)
        RfCmd.discover()
    elif operation == b'addtozone':
        zone_udn = RfCmd.rfConfig[b'zones'][zoneIndex][b'udn']
        rooms = set()
        result = b'zone creation adding rooms:\n'
        while arg_pos < len(argv):
            if device_format == b'udn':
                udn = argv[arg_pos]
            else:
                udn = RfCmd.get_room_udn(argv[arg_pos])
            result += (b"{0}'\n").format(str(udn))
            rooms.add(str(udn))
            arg_pos += 1

        RfCmd.raumfeld_host_device.add_rooms_to_zone(zone_udn, rooms)
        sleep(2)
        RfCmd.discover()
    elif operation == b'drop':
        result = b'drop rooms from zone:\n'
        while arg_pos < len(argv):
            if device_format == b'udn':
                udn = argv[arg_pos]
            else:
                udn = RfCmd.get_room_udn(argv[arg_pos])
            result += str(RfCmd.raumfeld_host_device.drop_room(str(udn)))
            arg_pos += 1

        sleep(2)
        RfCmd.discover()
    elif operation == b'browse':
        startIndex = 0
        requestCount = 0
        if len(sys.argv) > arg_pos + 2:
            startIndex = int(argv[(arg_pos + 1)])
            requestCount = int(argv[(arg_pos + 2)])
            print (startIndex, requestCount)
        if argv[arg_pos].endswith(b'/*'):
            result = uc_media.browse_recursive_children(argv[arg_pos][:-2], 3, format, startIndex, requestCount)
        else:
            result = uc_media.browse_recursive_children(argv[arg_pos], 0, format, startIndex, requestCount)
    elif operation == b'browseinfo':
        results = uc_media.browse(argv[arg_pos])
        result = RfCmd.get_didl_extract(results[b'Result'], format)
    elif operation == b'search':
        result = uc_media.search(argv[arg_pos], argv[(arg_pos + 1)], format)
    elif operation == b'rooms':
        result = RfCmd.get_rooms(verbose, format)
        result = result[:-1]
    elif operation == b'urls':
        result = b''
    elif operation == b'host':
        result = RfCmd.raumfeld_host_device.server_ip
    elif operation == b'deviceips':
        result = RfCmd.get_device_ips(verbose, format)
        result = result[:-1]
    elif operation == b'renderer':
        result = RfCmd.get_renderer(verbose, format)
        result = result[:-1]
    elif operation == b'unassignedrooms':
        result = RfCmd.get_unassigned_rooms(verbose, format)
        result = result[:-1]
    elif operation == b'zones':
        result = RfCmd.get_zone_info(format)
        result = result[:-1]
    elif operation == b'zoneinfo':
        result = RfCmd.get_specific_zoneinfo(uc, format)
        result = result[:-1]
    elif operation == b'info':
        result = RfCmd.get_info(verbose, format)
        result = result[:-1]
    elif operation == b'playinfo':
        result = RfCmd.get_play_info(verbose, format)
        result = result[:-1]
    elif operation == b'ssh':
        combined_args = (b' ').join(argv[arg_pos:])
        result = single_device_command(target_device, combined_args)
    else:
        usage(argv)
    if result is not None:
        sys.stdout.write(result)
    sys.stdout.write(b'\n')
    return


if __name__ == b'__main__':
    run_main()