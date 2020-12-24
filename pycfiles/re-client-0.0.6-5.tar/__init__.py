# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbielawa/rhat/release-engine/re-client/src/reclient/__init__.py
# Compiled at: 2015-01-27 15:30:49
import getpass, logging, json, reclient.utils
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from reclient.connectors import Connectors
from reclient.colorize import colorize
from logging import FileHandler
out = logging.getLogger('recore')
out.setLevel(logging.DEBUG)
out.addHandler(FileHandler('/tmp/out.log'))
reclient_config = {}

class ReClient(object):

    def __init__(self, version='v0', debug=1, format='yaml'):
        self.v = version
        self.debug = debug
        self.baseurl = reclient_config['baseurl']
        self.format = format
        self._config()

    def _config(self):
        """Get the endpoint configuration"""
        self.endpoint = '%s/api/%s/' % (self.baseurl, self.v)
        if reclient_config.get('use_kerberos', False):
            out.debug('Using kerberos per configuration.')
            self.connector = Connectors({'auth': HTTPKerberosAuth(mutual_authentication=OPTIONAL), 
               'baseurl': self.endpoint}, format=self.format)
        else:
            out.debug('Using HTTPAuth per configuration.')
            self.connector = Connectors({'auth': (
                      reclient_config['username'], getpass.getpass()), 
               'baseurl': self.endpoint}, format=self.format)

    def _get_playbook(self, project, pb_id=None):
        """project - name of the project to search for playbook with id
'pb_id'. Omit pb_id and you get all playbooks for 'project'.

Return a two-tuple of the serialized datastructure, as well as a
reference to the tempfile.NamedTemporaryFile object it has been
written out to.
        """
        if pb_id is None:
            suffix = '%s/playbook/' % project
            key = 'items'
        else:
            suffix = '%s/playbook/%s/' % (project, pb_id)
            key = 'item'
        result = self.connector.get(suffix)
        if result.status_code == 200:
            pb_blob = reclient.utils.deserialize(result.content, self.format)[key]
            pb_fp = reclient.utils.temp_blob(pb_blob, self.format)
            return (
             pb_blob, pb_fp)
        else:
            raise ReClientGETError(result)
            return

    def _send_playbook(self, project, pb_fp, pb_id=None):
        """Send a playbook to the REST endpoint. Note the ordering of the
args/kwargs as they're ordered differently than most other methods.

`pb_fp` - File pointer to a playbook file
`pb_id` - OPTIONAL - if 'None' then this is interpreted as a NEW
playbook. If not 'None' then this is interpreted as an update to an
existing playbook.
        """
        if pb_id:
            print 'Updating an existing playbook'
            suffix = '%s/playbook/%s/' % (project, pb_id)
            with open(pb_fp.name, 'r') as (pb_open):
                result = self.connector.post(suffix, data=pb_open)
        else:
            print 'Sending a new playbook'
            suffix = '%s/playbook/' % project
            with open(pb_fp.name, 'r') as (pb_open):
                result = self.connector.put(suffix, data=pb_open)
        code = result.status_code
        if code == 200:
            print '[%d] Updated playbook' % code
        elif code == 201:
            print '[%d] Created new playbook' % code
        else:
            print '[%d] Unexpected response from rerest endpoint' % code
            raise ReClientSendError(result)
        return result

    def get_all_playbooks_ever(self):
        """Get ALL THE PLAYBOOKS"""
        suffix = 'playbooks/'
        result = self.connector.get(suffix)
        try:
            response_msg = reclient.utils.deserialize(result.content, self.format)
            if response_msg['status'] == 'error':
                print colorize('Error while fetching all playbooks', color='red', background='lightgray')
                print colorize('%s - %s' % (str(result), response_msg), color='red', background='lightgray')
                raise ReClientGETError(result)
        except Exception:
            return False

        view_file = reclient.utils.temp_blob(result, self.format)
        reclient.utils.less_file(view_file.name)

    def get_all_playbooks(self, project):
        """
        Get all playbooks that match `project`
        """
        try:
            path, pb_fp = self._get_playbook(project)
        except ReClientGETError as e:
            response_msg = reclient.utils.deserialize(e.args[0], self.format)
            print colorize('Error while fetching playbooks for %s:' % project, color='red', background='lightgray')
            print colorize('%s - %s' % (
             str(e),
             response_msg['message']), color='red', background='lightgray')
        else:
            reclient.utils.less_file(pb_fp.name)

    def view_file(self, project, pb_id):
        """
        Open playbook with id `pd_id` in `project` with the /bin/less command
        """
        try:
            pb, path = self._get_playbook(project, pb_id)
        except ReClientGETError:
            print colorize("Error while attempting to find '%s' for project '%s'\nAre you sure it exists?" % (
             pb_id, project), color='red', background='lightgray')
        else:
            reclient.utils.less_file(path.name)

    def edit_playbook(self, project, pb_id):
        try:
            pb, path = self._get_playbook(project, pb_id)
        except ReClientGETError as rcge:
            response_msg = reclient.utils.deserialize(rcge.args[0].content, 'json')
            print colorize('Error while fetching playbooks for %s:' % project, color='red', background='lightgray')
            print colorize('%s - %s' % (
             str(rcge),
             response_msg['message']), color='red', background='lightgray')
            return False

        pb_fp = reclient.utils.edit_playbook(path, self.format)
        send_back = reclient.utils.user_prompt_yes_no('Upload?')
        if send_back:
            try:
                result = self._send_playbook(project, pb_fp, pb_id)
            except IOError as ioe:
                raise ioe
            except ReClientSendError as rcse:
                print 'Error while sending updated playbook: %s' % str(rcse)
            else:
                print colorize('Updated playbook for %s:' % project, color='green')
                return result

        else:
            print colorize('Not sending back. Playbook will be saved in %s until this program is closed.' % pb_fp.name, color='yellow')
            return

    def download_playbook(self, save_path, project, pb_id):
        pb, path = self._get_playbook(project, pb_id)
        print 'Playbook fetched'
        print 'Saving playbook to: %s' % save_path
        reclient.utils.save_playbook(pb, save_path, self.format)
        print colorize('Success: Playbook %s saved to %s' % (
         pb_id, save_path), color='green')

    def upload_playbook(self, source_path, project):
        with open(source_path, 'r') as (_source):
            result = self._send_playbook(project, _source)
        _result = reclient.utils.deserialize(result.content, self.format)
        _id = colorize(str(_result['id']), color='yellow')
        print colorize('Success: Playbook uploaded. ID: %s' % _id, color='green')

    def delete_playbook(self, project, pb_id):
        if reclient.utils.user_prompt_yes_no('Confirm Delete Playbook'):
            suffix = '%s/playbook/%s/' % (project, pb_id)
            result = self.connector.delete(suffix)
            return result
        else:
            return
            return

    def start_deployment(self, project, pb_id):
        suffix = '%s/playbook/%s/deployment/' % (
         project, pb_id)
        print colorize('Dynamic Arguments. Finish/skip by entering an empty key name', color='green')
        dargs = reclient.utils.read_dynamic_args()
        if dargs != {}:
            print colorize('Going to begin deployment with the following dynamic args', color='green')
            print reclient.utils.dynamic_args_table(dargs)
        if reclient.utils.user_prompt_yes_no('Run deployment? '):
            result = self.connector.put(suffix, data=json.dumps(dargs))
        else:
            return False
        try:
            _status = reclient.utils.deserialize(result.content, 'json').get('status')
            if _status == 'error':
                raise ReClientDeployError(result)
        except ReClientDeployError as rcde:
            response_msg = reclient.utils.deserialize(rcde.args[0].content, 'json')
            print colorize('Error while fetching playbooks for %s:' % project, color='red', background='lightgray')
            print colorize('%s - %s' % (
             str(rcde),
             response_msg['message']), color='red', background='lightgray')
            return False
        except Exception as e:
            print colorize('Unknown error while starting deployment: %s' % str(e), color='red')
            raise e
        else:
            return result

    def new_playbook(self, project):
        pb = {'execution': [
                       {'hosts': [], 'description': '', 
                          'steps': []}], 
           'group': '', 
           'name': ''}
        pb_fp = reclient.utils.temp_blob(pb, self.format)
        reclient.utils.edit_playbook(pb_fp, self.format)
        self._send_playbook(project, pb_fp)


class ReClientError(Exception):
    pass


class ReClientGETError(ReClientError):
    pass


class ReClientSendError(ReClientError):
    pass


class ReClientDeployError(ReClientError):
    pass