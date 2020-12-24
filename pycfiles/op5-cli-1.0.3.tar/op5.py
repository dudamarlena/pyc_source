# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ozan/git_trees/op5-cli/op5lib/op5.py
# Compiled at: 2015-09-22 05:30:11
from urllib import quote
import requests, json
from termcolor import colored
import time, sys, logging
logger = logging.getLogger('op5')

class NullHandler(logging.Handler):
    """
    For backward-compatibility with Python 2.6, a local class definition
    is used instead of logging.NullHandler
    """

    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None
        return


logger.addHandler(NullHandler())

class OP5(object):

    def __init__(self, api_url, api_username, api_password, dryrun=False, debug=False, logtofile=False, interactive=False):
        self.api_url = api_url
        self.api_username = api_username
        self.api_password = api_password
        self.dryrun = dryrun
        self.debug = debug
        self.interactive = interactive
        self.data = []
        self.status_code = -1
        self.logtofile = logtofile
        self.modified = False

    def get_debug_text(self, request_type, object_type, name, data):
        text = '%s(%s)' % (request_type, object_type)
        if name != '':
            text += ' name: %s' % name
        if not data:
            return text
        if object_type in ('host', 'hostgroup', 'service'):
            text += ' ('
            interesting_fields = ['service_description', 'host_name', 'hostgroup_name', 'address', 'hostgroups', 'contact_groups', 'check_command', 'check_command_args']
            available_fields = filter(lambda x: x in data, interesting_fields)
            text += (', ').join("%s='%s'" % (key, value) for key, value in [ (field, data[field]) for field in available_fields ])
            text += ')'
            return text
        if object_type == 'change':
            if request_type == 'GET':
                return 'Got list of changes'
            if request_type == 'POST':
                return 'Commit saved'
            if request_type == 'DELETE':
                return 'Changes removed'
        else:
            return '%s(%s) data: %s' % (request_type, object_type, data)

    def filter(self, api_type, query):
        return self.filter_operation(api_type, query)

    def create(self, object_type, data_dict):
        return self.operation('POST', object_type, data=data_dict)

    def read(self, object_type, name):
        return self.operation('GET', object_type, name)

    def update(self, object_type, name, data):
        return self.operation('PATCH', object_type, name, data)

    def delete(self, object_type, name):
        return self.operation('DELETE', object_type, name)

    def overwrite(self, object_type, name, data):
        return self.operation('PUT', object_type, name, data)

    def get_changes(self):
        return self.operation('GET', 'change')

    def undo_changes(self):
        return self.operation('DELETE', 'change')

    def commit_changes(self, force=False):
        fname = sys._getframe().f_code.co_name
        if not self.modified and not force:
            if self.debug:
                print colored('%s(): Not attempting commit since nothing has been modified' % fname, 'yellow')
            return False
        self.get_changes()
        if len(self.data) > 0:
            return self.operation('POST', 'change')
        else:
            print colored('%s(): Not attempting commit since nothing has been modified on the server' % fname, 'red')
            return False

    def get_group_members(self, object_type, group_name):
        if object_type in ('hostgroup', 'contactgroup', 'servicegroup', 'usergroup'):
            if self.read(object_type, group_name):
                if 'members' in self.data:
                    return self.data['members']
            else:
                return []
        else:
            fname = sys._getframe().f_code.co_name
            print colored("%s(): object_type '%s' is not valid" % (fname, object_type), 'red')
            return False

    def sync(self, object_type, name, data_at_source):
        if self.read(object_type, name):
            data_at_destination = self.data
            for key in data_at_source:
                if key not in data_at_destination or set(data_at_source[key]) != set(data_at_destination[key]):
                    if self.debug:
                        print 'Data at source:', data_at_source
                        print 'Data at destination:', data_at_destination
                    print key, ':', data_at_source[key], 'did not match', key, ':', data_at_destination.get(key, None), '! Making an update request.'
                    return self.update(object_type, name, data_at_source)

        else:
            return self.create(object_type, data_at_source)
        return

    def validate_object(self, request_type, object_type, data):
        required_properties = {}
        required_properties['default'] = [
         [
          'name', object_type + '_name']]
        required_properties['graph_template'] = ['check']
        required_properties['hostdependency'] = ['dependent_host_name', 'host_name']
        required_properties['hostescalation'] = ['first_notification', 'host_name', 'last_notification', 'notification_interval']
        required_properties['service'] = [['host_name', 'hostgroup_name'], 'service_description']
        required_properties['servicedependency'] = ['dependent_service', 'service']
        required_properties['user'] = ['username', 'password']
        if object_type in required_properties:
            required_properties_list = required_properties[object_type]
        else:
            required_properties_list = required_properties['default']
        validation_passed = True
        for req_prop in required_properties_list:
            if isinstance(req_prop, list):
                if not any(sub_req_prop in data for sub_req_prop in req_prop):
                    validation_passed = False
                    break
            elif req_prop not in data:
                validation_passed = False
                break

        if not validation_passed:
            print colored('%s(%s): All required properties for a %s object not set in data! data: %s' % (request_type, object_type, object_type, str(data)), 'red')
            return False
        return True

    def validate_request(self, request_type, object_type, name, data):
        if request_type not in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'):
            print colored("%s(%s): Invalid request type! name:'%s' data: %s" % (request_type, object_type, name, str(data)), 'red')
            return False
        if object_type != 'change':
            valid_object_types = [
             'host', 'hostgroup', 'service', 'servicegroup', 'contact', 'contactgroup', 'host_template', 'service_template', 'contact_template', 'hostdependency', 'servicedependency', 'hostescalation', 'serviceescalation', 'user', 'usergroup', 'combined_graph', 'graph_collection', 'graph_template', 'management_pack', 'timeperiod']
            if object_type not in valid_object_types:
                print colored("%s(%s): Invalid object type! name:'%s' data: %s" % (request_type, object_type, name, str(data)), 'red')
                return False
            if request_type in ('POST', 'PATCH', 'PUT') and not data:
                print colored('%s(%s): data not set! data: %s' % (request_type, object_type, str(data)), 'red')
                return False
            if request_type in ('PATCH', 'PUT', 'DELETE') and name == '':
                print colored('%s(%s): name not set! data: %s' % (request_type, object_type, str(data)), 'red')
                return False
            if request_type != 'POST' and object_type == 'service' and name != '' and name.count(';') == 0:
                print colored("%s(%s): Invalid service name! name:'%s' data: %s" % (request_type, object_type, name, str(data)), 'red')
                return False
            if request_type == 'POST':
                if not self.validate_object(request_type, object_type, data):
                    return False
        return True

    def filter_operation(self, api_type, query, rdepth=0):
        url = self.api_url + '/filter/' + api_type
        query = 'query=' + query.encode('UTF-8')
        if self.debug or self.dryrun:
            text = 'GET ' + url
            text += " Query string: '" + str(query) + "'"
            print text
        if self.dryrun:
            return False
        http_headers = {'content-type': 'application/json'}
        try:
            r = requests.get(url, auth=(self.api_username, self.api_password), params=query, headers=http_headers, timeout=10)
        except Exception as e:
            self.data = str(e)
            import pprint
            pprint.pprint(e)
            return False

        if self.debug:
            print r.status_code
            print r.text
            print r.headers
        try:
            self.data = json.loads(r.text)
        except ValueError as e:
            self.data = r.text
            if r.status_code == 509:
                print colored('ERROR: OP5 internal sanity protections activated. Please wait for a while and try again..', 'red')
                return
            if r.text.find('index mismatch') != -1 or r.status_code not in (200, 201) and r.headers['content-type'].find('text/html') != -1:
                raise e

        self.status_code = r.status_code
        if r.status_code != 200:
            print colored('GET(filter/%s): got HTTP Status Code %d %s. Query string: %s' % (api_type, r.status_code, r.reason, query), 'red')
            print colored('GET(filter/%s): got HTTP Response: %s' % (api_type, r.text), 'red')
            if self.logtofile:
                logger.error('GET(filter/%s): got HTTP Status Code %d %s. Query string: %s' % (api_type, r.status_code, r.reason, query))
                logger.error('GET(filter/%s): got HTTP Response: %s' % (api_type, r.text))
                logger.debug('GET(%s): HTTP Response headers were: %s' % (api_type, r.headers))
            return False
        if not self.interactive:
            print colored("GET(filter/%s): Query string: '%s'" % (api_type, query), 'green')
        if self.logtofile:
            logger.info("GET(filter/%s): Query string: '%s'" % (api_type, query))
        return True

    def operation(self, request_type, object_type, name='', data=None, rdepth=0):
        url = self.api_url + '/config/' + object_type
        if not self.validate_request(request_type, object_type, name, data):
            return False
        if (request_type in ('PATCH', 'PUT', 'DELETE') or request_type == 'GET' and name != '') and object_type == 'service':
            print 'INFO: Checking if the given name is a hostgroup first.'
            if self.read('hostgroup', name.split(';')[0]):
                name += '?parent_type=hostgroup'
        if request_type in ('GET', 'PATCH', 'PUT', 'DELETE') and object_type != 'change':
            url += '/' + quote(name.encode('UTF-8'))
        if self.debug:
            text = request_type + ' ' + url
            if data:
                text += ' Sent data: ' + str(data)
            print text
        if self.dryrun and request_type != 'GET':
            print colored('DRYRUN: ' + self.get_debug_text(request_type, object_type, name, data), 'yellow')
            return False
        http_headers = {'content-type': 'application/json'}
        try:
            r = getattr(requests, request_type.lower())(url, auth=(self.api_username, self.api_password), data=json.dumps(data), headers=http_headers, timeout=10)
        except Exception as e:
            self.data = str(e)
            import pprint
            pprint.pprint(e)
            return False

        if self.debug:
            print r.status_code
            print r.text
            print r.headers
        try:
            self.data = json.loads(r.text)
        except ValueError as e:
            self.data = r.text
            if r.status_code == 509:
                rdepth += 1
                if rdepth < 3:
                    print colored('ERROR: OP5 internal sanity protections activated. Waiting for a while before trying again..', 'red')
                    time.sleep(6)
                    return self.operation(request_type, object_type, name, data, rdepth)
                raise RuntimeError('Bailing out after 3 retries on HTTP 509 OP5 Sanity Protection Error')
            if r.text.find('index mismatch') != -1 or r.status_code not in (200, 201) and r.headers['content-type'].find('text/html') != -1:
                raise e

        self.status_code = r.status_code
        if r.status_code != 200 and r.status_code != 201 and r.status_code != 500:
            print colored("%s(%s): got HTTP Status Code %d %s. Name: '%s'. Sent data: %s" % (request_type, object_type, r.status_code, r.reason, name, str(data)), 'red')
            print colored('%s(%s): got HTTP Response: %s' % (request_type, object_type, r.text), 'red')
            if self.logtofile:
                logger.error("%s(%s): got HTTP Status Code %d %s. Name: '%s'. Sent data: %s" % (request_type, object_type, r.status_code, r.reason, name, str(data)))
                logger.error('%s(%s): got HTTP Response: %s' % (request_type, object_type, r.text))
                logger.debug('%s(%s): HTTP Response headers were: %s' % (request_type, object_type, r.headers))
            return False
        if r.status_code == 500:
            rdepth += 1
            if rdepth < 3:
                json_obj = json.loads(r.text)
                if json_obj['error'] == 'Export failed' and json_obj['full_error']['type'] == 'nothing to do':
                    return False
                time.sleep(6)
                return self.operation(request_type, object_type, name, data, rdepth)
            raise RuntimeError('Bailing out after 3 retries on HTTP 500 Internal Error')
        if not self.interactive:
            print colored(self.get_debug_text(request_type, object_type, name, data), 'green')
        if request_type != 'GET' and self.logtofile:
            logger.info(self.get_debug_text(request_type, object_type, name, data))
        if request_type != 'GET' and object_type != 'change':
            self.modified = True
        elif object_type == 'change' and (request_type in ('POST', 'DELETE') or request_type == 'GET' and len(self.data) == 0):
            self.modified = False
        return True