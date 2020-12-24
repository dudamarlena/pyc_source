# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/CECS/__init__.py
# Compiled at: 2015-11-22 19:20:24
"""
    Python module of different functions for manipulating UCS Director
    via the API.
"""
import requests, json
from markdown import markdown
from local_config import ucsdserver, ucsd_key, url, getstring, parameter_lead, headers, icfbserver, icfb_key
requests.packages.urllib3.disable_warnings()

def ucsdCall(api, param0=None, param1=None, param2=None, param3=None, param4=None):
    """
    NOTE: This is deprecated and will be removed once all functions have been migrated!

    Craetes the URL format to make the call to UCS Director Rest API.
    This is a hacked version of overloading (not sure how else to achieve)
    :param api: The specific API call required
    :param param0: The initial parameter required to create the request structure
    :return: JSON response (in Python dictionary) from API call
    """
    headers['X-Cloupia-Request-Key'] = ucsd_key
    if param0 is None:
        u = url % ucsdserver + getstring % api + parameter_lead + '{}'
    elif param1 is None:
        u = url % ucsdserver + getstring % api + parameter_lead + '{param0:"' + param0 + '"' + '}'
    elif param2 is None:
        u = url % ucsdserver + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + ',param1:"' + param1 + '"}'
    elif param3 is None:
        u = url % ucsdserver + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + 'param1:"' + param1 + '"' + ',param2:"' + param2 + '"}'
    elif param4 is None:
        u = url % ucsdserver + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + 'param1:"' + param1 + '"' + 'param2:"' + param2 + '"' + ',param3:"' + param3 + '"}'
    r = requests.get(u, headers=headers)
    j = json.loads(r.text)
    return r


def apiCall(env, api, param0=None, param1=None, param2=None, param3=None, param4=None):
    """
    Craetes the URL format to make the call to UCS Director or Intercloud Fabric
    Rest API. This is a hacked way to achieve overloading
    :param env: Specify if the API call should be against UCSD or ICFB
    :param api: The specific API call required
    :param param0: The initial parameter required to create the request structure
    :param param1: The 2nd if required
    :param param2: The 3rd if required
    :return: JSON response from API call
    """
    if env == 'icfb':
        headers['X-Cloupia-Request-Key'] = icfb_key
        server = icfbserver
    elif env == 'ucsd':
        headers['X-Cloupia-Request-Key'] = ucsd_key
        server = ucsdserver
    if param0 is None:
        u = url % server + getstring % api + parameter_lead + '{}'
    elif param1 is None:
        u = url % server + getstring % api + parameter_lead + '{param0:' + param0 + '}'
    elif param2 is None:
        u = url % server + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + ',param1:"' + param1 + '"}'
    elif param3 is None:
        u = url % server + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + 'param1:"' + param1 + '"' + ',param2:"' + param2 + '"}'
    elif param4 is None:
        u = url % server + getstring % api + parameter_lead + '{param0:"' + param0 + '",' + 'param1:"' + param1 + '"' + 'param2:"' + param2 + '"' + ',param3:"' + param3 + '"}'
    print u
    r = requests.get(u, headers=headers, verify=False)
    j = json.loads(r.text)
    return j


def sr_get(env):
    """
    Return the service request for the logged in user (Both UCSD & ICFB)
    :return: APITabularReport (JSON)
    """
    apioperation = 'userAPIGetServiceRequests'
    r = apiCall(env, apioperation)
    return r


def sr_details(srnumber):
    """
    Return the details of the Service Request Specified - Workflow Based Only
    :param srnumber: The Service Request ID
    :return: JSON of the SR Status
    """
    apioperation = 'userAPIGetServiceRequestWorkFlow'
    r = ucsdCall(apioperation, srnumber)
    return r


def sr_log(srnumber, severity):
    """
    Return the logs from the specified Service Request
    :param srnumber: The Service Request ID
    :param severity: Log severity (debug, info, warning, error)
    :return: JSON of the logs
    """
    apioperation = 'userAPIGetServiceRequestLogEntries'
    if severity == 'debug':
        severity = '0'
    elif severity == 'info':
        severity = '1'
    elif severity == 'warning':
        severity = '2'
    elif severity == 'error':
        severity = '3'
    else:
        severity = '1000'
    r = ucsdCall(apioperation, srnumber, severity)
    return r


def group_name(name):
    apioperation = 'userAPIGetGroupByName'
    r = ucsdCall(apioperation, name)
    return r


def report_tabular(group, report):
    apioperation = 'userAPIGetTabularReport'
    if group == '':
        rptid = '6'
        grpid = ''
    else:
        rptid = '7'
        grp = group_name(group)
        grpid = str(grp['serviceResult'][0]['groupId'])
    if report == 'sr-active':
        r = ucsdCall(apioperation, rptid, grpid, 'SERVICE-REQUESTS-T10')
        return r
    if report == 'sr-archive':
        r = ucsdCall(apioperation, rptId, grpid, 'ARCHIVED-SERVICE-REQUESTS-T10')
        return r


def getAllVMs(env):
    if env == 'ucsd':
        apioperation = 'userAPIGetAllVMs'
    elif env == 'icfb':
        apioperation = 'Intercloud:userAPIGetAllVms'
    print 'About to call in getAllVMs ' + env + ' using ' + apioperation
    r = apiCall(env, apioperation)
    return r


def VMNameToID(env, vm_name):
    """
    Will return the 'vmid' when the VM Name is passed. Currently on UCSD but will be expanded to ICF
    :param api: The specific API call required
    :param: VM_Name
    :return: vmid
    """
    if env == 'ucsd':
        apioperation = 'userAPIGetAllVMs'
    elif env == 'icfb':
        apioperation = 'Intercloud:userAPIGetAllVms'
    print 'About to call in VMnameToID ' + env + ' using ' + apioperation
    r = apiCall(env, apioperation)
    all_vms = r['serviceResult']['rows']
    if env == 'ucsd':
        print 'Checking against UCSD'
        for vm in all_vms:
            if vm['VM_Name'] == vm_name:
                vmid = vm['VM_ID']
                return vmid
            vmid = 'Error, ' + vm_name + ' not found!!'

    elif env == 'icfb':
        print 'Checking against ICFB'
        for vm in all_vms:
            if vm['Instance_ID'] == vm_name:
                vmid = vm['VM_ID']
                return vmid
            vmid = 'Error, ' + vm_name + ' not found!!'


def vm_action(env, vm_name, action, comment):
    """
    This will alter the status (on, off etc.) of a VM. It has to work out the
    vmid based on the VM name that is passed.
    """
    print 'Working out the vmid'
    vmid = VMNameToID(env, vm_name)
    print 'The vmid is' + str(vmid)
    if env == 'ucsd':
        apioperation = 'userAPIExecuteVMAction'
        generic_actions = ['discardSaveState',
         'pause',
         'powerOff',
         'powerOn',
         'reboot',
         'rebuildServer',
         'repairVM',
         'reset',
         'resume',
         'saveState',
         'shutdownGuest',
         'standby',
         'suspend']
        if action == 'help':
            return generic_actions
        if not any(action == a for a in generic_actions):
            return 'Action not valid'
    elif env == 'icfb':
        generic_actions = ['powerOff',
         'powerOn',
         'reboot',
         'terminate']
        if action == 'help':
            return generic_actions
        if not any(action == a for a in generic_actions):
            return 'Action not valid'
        if action == 'powerOff':
            apioperation = 'Intercloud:userAPIVmPowerOff'
        elif action == 'powerOn':
            apioperation = 'Intercloud:userAPIVmPowerOn'
        elif action == 'reboot':
            apioperation = 'Intercloud:userAPIVmReboot'
        elif action == 'terminate':
            apioperation = 'Intercloud:userAPIVmTerminate'
    else:
        r = 'Error, VM not found'
    print 'About to ' + action + " the VM '" + vm_name + "' with VM_ID '" + str(vmid) + "' ."
    r = apiCall(env, apioperation, str(vmid), action, comment)
    return r


def GetCatalogs(env, group):
    """
    Returns the catalogs for the specified user group or all groups.
    :param: GroupName
    :return: APITabularReport
    """
    if group == 'all':
        apioperation = 'userAPIGetAllCatalogs'
        r = apiCall(env, apioperation)
    else:
        apioperation = 'userAPIGetCatalogsPerGroup'
        r = apiCall(env, apioperation, group)
    return r


def GetIconURL(imageId):
    """
    Returns the icon image URL of the specified icon identifier. Only ICF API!
    :param: imageId
    :return: FormLOVPair[]
    """
    env = 'icfb'
    apioperation = 'userAPIGetIconImageURL'
    r = apiCall(env, apioperation, imageId)
    return r


def GetvCenter(env, vCenterAccountName):
    """
    Returns a list of all VMware vCenter servers or of all data centers that match the VMware vCenter account name.
    :param: None or vCenterAccountName
    :return: APITabularReport
    """
    if env == '':
        env = 'icfb'
    elif env == 'icfb':
        env = env
    else:
        error = "Not a valid environment, only 'icfb' is an option"
        return error
    if vCenterAccountName == 'all' or vCenterAccountName == '':
        apioperation = 'Intercloud:userAPIGetAllVCenters'
        r = apiCall(env, apioperation)
    else:
        apioperation = 'Intercloud:userAPIGetAllDataCenters'
        r = apiCall(env, apioperation, vCenterAccountName)
    return r


def GetClouds(env):
    """
    Returns a list of all Cisco Intercloud Fabric clouds.
    :param: None
    :return: APITabularReport
    """
    if env == '':
        env = 'icfb'
    elif env == 'icfb':
        env = env
    else:
        error = "Not a valid environment, only 'icfb' is an option"
        return error
    apioperation = 'Intercloud:userAPIGetAllicfClouds'
    r = apiCall(env, apioperation)
    return r


def GetTunnelProfiles(env):
    """
    Returns a list of all tunnel profiles.
    :param: None
    :return: APITabularReport
    """
    if env == '':
        env = 'icfb'
    elif env == 'icfb':
        env = env
    else:
        error = "Not a valid environment, only 'icfb' is an option"
        return error
    apioperation = 'Intercloud:userAPIGetAllTunnelProfiles'
    r = apiCall(env, apioperation)
    return r


def GetCloudSummary(env, icfCloudId):
    """
    Returns the details of the Cisco Intercloud Fabric clouds that match the specified cloud identifier.
    :param icfCloudId: Cisco Intercloud Fabric cloud identifier.
    :return: APITabularReport
    """
    if env == '':
        env = 'icfb'
    elif env == 'icfb':
        env = env
    else:
        error = "Not a valid environment, only 'icfb' is an option"
        return error
    apioperation = 'Intercloud:userAPIGeticfCloudSummary'
    r = apiCall(env, apioperation, icfCloudId)
    return r


def GetVMvNics(env, vmId):
    """
    Returns a list of the vNICs configured on the specified VM.
    :param vmId: VM identifier available from the VM report screen.
    :return: APITabularReport
    """
    if env == '':
        env = 'icfb'
    elif env == 'icfb':
        env = env
    else:
        error = "Not a valid environment, only 'icfb' is an option"
        return error
    apioperation = 'Intercloud:userAPIGetVMVnics'
    r = apiCall(env, apioperation, vmId)
    return r


def GetMgmtPortProfiles(env, vmManager, dataCenter):
    """
    Returns a list of all management port profiles for the specified VM Manager and data center.
    :param vmManager: VM Manager identifier.
    :param dataCenter: Data center identifier.
    :return: APITabularReport
    """
    apioperation = 'Intercloud:userAPIGetAllPvtMgmtPortProfiles'
    r = apiCall(env, apioperation, vmManager, dataCenter)
    return r


def GetStaticIPPoolPolicies(env):
    """
    Returns a list of all static IP address pool policies.
    :param None
    :return: APITabularReport
    """
    apioperation = 'Intercloud:userAPIGetAllStaticIPPoolPolicy'
    r = apiCall(env, apioperation)
    return r


def GetStaticIPPool(env):
    """
    Returns a list of all static IP address pools.
    :param id
    :return: APITabularReport
    """
    apioperation = 'Intercloud:userAPIGetAllStaticIPPools'
    r = apiCall(env, apioperation, '2')
    return r


def GetResIP(env):
    """
    Returns a list of all reserved IP addresses.
    :param None
    :return: APITabularReport
    """
    apioperation = 'Intercloud:userAPIGetIPAddressPool'
    r = apiCall(env, apioperation)
    return r


def GetAllVDCs(env):
    """
    Returns all VDCs for the logged-in user group
    :param None
    :return: APITabularReport
    """
    apioperation = 'userAPIGetAllVDCs'
    r = apiCall(env, apioperation)
    return r


def CreateVDC(env, APIVDCDetails):
    """
    Creates a vDC defined by the provided data.
    :param: APIVDCDetails
    :return: boolean
    """
    if env == '':
        env = 'ucsd'
    elif env == 'ucsd':
        env = env
    else:
        error = "Not a valid environment, only 'ucsd' is an option"
        return error
    apioperation = 'userAPICreateVDC'
    values = str(APIVDCDetails)
    print values
    r = apiCall(env, apioperation, values)
    return r


def ExportVDC(env, vdcName):
    """
    Exports a vDC.
    :param vdcName: Name of the vDC that you want to export
    :return: String
    """
    if env == '':
        env = 'ucsd'
    elif env == 'ucsd':
        env = env
    else:
        error = "Not a valid environment, only 'ucsd' is an option"
        return error
    apioperation = 'userAPIExportVDC'
    r = apiCall(env, apioperation, vdcName)
    return r


def ImportVDC(env, vdcName):
    """
    Imports a vDC.
    :param vdcName: Name of the vDC that you want to import
    :return: VDC
    """
    if env == '':
        env = 'ucsd'
    elif env == 'ucsd':
        env = env
    else:
        error = "Not a valid environment, only 'ucsd' is an option"
        return error
    apioperation = 'userAPIImportVDC'
    r = apiCall(env, apioperation, vdcName)
    return r