# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/prototypes/irati_templates.py
# Compiled at: 2018-07-25 06:09:26
# Size of source mod 2**32: 12636 bytes
env_dict = {'installpath':'/usr', 
 'varpath':''}

def get_ipcmconf_base():
    return {'configFileVersion':'1.4.1', 
     'localConfiguration':{'installationPath':'%(installpath)s/bin' % env_dict, 
      'libraryPath':'%(installpath)s/lib' % env_dict, 
      'logPath':'%(varpath)s/var/log' % env_dict, 
      'consoleSocket':'%(varpath)s/var/run/ipcm-console.sock' % env_dict, 
      'pluginsPaths':[
       '%(installpath)s/lib/rinad/ipcp' % env_dict,
       '/lib/modules/4.9.28-irati/extra']}, 
     'ipcProcessesToCreate':[],  'difConfigurations':[]}


da_map_base = {'applicationToDIFMappings': [
                              {'encodedAppName':'rina.apps.echotime.server-1--', 
                               'difName':'n.DIF'},
                              {'encodedAppName':'traffic.generator.server-1--', 
                               'difName':'n.DIF'}]}

def generate_qos_cube(name, cube_id, initial_credit=200, ordered=False, delay=None, loss=None, reliable=False, data_rxms_nmax=5, initial_rtx_time=1000):
    cube = {'name':name, 
     'id':cube_id, 
     'partialDelivery':False, 
     'orderedDelivery':ordered, 
     'efcpPolicies':{'dtpPolicySet':{'name':'default', 
       'version':'0'}, 
      'initialATimer':0, 
      'dtcpPresent':True, 
      'dtcpConfiguration':{'dtcpPolicySet':{'name':'default', 
        'version':'0'}, 
       'rtxControl':False, 
       'flowControl':True, 
       'flowControlConfig':{'rateBased':False, 
        'windowBased':True, 
        'windowBasedConfig':{'maxClosedWindowQueueLength':10, 
         'initialCredit':initial_credit}}}}}
    if delay is not None:
        cube['delay'] = delay
    if loss is not None:
        cube['loss'] = loss
    if reliable:
        cube['maxAllowableGap'] = 0
        cube['efcpPolicies']['dtcpConfiguration']['rtxControl'] = True
        cube['efcpPolicies']['dtcpConfiguration']['rtxControlConfig'] = {'dataRxmsNmax':data_rxms_nmax, 
         'initialRtxTime':initial_rtx_time}
    return cube


qos_cube_u_base = {'name':'unreliablewithflowcontrol', 
 'id':1, 
 'partialDelivery':False, 
 'orderedDelivery':True, 
 'efcpPolicies':{'dtpPolicySet':{'name':'default', 
   'version':'0'}, 
  'initialATimer':0, 
  'dtcpPresent':True, 
  'dtcpConfiguration':{'dtcpPolicySet':{'name':'default', 
    'version':'0'}, 
   'rtxControl':False, 
   'flowControl':True, 
   'flowControlConfig':{'rateBased':False, 
    'windowBased':True, 
    'windowBasedConfig':{'maxClosedWindowQueueLength':10, 
     'initialCredit':200}}}}}
qos_cube_r_base = {'name':'reliablewithflowcontrol', 
 'id':2, 
 'partialDelivery':False, 
 'orderedDelivery':True, 
 'maxAllowableGap':0, 
 'efcpPolicies':{'dtpPolicySet':{'name':'default', 
   'version':'0'}, 
  'initialATimer':0, 
  'dtcpPresent':True, 
  'dtcpConfiguration':{'dtcpPolicySet':{'name':'default', 
    'version':'0'}, 
   'rtxControl':True, 
   'rtxControlConfig':{'dataRxmsNmax':5, 
    'initialRtxTime':1000}, 
   'flowControl':True, 
   'flowControlConfig':{'rateBased':False, 
    'windowBased':True, 
    'windowBasedConfig':{'maxClosedWindowQueueLength':10, 
     'initialCredit':200}}}}}
normal_dif_base = {'difType':'normal-ipc', 
 'dataTransferConstants':{'addressLength':2, 
  'cepIdLength':2, 
  'lengthLength':2, 
  'portIdLength':2, 
  'qosIdLength':2, 
  'rateLength':4, 
  'frameLength':4, 
  'sequenceNumberLength':4, 
  'ctrlSequenceNumberLength':4, 
  'maxPduSize':10000, 
  'maxPduLifetime':60000}, 
 'qosCubes':[
  qos_cube_u_base, qos_cube_r_base], 
 'knownIPCProcessAddresses':[],  'addressPrefixes':[
  {'addressPrefix':0, 
   'organization':'N.Bourbaki'},
  {'addressPrefix':16, 
   'organization':'IRATI'}], 
 'rmtConfiguration':{'pffConfiguration':{'policySet': {'name':'default', 
                 'version':'0'}}, 
  'policySet':{'name':'default', 
   'version':'1'}}, 
 'enrollmentTaskConfiguration':{'policySet': {'name':'default', 
                'version':'1', 
                'parameters':[
                 {'name':'enrollTimeoutInMs', 
                  'value':'10000'},
                 {'name':'watchdogPeriodInMs', 
                  'value':'30000'},
                 {'name':'declaredDeadIntervalInMs', 
                  'value':'120000'},
                 {'name':'neighborsEnrollerPeriodInMs', 
                  'value':'0'},
                 {'name':'maxEnrollmentRetries', 
                  'value':'0'}]}}, 
 'flowAllocatorConfiguration':{'policySet': {'name':'default', 
                'version':'1'}}, 
 'namespaceManagerConfiguration':{'policySet': {'name':'default', 
                'version':'1'}}, 
 'securityManagerConfiguration':{'policySet': {'name':'default', 
                'version':'1'}}, 
 'resourceAllocatorConfiguration':{'pduftgConfiguration': {'policySet': {'name':'default', 
                                        'version':'0'}}}, 
 'routingConfiguration':{'policySet': {'name':'link-state', 
                'version':'1', 
                'parameters':[
                 {'name':'objectMaximumAge', 
                  'value':'10000'},
                 {'name':'waitUntilReadCDAP', 
                  'value':'5001'},
                 {'name':'waitUntilError', 
                  'value':'5001'},
                 {'name':'waitUntilPDUFTComputation', 
                  'value':'103'},
                 {'name':'waitUntilFSODBPropagation', 
                  'value':'101'},
                 {'name':'waitUntilAgeIncrement', 
                  'value':'997'},
                 {'name':'routingAlgorithm', 
                  'value':'Dijkstra'}]}}}

def ps_set--- This code section failed: ---

 L. 323         0  LOAD_FAST                'k'
                2  LOAD_FAST                'd'
                4  COMPARE_OP               not-in
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 324         8  LOAD_STR                 ''
               10  LOAD_STR                 '1'
               12  LOAD_CONST               ('name', 'version')
               14  BUILD_CONST_KEY_MAP_2     2 
               16  LOAD_FAST                'd'
               18  LOAD_FAST                'k'
               20  STORE_SUBSCR     
             22_0  COME_FROM             6  '6'

 L. 326        22  LOAD_FAST                'd'
               24  LOAD_FAST                'k'
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'name'
               30  BINARY_SUBSCR    
               32  LOAD_FAST                'v'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE   206  'to 206'
               38  LOAD_STR                 'parameters'
               40  LOAD_FAST                'd'
               42  LOAD_FAST                'k'
               44  BINARY_SUBSCR    
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE   206  'to 206'

 L. 327        50  LOAD_LISTCOMP            '<code_object <listcomp>>'
               52  LOAD_STR                 'ps_set.<locals>.<listcomp>'
               54  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               56  LOAD_FAST                'd'
               58  LOAD_FAST                'k'
               60  BINARY_SUBSCR    
               62  LOAD_STR                 'parameters'
               64  BINARY_SUBSCR    
               66  GET_ITER         
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  STORE_FAST               'cur_names'

 L. 328        72  SETUP_LOOP          240  'to 240'
               74  LOAD_FAST                'parms'
               76  GET_ITER         
               78  FOR_ITER            202  'to 202'
               80  STORE_FAST               'p'

 L. 329        82  LOAD_FAST                'p'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'name'
               88  STORE_FAST               'value'

 L. 330        90  LOAD_FAST                'name'
               92  LOAD_FAST                'cur_names'
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   176  'to 176'

 L. 331        98  SETUP_LOOP          200  'to 200'
              100  LOAD_GLOBAL              range
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'd'
              106  LOAD_FAST                'k'
              108  BINARY_SUBSCR    
              110  LOAD_STR                 'parameters'
              112  BINARY_SUBSCR    
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  GET_ITER         
            120_0  COME_FROM           146  '146'
              120  FOR_ITER            172  'to 172'
              122  STORE_FAST               'i'

 L. 332       124  LOAD_FAST                'd'
              126  LOAD_FAST                'k'
              128  BINARY_SUBSCR    
              130  LOAD_STR                 'parameters'
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'i'
              136  BINARY_SUBSCR    
              138  LOAD_STR                 'name'
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'name'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   120  'to 120'

 L. 333       148  LOAD_FAST                'value'
              150  LOAD_FAST                'd'
              152  LOAD_FAST                'k'
              154  BINARY_SUBSCR    
              156  LOAD_STR                 'parameters'
              158  BINARY_SUBSCR    
              160  LOAD_FAST                'i'
              162  BINARY_SUBSCR    
              164  LOAD_STR                 'value'
              166  STORE_SUBSCR     

 L. 334       168  BREAK_LOOP       
              170  JUMP_BACK           120  'to 120'
              172  POP_BLOCK        
              174  JUMP_BACK            78  'to 78'
            176_0  COME_FROM            96  '96'

 L. 336       176  LOAD_FAST                'd'
              178  LOAD_FAST                'k'
              180  BINARY_SUBSCR    
              182  LOAD_STR                 'parameters'
              184  BINARY_SUBSCR    
              186  LOAD_METHOD              append
              188  LOAD_FAST                'name'
              190  LOAD_FAST                'value'
              192  LOAD_CONST               ('name', 'value')
              194  BUILD_CONST_KEY_MAP_2     2 
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          
            200_0  COME_FROM_LOOP       98  '98'
              200  JUMP_BACK            78  'to 78'
              202  POP_BLOCK        
              204  JUMP_FORWARD        240  'to 240'
            206_0  COME_FROM            48  '48'
            206_1  COME_FROM            36  '36'

 L. 338       206  LOAD_GLOBAL              len
              208  LOAD_FAST                'parms'
              210  CALL_FUNCTION_1       1  '1 positional argument'
              212  LOAD_CONST               0
              214  COMPARE_OP               >
              216  POP_JUMP_IF_FALSE   240  'to 240'

 L. 340       218  LOAD_LISTCOMP            '<code_object <listcomp>>'
              220  LOAD_STR                 'ps_set.<locals>.<listcomp>'
              222  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 341       224  LOAD_FAST                'parms'
              226  GET_ITER         
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  LOAD_FAST                'd'
              232  LOAD_FAST                'k'
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'parameters'
              238  STORE_SUBSCR     
            240_0  COME_FROM           216  '216'
            240_1  COME_FROM           204  '204'
            240_2  COME_FROM_LOOP       72  '72'

 L. 343       240  LOAD_FAST                'v'
              242  LOAD_FAST                'd'
              244  LOAD_FAST                'k'
              246  BINARY_SUBSCR    
              248  LOAD_STR                 'name'
              250  STORE_SUBSCR     

Parse error at or near `COME_FROM_LOOP' instruction at offset 240_2


def dtp_ps_set(d, v, parms):
    for i in range(len(d['qosCubes'])):
        ps_set(d['qosCubes'][i]['efcpPolicies'], 'dtpPolicySet', v, parms)


def dtcp_ps_set(d, v, parms):
    for i in range(len(d['qosCubes'])):
        ps_set(d['qosCubes'][i]['efcpPolicies']['dtcpConfiguration'], 'dtcpPolicySet', v, parms)


policy_translator = {'rmt.pff':lambda d, v, p: ps_set(d['rmtConfiguration']['pffConfiguration'], 'policySet', v, p), 
 'rmt':lambda d, v, p: ps_set(d['rmtConfiguration'], 'policySet', v, p), 
 'enrollment-task':lambda d, v, p: ps_set(d['enrollmentTaskConfiguration'], 'policySet', v, p), 
 'flow-allocator':lambda d, v, p: ps_set(d['flowAllocatorConfiguration'], 'policySet', v, p), 
 'namespace-manager':lambda d, v, p: ps_set(d['namespaceManagerConfiguration'], 'policySet', v, p), 
 'security-manager':lambda d, v, p: ps_set(d['securityManagerConfiguration'], 'policySet', v, p), 
 'routing':lambda d, v, p: ps_set(d['routingConfiguration'], 'policySet', v, p), 
 'resource-allocator.pduftg':lambda d, v, p: ps_set(d['resourceAllocatorConfiguration']['pduftgConfiguration'], 'policySet', v, p), 
 'efcp.*.dtcp':None, 
 'efcp.*.dtp':None}

def is_security_path(path):
    sp = path.split'.'
    return len(sp) == 3 and sp[0] == 'security-manager' and sp[1] in ('auth', 'encrypt',
                                                                      'ttl', 'errorcheck')


def policy_path_valid(path):
    if path in policy_translator:
        return True
    if is_security_path(path):
        return True
    return False


def translate_security_path(d, path, ps, parms):
    u1, component, profile = path.split'.'
    if 'authSDUProtProfiles' not in d['securityManagerConfiguration']:
        d['securityManagerConfiguration']['authSDUProtProfiles'] = {}
    d = d['securityManagerConfiguration']['authSDUProtProfiles']
    tr = {'auth':'authPolicy', 
     'encrypt':'encryptPolicy',  'ttl':'TTLPolicy', 
     'errorcheck':'ErrorCheckPolicy'}
    if profile == 'default':
        if profile not in d:
            d['default'] = {}
        ps_set(d['default'], tr[component], ps, parms)
    else:
        if 'specific' not in d:
            d['specific'] = []
        j = -1
        for i in range(len(d['specific'])):
            if d['specific'][i]['underlyingDIF'] == profile + '.DIF':
                j = i
                break

        if j == -1:
            d['specific'].append{'underlyingDIF': profile + '.DIF'}
        ps_set(d['specific'][j], tr[component], ps, parms)


def translate_policy(difconf, path, ps, parms):
    if path == 'efcp.*.dtcp':
        dtcp_ps_set(difconf, ps, parms)
    else:
        if path == 'efcp.*.dtp':
            dtp_ps_set(difconf, ps, parms)
        else:
            if is_security_path(path):
                translate_security_path(difconf, path, ps, parms)
            else:
                policy_translator[path](difconf, ps, parms)