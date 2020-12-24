# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/Projects/tenable/nessrest/nessrest/ness6rest.py
# Compiled at: 2017-05-20 10:09:12
from __future__ import print_function
import os, sys, atexit, time, requests, json, collections

class SSLException(Exception):
    pass


class Scanner(object):
    """
    Scanner object
    """

    def __init__(self, url, login='', password='', api_akey='', api_skey='', insecure=False, ca_bundle=''):
        self.api_akey = None
        self.api_skey = None
        self.use_api = False
        self.name = ''
        self.policy_name = ''
        self.debug = False
        self.format = ''
        self.format_start = ''
        self.format_end = ''
        self.http_response = ''
        self.plugins = {}
        self.names = {}
        self.files = {}
        self.cisco_offline_configs = ''
        self.permissions = ''
        self.policy_id = ''
        self.policy_object = ''
        self.pref_cgi = ''
        self.pref_paranoid = ''
        self.pref_supplied = ''
        self.pref_thorough = ''
        self.pref_max_checks = ''
        self.pref_receive_timeout = ''
        self.set_safe_checks = ''
        self.pref_verbose = ''
        self.pref_silent_dependencies = ''
        self.res = {}
        self.scan_id = ''
        self.scan_name = ''
        self.scan_template_uuid = ''
        self.scan_uuid = ''
        self.tag_id = ''
        self.tag_name = ''
        self.targets = ''
        self.policy_template_uuid = ''
        self.token = ''
        self.url = url
        self.ver_feed = ''
        self.ver_gui = ''
        self.ver_plugins = ''
        self.ver_svr = ''
        self.ver_web = ''
        self.ca_bundle = ca_bundle
        self.insecure = insecure
        self.auth = []
        self.host_vulns = {}
        self.plugin_output = {}
        self.host_details = {}
        self.host_ids = {}
        if insecure and hasattr(requests, 'packages'):
            requests.packages.urllib3.disable_warnings()
        if api_akey and api_skey:
            self.api_akey = api_akey
            self.api_skey = api_skey
            self.use_api = True
        else:
            self._login(login, password)
            atexit.register(self.action, action='session', method='DELETE', retry=False)
        self._get_permissions()
        self._get_scanner_id()
        return

    def _login(self, login='', password=''):
        if login and password:
            self.auth = [
             login, password]
        self.action(action='session', method='POST', extra={'username': self.auth[0], 'password': self.auth[1]}, private=True, retry=False)
        try:
            self.token = self.res['token']
        except KeyError:
            if self.res['error']:
                print("It looks like you're trying to login into a Nessus 5")
                print('instance. Exiting.')
                sys.exit(0)

    def _get_permissions(self):
        """
        All development has been conducted using and administrator account which
        had the permissions '128'
        """
        self.action(action='session', method='GET')
        self.permissions = self.res['permissions']

    def _get_scanner_id(self):
        """
        Pull in information about scanner. The ID is necessary, everything else
        is "nice to have" for debugging.
        """
        self.action(action='scanners', method='GET')
        try:
            for scanner in self.res['scanners']:
                if scanner['type'] == 'local':
                    self.scanner_id = scanner['id']
                    self.ver_plugins = scanner['loaded_plugin_set']
                    self.ver_gui = scanner['ui_version']
                    self.ver_svr = scanner['engine_version']
                    self.ver_feed = scanner['license']['type']

        except:
            pass

    def action(self, action, method, extra={}, files={}, json_req=True, download=False, private=False, retry=True):
        """
        Generic actions for REST interface. The json_req may be unneeded, but
        the plugin searching functionality does not use a JSON-esque request.
        This is a backup setting to be able to change content types on the fly.
        """
        payload = {}
        payload.update(extra)
        if self.use_api:
            headers = {'X-ApiKeys': 'accessKey=' + self.api_akey + '; secretKey=' + self.api_skey}
        else:
            headers = {'X-Cookie': 'token=' + str(self.token)}
        if json_req:
            headers.update({'Content-type': 'application/json', 'Accept': 'text/plain'})
            payload = json.dumps(payload)
        url = '%s/%s' % (self.url, action)
        if self.debug:
            if private:
                print('JSON    : **JSON request hidden**')
            else:
                print('JSON    :')
                print(payload)
            print('HEADERS :')
            print(headers)
            print('URL     : %s ' % url)
            print('METHOD  : %s' % method)
            print('\n')
        if self.insecure:
            verify = False
        else:
            if self.ca_bundle:
                verify = self.ca_bundle
            else:
                verify = True
            try:
                req = requests.request(method, url, data=payload, files=files, verify=verify, headers=headers)
                if not download and req.text:
                    self.res = req.json()
                else:
                    if not req.text:
                        self.res = {}
                    if req.status_code != 200:
                        print('*****************START ERROR*****************')
                        if private:
                            print('JSON    : **JSON request hidden**')
                        else:
                            print('JSON    :')
                            print(payload)
                            print(files)
                        print('HEADERS :')
                        print(headers)
                        print('URL     : %s ' % url)
                        print('METHOD  : %s' % method)
                        print('RESPONSE: %d' % req.status_code)
                        print('\n')
                        self.pretty_print()
                        print('******************END ERROR******************')
                    if self.debug:
                        print('RESPONSE CODE: %d' % req.status_code)
                    if download:
                        return req.content
            except requests.exceptions.SSLError as ssl_error:
                raise SSLException('%s for %s.' % (ssl_error, url))
            except requests.exceptions.ConnectionError:
                raise Exception('Could not connect to %s.\nExiting!\n' % url)

        if self.res and 'error' in self.res and retry:
            if self.res['error'] == 'You need to log in to perform this request' or self.res['error'] == 'Invalid Credentials':
                self._login()
                self.action(action=action, method=method, extra=extra, files=files, json_req=json_req, download=download, private=private, retry=False)

    def _policy_template_uuid(self, name):
        """
        Get the template ID. This provides the default settings for the policy.
        """
        self.action(action='editor/policy/templates', method='GET')
        for template in self.res['templates']:
            if template['name'] == name:
                self.policy_template_uuid = template['uuid']
                break

    def _scan_template_uuid(self, name):
        """
        Get the template ID. This provides the default settings for the policy.
        """
        self.action(action='editor/scan/templates', method='GET')
        for template in self.res['templates']:
            if template['name'] == name:
                self.scan_template_uuid = template['uuid']
                break

    def policy_add(self, name, plugins, credentials=[], template='advanced'):
        """
        Add a policy and store the returned ID. The template defaults to
        "advanced" to remain compatible with the calls that occur in Nessus
        5.2.x.
        """
        self.policy_name = name
        self._policy_template_uuid(template)
        self._policy_edit_template(uuid=self.policy_template_uuid)
        try:
            self.policy_id = self.res['policy_id']
            self.policy_name = self.res['policy_name']
        except KeyError:
            print('policy_id was not returned. Exiting')
            sys.exit(1)

        self.policy_add_creds(credentials=credentials)
        self._policy_set_settings()
        self.plugins_info(plugins=plugins)
        self._enable_plugins()

    def policy_copy(self, existing_policy_name, new_policy_name):
        """
        Create a copy of an existing policy and set it to be used for a scan
        """
        self.action(action='policies', method='GET')
        for policy in self.res['policies']:
            if policy['name'] == existing_policy_name:
                self.action(action='policies/' + str(policy['id']) + '/copy', method='POST')
                self.policy_id = self.res['id']
                self.policy_name = new_policy_name
                self.action(action='policies/' + str(self.policy_id), method='PUT', extra={'settings': {'name': self.policy_name}})
                return True

        return False

    def policy_exists(self, name):
        """
        Set existing policy to use for a scan.
        """
        self.policy_name = name
        self.action(action='policies', method='GET')
        for policy in self.res['policies']:
            if policy['name'] == name:
                self.policy_id = policy['id']
                return True

        return False

    def policy_set(self, name):
        """
        Set existing policy to use for a scan.
        """
        self.policy_name = name
        self.action(action='policies', method='GET')
        for policy in self.res['policies']:
            if policy['name'] == name:
                self.policy_id = policy['id']
                break

        if not self.policy_id:
            print('no policy with name %s found. Exiting' % name)
            sys.exit(1)

    def policy_details(self, policy_id):
        """
        Retrieves details of an existing policy.
        """
        self.policy_id = policy_id
        self.action(action='policies/' + str(self.policy_id), method='GET')
        return self.res

    def _policy_edit_template(self, uuid):
        """
        Using the UUID, create the base policy, which will then be manipulated.
        This is easier than attempting to design an entire policy in one call.
        """
        extra = {'settings': {'name': self.policy_name}, 'uuid': uuid}
        self.action(action='policies', method='POST', extra=extra)

    def policy_add_ports(self, ports):
        """
        Read current ports and append needed ports. The current value could have
        been gathered when disabling the plugin families, but for the sake of an
        extra call, it is much more clear what is occurring.
        """
        discovery = {}
        default_ports = ''
        self.action(action='editor/policy/' + str(self.policy_id), method='GET')
        for inputs in self.res['settings']['discovery']['groups']:
            if inputs['name'] == 'network_discovery':
                discovery = inputs['sections']

        for item in discovery:
            for nested in item['inputs']:
                if nested['id'] == 'portscan_range':
                    default_ports = nested['default']

        new_ports = str(default_ports) + ',' + str(ports)
        extra = {'settings': {'portscan_range': new_ports}}
        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=extra)

    def policy_limit_ports(self, ports):
        """
        Limit the ports scanned to the given list.
        """
        extra = {'settings': {'portscan_range': str(ports)}}
        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=extra)

    def policy_add_creds(self, credentials, policy_id=''):
        """
        Add a list of credentials, defined using the objects in the credential
        module.
        """
        if not policy_id:
            policy_id = self.policy_id
        creds = collections.defaultdict(lambda : collections.defaultdict(list))
        for credential in credentials:
            creds[credential.category][credential.name].append(credential.__dict__)

        creds = {'credentials': {'add': creds}}
        self.action(action='policies/' + str(policy_id), method='PUT', extra=creds)

    def _policy_set_settings(self):
        """
        Current settings include: safe_checks, scan_webapps, report_paranoia,
        provided_creds_only, thorough_tests, report_verbosity,
        silent_dependencies
        """
        settings = {'settings': {}}
        if not self.set_safe_checks:
            self.set_safe_checks = 'yes'
        if not self.pref_cgi:
            self.pref_cgi = 'no'
        if not self.pref_paranoid:
            self.pref_paranoid = 'Normal'
        if not self.pref_supplied:
            self.pref_supplied = 'no'
        if not self.pref_thorough:
            self.pref_thorough = 'no'
        if not self.pref_verbose:
            self.pref_verbose = 'Normal'
        if not self.pref_silent_dependencies:
            self.pref_silent_dependencies = 'yes'
        if not self.pref_receive_timeout:
            self.pref_receive_timeout = '5'
        if not self.pref_max_checks:
            self.pref_max_checks = '5'
        settings['settings'].update({'safe_checks': self.set_safe_checks})
        settings['settings'].update({'scan_webapps': self.pref_cgi})
        settings['settings'].update({'report_paranoia': self.pref_paranoid})
        settings['settings'].update({'provided_creds_only': self.pref_supplied})
        settings['settings'].update({'thorough_tests': self.pref_thorough})
        settings['settings'].update({'report_verbosity': self.pref_verbose})
        settings['settings'].update({'silent_dependencies': self.pref_silent_dependencies})
        settings['settings'].update({'cisco_offline_configs': self.cisco_offline_configs})
        settings['settings'].update({'network_receive_timeout': self.pref_receive_timeout})
        settings['settings'].update({'max_checks_per_host': self.pref_max_checks})
        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=settings)

    def _policy_remove_audits(self, category, type='custom'):
        """
        Removes all audit files from the policy.
        """
        delete_ids = []
        self.action(action='editor/policy/' + str(self.policy_id), method='GET')
        for record in self.res['compliance']['data']:
            if record['name'] == category:
                for audit in record['audits']:
                    if audit['type'] == type and 'id' in audit:
                        delete_ids.append(str(audit['id']))

        audit = {'audits': {'custom': {'delete': []}}}
        if len(delete_ids) > 0:
            audit['audits']['custom']['delete'] = delete_ids
            self.action(action='policies/' + str(self.policy_id), method='PUT', extra=audit)

    def _policy_add_audit(self, category, filename):
        """
        Adds an audit file to the policy.
        """
        audit = {'audits': {'custom': {'add': []}}}
        audit['audits']['custom']['add'].append({'file': filename, 'category': category})
        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=audit)

    def plugins_info(self, plugins):
        """
        Gather information on plugins for reporting. This also ensures that the
        plugin exists, and exits if it does not.
        """
        for plugin in plugins.split(','):
            self.action(action='plugins/plugin/' + str(plugin), method='GET')
            if 'attributes' in self.res:
                for attrib in self.res['attributes']:
                    if attrib['attribute_name'] == 'fname':
                        self.plugins.update({str(plugin): {'fname': attrib['attribute_value'], 
                                         'name': self.res['name']}})

            else:
                print('Plugin with ID %s is not found. Exiting.' % plugin)
                sys.exit(1)

    def _enable_plugins(self, plugins=[]):
        """
        Disable all of the families, and then enable plugins that you need. This
        builds the entire "plugins" object, and can be very large for some
        families, such as "AIX", as it needs to make an entry for each plugin in
        the family to set the status.
        """
        families = {'plugins': {}}
        updates = {}
        family_id = {}
        self.action(action='editor/policy/' + str(self.policy_id), method='GET')
        for item in self.res['plugins']['families']:
            families['plugins'].update({item: {'status': 'disabled'}})

        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=families)
        for plugin in self.plugins.keys():
            self.action(action='editor/policy/' + str(self.policy_id) + '/families?filter.search_type=and&' + 'filter.0.filter=plugin_id&filter.0.quality=eq&' + 'filter.0.value=' + str(plugin), method='GET')
            for family in self.res['families']:
                if family not in updates:
                    updates.update({family: []})
                updates[family].append(plugin)
                family_id.update({family: str(self.res['families'][family]['id'])})

        for fam, fam_id in family_id.items():
            families['plugins'][fam].update({'status': 'mixed'})
            families['plugins'][fam].update({'individual': {}})
            self.action(action='editor/policy/' + str(self.policy_id) + '/families/' + str(fam_id), method='GET')
            all_disabled = {}
            for pid in self.res['plugins']:
                all_disabled.update({str(pid['id']): 'disabled'})

            families['plugins'][fam]['individual'].update(all_disabled)

        for fam, pids in updates.items():
            for pid in pids:
                families['plugins'][fam]['individual'].update({str(pid): 'enabled'})

        self.action(action='policies/' + str(self.policy_id), method='PUT', extra=families)

    def scan_add(self, targets, template='custom', name='', start=''):
        """
        After building the policy, create a scan.
        """
        self._scan_template_uuid(name=template)
        self._scan_tag()
        text_targets = targets.replace(',', '\n')
        self.targets = targets.replace(',', ' ')
        if name:
            self.scan_name = name
        else:
            self.scan_name = self.policy_name
        scan = {'uuid': self.scan_template_uuid}
        settings = {}
        settings.update({'launch': 'ON_DEMAND'})
        settings.update({'description': 'Created with REST API'})
        settings.update({'file_targets': ''})
        settings.update({'filters': []})
        settings.update({'emails': ''})
        settings.update({'filter_type': ''})
        settings.update({'scanner_id': str(self.scanner_id)})
        settings.update({'name': self.scan_name})
        if self.policy_id:
            settings.update({'policy_id': self.policy_id})
        settings.update({'folder_id': self.tag_id})
        settings.update({'text_targets': text_targets})
        if start:
            settings.update({'starttime': start})
            settings.update({'rrules': 'FREQ=ONETIME'})
        scan.update({'settings': settings})
        self.action(action='scans', method='POST', extra=scan)
        self.scan_uuid = self.res['scan']['uuid']
        self.scan_id = self.res['scan']['id']

    def scan_exists(self, name):
        """
        Set existing scan.
        """
        self.scan_name = name
        self.action(action='scans', method='GET')
        if 'scans' in self.res and self.res['scans']:
            for scan in self.res['scans']:
                if scan['name'] == name:
                    self.scan_id = scan['id']
                    return True

        return False

    def scan_update_targets(self, targets):
        """
        After update targets on existing scan.
        """
        text_targets = targets.replace(',', '\n')
        self.targets = targets.replace(',', ' ')
        self.action(action='scans/' + str(self.scan_id), method='GET')
        scan = {}
        settings = {}
        settings.update({'name': self.scan_name})
        settings.update({'policy_id': self.policy_id})
        settings.update({'folder_id': self.tag_id})
        settings.update({'text_targets': text_targets})
        scan.update({'settings': settings})
        self.action(action='scans/' + str(self.scan_id), method='PUT', extra=scan)

    def scan_run(self):
        """
        Start the scan and save the UUID to query the status
        """
        self.action(action='scans/' + str(self.scan_id) + '/launch', method='POST')
        self.scan_uuid = self.res['scan_uuid']
        print('Scan name : %s' % self.scan_name)
        print('Scan UUID : %s' % self.scan_uuid)

    def _scan_status(self):
        """
        Check on the scan every 2 seconds.
        """
        running = True
        counter = 0
        while running:
            self.action(action='scans?folder_id=' + str(self.tag_id), method='GET')
            for scan in self.res['scans']:
                if scan['uuid'] == self.scan_uuid and (scan['status'] == 'running' or scan['status'] == 'pending'):
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    time.sleep(2)
                    counter += 2
                    if counter % 60 == 0:
                        print('')
                if scan['uuid'] == self.scan_uuid and scan['status'] != 'running' and scan['status'] != 'pending':
                    running = False
                    print('\nComplete! Run time: %d seconds.' % counter)

    def _scan_tag(self, name='CLI'):
        """
        Set the 'tag' for the scan to CLI, if the tag doesn't exist, create it
        and use the resulting ID
        """
        if not self.tag_name:
            self.tag_name = name
        self.action(action='folders', method='GET')
        for tag in self.res['folders']:
            if tag['name'] == self.tag_name:
                self.tag_id = tag['id']
                break

        if not self.tag_id:
            self.action('folders', method='POST', extra={'name': self.tag_name})
            self.tag_id = self.res['id']

    def scan_details(self, name):
        """
        Fetch the details of the requested scan
        """
        self.action(action='scans', method='GET')
        for scan in self.res['scans']:
            if scan['name'] == name:
                self.scan_id = scan['id']
                break

        if not self.scan_id:
            print('no scan with name %s found. Exiting' % name)
            sys.exit(1)
        self.action(action='scans/' + str(self.scan_id), method='GET')

    def scan_list(self):
        """
        Fetch a list with scans
        """
        self.action(action='scans', method='GET')
        return self.res

    def get_host_vulns(self, name):
        """
        Fill in host_vulns dict with the host vulnerabilities found in a
        scan
        """
        self.scan_details(name)
        for host in self.res['hosts']:
            self.action(action='scans/' + str(self.scan_id) + '/hosts/' + str(host['host_id']), method='GET')
            if self.scan_id not in self.host_vulns:
                self.host_vulns[self.scan_id] = {}
            self.host_vulns[self.scan_id][host['host_id']] = self.res

    def get_host_ids(self, name):
        """
        List host_ids in given scan
        """
        self.scan_details(name)
        for host in self.res['hosts']:
            self.host_ids[host['host_id']] = 1

    def get_host_details(self, scan_id, host_id):
        """
        Fill in host_details dict with the host vulnerabilities found in a
        scan
        """
        self.action(action='scans/' + str(scan_id) + '/hosts/' + str(host_id), method='GET')
        if scan_id not in self.host_details:
            self.host_details[scan_id] = {}
        self.host_details[scan_id][host_id] = self.res

    def get_plugin_output(self, scan, plugin_id):
        """
        Fill in plugin_output dict with the output from a given plugin
        in a given scan
        """
        plugin_id = int(plugin_id)
        self.get_host_vulns(scan)
        for scan_id in self.host_vulns:
            for host_id in self.host_vulns[scan_id]:
                for vulnerability in self.host_vulns[scan_id][host_id]['vulnerabilities']:
                    if vulnerability['plugin_id'] == plugin_id:
                        self.action(action='scans/' + str(scan_id) + '/hosts/' + str(host_id) + '/plugins/' + str(plugin_id), method='GET')
                        if scan_id not in self.plugin_output:
                            self.plugin_output[scan_id] = {}
                        self.plugin_output[scan_id][host_id] = self.res

    def _deduplicate_hosts(self, hosts):
        return list({v['hostname']:v for v in hosts}.values())

    def download_kbs(self):
        self.action('scans/' + str(self.scan_id), method='GET')
        merged_hosts = self.res.get('hosts', []) + self.res.get('comphosts', [])
        hosts = self._deduplicate_hosts(hosts=merged_hosts)
        kbs = {}
        for host in hosts:
            kbs[host['hostname']] = self.action('scans/' + str(self.scan_id) + '/hosts/' + str(host['host_id']) + '/kb?token=' + str(self.token), method='GET', download=True)

        return kbs

    def download_scan(self, export_format='', chapters='', dbpasswd=''):
        running = True
        counter = 0
        self.action('scans/' + str(self.scan_id), method='GET')
        if export_format == 'db':
            data = {'format': 'db', 'password': dbpasswd}
        else:
            if export_format == 'html':
                data = {'format': export_format, 'chapters': chapters}
            else:
                data = {'format': export_format}
            self.action('scans/' + str(self.scan_id) + '/export', method='POST', extra=data)
            file_id = self.res['file']
            print('Download for file id ' + str(self.res['file']) + '.')
            while running:
                time.sleep(2)
                counter += 2
                self.action('scans/' + str(self.scan_id) + '/export/' + str(file_id) + '/status', method='GET')
                running = self.res['status'] != 'ready'
                sys.stdout.write('.')
                sys.stdout.flush()
                if counter % 60 == 0:
                    print('')

        print('')
        content = self.action('scans/' + str(self.scan_id) + '/export/' + str(file_id) + '/download', method='GET', download=True)
        return content

    def scan_results(self):
        """
        Get the list of hosts, then iterate over them and extract results
        """
        self._scan_status()
        self.action('scans/' + str(self.scan_id), method='GET')
        for host in self.res['hosts']:
            if self.format_start:
                print(self.format_start)
            print('----------------------------------------')
            print('Target    : %s' % host['hostname'])
            print('----------------------------------------\n')
            for plugin in self.plugins.keys():
                self.action('scans/' + str(self.scan_id) + '/hosts/' + str(host['host_id']) + '/plugins/' + str(plugin), method='GET')
                if self.res['outputs']:
                    print('Plugin Name   : ' + self.plugins[plugin]['name'])
                    print('Plugin File   : ' + self.plugins[plugin]['fname'])
                    print('Plugin ID     : %s' % plugin)
                    print('Plugin Output :')
                    for output in self.res['outputs']:
                        if 'plugin_output' in output:
                            print(output['plugin_output'])
                        else:
                            print('Success')
                            print()

                self.action('scans/' + str(self.scan_id) + '/trails/?plugin_id=' + str(plugin) + '&hostname=' + host['hostname'], method='GET')
                try:
                    if self.res['trails']:
                        for output in self.res['trails']:
                            print('Plugin Name   : ' + self.plugins[plugin]['name'])
                            print('Plugin File   : ' + self.plugins[plugin]['fname'])
                            print('Plugin ID     : %s' % plugin)
                            print('Audit trail   : ' + output['output'])
                            print()

                except:
                    pass

            if self.format_end:
                print(self.format_end)

        try:
            if self.res is not None:
                for host in self.res['comphosts']:
                    print('----------------------------------------')
                    print('Target    : %s' % host['hostname'])
                    print('----------------------------------------\n')
                    for plugin in self.res['compliance']:
                        self.action('scans/' + str(self.scan_id) + '/hosts/' + str(host['host_id']) + '/compliance/' + str(plugin['plugin_id']), method='GET')
                        self.pretty_print()

        except:
            pass

        return

    def upload(self, upload_file, file_contents=''):
        """
        Upload a file that can be used to import a policy or add an audit file
        to a policy. If file_contents are not provided then upload_file is
        treated as a full path to a file and opened.
        """
        if not file_contents:
            file_contents = open(upload_file, 'rb')
            upload_file = os.path.basename(upload_file)
        files = {'Filename': upload_file, 'Filedata': file_contents}
        self.action(action='file/upload', method='POST', files=files, json_req=False)

    def policy_import(self, filename):
        """
        Import a previously uploaded .nessus file as a policy.
        """
        data = {'file': filename}
        self.action(action='policies/import', method='POST', extra=data)
        print("Imported policy named '%s', id %s" % (self.res['name'],
         self.res['id']))
        return self.res['id']

    def pretty_print(self):
        """
        Used for debugging and error conditions to easily see the returned
        structure.
        """
        print(json.dumps(self.res, sort_keys=False, indent=2))
        print('\n')

    def objdump(self):
        """
        debugging function to dump all of the set values
        """
        for attr in dir(self):
            print('obj.%s = %s' % (attr, getattr(self, attr)))


if __name__ == '__main__':
    print('Import the module, do not call directly.')