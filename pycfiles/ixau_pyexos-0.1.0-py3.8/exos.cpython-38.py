# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/pyexos/exos.py
# Compiled at: 2020-04-20 02:45:00
# Size of source mod 2**32: 28016 bytes
"""
pyexos - Extreme Networks Config Manipulation
Copyright (C) 2020 Internet Association of Australian (IAA)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
from netmiko import ConnectHandler
from netmiko import NetMikoAuthenticationException
from netmiko import NetMikoTimeoutException
from .utils import acl_re
from .utils import CLICommandException
from .utils import community_re
from .utils import ConfigParseException
from .utils import hostname_re
from .utils import ip_re
from .utils import location_re
from .utils import mplsprotocols_re
from .utils import NotImplementedException
from .utils import ospfarea_re
from .utils import partition_re
from .utils import port_name_for_delete_re
from .utils import port_name_re
from .utils import sharing_for_delete_re
from .utils import sharing_re
from .utils import SSHException
from .utils import virtuallink_re
from .utils import vlan_create_re
from .utils import vlan_re
from .utils import vpls_re

class EXOS(object):

    def __init__(self, config=[], ip=False, name=False, username=False, password=False, port=22, protocol='ssh', timeout=15, ssh_config_file=None):
        """
        Returns a new EXOS device, allowing connections & config manipulation

        :param config:          Start with a loaded config to parse (default: [])
        :param ip:              IP
        :param name:            Hostname
        :param username:        Username
        :param password:        Password
        :param port:            SSH, Telnet or REST port (default: 22)
        :param protocol:        Protocol: 'ssh', 'telnet', 'rest' (default: ssh)
        :param timeout:         Timeout (default: 15 sec)
        :param ssh_config_file: Path to SSH Config File (default: None)
        :return:                EXOS Device
        """
        self.config = []
        self.ports = []
        self.snmp_community = ''
        self.ospf_areas = []
        self.location = ''
        self.ospf_virtual_links = []
        self.mpls_protocols = []
        self.port_partitions = []
        self.vpls = []
        self.vlans = []
        self.ip = ip
        self.name = name
        self.username = username
        self.password = password
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        self.ssh_config_file = ssh_config_file
        self.device = None
        if config:
            self.load_config(config)

    def _is_int(self, v):
        try:
            int(v)
        except ValueError:
            return False
        else:
            return True

    def _process_config(self):
        """
        A helper method that tries to process raw configuration into a usable state for auditing.

        :return:  None
        """
        self.ip = [m.group(1) for m in (ip_re.match(line) for line in self.config) if m][0]
        self.name = [m.group(1) for m in (hostname_re.match(line) for line in self.config) if m][0]
        self.snmp_community = [m.group(1) for m in (community_re.match(line) for line in self.config) if m][0]
        self.ospf_areas = [m.group(1) for m in (ospfarea_re.match(line) for line in self.config) if m]
        self.location = ''.join([m.group(1) for m in (location_re.match(line) for line in self.config) if m])
        self.ospf_virtual_links = [{'peer':m.group(1), 
         'area':m.group(2)} for m in (virtuallink_re.match(line) for line in self.config) if m]
        self.mpls_protocols = [m.group(1) for m in (mplsprotocols_re.match(line) for line in self.config) if m]
        self.port_partitions = [{'port':m.group(1), 
         'partition':m.group(2)} for m in (partition_re.match(line) for line in self.config) if m]
        for match in [m for m in (vpls_re.match(line) for line in self.config) if m]:
            vpls_vlan_re = re.compile(f"configure l2vpn vpls {match.group(1)} add service vlan (.*?)$")
            vpls_peer_core_re = re.compile(f"configure l2vpn vpls {match.group(1)} add peer (.*?) core full-mesh")
            vpls_peer_spoke_re = re.compile(f"configure l2vpn vpls {match.group(1)} add peer (.*?) spoke")
            vlan = [m.group(1) for m in (vpls_vlan_re.match(line) for line in self.config) if m]
            if vlan:
                vlan = vlan[0]
            peers_core = [{'ip':m.group(1), 
             'type':'core',  'type2':'full-mesh'} for m in (vpls_peer_core_re.match(line) for line in self.config) if m]
            peers_spoke = [{'ip':m.group(1), 
             'type':'spoke',  'type2':''} for m in (vpls_peer_spoke_re.match(line) for line in self.config) if m]
            vpls = {'name':match.group(1), 
             'pwid':match.group(2), 
             'vlan':vlan, 
             'peers':peers_core + peers_spoke}
            self.vpls.append(vpls)
        else:
            for vlan_name in [m.group(1) for m in (vlan_create_re.match(line) for line in self.config) if m]:
                vlan = {'name':vlan_name, 
                 'tag':'', 
                 'ip':'', 
                 'bfd':False, 
                 'acl':'', 
                 'loopback':False, 
                 'ipforwarding':False, 
                 'disable_snooping':False, 
                 'disable_igmp':False, 
                 'tagged_ports':[],  'untagged_ports':[],  'ospf':{'enable':False, 
                  'area':'', 
                  'type':'', 
                  'priority':None, 
                  'cost':None}, 
                 'mpls':{'enable':False, 
                  'ldp':False,  'rsvp':False}}
                for cmd in self.config:
                    if vlan_name in cmd:
                        if ' tag ' in cmd:
                            vlan['tag'] = cmd.split(' tag ')[1]
                        else:
                            if ' ipaddress ' in cmd:
                                vlan['ip'] = cmd.split(' ipaddress ')[1]
                            if 'enable loopback-mode vlan' in cmd:
                                vlan['loopback'] = True
                            if 'enable bfd vlan "' + vlan_name in cmd:
                                vlan['bfd'] = True
                            if 'disable igmp vlan "' + vlan_name in cmd:
                                vlan['disable_igmp'] = True
                            if 'disable igmp snooping vlan "' + vlan_name in cmd:
                                vlan['disable_snooping'] = True
                            if 'enable ipforwarding vlan' in cmd:
                                vlan['ipforwarding'] = True
                            if ' add ports ' in cmd:
                                if ' tagged' in cmd:
                                    vlan['tagged_ports'] = vlan['tagged_ports'] + self.expandports(cmd.split('add ports')[1].split('tagged')[0])
                                else:
                                    vlan['untagged_ports'] = vlan['untagged_ports'] + self.expandports(cmd.split('add ports')[1].split('untagged')[0])
                        if 'configure access-list NoiseFilterProfile' in cmd:
                            vlan['acl'] = cmd.split(' ')[2]
                        if 'enable mpls vlan' in cmd:
                            vlan['mpls']['enable'] = True
                        if 'enable mpls rsvp-te vlan' in cmd:
                            vlan['mpls']['rsvp'] = True
                        if 'enable mpls ldp vlan' in cmd:
                            vlan['mpls']['ldp'] = True
                    if 'configure ospf add vlan' in cmd:
                        vlan['ospf']['enable'] = True
                        vlan['ospf']['area'] = cmd.split('area')[1].split(' ')[1].strip()
                        if 'point-to-point' in cmd:
                            vlan['ospf']['type'] = 'point-to-point'
                        else:
                            if 'passive' in cmd:
                                vlan['ospf']['type'] = 'passive'

                if 'configure ospf vlan' in cmd:
                    if ' cost ' in cmd:
                        vlan['ospf']['cost'] = cmd.split(' cost ')[1]
                    if ' priority ' in cmd:
                        vlan['ospf']['priority'] = cmd.split(' priority ')[1]
                    self.vlans.append(vlan)
            else:
                port_scratch = {}
                for match in [m for m in (port_name_re.match(line) for line in self.config) if m]:
                    port = match.group(2)
                    if port not in port_scratch.keys():
                        port_scratch[port] = {'interface':port,  'description':'', 
                         'display':'', 
                         'sharing':{'enable':False, 
                          'grouping':[],  'algorithm':''}}
                    if match.group(3) == 'description-string':
                        port_scratch[port]['description'] = match.group(4).replace('"', '')
                    if match.group(3) == 'display-string':
                        port_scratch[port]['display'] = match.group(4)
                else:
                    for match in [m for m in (sharing_re.match(line) for line in self.config) if m]:
                        port = match.group(2)
                        if port in port_scratch.keys():
                            port_scratch[port]['sharing'] = {'enable':True,  'grouping':self.expandports(match.group(3)), 
                             'algorithm':match.group(4)}
                    else:
                        self.ports = list(port_scratch.values())

    def _compresslist(self, port_list):
        """
        A helper function for the compressports method that does the hard work

        :param port_list:
        :return:
        """
        port_list = list(map(int, port_list))
        result = []
        i = 0
        n = len(port_list)
        port_list.sort()
        while i < n:
            j = i
            if j + 1 < n and port_list[(j + 1)] == port_list[j] + 1:
                j += 1
            elif i == j:
                result.append(port_list[i])
                i += 1
            else:
                result.append(f"{port_list[i]}-{port_list[j]}")
                i = j + 1

        return result

    def _regex_search_list(self, search_term, search_list, expression):
        """
        A helper method to search a list of strings for a regular expression

        :param search_term:
        :param search_list:
        :param expression:
        :return:
        """
        found = False
        search_match = expression.match(search_term)
        if search_match:
            for item in search_list:
                match_item = expression.match(item)
                if match_item and match_item.group() == search_match.group():
                    found = True
                    continue

        return found

    def get_delete_command--- This code section failed: ---

 L. 342         0  LOAD_STR                 'rate-limit flood'
                2  LOAD_FAST                'cmd'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    38  'to 38'

 L. 343         8  LOAD_STR                 ' '
               10  LOAD_METHOD              join
               12  LOAD_FAST                'cmd'
               14  LOAD_METHOD              split
               16  LOAD_STR                 ' '
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               None
               22  LOAD_CONST               -1
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'no-limit'
               30  BUILD_LIST_1          1 
               32  BINARY_ADD       
               34  CALL_METHOD_1         1  ''
               36  RETURN_VALUE     
             38_0  COME_FROM             6  '6'

 L. 345        38  LOAD_STR                 'enable sharing'
               40  LOAD_FAST                'cmd'
               42  COMPARE_OP               in
               44  POP_JUMP_IF_FALSE    78  'to 78'

 L. 346        46  LOAD_STR                 ' '
               48  LOAD_METHOD              join
               50  LOAD_FAST                'cmd'
               52  LOAD_METHOD              split
               54  LOAD_STR                 ' '
               56  CALL_METHOD_1         1  ''
               58  LOAD_CONST               None
               60  LOAD_CONST               3
               62  BUILD_SLICE_2         2 
               64  BINARY_SUBSCR    
               66  CALL_METHOD_1         1  ''
               68  LOAD_METHOD              replace
               70  LOAD_STR                 'enable'
               72  LOAD_STR                 'disable'
               74  CALL_METHOD_2         2  ''
               76  RETURN_VALUE     
             78_0  COME_FROM            44  '44'

 L. 348        78  LOAD_STR                 'create vlan'
               80  LOAD_FAST                'cmd'
               82  COMPARE_OP               in
               84  POP_JUMP_IF_TRUE     94  'to 94'
               86  LOAD_STR                 'create meter'
               88  LOAD_FAST                'cmd'
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   106  'to 106'
             94_0  COME_FROM            84  '84'

 L. 349        94  LOAD_FAST                'cmd'
               96  LOAD_METHOD              replace
               98  LOAD_STR                 'create'
              100  LOAD_STR                 'delete'
              102  CALL_METHOD_2         2  ''
              104  RETURN_VALUE     
            106_0  COME_FROM            92  '92'

 L. 351       106  LOAD_STR                 'configure vlan'
              108  LOAD_FAST                'cmd'
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   188  'to 188'

 L. 352       114  LOAD_STR                 'tagged'
              116  LOAD_FAST                'cmd'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L. 353       122  LOAD_FAST                'cmd'
              124  LOAD_METHOD              replace
              126  LOAD_STR                 'add'
              128  LOAD_STR                 'delete'
              130  CALL_METHOD_2         2  ''
              132  RETURN_VALUE     
            134_0  COME_FROM           120  '120'

 L. 354       134  LOAD_STR                 'untagged'
              136  LOAD_FAST                'cmd'
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L. 355       142  LOAD_FAST                'cmd'
              144  LOAD_METHOD              replace
              146  LOAD_STR                 'add'
              148  LOAD_STR                 'delete'
              150  CALL_METHOD_2         2  ''
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L. 356       154  LOAD_STR                 'ipaddress'
              156  LOAD_FAST                'cmd'
              158  COMPARE_OP               in
              160  POP_JUMP_IF_FALSE   188  'to 188'

 L. 358       162  LOAD_FAST                'cmd'
              164  LOAD_METHOD              replace
              166  LOAD_STR                 'configure'
              168  LOAD_STR                 'unconfigure'
              170  CALL_METHOD_2         2  ''
              172  LOAD_METHOD              split
              174  LOAD_STR                 'ipaddress'
              176  CALL_METHOD_1         1  ''
              178  LOAD_CONST               0
              180  BINARY_SUBSCR    

 L. 359       182  LOAD_STR                 'ipaddress'

 L. 358       184  BINARY_ADD       

 L. 357       186  RETURN_VALUE     
            188_0  COME_FROM           160  '160'
            188_1  COME_FROM           112  '112'

 L. 363       188  LOAD_STR                 'disable igmp snooping vlan'
              190  LOAD_FAST                'cmd'
              192  COMPARE_OP               in

 L. 362   194_196  POP_JUMP_IF_TRUE    278  'to 278'

 L. 364       198  LOAD_STR                 'disable igmp vlan'
              200  LOAD_FAST                'cmd'
              202  COMPARE_OP               in

 L. 362   204_206  POP_JUMP_IF_TRUE    278  'to 278'

 L. 365       208  LOAD_STR                 'disable lldp ports'
              210  LOAD_FAST                'cmd'
              212  COMPARE_OP               in

 L. 362   214_216  POP_JUMP_IF_TRUE    278  'to 278'

 L. 366       218  LOAD_STR                 'disable edp ports'
              220  LOAD_FAST                'cmd'
              222  COMPARE_OP               in

 L. 362   224_226  POP_JUMP_IF_TRUE    278  'to 278'

 L. 367       228  LOAD_STR                 'disable learning port'
              230  LOAD_FAST                'cmd'
              232  COMPARE_OP               in

 L. 362   234_236  POP_JUMP_IF_TRUE    278  'to 278'

 L. 368       238  LOAD_STR                 'disable learning vlan'
              240  LOAD_FAST                'cmd'
              242  COMPARE_OP               in

 L. 362   244_246  POP_JUMP_IF_TRUE    278  'to 278'

 L. 369       248  LOAD_STR                 'disable port'
              250  LOAD_FAST                'cmd'
              252  COMPARE_OP               in

 L. 362   254_256  POP_JUMP_IF_TRUE    278  'to 278'

 L. 370       258  LOAD_STR                 'disable snmp access'
              260  LOAD_FAST                'cmd'
              262  COMPARE_OP               in

 L. 362   264_266  POP_JUMP_IF_TRUE    278  'to 278'

 L. 371       268  LOAD_STR                 'disable jumbo-frame ports'
              270  LOAD_FAST                'cmd'
              272  COMPARE_OP               in

 L. 362   274_276  POP_JUMP_IF_FALSE   290  'to 290'
            278_0  COME_FROM           264  '264'
            278_1  COME_FROM           254  '254'
            278_2  COME_FROM           244  '244'
            278_3  COME_FROM           234  '234'
            278_4  COME_FROM           224  '224'
            278_5  COME_FROM           214  '214'
            278_6  COME_FROM           204  '204'
            278_7  COME_FROM           194  '194'

 L. 373       278  LOAD_FAST                'cmd'
              280  LOAD_METHOD              replace
              282  LOAD_STR                 'disable'
              284  LOAD_STR                 'enable'
              286  CALL_METHOD_2         2  ''
              288  RETURN_VALUE     
            290_0  COME_FROM           274  '274'

 L. 376       290  LOAD_STR                 'configure ssh2 enable'
              292  LOAD_FAST                'cmd'
              294  COMPARE_OP               in

 L. 375   296_298  POP_JUMP_IF_TRUE    400  'to 400'

 L. 377       300  LOAD_STR                 'enable cdp port'
              302  LOAD_FAST                'cmd'
              304  COMPARE_OP               in

 L. 375   306_308  POP_JUMP_IF_TRUE    400  'to 400'

 L. 378       310  LOAD_STR                 'enable snmp access'
              312  LOAD_FAST                'cmd'
              314  COMPARE_OP               in

 L. 375   316_318  POP_JUMP_IF_TRUE    400  'to 400'

 L. 379       320  LOAD_STR                 'enable web'
              322  LOAD_FAST                'cmd'
              324  COMPARE_OP               in

 L. 375   326_328  POP_JUMP_IF_TRUE    400  'to 400'

 L. 380       330  LOAD_STR                 'enable dhcp vlan'
              332  LOAD_FAST                'cmd'
              334  COMPARE_OP               in

 L. 375   336_338  POP_JUMP_IF_TRUE    400  'to 400'

 L. 381       340  LOAD_STR                 'enable jumbo-frame ports'
              342  LOAD_FAST                'cmd'
              344  COMPARE_OP               in

 L. 375   346_348  POP_JUMP_IF_TRUE    400  'to 400'

 L. 382       350  LOAD_STR                 'enable ipforwarding vlan'
              352  LOAD_FAST                'cmd'
              354  COMPARE_OP               in

 L. 375   356_358  POP_JUMP_IF_TRUE    400  'to 400'

 L. 383       360  LOAD_STR                 'enable bfd vlan'
              362  LOAD_FAST                'cmd'
              364  COMPARE_OP               in

 L. 375   366_368  POP_JUMP_IF_TRUE    400  'to 400'

 L. 384       370  LOAD_STR                 'enable mpls vlan'
              372  LOAD_FAST                'cmd'
              374  COMPARE_OP               in

 L. 375   376_378  POP_JUMP_IF_TRUE    400  'to 400'

 L. 385       380  LOAD_STR                 'enable mpls ldp vlan'
              382  LOAD_FAST                'cmd'
              384  COMPARE_OP               in

 L. 375   386_388  POP_JUMP_IF_TRUE    400  'to 400'

 L. 386       390  LOAD_STR                 'enable mpls bfd vlan'
              392  LOAD_FAST                'cmd'
              394  COMPARE_OP               in

 L. 375   396_398  POP_JUMP_IF_FALSE   412  'to 412'
            400_0  COME_FROM           386  '386'
            400_1  COME_FROM           376  '376'
            400_2  COME_FROM           366  '366'
            400_3  COME_FROM           356  '356'
            400_4  COME_FROM           346  '346'
            400_5  COME_FROM           336  '336'
            400_6  COME_FROM           326  '326'
            400_7  COME_FROM           316  '316'
            400_8  COME_FROM           306  '306'
            400_9  COME_FROM           296  '296'

 L. 388       400  LOAD_FAST                'cmd'
              402  LOAD_METHOD              replace
              404  LOAD_STR                 'enable'
              406  LOAD_STR                 'disable'
              408  CALL_METHOD_2         2  ''
              410  RETURN_VALUE     
            412_0  COME_FROM           396  '396'

 L. 390       412  LOAD_STR                 'create fdbentry'
              414  LOAD_FAST                'cmd'
              416  COMPARE_OP               in
          418_420  POP_JUMP_IF_TRUE    432  'to 432'
              422  LOAD_STR                 'create fdb'
              424  LOAD_FAST                'cmd'
              426  COMPARE_OP               in
          428_430  POP_JUMP_IF_FALSE   458  'to 458'
            432_0  COME_FROM           418  '418'

 L. 391       432  LOAD_FAST                'cmd'
              434  LOAD_METHOD              replace
              436  LOAD_STR                 'create'
              438  LOAD_STR                 'delete'
              440  CALL_METHOD_2         2  ''
              442  LOAD_METHOD              split
              444  LOAD_STR                 'port'
              446  CALL_METHOD_1         1  ''
              448  LOAD_CONST               0
              450  BINARY_SUBSCR    
              452  LOAD_METHOD              strip
              454  CALL_METHOD_0         0  ''
              456  RETURN_VALUE     
            458_0  COME_FROM           428  '428'

 L. 393       458  LOAD_STR                 'enable sflow ports'
              460  LOAD_FAST                'cmd'
              462  COMPARE_OP               in
          464_466  POP_JUMP_IF_FALSE   500  'to 500'

 L. 394       468  LOAD_STR                 ' '
              470  LOAD_METHOD              join
              472  LOAD_FAST                'cmd'
              474  LOAD_METHOD              split
              476  LOAD_STR                 ' '
              478  CALL_METHOD_1         1  ''
              480  LOAD_CONST               None
              482  LOAD_CONST               -1
              484  BUILD_SLICE_2         2 
              486  BINARY_SUBSCR    
              488  CALL_METHOD_1         1  ''
              490  LOAD_METHOD              replace
              492  LOAD_STR                 'enable'
              494  LOAD_STR                 'disable'
              496  CALL_METHOD_2         2  ''
              498  RETURN_VALUE     
            500_0  COME_FROM           464  '464'

 L. 396       500  LOAD_STR                 'description-string'
              502  LOAD_FAST                'cmd'
              504  COMPARE_OP               in
          506_508  POP_JUMP_IF_FALSE   536  'to 536'

 L. 398       510  LOAD_FAST                'cmd'
              512  LOAD_METHOD              replace
              514  LOAD_STR                 'configure'
              516  LOAD_STR                 'unconfigure'
              518  CALL_METHOD_2         2  ''
              520  LOAD_METHOD              split
              522  LOAD_STR                 'description-string'
              524  CALL_METHOD_1         1  ''
              526  LOAD_CONST               0
              528  BINARY_SUBSCR    

 L. 399       530  LOAD_STR                 'description-string'

 L. 398       532  BINARY_ADD       

 L. 397       534  RETURN_VALUE     
            536_0  COME_FROM           506  '506'

 L. 402       536  LOAD_STR                 'display-string'
              538  LOAD_FAST                'cmd'
              540  COMPARE_OP               in
          542_544  POP_JUMP_IF_FALSE   572  'to 572'

 L. 404       546  LOAD_FAST                'cmd'
              548  LOAD_METHOD              replace
              550  LOAD_STR                 'configure'
              552  LOAD_STR                 'unconfigure'
              554  CALL_METHOD_2         2  ''
              556  LOAD_METHOD              split
              558  LOAD_STR                 'display-string'
              560  CALL_METHOD_1         1  ''
              562  LOAD_CONST               0
              564  BINARY_SUBSCR    

 L. 405       566  LOAD_STR                 'display-string'

 L. 404       568  BINARY_ADD       

 L. 403       570  RETURN_VALUE     
            572_0  COME_FROM           542  '542'

 L. 408       572  LOAD_STR                 'configure sharing'
              574  LOAD_FAST                'cmd'
              576  COMPARE_OP               in
          578_580  POP_JUMP_IF_FALSE   596  'to 596'
              582  LOAD_STR                 'lacp system-priority'
              584  LOAD_FAST                'cmd'
              586  COMPARE_OP               in
          588_590  POP_JUMP_IF_FALSE   596  'to 596'

 L. 410       592  LOAD_CONST               False
              594  RETURN_VALUE     
            596_0  COME_FROM           588  '588'
            596_1  COME_FROM           578  '578'

 L. 412       596  LOAD_STR                 'configure vlan'
              598  LOAD_FAST                'cmd'
              600  COMPARE_OP               in
          602_604  POP_JUMP_IF_FALSE   620  'to 620'
              606  LOAD_STR                 'tag'
              608  LOAD_FAST                'cmd'
              610  COMPARE_OP               in
          612_614  POP_JUMP_IF_FALSE   620  'to 620'

 L. 414       616  LOAD_CONST               False
              618  RETURN_VALUE     
            620_0  COME_FROM           612  '612'
            620_1  COME_FROM           602  '602'

 L. 416       620  LOAD_STR                 'configure timezone name'
              622  LOAD_FAST                'cmd'
              624  COMPARE_OP               in
          626_628  POP_JUMP_IF_FALSE   634  'to 634'

 L. 418       630  LOAD_CONST               False
              632  RETURN_VALUE     
            634_0  COME_FROM           626  '626'

 L. 420       634  LOAD_STR                 'create l2vpn vpws'
              636  LOAD_FAST                'cmd'
              638  COMPARE_OP               in
          640_642  POP_JUMP_IF_FALSE   666  'to 666'

 L. 421       644  LOAD_FAST                'cmd'
              646  LOAD_METHOD              replace
              648  LOAD_STR                 'create'
              650  LOAD_STR                 'delete'
              652  CALL_METHOD_2         2  ''
              654  LOAD_METHOD              split
              656  LOAD_STR                 'fec-id-type'
              658  CALL_METHOD_1         1  ''
              660  LOAD_CONST               0
              662  BINARY_SUBSCR    
              664  RETURN_VALUE     
            666_0  COME_FROM           640  '640'

 L. 423       666  LOAD_STR                 'configure l2vpn vpws'
              668  LOAD_FAST                'cmd'
              670  COMPARE_OP               in
          672_674  POP_JUMP_IF_FALSE   770  'to 770'

 L. 424       676  LOAD_STR                 'add peer'
              678  LOAD_FAST                'cmd'
              680  COMPARE_OP               in
          682_684  POP_JUMP_IF_FALSE   712  'to 712'

 L. 425       686  LOAD_FAST                'cmd'
              688  LOAD_METHOD              replace
              690  LOAD_STR                 'add'
              692  LOAD_STR                 'delete'
              694  CALL_METHOD_2         2  ''
              696  LOAD_METHOD              split
              698  LOAD_STR                 'peer'
              700  CALL_METHOD_1         1  ''
              702  LOAD_CONST               0
              704  BINARY_SUBSCR    
              706  LOAD_STR                 'peer'
              708  BINARY_ADD       
              710  RETURN_VALUE     
            712_0  COME_FROM           682  '682'

 L. 426       712  LOAD_STR                 'add service vlan'
              714  LOAD_FAST                'cmd'
              716  COMPARE_OP               in
          718_720  POP_JUMP_IF_FALSE   734  'to 734'

 L. 427       722  LOAD_FAST                'cmd'
              724  LOAD_METHOD              replace
              726  LOAD_STR                 'add service vlan'
              728  LOAD_STR                 'delete service vlan'
              730  CALL_METHOD_2         2  ''
              732  RETURN_VALUE     
            734_0  COME_FROM           718  '718'

 L. 428       734  LOAD_STR                 'add service vman'
              736  LOAD_FAST                'cmd'
              738  COMPARE_OP               in
          740_742  POP_JUMP_IF_FALSE   756  'to 756'

 L. 429       744  LOAD_FAST                'cmd'
              746  LOAD_METHOD              replace
              748  LOAD_STR                 'add service vman'
              750  LOAD_STR                 'delete service vman'
              752  CALL_METHOD_2         2  ''
              754  RETURN_VALUE     
            756_0  COME_FROM           740  '740'

 L. 431       756  LOAD_STR                 'mtu'
              758  LOAD_FAST                'cmd'
              760  COMPARE_OP               in
          762_764  POP_JUMP_IF_FALSE   770  'to 770'

 L. 432       766  LOAD_CONST               False
              768  RETURN_VALUE     
            770_0  COME_FROM           762  '762'
            770_1  COME_FROM           672  '672'

 L. 434       770  LOAD_STR                 'create account'
              772  LOAD_FAST                'cmd'
              774  COMPARE_OP               in
          776_778  POP_JUMP_IF_FALSE   830  'to 830'

 L. 436       780  LOAD_FAST                'cmd'
              782  LOAD_METHOD              replace
              784  LOAD_STR                 'create'
              786  LOAD_STR                 'delete'
              788  CALL_METHOD_2         2  ''
              790  LOAD_METHOD              replace

 L. 437       792  LOAD_STR                 'user'

 L. 437       794  LOAD_STR                 ''

 L. 436       796  CALL_METHOD_2         2  ''
              798  LOAD_METHOD              replace

 L. 438       800  LOAD_STR                 'admin'

 L. 438       802  LOAD_STR                 ''

 L. 436       804  CALL_METHOD_2         2  ''
              806  LOAD_METHOD              replace

 L. 439       808  LOAD_STR                 '  '

 L. 439       810  LOAD_STR                 ' '

 L. 436       812  CALL_METHOD_2         2  ''
              814  LOAD_METHOD              split

 L. 440       816  LOAD_STR                 'encrypted'

 L. 436       818  CALL_METHOD_1         1  ''

 L. 440       820  LOAD_CONST               0

 L. 436       822  BINARY_SUBSCR    
              824  LOAD_METHOD              strip
              826  CALL_METHOD_0         0  ''

 L. 435       828  RETURN_VALUE     
            830_0  COME_FROM           776  '776'

 L. 444       830  LOAD_STR                 'configure ospf add vlan'
              832  LOAD_FAST                'cmd'
              834  COMPARE_OP               in
          836_838  POP_JUMP_IF_FALSE   862  'to 862'

 L. 445       840  LOAD_FAST                'cmd'
              842  LOAD_METHOD              replace
              844  LOAD_STR                 'add vlan'
              846  LOAD_STR                 'delete vlan'
              848  CALL_METHOD_2         2  ''
              850  LOAD_METHOD              split
              852  LOAD_STR                 'area'
              854  CALL_METHOD_1         1  ''
              856  LOAD_CONST               0
              858  BINARY_SUBSCR    
              860  RETURN_VALUE     
            862_0  COME_FROM           836  '836'

 L. 447       862  LOAD_STR                 'configure ospf vlan'
              864  LOAD_FAST                'cmd'
              866  COMPARE_OP               in
          868_870  POP_JUMP_IF_FALSE   922  'to 922'

 L. 448       872  LOAD_STR                 ' cost '
              874  LOAD_FAST                'cmd'
              876  COMPARE_OP               in
          878_880  POP_JUMP_IF_FALSE   900  'to 900'

 L. 449       882  LOAD_FAST                'cmd'
              884  LOAD_METHOD              split
              886  LOAD_STR                 ' cost '
              888  CALL_METHOD_1         1  ''
              890  LOAD_CONST               0
              892  BINARY_SUBSCR    
              894  LOAD_STR                 ' automatic'
              896  BINARY_ADD       
              898  RETURN_VALUE     
            900_0  COME_FROM           878  '878'

 L. 450       900  LOAD_STR                 ' bfd on'
              902  LOAD_FAST                'cmd'
              904  COMPARE_OP               in
          906_908  POP_JUMP_IF_FALSE   922  'to 922'

 L. 451       910  LOAD_FAST                'cmd'
              912  LOAD_METHOD              replace
              914  LOAD_STR                 'bfd on'
              916  LOAD_STR                 'bfd off'
              918  CALL_METHOD_2         2  ''
              920  RETURN_VALUE     
            922_0  COME_FROM           906  '906'
            922_1  COME_FROM           868  '868'

 L. 453       922  LOAD_STR                 'configure ports'
              924  LOAD_FAST                'cmd'
              926  COMPARE_OP               in
          928_930  POP_JUMP_IF_FALSE   946  'to 946'

 L. 454       932  LOAD_STR                 'partition'
              934  LOAD_FAST                'cmd'
              936  COMPARE_OP               in
          938_940  POP_JUMP_IF_FALSE   946  'to 946'

 L. 456       942  LOAD_CONST               False
              944  RETURN_VALUE     
            946_0  COME_FROM           938  '938'
            946_1  COME_FROM           928  '928'

 L. 458       946  LOAD_STR                 'create l2vpn vpls'
              948  LOAD_FAST                'cmd'
              950  COMPARE_OP               in
          952_954  POP_JUMP_IF_FALSE   988  'to 988'

 L. 459       956  LOAD_STR                 ' '
              958  LOAD_METHOD              join
              960  LOAD_FAST                'cmd'
              962  LOAD_METHOD              replace
              964  LOAD_STR                 'create'
              966  LOAD_STR                 'delete'
              968  CALL_METHOD_2         2  ''
              970  LOAD_METHOD              split
              972  LOAD_STR                 ' '
              974  CALL_METHOD_1         1  ''
              976  LOAD_CONST               None
              978  LOAD_CONST               4
              980  BUILD_SLICE_2         2 
              982  BINARY_SUBSCR    
              984  CALL_METHOD_1         1  ''
              986  RETURN_VALUE     
            988_0  COME_FROM           952  '952'

 L. 461       988  LOAD_STR                 'configure l2vpn vpls'
              990  LOAD_FAST                'cmd'
              992  COMPARE_OP               in
          994_996  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 462       998  LOAD_STR                 'add service vlan'
             1000  LOAD_FAST                'cmd'
             1002  COMPARE_OP               in
         1004_1006  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 463      1008  LOAD_FAST                'cmd'
             1010  LOAD_METHOD              replace
             1012  LOAD_STR                 'add service vlan'
             1014  LOAD_STR                 'delete service vlan'
             1016  CALL_METHOD_2         2  ''
             1018  RETURN_VALUE     
           1020_0  COME_FROM          1004  '1004'

 L. 464      1020  LOAD_STR                 'add peer'
             1022  LOAD_FAST                'cmd'
             1024  COMPARE_OP               in
         1026_1028  POP_JUMP_IF_FALSE  1062  'to 1062'

 L. 465      1030  LOAD_STR                 ' '
             1032  LOAD_METHOD              join
             1034  LOAD_FAST                'cmd'
             1036  LOAD_METHOD              replace
             1038  LOAD_STR                 'add peer'
             1040  LOAD_STR                 'delete peer'
             1042  CALL_METHOD_2         2  ''
             1044  LOAD_METHOD              split
             1046  LOAD_STR                 ' '
             1048  CALL_METHOD_1         1  ''
             1050  LOAD_CONST               None
             1052  LOAD_CONST               -2
             1054  BUILD_SLICE_2         2 
             1056  BINARY_SUBSCR    
             1058  CALL_METHOD_1         1  ''
             1060  RETURN_VALUE     
           1062_0  COME_FROM          1026  '1026'

 L. 467      1062  LOAD_STR                 'mtu'
             1064  LOAD_FAST                'cmd'
             1066  COMPARE_OP               in
         1068_1070  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 468      1072  LOAD_FAST                'cmd'
             1074  LOAD_METHOD              split
             1076  LOAD_STR                 'mtu'
             1078  CALL_METHOD_1         1  ''
             1080  LOAD_CONST               0
             1082  BINARY_SUBSCR    
             1084  LOAD_STR                 'mtu 1500'
             1086  BINARY_ADD       
             1088  RETURN_VALUE     
           1090_0  COME_FROM          1068  '1068'
           1090_1  COME_FROM           994  '994'

 L. 470      1090  LOAD_STR                 'configure meter'
             1092  LOAD_FAST                'cmd'
             1094  COMPARE_OP               in
         1096_1098  POP_JUMP_IF_FALSE  1104  'to 1104'

 L. 472      1100  LOAD_CONST               False
             1102  RETURN_VALUE     
           1104_0  COME_FROM          1096  '1096'

 L. 474      1104  LOAD_STR                 'configure sflow ports'
             1106  LOAD_FAST                'cmd'
             1108  COMPARE_OP               in
         1110_1112  POP_JUMP_IF_FALSE  1150  'to 1150'

 L. 475      1114  LOAD_STR                 'sample-rate'
             1116  LOAD_FAST                'cmd'
             1118  COMPARE_OP               in
         1120_1122  POP_JUMP_IF_FALSE  1146  'to 1146'

 L. 476      1124  LOAD_FAST                'cmd'
             1126  LOAD_METHOD              replace
             1128  LOAD_STR                 'configure'
             1130  LOAD_STR                 'unconfigure'
             1132  CALL_METHOD_2         2  ''
             1134  LOAD_METHOD              split
             1136  LOAD_STR                 'sample-rate'
             1138  CALL_METHOD_1         1  ''
             1140  LOAD_CONST               0
             1142  BINARY_SUBSCR    
             1144  RETURN_VALUE     
           1146_0  COME_FROM          1120  '1120'

 L. 477      1146  LOAD_CONST               False
             1148  RETURN_VALUE     
           1150_0  COME_FROM          1110  '1110'

 L. 479      1150  LOAD_STR                 'configure access-list'
             1152  LOAD_FAST                'cmd'
             1154  COMPARE_OP               in
         1156_1158  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 480      1160  LOAD_STR                 'ports '
             1162  LOAD_FAST                'cmd'
             1164  COMPARE_OP               in
         1166_1168  POP_JUMP_IF_FALSE  1206  'to 1206'
             1170  LOAD_STR                 'ingress'
             1172  LOAD_FAST                'cmd'
             1174  COMPARE_OP               in
         1176_1178  POP_JUMP_IF_FALSE  1206  'to 1206'

 L. 481      1180  LOAD_GLOBAL              str

 L. 482      1182  LOAD_GLOBAL              re
             1184  LOAD_METHOD              sub
             1186  LOAD_STR                 'access-list (.*?) ports'
             1188  LOAD_STR                 'access-list ports'
             1190  LOAD_FAST                'cmd'
             1192  CALL_METHOD_3         3  ''

 L. 481      1194  CALL_FUNCTION_1       1  ''
             1196  LOAD_METHOD              replace

 L. 483      1198  LOAD_STR                 'configure'

 L. 483      1200  LOAD_STR                 'unconfigure'

 L. 481      1202  CALL_METHOD_2         2  ''
             1204  RETURN_VALUE     
           1206_0  COME_FROM          1176  '1176'
           1206_1  COME_FROM          1166  '1166'
           1206_2  COME_FROM          1156  '1156'

 L. 485      1206  LOAD_STR                 'configure mpls add vlan'
             1208  LOAD_FAST                'cmd'
             1210  COMPARE_OP               in
         1212_1214  POP_JUMP_IF_FALSE  1228  'to 1228'

 L. 486      1216  LOAD_FAST                'cmd'
             1218  LOAD_METHOD              replace
             1220  LOAD_STR                 'add vlan'
             1222  LOAD_STR                 'delete vlan'
             1224  CALL_METHOD_2         2  ''
             1226  RETURN_VALUE     
           1228_0  COME_FROM          1212  '1212'

 L. 489      1228  LOAD_GLOBAL              NotImplementedException
             1230  LOAD_STR                 'Cannot process: {}'
             1232  LOAD_METHOD              format
             1234  LOAD_FAST                'cmd'
             1236  CALL_METHOD_1         1  ''
             1238  CALL_FUNCTION_1       1  ''
             1240  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 1238

    def expandports(self, port_list):
        """
        Takes an arbitrary string of compressed ports and expands them to a list of single ports

        :param port_list:   A list of ports to compress (e.g. '1-3,5-6,9-10')
        :return:            Compressed list of ports (e.g. 1,2,3,5,6,9,10)
        """
        new_list = []
        ports = port_list.split(',')
        for p in ports:
            if '-' in p:
                if ':' in p:
                    mod, po = p.split(':')
                    s, e = po.split('-')
                    for i in list(range(int(s), int(e) + 1)):
                        new_list.append(str(mod) + ':' + str(i))

                else:
                    s, e = p.split('-')
                    new_list = new_list + [str(p) for p in list(range(int(s), int(e) + 1))]
            else:
                new_list.append(p.strip())
        else:
            return new_list

    def compressports(self, port_list):
        """
        Takes an arbitrary list of ports and returns a compressed list

        :param port_list:   A list of ports to compress (e.g. 1,2,3,5,6,9,10)
        :return:            Compressed list of ports (e.g. 1-3,5-6,9-10)
        """
        stack = {0: []}
        for item in port_list:
            if self._is_int(item):
                stack[0].append(item)
            else:
                if ':' in item:
                    module, port = item.split(':', 1)
                    module = int(module)
                    if module not in stack.keys():
                        stack[module] = []
                    stack[module].append(port)
                final_list = []
                modules = list(stack.keys())
                modules.sort()
                for module in modules:
                    ports = self._compresslist(stack[module])
                    if module != 0:
                        ports = [f"{module}:{p}" for p in ports]
                    final_list = final_list + ports
                else:
                    return list(map(str, final_list))

    def load_config(self, config):
        """
        Processes the running configuration loaded from the device, or from a flat file on create.

        :param config:  The raw device configuration
        :return:        None
        :raises:        ConfigParseException
        """
        self.config = []
        config = [line.strip() for line in config if line.strip() if not line.startswith('#')]
        for line in config:
            match_vlan_re = vlan_re.match(line)
            if match_vlan_re:
                match_vlan = match_vlan_re.group(2)
                match_ports = self.expandports(match_vlan_re.group(3))
                match_tag = match_vlan_re.group(4)
                if match_ports:
                    line = False
                    for port in match_ports:
                        self.config.append('configure vlan {} add ports {} {}'.formatmatch_vlanportmatch_tag)

        else:
            if line:
                self.config.append(line)
            try:
                self._process_config()
            except (ValueError, IndexError, IOError) as error:
                try:
                    raise ConfigParseException('Could not parse switch config: {}'.format(error))
                finally:
                    error = None
                    del error

    def diff_config_merge(self, new_config):
        """
        Builds a diff of the current config to the new config, to merge existing lines.
        e.g. Allowing running "create vlan XX" twice, without getting a CLI Config Error

        :param new_config:  A complete switch configuration
        :return:            A diff of changes from the running configration to merge the new config
        """
        if self.config is None:
            return False
        running_config = self.config
        candidate_config = running_config + [line.strip() for line in new_config if line.strip() if line.strip()[0] != '#']
        final_config = []
        for cmd in candidate_config:
            if cmd in running_config:
                pass
            elif 'enable sharing' in cmd and self._regex_search_listcmdrunning_configsharing_for_delete_re:
                pass
            elif 'configure access-list' in cmd and self._regex_search_listcmdrunning_configacl_re:
                pass
            else:
                final_config.append(cmd)
        else:
            return final_config

    def diff_config_replace(self, new_config, skip_lines=[]):
        """
        Builds a delta configuration that can be applied to transition the switch from the running config, to the new config. A 'Config Merge Replace' in any sane vendor.

        :param new_config:  A complete switch configuration
        "param skip_lines:  A list of any config lines you DO NOT WANT IN THE DIFF - Useful to remove things before applying.
        :return:            A list of changes to apply to the switch to transition to the new config.
        """
        to_delete = []
        new_config = [line.strip() for line in new_config if line.strip() if line.strip() not in skip_lines]
        for cmd in self.config:
            if cmd in new_config:
                pass
            elif self._regex_search_listcmdnew_configport_name_for_delete_re:
                pass
            elif self._regex_search_listcmdnew_configsharing_for_delete_re:
                pass
            else:
                cmd = self.get_delete_command(cmd)
                if cmd:
                    to_delete.append(cmd)
        else:
            to_delete_scratch = {'configure':[],  'unconfigure':[],  'enable':[],  'disable':[],  'create':[],  'delete':[]}

        for cmd in to_delete:
            to_delete_scratch[cmd.split(' ')[0]].append(cmd)
        else:
            changes = []
            for cmd_type in to_delete_scratch.keys():
                changes = changes + to_delete_scratch[cmd_type]
            else:
                new_cmds = self.diff_config_merge(new_config)
                return changes + new_cmds

    def open(self):
        """
        Opens a connection to the device

        :return: None
        :raises: SSHException
        """
        exos_type = {'ssh':'extreme', 
         'telnet':'extreme_telnet'}
        try:
            self.device = ConnectHandler(device_type=(exos_type[self.protocol]),
              ip=(self.ip),
              port=(self.port),
              username=(self.username),
              password=(self.password),
              ssh_config_file=(self.ssh_config_file))
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            try:
                raise SSHException(e)
            finally:
                e = None
                del e

    def close(self):
        """
        Closes connection to the device if open

        :return:    None
        """
        if hasattr(self.device, 'remote_conn'):
            self.device.remote_conn.close()

    def is_alive(self):
        """
        Check if connection to device is alive

        :return:    Boolean
        """
        if self.device:
            return self.device.remote_conn.transport.is_active()
        return False

    def get_running_config(self):
        if not self.is_alive():
            self.open()
        try:
            running_config = self.send_command('show configuration',
              save=False, delay_factor=30)
        except CLICommandException:
            raise
        else:
            self.load_config(running_config.splitlines())
            return self.config

    def send_command(self, command, save=True, delay_factor=1):
        """
        Send a single command to the device

        :param command:         (String) Configuration Statements to apply to switch
        :param save:            (Boolean) Save configuration
        :param delay_factor:    (Int) Netmiko Delay Factor (default: 1)
        :return:                (String) Output from device
        :raises:                CLICommandException, SSHException
        """
        if not self.is_alive():
            self.open()
        output = self.device.send_command(command, delay_factor=delay_factor)
        if '%% Invalid' in output or '%% A number' in output or '%% Incomplete command' in output:
            msg = f'Error sending command: "{command}" - ({output})'
            raise CLICommandException(msg)
        if save:
            output = output + self.device.save_config()
        return output

    def send_config_set(self, config=[], save=True):
        """
        Send a configuration set to the device

        :param config:  (List) Configuration Statements to apply to switch
        :param save:    (Boolean) Save configuration
        :return:        (List) A list of cli output for each command
        :raises:        CLICommandException, SSHException
        """
        if not self.is_alive():
            self.open()
        output = []
        try:
            for cmd in config:
                result = self.send_command(command=cmd, save=False)
                output.append({'command':cmd,  'output':result})

        except CLICommandException:
            if save:
                self.device.save_config()
            raise
        else:
            if save:
                output.append({'cmd':'save configuration', 
                 'output':self.device.save_config()})
            return output