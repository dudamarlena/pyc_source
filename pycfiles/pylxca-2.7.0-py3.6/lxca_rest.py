# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/pylxca_api/lxca_rest.py
# Compiled at: 2020-03-12 01:40:34
# Size of source mod 2**32: 84267 bytes
"""
@since: 4 Sep 2015
@author: Prashant Bhosale <pbhosale@lenovo.com>, Girish Kumar <gkumar1@lenovo.com>
@license: Lenovo License
@copyright: Copyright 2016, Lenovo
@organization: Lenovo
@summary: This module is for creating a connection session object for given xHMC
"""
import logging, os, json, pprint, requests, logging.config
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from requests.exceptions import HTTPError
import ast, json, re, socket, time, urllib
try:
    logging.captureWarnings(True)
except:
    pass

logger_conf_file = 'lxca_logger.conf'
pylxca_logger = os.path.join(os.getenv('PYLXCA_API_PATH'), logger_conf_file)
logger = logging.getLogger(__name__)
REST_TIMEOUT = 60

def callback(encoder):
    pass


class lxca_rest(object):
    __doc__ = '\n    classdocs\n    '

    def get_chassis(self, url, session, uuid, status):
        url = url + '/chassis'
        if uuid:
            url = url + '/' + uuid
        else:
            if status:
                url = url + '?status=' + status
            else:
                url = url + '?status=managed'
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_metrics(self, url, session, uuid):
        url = url + '/nodes/metrics'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_nodes(self, url, session, uuid, status):
        url = url + '/nodes'
        if uuid:
            url = url + '/' + uuid
        if status:
            url = url + '?status=' + status
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def set_nodes(self, url, session, uuid, modify):
        url = url + '/nodes'
        job = None
        if uuid:
            url = url + '/' + uuid + '?synchronous=false'
        try:
            payload = dict()
            payload = modify
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                if 'location' in resp.headers._store:
                    job = resp.headers._store['location'][(-1)].split('/')[(-1)]
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return job

    def get_switches(self, url, session, uuid):
        url = url + '/switches'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_switches_port(self, url, session, uuid, list_port):
        url = url + '/switches'
        if uuid:
            url = url + '/' + uuid
        else:
            raise Exception('Invalid argument uuid is required')
        if list_port:
            url = url + '/ports'
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def put_switches_port(self, url, session, uuid, port_name, action):
        url = url + '/switches'
        if uuid:
            url = url + '/' + uuid
        else:
            raise Exception('Invalid argument uuid is required')
        if port_name:
            url = url + '/ports'
        else:
            raise Exception('Invalid argument port name is required')
        if action not in ('enable', 'disable'):
            raise Exception('Invalid argument action [enable/disable] is required %s' % action)
        payload = {'action':'enable', 
         'ports':[]}
        uuid_list = port_name.split(',')
        payload['action'] = action
        payload['ports'] = uuid_list
        try:
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_fan(self, url, session, uuid):
        url = url + '/fans'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_powersupply(self, url, session, uuid):
        url = url + '/powerSupplies'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_fanmux(self, url, session, uuid):
        url = url + '/fanMuxes'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_cmm(self, url, session, uuid):
        url = url + '/cmms'
        if uuid:
            url = url + '/' + uuid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_scalablesystem(self, url, session, complexid, complextype):
        url = url + '/scalableComplex'
        if complexid:
            url = url + '/' + complexid
        if complextype:
            if complextype == 'flex' or complextype == 'rackserver':
                url = url + '?complexType=' + complextype
            else:
                raise Exception("Invalid argument 'complexType': %s" % complextype)
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def set_log_config(self):
        logging.config.fileConfig(pylxca_logger)

    def get_log_level(self):
        logger.debug('Current Log Level is: ' + str(logger.getEffectiveLevel()))
        return logging.getLevelName(logger.getEffectiveLevel())

    def set_log_level(self, log_value):
        logger.setLevel(log_value)
        for handler in logger.handlers:
            handler.setLevel(log_value)

        logger.debug('Current Log Level is: ' + str(logger.getEffectiveLevel()))

    def do_discovery(self, url, session, ip_addr, jobid):
        try:
            if ip_addr:
                url = url + '/discoverRequest'
                payload = [{'ipAddresses': ip_addr.split(',')}]
                resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    if 'location' in resp.headers._store:
                        job = resp.headers._store['location'][(-1)].split('/')[(-1)]
                        return job
                    else:
                        return
            else:
                if jobid:
                    url = url + '/discoverRequest/jobs/' + str(jobid)
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                else:
                    url = url + '/discovery'
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

        return resp

    def do_manage(self, url, session, ip_addr, user, pw, rpw, force, jobid, storedcredential_id):
        try:
            orig_url = url
            if ip_addr and (user and pw or storedcredential_id):
                url = url + '/manageRequest'
                payload = list()
                param_dict = dict()
                param_dict['ipAddresses'] = ip_addr.split(',')
                param_dict['username'] = user
                param_dict['password'] = pw
                if rpw:
                    param_dict['recoveryPassword'] = rpw
                disc_job_id = self.do_discovery(url.rsplit('/', 1)[0], session, ip_addr, None)
                disc_progress = 0
                if disc_job_id:
                    while disc_progress < 100:
                        time.sleep(2)
                        disc_job_resp = self.do_discovery(url.rsplit('/', 1)[0], session, None, disc_job_id)
                        disc_resp_py_obj = json.loads(disc_job_resp.text)
                        disc_progress = disc_resp_py_obj['progress']

                discovered_endpoint = False
                for key in list(disc_resp_py_obj.keys()):
                    if isinstance(disc_resp_py_obj[key], list) and disc_resp_py_obj[key] != []:
                        discovered_endpoint = True
                        param_dict['managementPorts'] = disc_resp_py_obj[key][0]['managementPorts']
                        param_dict['type'] = disc_resp_py_obj[key][0]['type']
                        param_dict['machineType'] = disc_resp_py_obj[key][0]['machineType']
                        if param_dict['type'] == 'Rack-Tower Server':
                            param_dict['managementProcessor'] = disc_resp_py_obj[key][0]['managementProcessor']
                            param_dict['server-type'] = 'Rack-Tower Server'
                        param_dict['uuid'] = disc_resp_py_obj[key][0]['uuid']
                        disc_ip_addr = disc_resp_py_obj[key][0]['ipAddresses'][0]
                        param_dict['ipAddresses'] = [
                         disc_ip_addr]
                        if param_dict['type'] == 'Rackswitch':
                            param_dict['os'] = disc_resp_py_obj[key][0]['os']

                if not discovered_endpoint:
                    logger.debug('Failed to discover given endpoint  %s' % param_dict['ipAddresses'])
                    raise Exception('Failed to discover given endpoint  %s' % param_dict['ipAddresses'])
                if force:
                    if isinstance(force, bool):
                        param_dict['forceManage'] = force
                    else:
                        if force.lower() == 'true':
                            param_dict['forceManage'] = True
                        else:
                            param_dict['forceManage'] = False
                        security_Descriptor = {}
                        if storedcredential_id:
                            security_Descriptor['managedAuthEnabled'] = False
                            security_Descriptor['managedAuthSupported'] = False
                            cred = self.get_storedcredentials(orig_url, session, storedcredential_id)
                            cred_resp = json.loads(cred.text)
                            storedCredentials = {}
                            storedCredentials['id'] = storedcredential_id
                            storedCredentials['userName'] = cred_resp['response']['userName']
                            storedCredentials['description'] = cred_resp['response']['description']
                            security_Descriptor['storedCredentials'] = storedCredentials
                        else:
                            security_Descriptor['managedAuthEnabled'] = True
                            security_Descriptor['managedAuthSupported'] = False
                    param_dict['securityDescriptor'] = security_Descriptor
                    payload = [param_dict]
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                        if 'location' in resp.headers._store:
                            job = resp.headers._store['location'][(-1)].split('/')[(-1)]
                            return job
                        else:
                            return
            else:
                if jobid:
                    url = url + '/manageRequest/jobs/' + str(jobid)
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                else:
                    logger.error('Invalid execution of manage REST API')
                    raise Exception('Invalid execution of manage REST API')
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

        return resp

    def do_unmanage(self, url, session, endpoints, force, jobid):
        endpoints_list = list()
        param_dict = dict()
        try:
            if endpoints:
                url = url + '/unmanageRequest'
                for each_ep in endpoints.split(','):
                    ip_addr = None
                    each_ep_dict = dict()
                    ep_data = each_ep.split(';')
                    ip_addr = ep_data[0]
                    uuid = ep_data[1]
                    type = ep_data[2]
                    type_list = [
                     'Chassis', 'Rackswitch', 'ThinkServer', 'Storage', 'Rack-Tower']
                    if type not in type_list:
                        raise Exception('Invalid Type Specified')
                    if type == 'ThinkServer':
                        type = 'Lenovo ThinkServer'
                    else:
                        if type == 'Storage':
                            type = 'Lenovo Storage'
                        else:
                            if type == 'Rack-Tower':
                                type = 'Rack-Tower Server'
                    each_ep_dict = {'ipAddresses':ip_addr.split('#'), 
                     'type':type,  'uuid':uuid}
                    endpoints_list.append(each_ep_dict)

                param_dict['endpoints'] = endpoints_list
                if force:
                    if isinstance(force, bool):
                        param_dict['forceUnmanage'] = force
                    else:
                        if force.lower() == 'true':
                            param_dict['forceUnmanage'] = True
                        else:
                            param_dict['forceUnmanage'] = False
                    payload = param_dict
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                        if 'location' in resp.headers._store:
                            job = resp.headers._store['location'][(-1)].split('/')[(-1)]
                            return job
                        else:
                            return
            else:
                if jobid:
                    url = url + '/unmanageRequest/jobs/' + str(jobid)
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                else:
                    logger.error('Invalid execution of unmanage REST API')
                    raise Exception('Invalid execution of unmanage REST API')
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

        return resp

    def get_jobs(self, url, session, jobid, uuid, state, canceljobid, deletejobid):
        url = url + '/jobs'
        try:
            if jobid:
                url = url + '/' + jobid
                if state:
                    if state == 'Pending ' or state == 'Running' or state == 'Complete' or state == 'Cancelled' or state == 'Running_With_Errors' or state == 'Cancelled_With_Errors' or state == 'Stopped_With_Error' or state == 'Interrupted':
                        url = url + '?state=' + state
                        if uuid:
                            url = url + ',uuid=' + uuid
                    else:
                        raise Exception("Invalid argument 'state': %s" % state)
                if state == None:
                    if uuid:
                        url = url + '?uuid=' + uuid
                resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
            else:
                if canceljobid:
                    url = url + '/' + canceljobid
                    payload = {'cancelRequest': 'true'}
                    resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                        return True
                    resp.raise_for_status()
                else:
                    if deletejobid:
                        url = url + '/' + deletejobid
                        resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
                        if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                            return True
                        resp.raise_for_status()
                    else:
                        if state:
                            if state == 'Pending' or state == 'Running' or state == 'Complete' or state == 'Cancelled' or state == 'Running_With_Errors' or state == 'Cancelled_With_Errors' or state == 'Stopped_With_Error' or state == 'Interrupted':
                                url = url + '?state=' + state
                                if uuid:
                                    url = url + ',uuid=' + uuid
                            else:
                                raise Exception("Invalid argument 'state': %s" % state)
                        if state == None:
                            if uuid:
                                url = url + '?uuid=' + uuid
                        resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                        resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_users(self, url, session, userid):
        url = url + '/userAccounts'
        if userid:
            url = url + '/' + userid
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_lxcalog(self, url, session, filter):
        url = url + '/events'
        if filter:
            url = url + '?filterWith=' + filter
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_ffdc(self, url, session, uuid):
        url = url + '/ffdc/endpoint'
        try:
            if uuid:
                url = url + '/' + uuid
                resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                if resp.status_code == requests.codes['ok'] or resp.status_code == requests.codes['created'] or resp.status_code == requests.codes['accepted']:
                    job_info = ast.literal_eval(resp.content)
                    if 'jobURL' in job_info:
                        job = job_info['jobURL'].split('/')[(-1)]
                        return job
                    else:
                        return resp
            else:
                logger.error('Invalid execution of ffdc REST API mandatory parameter uuid is missing')
                raise Exception('Invalid execution of ffdc REST API mandatory parameter uuid is missing')
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def get_updatepolicy(self, url, session, info, jobid, uuid):
        url = url + '/compliancePolicies'
        try:
            if info in ('FIRMWARE', 'RESULTS', 'NAMELIST'):
                if info == 'FIRMWARE':
                    url = url + '/applicableFirmware'
                else:
                    if info == 'RESULTS':
                        url = url + '/persistedResult'
                    else:
                        if info == 'NAMELIST':
                            url = url + '/nameList'
                resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                return resp
            if jobid:
                url = url + '/compareResult'
                payload = dict()
                payload['jobid'] = jobid
                payload['uuid'] = uuid
                resp = session.get(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                return resp
            url = url + '?basic_full=full'
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def post_updatepolicy(self, url, session, policy, type, uuid):
        url = url + '/compliancePolicies/compareResult'
        try:
            if not policy or not type or not uuid:
                raise Exception('Invalid argument key')
            payload = dict()
            policy_dict = dict()
            policy_dict['policyName'] = policy
            policy_dict['uuid'] = uuid
            policy_dict['type'] = type
            compliance_list = []
            compliance_list.append(policy_dict)
            payload['compliance'] = compliance_list
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def get_updaterepo(self, url, session, key, mt, scope):
        url = url + '/updateRepositories/firmware'
        try:
            if key:
                url = url + '?key=' + key
            else:
                if mt:
                    url = url + '&mt=' + mt
                if scope:
                    if scope.lower() in ('all', 'latest'):
                        if key == 'updates' or key == 'updatesByMt':
                            url = url + '&with=' + scope.lower()
                        else:
                            raise Exception('Invalid argument combination of key and scope')
                    else:
                        raise Exception('Invalid argument scope: ' + scope)
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def put_updaterepo(self, url, session, action, fixids, mt, type, scope):
        url = url + '/updateRepositories/firmware'
        try:
            url = url + '?action=' + action
            if type:
                if type.lower() in ('all', 'payloads'):
                    if action == 'delete' or action == 'export':
                        url = url + '&filetypes=' + type.lower()
                    else:
                        raise Exception('Invalid argument combination of action and type')
                else:
                    raise Exception('Invalid argument type:' + type)
            if scope:
                if scope.lower() in ('all', 'latest', 'payloads'):
                    if action == 'refresh':
                        if scope.lower() in ('all', 'latest'):
                            url = url + '&with=' + scope.lower()
                    if action == 'acquire':
                        if scope.lower() in ('payloads', ):
                            url = url + '&with=' + scope.lower()
                    raise Exception('Invalid argument combination of action and scope')
                else:
                    raise Exception('Invalid argument scope:' + scope)
            payload = dict()
            if action == 'delete':
                if fixids:
                    fixids_list = fixids.split(',')
                    payload['fixids'] = fixids_list
                else:
                    raise Exception('Invalid argument fixids is required for delete')
            if action == 'acquire':
                if fixids:
                    fixids_list = fixids.split(',')
                    payload['fixids'] = fixids_list
            if action == 'acquire' or action == 'refresh':
                if mt:
                    mt_list = mt.split(',')
                    payload['mt'] = mt_list
                else:
                    raise Exception('Invalid argument mt is required for action acquire and refresh')
            if action == 'refresh':
                payload['os'] = ''
                payload['type'] = 'catalog'
            if action == 'acquire':
                payload['type'] = 'latest'
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def get_managementserver--- This code section failed: ---

 L. 734         0  LOAD_FAST                'url'
                2  LOAD_STR                 '/managementServer/updates'
                4  BINARY_ADD       
                6  STORE_FAST               'url'

 L. 735         8  SETUP_EXCEPT        122  'to 122'

 L. 736        10  LOAD_FAST                'fixids'
               12  POP_JUMP_IF_FALSE    70  'to 70'

 L. 737        14  LOAD_FAST                'url'
               16  LOAD_STR                 '/'
               18  BINARY_ADD       
               20  LOAD_FAST                'fixids'
               22  BINARY_ADD       
               24  STORE_FAST               'url'

 L. 739        26  LOAD_FAST                'key'
               28  POP_JUMP_IF_FALSE    52  'to 52'

 L. 740        30  LOAD_FAST                'key'
               32  LOAD_CONST               ('all',)
               34  COMPARE_OP               not-in
               36  POP_JUMP_IF_FALSE    68  'to 68'

 L. 741        38  LOAD_FAST                'url'
               40  LOAD_STR                 '?key='
               42  BINARY_ADD       
               44  LOAD_FAST                'key'
               46  BINARY_ADD       
               48  STORE_FAST               'url'
               50  JUMP_ABSOLUTE        94  'to 94'
               52  ELSE                     '68'

 L. 742        52  LOAD_FAST                'type'
               54  POP_JUMP_IF_FALSE    94  'to 94'

 L. 743        56  LOAD_FAST                'url'
               58  LOAD_STR                 '?filetype='
               60  BINARY_ADD       
               62  LOAD_FAST                'type'
               64  BINARY_ADD       
               66  STORE_FAST               'url'
             68_0  COME_FROM            36  '36'
               68  JUMP_FORWARD         94  'to 94'
               70  ELSE                     '94'

 L. 746        70  LOAD_FAST                'key'
               72  POP_JUMP_IF_FALSE    94  'to 94'

 L. 747        74  LOAD_FAST                'key'
               76  LOAD_CONST               ('all',)
               78  COMPARE_OP               not-in
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L. 748        82  LOAD_FAST                'url'
               84  LOAD_STR                 '?key='
               86  BINARY_ADD       
               88  LOAD_FAST                'key'
               90  BINARY_ADD       
               92  STORE_FAST               'url'
             94_0  COME_FROM            80  '80'
             94_1  COME_FROM            72  '72'
             94_2  COME_FROM            68  '68'
             94_3  COME_FROM            54  '54'

 L. 750        94  LOAD_FAST                'session'
               96  LOAD_ATTR                get
               98  LOAD_FAST                'url'
              100  LOAD_CONST               False
              102  LOAD_GLOBAL              REST_TIMEOUT
              104  LOAD_CONST               ('verify', 'timeout')
              106  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              108  STORE_FAST               'resp'

 L. 751       110  LOAD_FAST                'resp'
              112  LOAD_ATTR                raise_for_status
              114  CALL_FUNCTION_0       0  '0 positional arguments'
              116  POP_TOP          

 L. 752       118  LOAD_FAST                'resp'
              120  RETURN_VALUE     
            122_0  COME_FROM_EXCEPT      8  '8'

 L. 754       122  DUP_TOP          
              124  LOAD_GLOBAL              HTTPError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   170  'to 170'
              130  POP_TOP          
              132  STORE_FAST               're'
              134  POP_TOP          
              136  SETUP_FINALLY       160  'to 160'

 L. 755       138  LOAD_GLOBAL              logger
              140  LOAD_ATTR                error
              142  LOAD_STR                 'Exception occured: %s'
              144  LOAD_FAST                're'
              146  CALL_FUNCTION_2       2  '2 positional arguments'
              148  POP_TOP          

 L. 756       150  LOAD_FAST                're'
              152  RAISE_VARARGS_1       1  'exception'
              154  POP_BLOCK        
              156  POP_EXCEPT       
              158  LOAD_CONST               None
            160_0  COME_FROM_FINALLY   136  '136'
              160  LOAD_CONST               None
              162  STORE_FAST               're'
              164  DELETE_FAST              're'
              166  END_FINALLY      
              168  JUMP_FORWARD        172  'to 172'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'

Parse error at or near `COME_FROM_EXCEPT' instruction at offset 122_0

    def set_managementserver(self, url, session, action, files, jobid, fixids):
        url = url + '/managementServer/updates'
        try:
            if not action == None:
                if action == 'apply':
                    url = url + '?action=apply'
                    payload = {}
                    if fixids:
                        payload['fixids'] = [
                         fixids]
                    else:
                        raise Exception('Invalid argument apply requires fixids')
                    resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    return resp
                else:
                    if not action == None and action == 'import':
                        file_list = files.strip().split(',')
                        file_type_dict = {'.txt':'text/plain',  '.xml':'text/xml', 
                         '.chg':'application/octet-stream', 
                         '.tgz':'application/x-compressed'}
                        if jobid == None:
                            url = url + '?action=import'
                            payload_files = [{'index':index,  'name':os.path.basename(file),  'size':os.path.getsize(file),  'type':file_type_dict[os.path.splitext(os.path.basename(file))[(-1)]]} for index, file in enumerate(file_list)]
                            payload = {'files': payload_files}
                            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=(2 * REST_TIMEOUT))
                            return resp
                        else:
                            url = url.replace('/managementServer/updates', '/files/managementServer/updates')
                            url = url + '?action=import&jobid=' + jobid
                            m = MultipartEncoder(fields=[('uploadedfile[]', (os.path.basename(file), open(file, 'rb'), file_type_dict[os.path.splitext(os.path.basename(file))[(-1)]])) for file in file_list])
                            monitor = MultipartEncoderMonitor(m, callback)
                            resp = session.post(url, data=monitor, headers={'Content-Type': monitor.content_type}, verify=False, timeout=(100 * REST_TIMEOUT))
                            return resp
                    else:
                        if not action == None:
                            if action == 'acquire':
                                url = url + '?action=acquire'
                                payload = {}
                                if fixids:
                                    fixids_list = fixids.split(',')
                                    payload['fixids'] = fixids_list
                                else:
                                    raise Exception('Invalid argument key action: acquire requires fixids ')
                                resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                                return resp
                    if not action == None:
                        if action == 'refresh':
                            url = url + '?action=refresh'
                            payload = {}
                            payload['mts'] = ['lxca']
                            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                            return resp
            else:
                if not action == None:
                    if action == 'delete':
                        if fixids:
                            url = url + '/' + fixids
                        else:
                            raise Exception('Invalid argument key action: delete requires fixids ')
                        resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
                        return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def do_updatecomp(self, url, session, query, mode, action, server, switch, storage, cmm, dev_list):
        if dev_list:
            resp = self.do_updatecomp_all(url, session, action, mode, dev_list)
            return resp
        serverlist = list()
        storagelist = list()
        cmmlist = list()
        switchlist = list()
        url = url + '/updatableComponents'
        try:
            if mode == None and action == None and server == None and switch == None and storage == None and cmm == None:
                if query:
                    if query.lower() == 'components':
                        url = url + '?action=getComponents'
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    return resp
                else:
                    if action == 'apply' or action == 'cancelApply':
                        url = url + '?action=' + action
                        if not mode == None and mode == 'immediate' or mode == 'delayed' or mode == 'prioritized':
                            url = url + '&activationMode=' + mode
                        else:
                            raise Exception('Invalid argument mode')
                        if server:
                            if len(server.split(',')) == 3:
                                server_data = server.split(',')
                                serverlist = [{'UUID':server_data[0],  'Components':[{'Fixid':server_data[1],  'Component':server_data[2]}]}]
                            elif len(server.split(',')) == 2:
                                server_data = server.split(',')
                                serverlist = [{'UUID':server_data[0],  'Components':[{'Component': server_data[1]}]}]
                        if switch:
                            if len(switch.split(',')) == 3:
                                switch_data = switch.split(',')
                                switchlist = [{'UUID':switch_data[0],  'Components':[{'Fixid':switch_data[1],  'Component':switch_data[2]}]}]
                            elif len(switch.split(',')) == 2:
                                switch_data = switch.split(',')
                                switchlist = [{'UUID':switch_data[0],  'Components':[{'Component': switch_data[1]}]}]
                        if storage:
                            if len(storage.split(',')) == 3:
                                storage_data = storage.split(',')
                                storagelist = [{'UUID':storage_data[0],  'Components':[{'Fixid':storage_data[1],  'Component':storage_data[2]}]}]
                            elif len(storage.split(',')) == 2:
                                storage_data = storage.split(',')
                                storagelist = [{'UUID':storage_data[0],  'Components':[{'Component': storage_data[1]}]}]
                        if cmm:
                            if len(cmm.split(',')) == 3:
                                cmm_data = cmm.split(',')
                                cmmlist = [{'UUID':cmm_data[0],  'Components':[{'Fixid':cmm_data[1],  'Component':cmm_data[2]}]}]
                            else:
                                if len(cmm.split(',')) == 2:
                                    cmm_data = cmm.split(',')
                                    cmmlist = [{'UUID':cmm_data[0],  'Components':[{'Component': cmm_data[1]}]}]
                    elif action == 'power':
                        url = url + '?action=' + 'powerState'
                        if server:
                            if len(server.split(',')) == 2:
                                server_data = server.split(',')
                                serverlist = [{'UUID':server_data[0],  'PowerState':server_data[1]}]
                        if switch:
                            if len(switch.split(',')) == 2:
                                switch_data = switch.split(',')
                                switchlist = [{'UUID':switch_data[0],  'PowerState':switch_data[1]}]
                        if storage:
                            if len(storage.split(',')) == 2:
                                storage_data = storage.split(',')
                                storagelist = [{'UUID':storage_data[0],  'PowerState':storage_data[1]}]
                        if cmm:
                            if len(cmm.split(',')) == 2:
                                cmm_data = cmm.split(',')
                                cmmlist = [{'UUID':cmm_data[0],  'PowerState':cmm_data[1]}]
                param_dict = dict()
                if serverlist:
                    param_dict['ServerList'] = serverlist
                if storagelist:
                    param_dict['StorageList'] = storagelist
            else:
                if cmmlist:
                    param_dict['CMMList'] = cmmlist
                if switchlist:
                    param_dict['SwitchList'] = switchlist
            payload = dict()
            payload['DeviceList'] = [param_dict]
            logger.debug('Update Firmware payload: ' + str(payload))
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def do_updatecomp_all(self, url, session, action, mode, dev_list):
        try:
            url = url + '/updatableComponents'
            if action == 'apply' or action == 'cancelApply':
                url = url + '?action=' + action
                if not mode == None and mode == 'immediate' or mode == 'delayed' or mode == 'prioritized':
                    url = url + '&activationMode=' + mode
                else:
                    raise Exception('Invalid argument mode')
            else:
                raise Exception('Invalid argument action')
            payload_data = json.dumps(dev_list)
            logger.debug('Update Firmware payload: ' + str(payload_data))
            resp = session.put(url, data=payload_data, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
            return resp
        except HTTPError as re:
            logger.error('Exception occured: %s', re)
            raise re

    def get_configprofiles(self, url, session, profileid):
        url = url + '/profiles'
        if profileid:
            url = url + '/' + str(profileid)
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def put_configprofiles(self, url, session, profileid, profilename):
        url = url + '/profiles'
        if profileid:
            url = url + '/' + str(profileid)
        else:
            raise Exception('Invalid argument ')
        try:
            payload = dict()
            payload['profileName'] = profilename
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def post_configprofiles(self, url, session, profileid, endpoint, restart):
        url = url + '/profiles'
        if profileid:
            url = url + '/' + str(profileid)
        else:
            raise Exception('Invalid argument ')
        try:
            payload = dict()
            if restart:
                if endpoint:
                    payload['restart'] = restart
                    payload['uuid'] = endpoint
            else:
                raise Exception('Invalid argument, restart and endpoint ')
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def delete_configprofiles(self, url, session, profileid):
        url = url + '/profiles'
        if profileid:
            url = url + '/' + str(profileid)
        try:
            resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def unassign_configprofiles(self, url, session, profileid, powerdown, resetimm, resetswitch, force):
        url = url + '/profiles/unassign'
        if profileid:
            url = url + '/' + str(profileid)
        else:
            raise Exception('Invalid argument, profile id is required for unassign ')
        payload = dict()
        if powerdown:
            if powerdown.lower() == 'true':
                payload['powerDownITE'] = True
            else:
                payload['powerDownITE'] = False
        if resetimm:
            if resetimm.lower() == 'true':
                payload['resetIMM'] = True
            else:
                payload['resetIMM'] = False
        if resetswitch:
            if resetimm.lower() == 'true':
                payload['resetSwitch'] = True
            else:
                payload['resetSwitch'] = False
        if force:
            if isinstance(force, bool):
                payload['force'] = force
            elif force:
                if force.lower() == 'true':
                    payload['force'] = True
                else:
                    payload['force'] = False
        try:
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def _validate_uuids(self, uuids):
        uuids_list = uuids.split(',')
        for uuid in uuids_list:
            if len(uuid) < 16:
                raise Exception('Invalid Arguments, uuid : %s' % uuid)

    def do_configpatterns(self, url, session, id, includeSettings, endpoint, restart, etype, pattern_update_dict):
        """
        input_dict = {}
        input_dict['id'] = id
        input_dict['includeSettings'] = includeSettings
        input_dict['endpoint'] = endpoint
        input_dict['restart'] = restart
        input_dict['type'] = etype
        input_dict['pattern_update_dict'] = pattern_update_dict

        valid_arg_combination = [[], ['id'], ['id', 'includeSettings'],
                                 ['id', 'endpoint', 'restart', 'type'],
                                 ['pattern_update_dict']]

        valid, combination = _validate_combination(input_dict, valid_arg_combination)
        if not valid:
            raise Exception("Invalid Missing Arguments %s" %str(combination))

        """
        resp = None
        url = url + '/patterns'
        if endpoint:
            self._validate_uuids(endpoint)
        if id != None:
            if len(id) == 0:
                raise Exception('Invalid Argument, id ')
            else:
                if not id.isdigit():
                    raise Exception('Invalid Argument, id is not Numeric ')
                url = url + '/' + id
                if includeSettings:
                    url = url + '/includeSettings'
        try:
            if endpoint:
                if restart:
                    if etype:
                        param_dict = dict()
                        if etype.lower() == 'node' or etype.lower() == 'rack' or etype.lower() == 'tower':
                            param_dict['uuid'] = [
                             endpoint]
                        else:
                            if etype.lower() == 'flex':
                                param_dict['endpointIds'] = [
                                 endpoint]
                        param_dict['restart'] = restart
                        payload = param_dict
                        resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            else:
                if pattern_update_dict:
                    payload = dict()
                    payload = pattern_update_dict
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                else:
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_configstatus(self, url, session, endpoint):
        resp = None
        url = url + '/config/server'
        if endpoint:
            url = url + '/' + endpoint + '/status'
        else:
            raise Exception('Invalid argument endpoint uuid is required for config status')
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_configtargets(self, url, session, targetid):
        url = url + '/config/target'
        if targetid:
            url = url + '/' + targetid
        else:
            raise Exception('Invalid argument ID')
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_tasks(self, url, session, job_uid, includeChildren):
        url = url + '/tasks'
        if job_uid:
            url = url + '/' + job_uid
        if includeChildren.lower() == 'false':
            url = url + '?compact=true'
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def post_tasks(self, url, session, post_dict):
        """
        Handle action post
        """
        url = url + '/tasks'
        payload = post_dict
        try:
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def put_tasks(self, url, session, job_uuid, action):
        """
        Handle action cancel
        """
        url = url + '/tasks'
        job_list = job_uuid.split(',')
        payload = {'action':action, 
         'list':job_list}
        try:
            resp = resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def delete_tasks(self, url, session, job_uuid):
        """
        Handle action delete
        """
        url = url + '/tasks/' + job_uuid
        try:
            resp = resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def put_tasks_update(self, url, session, updated_dict):
        """
        Handle action update
        """
        url = url + '/tasks' + '/' + updated_dict[0]['jobUID']
        payload = updated_dict[0]
        try:
            resp = resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_set_manifests(self, url, session, sol_id, filepath):
        resp = None
        param_dict = dict()
        url = url + '/manifests'
        try:
            if sol_id:
                url = url + '/' + str(sol_id)
            else:
                raise Exception('Invalid argument ID')
            if filepath:
                param_dict['filepath'] = filepath
                payload = dict()
                payload = param_dict
                resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            else:
                resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

    def list_resourcegroups(self, url, session, uuid):
        url = url + '/resourceGroups'
        try:
            if uuid:
                url = url + '/' + uuid
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def criteriaproperties_resourcegroups(self, url, session):
        url = url + '/resourceGroups/criteriaProperties'
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def delete_resourcegroups(self, url, session, uuid):
        url = url + '/resourceGroups'
        try:
            url = url + '/' + uuid
            resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def dynamic_resourcegroups(self, url, session, uuid, name, desc, type, criteria):
        resp = None
        url = url + '/resourceGroups'
        try:
            param_dict = dict()
            param_dict['name'] = name
            param_dict['description'] = desc
            param_dict['type'] = type
            param_dict['criteria'] = criteria
            if uuid:
                param_dict['uuid'] = uuid
                resp = session.put(url, data=(json.dumps(param_dict)), verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                return resp
            if name:
                resp = session.post(url, data=(json.dumps(param_dict)), verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def solution_resourcegroups(self, url, session, uuid, name, desc, type, solutionVPD, members, criteria):
        resp = None
        url = url + '/resourceGroups'
        try:
            if uuid:
                url = url + '/' + uuid
                if members:
                    payload = []
                    for dev in members:
                        param_dict = dict()
                        param_dict['op'] = 'add'
                        param_dict['path'] = '/members/-'
                        param_dict['value'] = dev
                        payload.append(param_dict)

                    resp = session.patch(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    return resp
            else:
                if name:
                    param_dict = dict()
                    param_dict['name'] = name
                    param_dict['description'] = desc
                    param_dict['type'] = type
                    if type == 'solution':
                        if isinstance(solutionVPD, dict):
                            if set(['id', 'machineType', 'model', 'serialNumber', 'manufacturer']).issubset(set(solutionVPD.keys())):
                                param_dict['solutionVPD'] = solutionVPD
                    else:
                        raise ValueError('Invalid Argument SolutionVPD')
                    param_dict['members'] = members
                    param_dict['criteria'] = None
                    payload = dict()
                    payload = param_dict
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def list_osimage(self, url, session):
        resp = None
        url = url + '/osImages'
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_globalsettings(self, url, session, kwargs):
        resp = None
        url = url + '/osdeployment/globalSettings'
        try:
            if kwargs:
                if set(['activeDirectory', 'credentials', 'ipAssignment', 'isVLANMode', 'licenseKeys']).difference(set(kwargs.keys())):
                    raise Exception("Invalid Arguments, Try:['activeDirectory'=<list>, 'credentials'=<list>,'ipAssignment','isVLANMode','licenseKeys'=<dict>]")
                if not isinstance(kwargs['activeDirectory'], dict) or not isinstance(kwargs['credentials'], list) or not isinstance(kwargs['licenseKeys'], dict):
                    raise Exception("Invalid Arguments, Try:['activeDirectory'=<list>, 'credentials'=<list>,'licenseKeys'=<dict>]")
                payload = {}
                for k, v in list(kwargs.items()):
                    payload[k] = v

                resp = self.put_method(url, session, payload)
                return resp
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def create_osimage_hostsettings(self, url, session, hosts):
        resp = None
        url = url + '/osdeployment/hostSettings'
        try:
            if hosts:
                for kwargs in hosts:
                    if set(['uuid', 'storageSettings', 'networkSettings']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
                    if not isinstance(kwargs['storageSettings'], dict) or not isinstance(kwargs['networkSettings'], dict):
                        raise Exception("Invalid Arguments, Try:['storageSettings'=<dict>, 'networkSettings'=<dict>]")

                payload = hosts
                resp = self.post_method(url, session, payload)
                return resp
            raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def update_osimage_hostsettings(self, url, session, hosts):
        resp = None
        url = url + '/osdeployment/hostSettings'
        try:
            if hosts:
                for kwargs in hosts:
                    if set(['uuid', 'storageSettings', 'networkSettings']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
                    if not isinstance(kwargs['storageSettings'], dict) or not isinstance(kwargs['networkSettings'], dict):
                        raise Exception("Invalid Arguments, Try:['storageSettings'=<dict>, 'networkSettings'=<dict>]")

                payload = hosts
                resp = self.put_method(url, session, payload)
                return resp
            raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def list_osimage_hostsettings(self, url, session, kwargs):
        resp = None
        url = url + '/osdeployment/hostSettings'
        if kwargs:
            if 'uuid' in kwargs:
                url = url + '/' + kwargs['uuid']
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def delete_osimage_hostsettings(self, url, session, kwargs):
        resp = None
        url = url + '/osdeployment/hostSettings'
        if kwargs:
            if 'uuid' in kwargs:
                url = url + '/' + kwargs['uuid']
        else:
            raise Exception('Invalid Arguments, Try:uuid is required')
        try:
            resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_hostplatforms(self, url, session, kwargs):
        resp = None
        url = url + '/hostPlatforms'
        try:
            if kwargs:
                if set(['networkSettings', 'selectedImage', 'storageSettings', 'uuid']).difference(set(kwargs.keys())):
                    raise Exception("Invalid Arguments, Try:['networkSettings'=<dict>, 'selectedImage', 'storageSettings'=<dict>,'uuid',]")
                if not isinstance(kwargs['networkSettings'], dict) or not isinstance(kwargs['storageSettings'], dict):
                    raise Exception('Invalid Arguments, Try: networkSettings=<dict>, and storageSettings=<dict>')
                payload = {}
                for k, v in list(kwargs.items()):
                    payload[k] = v

                resp = self.put_method(url, session, [payload])
                return resp
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_import(self, url, session, kwargs):
        resp = None
        try:
            payload = {}
            if 'imageType' in kwargs:
                if 'jobId' not in kwargs:
                    url = url + '/osImages'
                    if kwargs['imageType'] not in ('BUNDLE', 'BUNDLESIG', 'BOOT', 'DUD',
                                                   'OS', 'OSPROFILE', 'SCRIPT', 'CUSTOM_CONFIG',
                                                   'UNATTEND'):
                        raise Exception("Invalid Arguments, Try: [BUNDLE,BUNDLESIG,BOOT,DUD,OS,OSPROFILE,SCRIPT, 'CUSTOM_CONFIG', 'UNATTEND']")
                    if 'fileSize' in kwargs:
                        payload['fileSize'] = kwargs['fileSize']
                    url = url + '/?imageType=' + kwargs['imageType']
                    payload['Action'] = 'Init'
                    resp = self.post_method(url, session, payload)
                    return resp
            if 'jobId' in kwargs:
                url = url + '/files/osImages'
                url = url + '?'
                if kwargs['imageType'] in ('BOOT', 'DUD', 'OS', 'OSPROFILE', 'SCRIPT',
                                           'CUSTOM_CONFIG', 'UNATTEND'):
                    if set(['jobId', 'imageName', 'imageType', 'os']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType','os']")
                else:
                    if kwargs['imageType'] in ('BUNDLE', 'BUNDLESIG'):
                        if set(['jobId', 'imageName', 'imageType']).difference(set(kwargs.keys())):
                            raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType']")
                if kwargs['imageType'] in ('BOOT', 'DUD'):
                    if 'osrelease' not in kwargs:
                        raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType','os','osrelease]")
                if 'serverId' in kwargs:
                    payload_keylist = [
                     'serverId', 'path']
                    for k, v in list(kwargs.items()):
                        if k in payload_keylist:
                            payload[k] = v
                        else:
                            url = url + '%s=%s&' % (k, v)

                    url = url.rstrip('&')
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=(100 * REST_TIMEOUT))
                    return resp
                else:
                    if not kwargs['file']:
                        raise Exception('Invalid Arguments, file is required for local import')
                    url = url + 'jobId=' + str(kwargs['jobId']) + '&'
                    kwargs.pop('jobId')
                    for k in ('imageName', 'imageType', 'os', 'description'):
                        if k in kwargs:
                            url = url + '%s=%s&' % (k, kwargs[k])

                    if 'osrelease' in kwargs:
                        url = url + '%s=%s&' % ('osrelease', kwargs['osrelease'])
                    url = url.rstrip('&')
                    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
                    m = MultipartEncoder(fields={'name':'uploadedfile', 
                     'uploadedfile':(os.path.basename(kwargs['file']), open(kwargs['file'], 'rb'), 'application/octet-stream')})
                    monitor = MultipartEncoderMonitor(m, callback)
                    logger.debug('before sending second call')
                    resp = session.post(url, data=monitor, headers={'Content-Type': monitor.content_type}, verify=False, timeout=(100 * REST_TIMEOUT))
                    logger.debug('after  second call response')
                    return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_remotefileservers(self, url, session, kwargs):
        resp = None
        try:
            payload = {}
            url = url + '/osImages/remoteFileServers'
            if 'putid' in kwargs or 'deleteid' in kwargs:
                if 'putid' in kwargs:
                    url = url + '/' + kwargs['putid']
                    kwargs.pop('putid')
                    if set(['address', 'displayName', 'port', 'protocol']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['address','displayName','port', 'protocol']")
                    for k, v in list(kwargs.items()):
                        payload[k] = v

                    resp = self.put_method(url, session, payload)
                    return resp
                if 'deleteid' in kwargs:
                    if list(kwargs.keys()).__len__() != 1:
                        raise Exception('Invalid Arguments, Try:deleteid=<id> only')
                    url = url + '/' + kwargs['deleteid']
                    payload = {}
                    resp = self.delete_method(url, session, payload)
                    return resp
            else:
                if 'address' in kwargs and 'putid' not in kwargs and 'deleteid' not in kwargs:
                    if set(['address', 'displayName', 'port', 'protocol']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['address','displayName','port', 'protocol']")
                    for k, v in list(kwargs.items()):
                        payload[k] = v

                    resp = self.post_method(url, session, payload)
                    return resp
                else:
                    if 'id' in kwargs:
                        url = url + '/' + kwargs['id']
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

    def create_osimage_hostsettings(self, url, session, hosts):
        resp = None
        url = url + '/osdeployment/hostSettings'
        try:
            if hosts:
                for kwargs in hosts:
                    if set(['uuid', 'storageSettings', 'networkSettings']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
                    if not isinstance(kwargs['storageSettings'], dict) or not isinstance(kwargs['networkSettings'], dict):
                        raise Exception("Invalid Arguments, Try:['storageSettings'=<dict>, 'networkSettings'=<dict>]")

                payload = hosts
                resp = self.post_method(url, session, payload)
                return resp
            raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def update_osimage_hostsettings(self, url, session, hosts):
        resp = None
        url = url + '/osdeployment/hostSettings'
        try:
            if hosts:
                for kwargs in hosts:
                    if set(['uuid', 'storageSettings', 'networkSettings']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
                    if not isinstance(kwargs['storageSettings'], dict) or not isinstance(kwargs['networkSettings'], dict):
                        raise Exception("Invalid Arguments, Try:['storageSettings'=<dict>, 'networkSettings'=<dict>]")

                payload = hosts
                resp = self.put_method(url, session, payload)
                return resp
            raise Exception("Invalid Arguments, Try:[{'storageSettings'=<dict>, 'networkSettings'=<dict>,'uuid'}]")
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def list_osimage_hostsettings(self, url, session, kwargs):
        resp = None
        url = url + '/osdeployment/hostSettings'
        if kwargs:
            if 'uuid' in kwargs:
                url = url + '/' + kwargs['uuid']
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def delete_osimage_hostsettings(self, url, session, kwargs):
        resp = None
        url = url + '/osdeployment/hostSettings'
        if kwargs:
            if 'uuid' in kwargs:
                url = url + '/' + kwargs['uuid']
        else:
            raise Exception('Invalid Arguments, Try:uuid is required')
        try:
            resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_hostplatforms(self, url, session, kwargs):
        resp = None
        url = url + '/hostPlatforms'
        try:
            if kwargs:
                if set(['networkSettings', 'selectedImage', 'storageSettings', 'uuid']).difference(set(kwargs.keys())):
                    raise Exception("Invalid Arguments, Try:['networkSettings'=<dict>, 'selectedImage', 'storageSettings'=<dict>,'uuid',]")
                if not isinstance(kwargs['networkSettings'], dict) or not isinstance(kwargs['storageSettings'], dict):
                    raise Exception('Invalid Arguments, Try: networkSettings=<dict>, and storageSettings=<dict>')
                payload = {}
                for k, v in list(kwargs.items()):
                    payload[k] = v

                resp = self.put_method(url, session, [payload])
                return resp
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_import(self, url, session, kwargs):
        resp = None
        try:
            payload = {}
            if 'imageType' in kwargs:
                if 'jobId' not in kwargs:
                    url = url + '/osImages'
                    if kwargs['imageType'] not in ('BUNDLE', 'BUNDLESIG', 'BOOT', 'DUD',
                                                   'OS', 'OSPROFILE', 'SCRIPT', 'CUSTOM_CONFIG',
                                                   'UNATTEND'):
                        raise Exception("Invalid Arguments, Try: [BUNDLE,BUNDLESIG,BOOT,DUD,OS,OSPROFILE,SCRIPT, 'CUSTOM_CONFIG', 'UNATTEND']")
                    if 'fileSize' in kwargs:
                        payload['fileSize'] = kwargs['fileSize']
                    url = url + '/?imageType=' + kwargs['imageType']
                    payload['Action'] = 'Init'
                    resp = self.post_method(url, session, payload)
                    return resp
            if 'jobId' in kwargs:
                url = url + '/files/osImages'
                url = url + '?'
                if kwargs['imageType'] in ('BOOT', 'DUD', 'OS', 'OSPROFILE', 'SCRIPT',
                                           'CUSTOM_CONFIG', 'UNATTEND'):
                    if set(['jobId', 'imageName', 'imageType', 'os']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType','os']")
                else:
                    if kwargs['imageType'] in ('BUNDLE', 'BUNDLESIG'):
                        if set(['jobId', 'imageName', 'imageType']).difference(set(kwargs.keys())):
                            raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType']")
                        ext = os.path.splitext(os.path.basename(kwargs['imageName']))[(-1)]
                        if ext not in ('.zip', '.asc'):
                            raise Exception("Invalid Arguments, Try:imageName extension with ['.asc','.zip'")
                if kwargs['imageType'] in ('BOOT', 'DUD'):
                    if 'osrelease' not in kwargs:
                        raise Exception("Invalid Arguments, Try:['jobId','imageName','imageType','os','osrelease]")
                if 'serverId' in kwargs:
                    payload_keylist = [
                     'serverId', 'path']
                    for k, v in list(kwargs.items()):
                        if k in payload_keylist:
                            payload[k] = v
                        else:
                            url = url + '%s=%s&' % (k, v)

                    url = url.rstrip('&')
                    resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=(100 * REST_TIMEOUT))
                    return resp
                else:
                    if not kwargs['file']:
                        raise Exception('Invalid Arguments, file is required for local import')
                    url = url + 'jobId=' + str(kwargs['jobId']) + '&'
                    kwargs.pop('jobId')
                    for k in ('imageName', 'imageType', 'os', 'description'):
                        if k in kwargs:
                            url = url + '%s=%s&' % (k, kwargs[k])

                    if 'osrelease' in kwargs:
                        url = url + '%s=%s&' % ('osrelease', kwargs['osrelease'])
                    url = url.rstrip('&')
                    url = urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]")
                    m = MultipartEncoder(fields={'name':'uploadedfile', 
                     'uploadedfile':(os.path.basename(kwargs['file']), open(kwargs['file'], 'rb'), 'application/octet-stream')})
                    logger.debug('before sending second call')
                    resp = session.post(url, data=m, headers={'Content-Type': m.content_type}, verify=False, timeout=(100 * REST_TIMEOUT))
                    logger.debug('after  second call response')
                    return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_remotefileservers(self, url, session, kwargs):
        resp = None
        try:
            payload = {}
            url = url + '/osImages/remoteFileServers'
            if 'putid' in kwargs or 'deleteid' in kwargs:
                if 'putid' in kwargs:
                    url = url + '/' + kwargs['putid']
                    kwargs.pop('putid')
                    if set(['address', 'displayName', 'port', 'protocol']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['address','displayName','port', 'protocol']")
                    for k, v in list(kwargs.items()):
                        payload[k] = v

                    resp = self.put_method(url, session, payload)
                    return resp
                if 'deleteid' in kwargs:
                    if list(kwargs.keys()).__len__() != 1:
                        raise Exception('Invalid Arguments, Try:deleteid=<id> only')
                    url = url + '/' + kwargs['deleteid']
                    payload = {}
                    resp = self.delete_method(url, session, payload)
                    return resp
            else:
                if 'address' in kwargs and 'putid' not in kwargs and 'deleteid' not in kwargs:
                    if set(['address', 'displayName', 'port', 'protocol']).difference(set(kwargs.keys())):
                        raise Exception("Invalid Arguments, Try:['address','displayName','port', 'protocol']")
                    for k, v in list(kwargs.items()):
                        payload[k] = v

                    resp = self.post_method(url, session, payload)
                    return resp
                else:
                    if 'id' in kwargs:
                        url = url + '/' + kwargs['id']
                    resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
                    resp.raise_for_status()
                    return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def osimage_delete(self, url, session, kwargs):
        resp = None
        url = url + '/osImages'
        try:
            if 'id' not in kwargs:
                raise Exception("Invalid Arguments, Try: id='id1,id2, .. ,idn' ")
            url = url + '/' + str(kwargs['id'])
            resp = self.delete_method(url, session, payload={})
            return resp
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_method(self, url, session, **kwargs):
        resp = None
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def put_method(self, url, session, payload, **kwargs):
        resp = None
        try:
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=60)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def delete_method(self, url, session, payload, **kwargs):
        resp = None
        try:
            resp = session.delete(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def post_method(self, url, session, payload, **kwargs):
        resp = None
        try:
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def get_rules(self, url, session, id):
        url = url + '/compliance/rules'
        if id:
            url = url + '/' + id
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def set_rules(self, url, session, rule):
        resp = None
        url = url + '/compliance/rules'
        try:
            resp = session.post(url, data=(json.dumps(rule)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_compositeResults(self, url, session, id, query_solutionGroups):
        url = url + '/compliance/compositeResults'
        if id:
            url = url + '/' + id
        else:
            if query_solutionGroups:
                url = url + '?groupID=' + query_solutionGroups
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def set_compositeResults(self, url, session, solutionGroups, targetResources, all_rules):
        resp = None
        url = url + '/compliance/compositeResults'
        try:
            if all_rules:
                resp = session.post(url, verify=False, timeout=REST_TIMEOUT)
                resp.raise_for_status()
                return resp
            payload = dict()
            if solutionGroups:
                payload['solutionGroups'] = solutionGroups
            else:
                if targetResources:
                    payload['targetResources'] = targetResources
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def get_storedcredentials(self, url, session, id):
        """
        Get stored credential details
        :param url:
        :param session:
        :param id:
        :return:
        """
        url = url + '/storedCredentials'
        if id:
            url = url + '/' + id
        try:
            resp = session.get(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp

    def post_storedcredentials(self, url, session, user_name, password, description):
        """
        Add new credentials to store
        :param url:
        :param session:
        :param user_name:
        :param password:
        :param description:
        :return:
        """
        resp = None
        url = url + '/storedCredentials'
        try:
            payload = dict()
            payload['userName'] = user_name
            payload['password'] = password
            payload['description'] = description
            resp = session.post(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def put_storedcredentials(self, url, session, id, user_name, password, description):
        """
        Update already stored credential with specified id
        :param url:
        :param session:
        :param id:
        :param user_name:
        :param password:
        :param description:
        :return:
        """
        resp = None
        url = url + '/storedCredentials'
        if id:
            url = url + '/' + id
        else:
            raise Exception('Invalid Arguments, id is mandatory for put operation only')
        if not user_name or not password:
            raise Exception('Invalid Arguments, userName and password are mandatory for put operation only')
        try:
            payload = dict()
            payload['userName'] = user_name
            payload['password'] = password
            payload['description'] = description
            resp = session.put(url, data=(json.dumps(payload)), verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            raise re

        return resp

    def delete_storedcredentials(self, url, session, delete_id):
        """
        delete stored credential with specified id.
        :param url:
        :param session:
        :param delete_id:
        :return:
        """
        url = url + '/storedCredentials'
        if id:
            url = url + '/' + delete_id
        try:
            resp = session.delete(url, verify=False, timeout=REST_TIMEOUT)
            resp.raise_for_status()
        except HTTPError as re:
            logger.error('REST API Exception: Exception = %s', re)
            raise re

        return resp