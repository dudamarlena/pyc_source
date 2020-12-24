# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/upnpCommand.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import json
from time import time
import requests, sys, cgi
from xml.dom import minidom
from pyfeld.xmlHelper import XmlHelper
from pyfeld.didlInfo import DidlInfo
user_agent = b'xrf/1.0'

class UpnpCommand():

    def __init__(self, host):
        self.host = host
        self.verbose = False

    @staticmethod
    def overwrite_user_agent(new_user_agent):
        global user_agent
        user_agent = new_user_agent

    def host_send(self, action, control_path, control_name, action_args):
        if self.host is None:
            print b'Serious problem, no host defined!'
            return
        else:
            if self.host.startswith(b'http://'):
                control_url = self.host + control_path
                host_name = self.host[7:]
            else:
                control_url = b'http://' + self.host + control_path
                host_name = self.host
            body = b'<?xml version="1.0"?>'
            body += b'<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" '
            body += b'SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
            body += b'<SOAP-ENV:Body>'
            body += b'\t<m:' + action + b' xmlns:m="urn:schemas-upnp-org:service:' + control_name + b':1">'
            body += action_args
            body += b'\t</m:' + action + b'>'
            body += b'</SOAP-ENV:Body>'
            body += b'</SOAP-ENV:Envelope>'
            if self.verbose:
                print body
            headers = {b'Host': host_name, b'User-Agent': user_agent, 
               b'Content-Type': b'text/xml; charset="utf-8"', 
               b'Content-Length': str(len(body)), 
               b'SOAPAction': b'"urn:schemas-upnp-org:service:' + control_name + b':1#' + action + b'"'}
            try:
                t = time()
                if self.verbose:
                    print (
                     str(control_url), str(body), str(headers))
                response = requests.post(control_url, data=body, headers=headers, verify=False)
                if response.status_code < 300:
                    if self.verbose:
                        print response.content
                    result = minidom.parseString(response.content)
                    if self.verbose:
                        print result.toprettyxml()
                    return result
                if self.verbose:
                    print (b'query {0} returned status_code:{1}').format(control_url, response.status_code)
            except Exception as e:
                if self.verbose:
                    print (b'warning! host send error {0}').format(e)

            return

    def device_send_rendering(self, action, action_args):
        return self.host_send(action, b'/RenderingControl/ctrl', b'RenderingControl', action_args)

    def host_send_rendering(self, action, action_args):
        return self.host_send(action, b'/RenderingService/Control', b'RenderingControl', action_args)

    def host_send_transport(self, action, action_args):
        return self.host_send(action, b'/TransportService/Control', b'AVTransport', action_args)

    def host_send_contentdirectory(self, action, action_args):
        return self.host_send(action, b'/cd/Control', b'ContentDirectory', action_args)

    def play(self):
        xml_root = self.host_send_transport(b'Play', b'<InstanceID>0</InstanceID><Speed>1</Speed>')
        return xml_root.toprettyxml()

    def stop(self):
        xml_root = self.host_send_transport(b'Stop', b'<InstanceID>0</InstanceID>')
        return xml_root.toprettyxml()

    def pause(self):
        xml_root = self.host_send_transport(b'Pause', b'<InstanceID>0</InstanceID>')
        return xml_root.toprettyxml()

    def seek(self, value):
        xml_root = self.host_send_transport(b'Seek', b'<InstanceID>0</InstanceID><Unit>ABS_TIME</Unit><Target>' + value + b'</Target>')
        return xml_root.toprettyxml()

    def previous(self):
        xml_root = self.host_send_transport(b'Previous', b'<InstanceID>0</InstanceID>')
        return xml_root.toprettyxml()

    def next(self):
        xml_root = self.host_send_transport(b'Next', b'<InstanceID>0</InstanceID>')
        return xml_root.toprettyxml()

    def get_state_var(self):
        xml_root = self.host_send_rendering(b'GetStateVariables', b'<InstanceID>0</InstanceID><StateVariableList>TransportStatus</StateVariableList>')
        return xml_root.toprettyxml()

    def get_position_info(self):
        xml_root = self.host_send_transport(b'GetPositionInfo', b'<InstanceID>0</InstanceID>')
        return XmlHelper.xml_extract_dict(xml_root, [b'Track',
         b'TrackDuration',
         b'TrackMetaData',
         b'TrackURI',
         b'RelTime',
         b'AbsTime',
         b'RelCount',
         b'AbsCount'])

    def get_transport_setting(self):
        xml_root = self.host_send_transport(b'GetTransportSettings', b'<InstanceID>0</InstanceID>')
        return XmlHelper.xml_extract_dict(xml_root, [b'PlayMode'])

    def get_media_info(self):
        xml_root = self.host_send_transport(b'GetMediaInfo', b'<InstanceID>0</InstanceID>')
        return XmlHelper.xml_extract_dict(xml_root, [b'PlayMedium', b'NrTracks', b'CurrentURI', b'CurrentURIMetaData'])

    def set_transport_uri(self, data):
        print b'CurrentURI:\n' + data[b'CurrentURI']
        print b'CurrentURIMetaData:\n' + data[b'CurrentURIMetaData']
        send_data = b'<InstanceID>0</InstanceID>'
        add_uri = data[b'CurrentURI']
        if b'raumfeldname' in data:
            if data[b'raumfeldname'] == b'Station':
                if b'TrackURI' in data:
                    add_uri = data[b'TrackURI']
        send_data += b'<CurrentURI><![CDATA[' + add_uri + b']]></CurrentURI>'
        send_data += b'<CurrentURIMetaData>' + cgi.escape(data[b'CurrentURIMetaData']) + b'</CurrentURIMetaData>'
        print send_data
        xml_root = self.host_send_transport(b'SetAVTransportURI', send_data)
        return XmlHelper.xml_extract_dict(xml_root, [b'SetAVTransportURI'])

    def get_volume(self, format=b'plain'):
        xml_root = self.host_send_rendering(b'GetVolume', b'<InstanceID>0</InstanceID><Channel>Master</Channel>')
        dict = XmlHelper.xml_extract_dict(xml_root, [b'CurrentVolume'])
        if format == b'json':
            return b'{ "CurrentVolume": "' + dict[b'CurrentVolume'] + b'"}'
        else:
            return dict[b'CurrentVolume']

    def set_volume(self, value):
        xml_root = self.host_send_rendering(b'SetVolume', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredVolume>' + str(value) + b'</DesiredVolume>')
        return xml_root.toprettyxml()

    def get_volume_by_udn(self, format=b'plain'):
        xml_root = self.device_send_rendering(b'GetVolume', b'<InstanceID>0</InstanceID><Channel>Master</Channel>')
        dict = XmlHelper.xml_extract_dict(xml_root, [b'CurrentVolume'])
        if format == b'json':
            return b'{ "CurrentVolume": "' + dict[b'CurrentVolume'] + b'"}'
        else:
            return dict[b'CurrentVolume']

    def set_volume_by_udn(self, value):
        xml_root = self.device_send_rendering(b'SetVolume', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredVolume>' + str(value) + b'</DesiredVolume>')
        return xml_root.toprettyxml()

    def get_room_volume(self, uuid, format=b'plain'):
        xml_root = self.host_send_rendering(b'GetRoomVolume', b'<InstanceID>0</InstanceID><Room>' + uuid + b'</Room>')
        dict = XmlHelper.xml_extract_dict(xml_root, [b'CurrentVolume'])
        if format == b'json':
            return b'{ "CurrentVolume": "' + dict[b'CurrentVolume'] + b'"}'
        else:
            return dict[b'CurrentVolume']

    def set_room_volume(self, uuid, value):
        xml_root = self.host_send_rendering(b'SetRoomVolume', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredVolume>' + str(value) + b'</DesiredVolume>' + b'<Room>' + uuid + b'</Room>')
        return

    def get_mute(self, format=b'plain'):
        xml_root = self.host_send_rendering(b'GetMute', b'<InstanceID>0</InstanceID><Channel>Master</Channel>')
        dict = XmlHelper.xml_extract_dict(xml_root, [b'CurrentMute'])
        if format == b'json':
            return b'{ "CurrentMute": "' + dict[b'CurrentMute'] + b'"}'
        else:
            return dict[b'CurrentMute']

    def set_mute(self, value):
        xml_root = self.host_send_rendering(b'SetMute', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredMute>' + str(value) + b'</DesiredMute>')
        return xml_root.toprettyxml()

    def get_room_mute(self, uuid, format=b'plain'):
        xml_root = self.host_send_rendering(b'GetRoomMute', b'<InstanceID>0</InstanceID><Room>' + uuid + b'</Room>')
        dict = XmlHelper.xml_extract_dict(xml_root, [b'CurrentMute'])
        if format == b'json':
            return b'{ "CurrentMute": "' + dict[b'CurrentMute'] + b'"}'
        else:
            return dict[b'CurrentMute']

    def set_room_mute(self, uuid, value):
        xml_root = self.host_send_rendering(b'SetRoomMute', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredMute>' + str(value) + b'</DesiredMute>' + b'<Room>' + uuid + b'</Room>')
        return

    def get_setting(self, setting_name, output_format=b'plain'):
        xml_root = self.device_send_rendering(b'GetDeviceSetting', b'<InstanceID>0</InstanceID>' + b'<Name>' + str(setting_name) + b'</Name>')
        dict_result = XmlHelper.xml_extract_dict(xml_root, [b'Value'])
        if output_format == b'json':
            return b'{ "Value": "' + dict_result[b'Value'] + b'"}'
        else:
            return dict_result[b'Value']

    def set_setting(self, setting_name, value):
        xml_root = self.device_send_rendering(b'SetDeviceSetting', b'<InstanceID>0</InstanceID>' + b'<Name>' + str(setting_name) + b'</Name>' + b'<Value>' + str(value) + b'</Value>')
        return xml_root.toprettyxml()

    def get_filter(self, output_format=b'plain'):
        xml_root = self.device_send_rendering(b'GetFilter', b'<InstanceID>0</InstanceID>')
        dict_result = XmlHelper.xml_extract_dict(xml_root, [b'LowDB', b'MidDB', b'HighDB'])
        if output_format == b'json':
            return b'{ "LowDB": "' + dict_result[b'LowDB'] + b'",  "MidDB": "' + dict_result[b'MidDB'] + b'",  "HighDB": "' + dict_result[b'HighDB'] + b'"}'
        else:
            if output_format == b'list':
                return dict_result
            return dict_result[b'LowDB'] + b' ' + dict_result[b'MidDB'] + b' ' + dict_result[b'HighDB']

    def set_filter(self, valueLow, valueMid, valueHigh):
        xml_root = self.device_send_rendering(b'SetFilter', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<LowDB>' + str(valueLow) + b'</LowDB>' + b'<MidDB>' + str(valueMid) + b'</MidDB>' + b'<HighDB>' + str(valueHigh) + b'</HighDB>')
        return

    def get_balance(self, output_format=b'plain'):
        xml_root = self.device_send_rendering(b'GetBalance', b'<InstanceID>0</InstanceID>')
        dict_result = XmlHelper.xml_extract_dict(xml_root, [b'CurrentBalance'])
        if output_format == b'json':
            return b'{ "CurrentBalance": "' + dict_result[b'CurrentBalance'] + b'"}'
        else:
            return dict_result[b'CurrentBalance']

    def set_balance(self, value):
        xml_root = self.device_send_rendering(b'SetBalance', b'<InstanceID>0</InstanceID><Channel>Master</Channel>' + b'<DesiredBalance>' + str(value) + b'</DesiredBalance>')
        return

    def get_browse_capabilites(self):
        xml_root = self.host_send_contentdirectory(b'GetSearchCapabilities', b'')
        return XmlHelper.xml_extract_dict(xml_root, [b'SearchCaps'])

    def search(self, path, search_string, format=b'plain'):
        browse_data = b'<ContainerID>' + path + b'</ContainerID>' + b'<SearchCriteria>' + search_string + b'</SearchCriteria>' + b'<Filter>*</Filter>' + b'<StartingIndex>0</StartingIndex>' + b'<RequestedCount>0</RequestedCount>' + b'<SortCriteria>dc:title</SortCriteria>'
        xml_root = self.host_send_contentdirectory(b'Search', browse_data)
        result = XmlHelper.xml_extract_dict(xml_root, [b'Result', b'TotalMatches', b'NumberReturned'])
        return self.scan_browse_result(result, 0, format)

    def browse(self, path, startIndex=0, requestCount=0):
        browse_data = b'<ObjectID>' + path + b'</ObjectID>' + b'<BrowseFlag>BrowseMetadata</BrowseFlag>' + b'<Filter>*</Filter>' + b'<StartingIndex>' + str(startIndex) + b'</StartingIndex>' + b'<RequestedCount>' + str(requestCount) + b'</RequestedCount>' + b'<SortCriteria>dc:title</SortCriteria>'
        xml_root = self.host_send_contentdirectory(b'Browse', browse_data)
        return XmlHelper.xml_extract_dict(xml_root, [b'Result', b'TotalMatches', b'NumberReturned'])

    def browsechildren(self, path, startIndex=0, requestCount=0):
        browse_data = b'<ObjectID>' + path + b'</ObjectID>' + b'<BrowseFlag>BrowseDirectChildren</BrowseFlag>' + b'<Filter>*</Filter>' + b'<StartingIndex>' + str(startIndex) + b'</StartingIndex>' + b'<RequestedCount>' + str(requestCount) + b'</RequestedCount>' + b'<SortCriteria>dc:title</SortCriteria>'
        xml_root = self.host_send_contentdirectory(b'Browse', browse_data)
        if xml_root is None:
            return
        else:
            return XmlHelper.xml_extract_dict(xml_root, [b'Result', b'TotalMatches', b'NumberReturned'])

    def get_node_element(self, node, tag):
        element = node.getElementsByTagName(tag)
        if element[0].firstChild is not None:
            title = element[0].firstChild.nodeValue
        return

    def scan_browse_result(self, result, level, output_format=b'plain'):
        if output_format == b'plain':
            s = b''
            xml_root = minidom.parseString(result[b'Result'].encode(b'utf-8'))
            container_list = xml_root.getElementsByTagName(b'container')
            for container in container_list:
                dict = DidlInfo.extract_from_node(container, True)
                npath = dict[b'idPath']
                adds = b'C ' + npath + b' * ' + dict[b'title'] + b'\n'
                s += adds
                if int(level) > 0:
                    self.browse_recursive_children(npath, int(level) - 1, output_format)

            item_list = xml_root.getElementsByTagName(b'item')
            for item in item_list:
                dict = DidlInfo.extract_from_node(item, True)
                npath = dict[b'idPath']
                s += b'+ ' + npath + b' * ' + dict[b'title'] + b'\n'

            return s
        s = b'['
        xml_root = minidom.parseString(result[b'Result'])
        container_list = xml_root.getElementsByTagName(b'container')
        for container in container_list:
            dict = DidlInfo.extract_from_node(container, True)
            s += json.dumps(dict)
            s += b','

        item_list = xml_root.getElementsByTagName(b'item')
        for item in item_list:
            dict = DidlInfo.extract_from_node(item, True)
            s += json.dumps(dict)
            s += b','

        if len(s) > 2:
            s = s[:-1]
        s += b']'
        return s

    def browse_recursive_children(self, path, level=3, output_format=b'plain', startIndex=0, requestCount=0):
        if int(level) < 0:
            return b'error on level < 0'
        else:
            if path == b'0/RadioTime':
                UpnpCommand.overwrite_user_agent(b'RaumfeldControl')
            result = self.browsechildren(path, startIndex, requestCount)
            if result is None:
                result = self.browse(path, startIndex, requestCount)
            if len(result) == 0:
                return b''
            return self.scan_browse_result(result, int(level), output_format)


def usage(argv):
    print b'Usage: ' + argv[0] + b' ip:port [COMMAND|INFO] {args}'
    print b'COMMAND: '
    print b'  play                  play last stuff'
    print b'  stop                  stop current playing'
    print b'  setv vol              set volume args=0..100'
    print b'  seek pos              seek to position args=00:00:00 ... 99:59:59'
    print b'INFO: '
    print b'  getv                  get volume info'
    print b'  position              GetPositionInfo '
    print b'  getsetting id            GetSetting'
    print b'  media                 GetMediaInfo'
    print b'  transport             GetTransportSettings '
    print b'  allinfo               all infos in one call '
    print b'BROWSE: '
    print b'  cap                   get browse capabilities'
    print b'  browse path           Browse for data'
    print b'  browsechildren path   Browse for data append /* for recursive'


def main(argv):
    if len(sys.argv) < 3:
        usage(sys.argv)
        sys.exit(2)
    host = sys.argv[1]
    uc = UpnpCommand(host)
    operation = sys.argv[2]
    result = None
    if operation == b'play':
        result = uc.play()
    elif operation == b'stop':
        result = uc.stop()
    elif operation == b'getv':
        result = uc.get_volume()
    elif operation == b'getfilter':
        result = uc.get_filter()
    elif operation == b'setv':
        result = uc.set_volume(sys.argv[3])
    elif operation == b'seek':
        result = uc.seek(sys.argv[3])
    elif operation == b'prev':
        result = uc.previous()
    elif operation == b'next':
        result = uc.next()
    elif operation == b'position':
        result = uc.get_position_info()
    elif operation == b'transport':
        result = uc.get_transport_setting()
    elif operation == b'getstatevar':
        result = uc.get_state_var()
    elif operation == b'getsetting':
        result = uc.get_setting(sys.argv[3])
    elif operation == b'media':
        result = uc.get_media_info()
        result += uc.get_position_info()
    elif operation == b'allinfo':
        result = uc.get_volume()
        result += uc.get_position_info()
        result += uc.get_transport_setting()
        result += uc.get_media_info()
    elif operation == b'cap':
        result = uc.get_browse_capabilites()
    elif operation == b'browse':
        result = uc.browse(argv[3])
        xml_root = minidom.parseString(result[b'Result'])
        print xml_root.toprettyxml(indent=b'\t')
    else:
        if operation == b'browsechildren':
            if argv[3].endswith(b'/*'):
                result = uc.browse_recursive_children(argv[3][:-2])
                print result
            else:
                result = uc.browsechildren(argv[3])
                xml_root = minidom.parseString(result[b'Result'])
                print xml_root.toprettyxml(indent=b'\t')
            return
        usage(sys.argv)
    print result
    return


if __name__ == b'__main__':
    main(sys.argv)