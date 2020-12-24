# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/cisco/aci/__init__.py
# Compiled at: 2020-04-27 04:15:15
# Size of source mod 2**32: 18200 bytes
import jinja2
from jinjamator.external.acitoolkit.acisession import Session
import json, re, logging, getpass
from pprint import pprint
log = logging.getLogger()
switchdb = {'N9K-C93108TC-EX':{'uplinks':[
   49, 50, 51, 52, 53, 54], 
  'downlinks':range(1, 49), 
  'type':'leaf'}, 
 'N9K-C93108TC-FX':{'uplinks':[
   49, 50, 51, 52, 53, 54], 
  'downlinks':range(1, 49), 
  'type':'leaf'}, 
 'N9K-C93180YC-FX':{'uplinks':[
   49, 50, 51, 52, 53, 54], 
  'downlinks':range(1, 49), 
  'type':'leaf'}, 
 'N9K-C93240YC-FX2':{'uplinks':[
   49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], 
  'downlinks':range(1, 49), 
  'type':'leaf'}, 
 'N9K-C9348GC-FXP':{'uplinks':[
   53, 54], 
  'downlinks':range(1, 53),  'type':'leaf'}, 
 'N9K-C93180YC-EX':{'uplinks':[
   49, 50, 51, 52, 53, 54], 
  'downlinks':range(1, 49), 
  'type':'leaf'}, 
 'N2K-B22HP-P':{'uplinks':range(17, 25), 
  'downlinks':range(1, 17), 
  'type':'fex'}, 
 'N2K-C2248TP-1GE':{'uplinks':range(49, 53), 
  'downlinks':range(1, 49), 
  'type':'fex'}, 
 'N9K-C9364C':{'uplinks':[],  'downlinks':range(1, 67),  'type':'spine'},  'N9K-C9332C':{'uplinks':[],  'downlinks':range(1, 35),  'type':'spine'},  'N9K-C9336PQ':{'uplinks':[],  'downlinks':range(1, 37),  'type':'spine'},  'N9K-C93216TC-FX2':{'uplinks':range(96, 109), 
  'downlinks':range(1, 97), 
  'type':'leaf'}, 
 'N9K-C9396PX':{'uplinks':range(49, 61), 
  'downlinks':range(1, 49), 
  'type':'leaf'}}
log = logging.getLogger()

def connect_apic(subscription_enabled=False):
    if not self._parent.configuration['apic_url']:
        self._parent.handle_undefined_var('apic_url')
    else:
        if not self._parent.configuration['apic_username']:
            self._parent.handle_undefined_var('apic_username')
        else:
            if not self._parent.configuration['apic_key']:
                del self._parent.configuration['apic_key']
            if not self._parent.configuration['apic_cert_name']:
                del self._parent.configuration['apic_cert_name']
            if 'apic_key' in self._parent.configuration.keys() and 'apic_cert_name' in self._parent.configuration.keys():
                apic_session = Session((self._parent.configuration['apic_url']),
                  (self._parent.configuration['apic_username']),
                  cert_name=(self._parent.configuration['apic_cert_name']),
                  key=(self._parent.configuration['apic_key']),
                  subscription_enabled=False)
            else:
                self._parent.configuration['apic_password'] or self._parent.handle_undefined_var('apic_password')
        apic_session = Session((self._parent.configuration['apic_url']),
          (self._parent.configuration['apic_username']),
          (self._parent.configuration['apic_password']),
          subscription_enabled=subscription_enabled)
        apic_session.login()
    return apic_session


def query--- This code section failed: ---

 L. 119         0  LOAD_STR                 'subscription=yes'
                2  LOAD_FAST                'queryURL'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 120         8  LOAD_CONST               True
               10  STORE_FAST               'subscription_enabled'
               12  JUMP_FORWARD         18  'to 18'
             14_0  COME_FROM             6  '6'

 L. 122        14  LOAD_CONST               False
               16  STORE_FAST               'subscription_enabled'
             18_0  COME_FROM            12  '12'

 L. 123        18  LOAD_GLOBAL              connect_apic
               20  LOAD_FAST                'subscription_enabled'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'session'

 L. 124        26  SETUP_FINALLY        44  'to 44'

 L. 125        28  LOAD_FAST                'session'
               30  LOAD_METHOD              get
               32  LOAD_FAST                'queryURL'
               34  LOAD_FAST                'timeout'
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'data'
               40  POP_BLOCK        
               42  JUMP_FORWARD        110  'to 110'
             44_0  COME_FROM_FINALLY    26  '26'

 L. 126        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE   108  'to 108'
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        96  'to 96'

 L. 127        60  LOAD_GLOBAL              log
               62  LOAD_METHOD              error
               64  LOAD_FAST                'e'
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 128        70  LOAD_FAST                'session'
               72  LOAD_METHOD              close
               74  CALL_METHOD_0         0  ''
               76  POP_TOP          

 L. 129        78  BUILD_LIST_0          0 
               80  LOAD_STR                 '0'
               82  LOAD_CONST               ('imdata', 'totalCount')
               84  BUILD_CONST_KEY_MAP_2     2 
               86  ROT_FOUR         
               88  POP_BLOCK        
               90  POP_EXCEPT       
               92  CALL_FINALLY         96  'to 96'
               94  RETURN_VALUE     
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM_FINALLY    58  '58'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  END_FINALLY      
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
            108_0  COME_FROM            50  '50'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            42  '42'

 L. 130       110  LOAD_GLOBAL              json
              112  LOAD_METHOD              loads
              114  LOAD_FAST                'data'
              116  LOAD_ATTR                text
              118  CALL_METHOD_1         1  ''
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 88


def model_is_spine(model):
    if model in ('N9K-C9336PQ', 'N9K-C9364C', 'N9K-C9332C', 'N9K-C9504', 'N9K-C9508',
                 'N9K-C9516', 'N9K-C9332C'):
        return True
    return False


def get_leaf_types():
    return [switch for switch in switchdb.keys() if switchdb[switch]['type'] == 'leaf']


def get_spine_types():
    return [switch for switch in switchdb.keys() if switchdb[switch]['type'] == 'spine']


def get_fex_types():
    return [switch for switch in switchdb.keys() if switchdb[switch]['type'] == 'fex']


def model_is_leaf(model):
    if model.beginswith('APIC'):
        return False
    return not aci_model_is_spine(model)


def get_role_by_model(model):
    if aci_model_is_spine(model):
        return 'spine'
    if aci_model_is_leaf(model):
        return 'leaf'
    if model.beginswith('APIC'):
        return 'controller'
    return 'unspecified'


def get_all_uplinks(model):
    return switchdb[model.upper()]['uplinks']


def get_convertible_uplinks(model, count, min_uplinks=2):
    try:
        possible = switchdb[model]['uplinks'][-count:]
    except KeyError:
        return []
    else:
        if len(switchdb[model]['uplinks']) - len(possible) < min_uplinks:
            return []
        return possible


def get_all_downlinks(model):
    return switchdb[model.upper()]['downlinks']


def get_parent_dn_from_child_dn(dn):
    dn = re.sub('\\[\\S+\\]', '', dn)
    tmp = dn.split('/')
    return '/'.join(tmp[:-1])


def is_dn_in_use(dn, ignore_children=False):
    in_use = False
    retval = query('/api/node/mo/{0}.json?query-target=children'.format(dn))
    log.debug(retval)
    if int(retval['totalCount']) != len(retval['imdata']):
        log.warning('ACI API bug detected -> totalCount is {0} but {1} objects retured -> fixing up'.formatretval['totalCount']len(retval['imdata']))
        retval['totalCount'] = str(len(retval['imdata']))
    if int(retval['totalCount']) > 0:
        ignore_children or log.info('dn has child objects -> is in use')
        in_use = True
    else:
        if int(retval['totalCount']) > 0:
            if type(ignore_children) == list:
                for i in ignore_children:
                    log.info('dn has child objects -> ignoring {0} by user request'.format(i))
                    for x, child in enumerate(retval['imdata']):
                        if list(child.keys())[0] == i:
                            del retval['imdata'][x]

                else:
                    if len(retval['imdata']) > 0:
                        log.info('dn has child objects -> is in use')
                        in_use = True

        retval = query('/api/node/mo/{0}.json?query-target=children&target-subtree-class=relnFrom'.format(dn))
        log.debug(retval)
        in_use_count = 0
        if int(retval['totalCount']) > 0:
            for obj in retval['imdata']:
                in_use_count += 1
                try:
                    obj_type = list(obj.keys())[0]
                    if obj[obj_type]['attributes']['childAction'] in ('deleteNonPresent', ):
                        log.info('ignoring {0} with childAction deleteNonPresent relation'.format(obj_type))
                        in_use_count -= 1
                except KeyError:
                    pass

        if in_use_count > 0:
            log.info('object has active relnFrom objects -> is in use')
            in_use = True
        return in_use


def dn_exists(dn):
    data = query('/api/node/mo/{0}.json'.format(dn))
    if int(data['totalCount']) > 0:
        return True
    return False


def get_podid_by_switch_id(switch_id):
    data = query('/api/node/class/fabricNode.json?query-target-filter=and(eq(fabricNode.id,"{0}"))'.format(switch_id))
    return get_parent_dn_from_child_dn(data['imdata'][0]['fabricNode']['attributes']['dn']).split('/')[-1:][0].split('-')[1]


def version(node_id=1):
    pod_id = get_podid_by_switch_id(node_id)
    data = query('/api/node/class/topology/pod-{0}/node-{1}/firmwareCtrlrRunning.json'.formatpod_idnode_id)
    return data['imdata'][0]['firmwareCtrlrRunning']['attributes']['version']


def is_min_version(major, minor, patch_level, node_id=1):
    """
    {% if aci_is_min_version(4, 0, None) %}
    {% endif %}
    """
    running_version = aci_version(node_id)
    m = re.match'(?P<major>\\d+)\\.(?P<minor>\\d+)\\((?P<patchlevel>.+)\\)'running_version
    if int(major) <= int(m.group('major')):
        if minor != None:
            if int(minor) <= int(m.group('minor')):
                if patch_level != None:
                    if patch_level <= m.group('patchlevel'):
                        return True
                else:
                    return True
        else:
            return True
    return False


def get_next_free_vpc_domain_id():
    data = query('/api/node/class/fabricExplicitGEp.json?&order-by=fabricExplicitGEp.id|desc&page=0&page-size=1')
    if data['totalCount'] == '1':
        return int(data['imdata'][0]['fabricExplicitGEp']['attributes']['id']) + 1
    return 1


def get_access_aep_name_by_vlan_id--- This code section failed: ---

 L. 314         0  SETUP_FINALLY        62  'to 62'

 L. 315         2  LOAD_GLOBAL              query

 L. 316         4  LOAD_STR                 '/api/node/class/infraRsFuncToEpg.json?query-target-filter=and(wcard(infraRsFuncToEpg.dn,"{1}"),eq(infraRsFuncToEpg.encap,"vlan-{0}"),eq(infraRsFuncToEpg.mode,"untagged"))&order-by=infraRsFuncToEpg.dn'
                6  LOAD_METHOD              format

 L. 317         8  LOAD_FAST                'vlan_id'

 L. 317        10  LOAD_FAST                'dn_filter'

 L. 316        12  CALL_METHOD_2         2  ''

 L. 315        14  CALL_FUNCTION_1       1  ''

 L. 319        16  LOAD_STR                 'imdata'

 L. 315        18  BINARY_SUBSCR    

 L. 319        20  LOAD_CONST               0

 L. 315        22  BINARY_SUBSCR    

 L. 319        24  LOAD_STR                 'infraRsFuncToEpg'

 L. 315        26  BINARY_SUBSCR    

 L. 319        28  LOAD_STR                 'attributes'

 L. 315        30  BINARY_SUBSCR    
               32  STORE_FAST               'access_aep'

 L. 320        34  LOAD_FAST                'access_aep'
               36  LOAD_STR                 'dn'
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              split
               42  LOAD_STR                 '/'
               44  CALL_METHOD_1         1  ''
               46  LOAD_CONST               2
               48  BINARY_SUBSCR    
               50  LOAD_CONST               8
               52  LOAD_CONST               None
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY     0  '0'

 L. 321        62  DUP_TOP          
               64  LOAD_GLOBAL              IndexError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    94  'to 94'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 322        76  LOAD_GLOBAL              ValueError
               78  LOAD_STR                 'no AEP for vlan id {0} found'
               80  LOAD_METHOD              format
               82  LOAD_FAST                'vlan_id'
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            68  '68'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'

Parse error at or near `POP_TOP' instruction at offset 72


def get_all_vlans_from_pool(pool_name):
    data = query('/api/node/class/fvnsEncapBlk.json?query-target-filter=and(wcard(fvnsEncapBlk.dn,"{0}"))&order-by=fvnsEncapBlk.modTs|desc'.format(pool_name))
    vlan_ids = []
    for block in data['imdata']:
        from_id = int(block['fvnsEncapBlk']['attributes']['from'][5:])
        to_id = int(block['fvnsEncapBlk']['attributes']['to'][5:])
        vlan_ids = vlan_ids + list(range(from_id, to_id + 1))
    else:
        vlan_ids.sort()
        return vlan_ids


def vlan_pool_contains_vlan(pool_name, vlan_id):
    if vlan_id in get_all_vlans_from_pool(pool_name):
        return True
    return False


def dn_has_attribute--- This code section failed: ---

 L. 358         0  LOAD_STR                 '/api/node/mo/{0}.json'
                2  LOAD_METHOD              format
                4  LOAD_FAST                'dn'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'url'

 L. 359        10  LOAD_GLOBAL              self
               12  LOAD_ATTR                _parent
               14  LOAD_ATTR                _log
               16  LOAD_METHOD              debug
               18  LOAD_FAST                'url'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 360        24  LOAD_GLOBAL              query
               26  LOAD_FAST                'url'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_STR                 'imdata'
               32  BINARY_SUBSCR    
               34  GET_ITER         
               36  FOR_ITER            122  'to 122'
               38  STORE_FAST               'obj'

 L. 361        40  LOAD_FAST                'obj'
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  GET_ITER         
               48  FOR_ITER            120  'to 120'
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'k'
               54  STORE_FAST               'v'

 L. 362        56  SETUP_FINALLY        92  'to 92'

 L. 363        58  LOAD_FAST                'obj'
               60  LOAD_FAST                'k'
               62  BINARY_SUBSCR    
               64  LOAD_STR                 'attributes'
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'key'
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'value'
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 364        78  POP_BLOCK        
               80  POP_TOP          
               82  POP_TOP          
               84  LOAD_CONST               False
               86  RETURN_VALUE     
             88_0  COME_FROM            76  '76'
               88  POP_BLOCK        
               90  JUMP_BACK            48  'to 48'
             92_0  COME_FROM_FINALLY    56  '56'

 L. 365        92  DUP_TOP          
               94  LOAD_GLOBAL              IndexError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   116  'to 116'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 366       106  POP_EXCEPT       
              108  POP_TOP          
              110  POP_TOP          
              112  LOAD_CONST               False
              114  RETURN_VALUE     
            116_0  COME_FROM            98  '98'
              116  END_FINALLY      
              118  JUMP_BACK            48  'to 48'
              120  JUMP_BACK            36  'to 36'

 L. 367       122  LOAD_CONST               True
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 82


def get_all_configured_spine_uplinks():
    infra_ports = {}
    try:
        infra_port_blks = query('/api/node/class/infraSHPortS.json?query-target=children&target-subtree-class=infraPortBlk')['imdata']
        for infra_port_blk in infra_port_blks:
            info = query('/api/node/mo/{}.json?rsp-subtree-include=full-deployment'.format(infra_port_blk['infraPortBlk']['attributes']['dn']))['imdata'][0]
            node_id = info['infraPortBlk']['children'][0]['pconsNodeDeployCtx']['attributes']['nodeId']
            for card in range(int(infra_port_blk['infraPortBlk']['attributes']['fromCard']), int(infra_port_blk['infraPortBlk']['attributes']['toCard']) + 1):
                for interface in range(int(infra_port_blk['infraPortBlk']['attributes']['fromPort']), int(infra_port_blk['infraPortBlk']['attributes']['toPort']) + 1):
                    try:
                        infra_ports[node_id] += [(card, interface)]
                    except:
                        infra_ports[node_id] = [
                         (
                          card, interface)]

    except:
        pass
    else:
        return infra_ports


def get_all_fabric_ports():
    fab_ports = query('/api/node/class/eqptFabP.json')['imdata']
    retval = []
    for fab_port in fab_ports:
        tmp = fab_port['eqptFabP']['attributes']['dn'].split('/')
        pod_id = tmp[1].split('-')[1]
        node_id = tmp[2].split('-')[1]
        slot = tmp[5].split('-')[1]
        port = fab_port['eqptFabP']['attributes']['id']
        retval.append({'node_id':node_id, 
         'pod_id':pod_id, 
         'port':port, 
         'slot':slot, 
         'interface_name':'eth{0}/{1}'.formatslotport, 
         'long_interface_name':'Ethernet{0}/{1}'.formatslotport})
    else:
        return retval


def get_all_lldp_neighbours():
    lldp_neighbours = query('/api/node/class/lldpAdjEp.json')['imdata']
    retval = []
    localinterface_rgx = re.compile('.+\\[(\\S+)\\].+')
    for lldp_neighbour in lldp_neighbours:
        tmp = lldp_neighbour['lldpAdjEp']['attributes']['dn'].split('/')
        result = localinterface_rgx.match(lldp_neighbour['lldpAdjEp']['attributes']['dn'])
        lldp_neighbour['lldpAdjEp']['attributes']['pod_id'] = tmp[1].split('-')[1]
        lldp_neighbour['lldpAdjEp']['attributes']['node_id'] = tmp[2].split('-')[1]
        lldp_neighbour['lldpAdjEp']['attributes']['interface_name'] = result.group(1)
        retval.append(lldp_neighbour['lldpAdjEp']['attributes'])
    else:
        return retval


def get_all_nodes(index_by='id'):
    retval = {}
    fabric_nodes = query('/api/node/class/fabricNode.json')['imdata']
    for node in fabric_nodes:
        retval[node['fabricNode']['attributes'][index_by]] = node['fabricNode']['attributes']
    else:
        return retval


def get_endpoint_table():
    endpoint_data = {}
    vpc_fabric_path_ep_rxg = re.compile('topology/pod-(\\d+)/protpaths-(\\d+)-(\\d+)/pathep-\\[(.*)\\]')
    fabric_path_ep_rxg = re.compile('topology/pod-(\\d+)/paths-(\\d+)/pathep-\\[(.*)\\]')
    fex_fabric_path_ep_rxg = re.compile('topology/pod-(\\d+)/paths-(\\d+)/extpaths-(\\d+)/pathep-\\[(.*)\\]')
    for endpoint_obj in query('/api/node/class/fvCEp.json?query-target-filter=not(wcard(fvCEp.dn,"__ui_"))&rsp-subtree=children&target-subtree-class=fvRsCEpToPathEp')['imdata']:
        ip = endpoint_obj['fvCEp']['attributes']['ip']
        mac = endpoint_obj['fvCEp']['attributes']['mac']
        encap = endpoint_obj['fvCEp']['attributes']['encap']
        ep_dn = endpoint_obj['fvCEp']['attributes']['dn']
        for path_obj in endpoint_obj['fvCEp']['children']:
            switch_a = None
            switch_b = None
            fex_id = None
            if 'fvRsCEpToPathEp' in path_obj:
                path = path_obj['fvRsCEpToPathEp']['attributes']['tDn']
                result = vpc_fabric_path_ep_rxg.match(path)
                if result:
                    pod_id, switch_a, switch_b, interface = result.groups()
                else:
                    result = fabric_path_ep_rxg.match(path)
                    if result:
                        pod_id, switch_a, interface = result.groups()
                        switch_b = None
                    else:
                        result = fex_fabric_path_ep_rxg.match(path)
                        if result:
                            pod_id, switch_a, fex_id, interface = result.groups()
                        ds = {'ip':ip, 
                         'mac':mac,  'encap':encap}
                        if switch_a:
                            if switch_a not in endpoint_data:
                                endpoint_data[switch_a] = {}
                            elif fex_id and fex_id not in endpoint_data[switch_a]:
                                endpoint_data[switch_a][fex_id] = {}
                                if interface not in endpoint_data[switch_a][fex_id]:
                                    endpoint_data[switch_a][fex_id][interface] = []
                                endpoint_data[switch_a][fex_id][interface].append(ds)
                            if interface not in endpoint_data[switch_a]:
                                endpoint_data[switch_a][interface] = []
                            endpoint_data[switch_a][interface].append(ds)
                if switch_b:
                    if switch_b not in endpoint_data:
                        endpoint_data[switch_b] = {}
                    if interface not in endpoint_data[switch_b]:
                        endpoint_data[switch_b][interface] = []
                    endpoint_data[switch_b][interface].append(ds)
        else:
            return endpoint_data


def get_dict_from_epg_dn(dn):
    rgx = re.compile('uni/tn-(\\S+)/ap-(\\S+)/epg-(\\S+)')
    result = rgx.match(dn)
    if result:
        return {'tenant_name':result.group(1),  'ap_name':result.group(2), 
         'epg_name':result.group(3)}
    return


def get_dict_from_vrf_dn(dn):
    rgx = re.compile('uni/tn-(\\S+)/ctx-(\\S+)')
    result = rgx.match(dn)
    if result:
        return {'tenant_name':result.group(1),  'vrf_name':result.group(2)}
    return


def get_dict_from_external_epg_dn(dn):
    rgx = re.compile('uni/tn-(\\S+)/out-(\\S+)/instP-(\\S+)')
    result = rgx.match(dn)
    if result:
        return {'tenant_name':result.group(1),  'l3out_name':result.group(2), 
         'external_epg_name':result.group(3)}
    return