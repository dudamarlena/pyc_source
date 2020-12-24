# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/refresh.py
# Compiled at: 2020-05-10 13:41:12
# Size of source mod 2**32: 32630 bytes
__doc__ = '\naehostd.refresh - various worker threads for data refreshing\n'
import os, glob, time, logging, pprint, threading, random, subprocess
from io import BytesIO
import ldap0
from ldap0.dn import DNObj
from ldap0.ldif import LDIFWriter
from ldap0.functions import strf_secs
from ldap0.controls.deref import DereferenceControl
from .base import IdempotentFile, dict_del
from .cfg import CFG
from . import passwd
from . import group
from . import hosts
from .ldapconn import LDAP_CONN
SUDOERS_ATTRS = [
 'cn',
 'objectClass',
 'sudoCommand',
 'sudoHost',
 'sudoNotAfter', 'sudoNotBefore',
 'sudoOption', 'sudoOrder',
 'sudoRunAs', 'sudoRunAsGroup', 'sudoRunAsUser', 'sudoUser']

class RefreshThread(threading.Thread):
    """RefreshThread"""
    __slots__ = ('enabled', 'schedule_interval', '_refresh_sleep', '_rand', 'refresh_counter',
                 'avg_refresh_time', 'max_refresh_time', '_last_run', '_next_run')
    rand_factor = 2.0
    avg_window = 30.0

    def __init__(self, refresh_sleep):
        threading.Thread.__init__(self,
          group=None,
          target=None,
          name=None,
          args=(),
          kwargs={})
        self.enabled = True
        self.schedule_interval = 0.4
        self._refresh_sleep = refresh_sleep
        self._rand = random.SystemRandom()
        self.refresh_counter = 0
        self.avg_refresh_time = 0.0
        self.max_refresh_time = 0.0
        self.reset()

    def _log(self, log_level, msg, *args, **kwargs):
        msg = ' '.join((self.__class__.__name__, msg))
        (logging.log)(log_level, msg, *args, **kwargs)

    def _refresh_task(self, ldap_conn):
        """
        refresh task
        """
        raise NotImplementedError

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        return dict(refresh_count=(self.refresh_counter),
          avg_refresh_time=(self.avg_refresh_time),
          max_refresh_time=(self.max_refresh_time))

    def reset(self):
        """
        trigger next run, skips refresh sleep time
        """
        self._last_run = 0.0
        self._next_run = time.time()
        self._log(logging.INFO, 'Finished %s.reset()', self.__class__.__name__)

    def run(self):
        """
        retrieve data forever
        """
        self._log(logging.DEBUG, 'Starting %s.run()', self.__class__.__name__)
        while self.enabled:
            start_time = time.time()
            if start_time > self._next_run:
                self._log(logging.DEBUG, 'Invoking %s._refresh_task()', self.__class__.__name__)
                try:
                    ldap_conn = LDAP_CONN.get_ldap_conn()
                    if ldap_conn is None:
                        self._log(logging.WARN, 'No valid LDAP connection => abort')
                    else:
                        self._refresh_task(ldap_conn)
                        self.refresh_counter += 1
                        refresh_time = time.time() - start_time
                        if self.max_refresh_time < refresh_time:
                            self.max_refresh_time = refresh_time
                        avg_window = min(self.avg_window, self.refresh_counter)
                        self.avg_refresh_time = ((avg_window - 1) * self.avg_refresh_time + refresh_time) / avg_window
                        self._log(logging.INFO, '%d. refresh run with %s (%0.3f secs, avg: %0.3f secs)', self.refresh_counter, ldap_conn.uri, refresh_time, self.avg_refresh_time)
                except ldap0.SERVER_DOWN as ldap_error:
                    try:
                        self._log(logging.WARN, 'Invalid connection: %s', ldap_error)
                        LDAP_CONN.disable_ldap_conn()
                    finally:
                        ldap_error = None
                        del ldap_error

                except Exception:
                    self._log((logging.ERROR),
                      'Aborted refresh with unhandled exception',
                      exc_info=True)
                else:
                    self._last_run = start_time
                    self._next_run = time.time() + self._refresh_sleep + self.rand_factor * self._rand.random()
            time.sleep(self.schedule_interval)

        self._log(logging.DEBUG, 'Exiting %s.run()', self.__class__.__name__)


def visudo_check_cmd(sudoers_filename):
    """
    return command arguments for running visudo to check the given file
    """
    return [
     CFG.visudo_exec, '-c', '-s', '-q', '-f', sudoers_filename]


class UsersUpdater(RefreshThread):
    """UsersUpdater"""
    __slots__ = ('_last_role_groups', )
    posix_account_attrs = [
     'aeRemoteHost',
     'uidNumber',
     'sshPublicKey']

    def __init__(self, refresh_sleep):
        RefreshThread.__init__(self, refresh_sleep)
        passwd.PASSWD_MAP.update({CFG.aehost_vaccount_t[2]: CFG.aehost_vaccount_t})
        passwd.PASSWD_NAME_MAP.update({CFG.aehost_vaccount_t[0]: CFG.aehost_vaccount_t[2]})
        group.GROUP_MEMBER_MAP = {CFG.aehost_vaccount_t[0]: []}
        if CFG.homedir_tmpl is None:
            self.posix_account_attrs.append('homeDirectory')
        if CFG.loginshell_override is None:
            self.posix_account_attrs.append('loginShell')
        self.srvgrp_deref_ctrl = DereferenceControl(True, {'aeVisibleGroups':[
          'gidNumber', 'memberUid'], 
         'aeVisibleSudoers':SUDOERS_ATTRS})
        if CFG.sudoers_file:
            self.ldif_filename = CFG.sudoers_file + '.ldif'
            self.sudoers_tmp_filename = CFG.sudoers_file + '.tmp'
            self.cvtsudoers_cmd = [
             CFG.cvtsudoers_exec,
             '-d', 'all',
             '-i', 'LDIF',
             '-f', 'sudoers',
             '-o', self.sudoers_tmp_filename,
             self.ldif_filename]
            self.visudo_check_cmd = visudo_check_cmd(self.sudoers_tmp_filename)

    @staticmethod
    def _passwd_convert(entry):
        """
        convert an LDAP entry dict to a passwd map tuple
        """
        name = entry['uid'][0]
        uid = int(entry['uidNumber'][0])
        gid = uid
        gecos = entry.get('cn', [
         CFG.gecos_tmpl.format(username=name)])[0]
        if CFG.homedir_tmpl:
            home = CFG.homedir_tmpl.format(username=name)
        else:
            home = entry['homeDirectory'][0]
        if CFG.loginshell_override is None:
            shell = entry.get('loginShell', [CFG.loginshell_default])[0]
        else:
            shell = CFG.loginshell_override
        return (name, 'x', uid, gid, gecos, home, shell)

    @staticmethod
    def _group_convert(entry):
        """
        convert an LDAP entry dict to a group map tuple
        """
        logging.debug('group_convert(): %r', entry)
        return (
         entry['cn'][0],
         'x',
         int(entry['gidNumber'][0]),
         entry.get('memberUid', tuple()))

    def _store_ssh_key(self, user):
        user_entry = user.entry_s
        user_name = user_entry['uid'][0]
        self._log(logging.DEBUG, 'Found user %r with %d SSH keys', user_name, len(user_entry['sshPublicKey']))
        raddr_list = [av.strip() for av in user_entry.get('aeRemoteHost', []) if av.strip()]
        if raddr_list:
            self._log(logging.DEBUG, 'Attribute aeRemoteHost contains: %r', raddr_list)
            ssh_key_prefix = 'from="%s" ' % ','.join(raddr_list)
        else:
            ssh_key_prefix = ''
        self._log(logging.DEBUG, 'ssh_key_prefix = %r', ssh_key_prefix)
        new_user_ssh_keys = sorted([''.join((ssh_key_prefix, ssh_key.strip())) for ssh_key in user_entry['sshPublicKey']])
        sshkey_file = IdempotentFile(os.path.join(CFG.sshkeys_dir, user_name))
        sshkey_file.write(('\n'.join(new_user_ssh_keys).encode('utf-8')), mode=416)

    def _ldifstring(self, ldap_results, entry_comment):
        """
        return ldap_results as LDIF string
        """
        ldif_file = BytesIO()
        ldif_writer = LDIFWriter(ldif_file)
        for res in ldap_results:
            self._log(logging.DEBUG, 'Found %s entry %r: %r', entry_comment, res.dn_s, res.entry_s)
            ldif_writer.unparse(res.dn_b, res.entry_b)

        if len(ldap_results) != ldif_writer.records_written:
            self._log(logging.WARN, '%d entries to be exported, but only wrote %d', len(ldap_results), ldif_writer.records_written)
        return ldif_file.getvalue()

    def _export_sudoers(self, sudoers_result):
        """
        write sudoers entries to LDIF file and convert it
        """
        if sudoers_result:
            ldif_str = self._ldifstring(sudoers_result, 'sudoers')
            self._log(logging.DEBUG, 'Added %d sudoers entries to LDIF buf (%d bytes)', len(sudoers_result), len(ldif_str))
        else:
            ldif_str = '# No sudoers entries found\n'
            self._log(logging.DEBUG, 'No sudoers entries to be exported => dummy comment line')
        ldif_file = IdempotentFile(self.ldif_filename)
        if not ldif_file.write(ldif_str, mode=416, remove=True):
            return
        if not os.path.exists(self.ldif_filename):
            self._log(logging.ERROR, 'LDIF sudoers file %r does not exist!', self.ldif_filename)
            return
        self._log(logging.DEBUG, 'Converting LDIF to sudoers file: %r', self.cvtsudoers_cmd)
        cvssudoers_rc = subprocess.call((self.cvtsudoers_cmd), shell=False)
        if cvssudoers_rc != 0:
            self._log(logging.ERROR, 'Converting to sudoers file %r failed with return code %d, command was: %r', self.sudoers_tmp_filename, cvssudoers_rc, self.cvtsudoers_cmd)
            return
        self._log(logging.DEBUG, 'Checking sudoers file: %r', self.visudo_check_cmd)
        visudo_rc = subprocess.call((self.visudo_check_cmd), shell=False)
        if visudo_rc != 0:
            self._log(logging.ERROR, 'Checking sudoers file %r failed with return code %d, command was: %r', self.sudoers_tmp_filename, visudo_rc, self.visudo_check_cmd)
            return
        os.chmod(self.sudoers_tmp_filename, 288)
        os.rename(self.sudoers_tmp_filename, CFG.sudoers_file)
        self._log(logging.INFO, 'Successfully updated sudoers file %s with %d entries', CFG.sudoers_file, len(sudoers_result))

    def _get_group_maps(self, ldap_conn):
        """
        initialize group map and search LDAP groups
        """
        role_groups = {set():role_attr for role_attr in CFG.vgroup_role_map}
        group_map = {}
        group_name_map = {}
        group_dn2id_map = {}
        for group_id, group_name in CFG.vgroup_role_map.values():
            group_map[group_id] = UsersUpdater._group_convert({'cn':[
              group_name], 
             'gidNumber':[
              group_id], 
             'memberUid':set()})
            group_name_map[group_name] = group_id

        try:
            ldap_conn.read_s((ldap_conn.get_whoami_dn()), attrlist=['aeSrvGroup'])
        except ldap0.NO_SUCH_OBJECT:
            self.reset()
            raise ldap0.SERVER_DOWN('forced re-bind')
        else:
            msg_id = ldap_conn.search_service_groups((ldap_conn.get_whoami_dn()),
              attrlist=(CFG.vgroup_role_map.keys()),
              req_ctrls=[
             self.srvgrp_deref_ctrl])
            group_results = []
            sudoers_results = []
            for res in ldap_conn.results(msg_id):
                for sudoer in res.rdata:
                    for role_attr in CFG.vgroup_role_map:
                        role_groups[role_attr].update(sudoer.entry_s.get(role_attr, []))

                    for ctrl in sudoer.ctrls:
                        if ctrl.controlType == DereferenceControl.controlType:
                            group_results.extend([grp for grp in ctrl.derefRes.get('aeVisibleGroups', []) if grp.entry_b])
                            sudoers_results.extend([sre for sre in ctrl.derefRes.get('aeVisibleSudoers', []) if sre.entry_b])

                    if CFG.sudoers_file:
                        self._export_sudoers(sudoers_results)
                    all_user_names = set()

        for group_res in group_results:
            self._log(logging.DEBUG, 'Found group entry %r : %r', group_res.dn_s, group_res.entry_s)
            group_name = group_res.dn_s.split(',', 1)[0][3:]
            gid_number = int(group_res.entry_s['gidNumber'][0])
            group_res.entry_s['cn'] = [group_name]
            if 'memberUid' not in group_res.entry_s:
                group_res.entry_s['memberUid'] = [user_dn.split(',', 1)[0][4:] for user_dn in group_res.entry_s.get('member', [])]
            all_user_names.update(group_res.entry_s['memberUid'])
            group_map[gid_number] = UsersUpdater._group_convert(group_res.entry_s)
            group_name_map[group_name] = gid_number
            group_dn2id_map[group_res.dn_s] = gid_number
            self._log(logging.DEBUG, 'Group entry %r : %r', group_res.dn_s, group_map[gid_number])
            for role_attr in role_groups:
                if 'memberUid' in group_res.entry_s and group_res.dn_s in role_groups[role_attr]:
                    role_gid_number = CFG.vgroup_role_map[role_attr][0]
                    group_map[role_gid_number][3].update(group_res.entry_s['memberUid'])

            self._log(logging.DEBUG, 'Role group mappings: %r', role_groups)
            group_member_map = {CFG.aehost_vaccount_t[0]: set()}

        for group_map_entry in group_map.values():
            gid_number = group_map_entry[2]
            for user_name in group_map_entry[3]:
                try:
                    group_member_map[user_name].add(gid_number)
                except KeyError:
                    group_member_map[user_name] = set([gid_number])

            if len(group_map) != len(group_results) + len(CFG.vgroup_role_map):
                self._log(logging.WARN, 'Different group length! group_map=%d group_results=%d', len(group_map), len(group_results))

        for user_name in all_user_names:
            if user_name not in passwd.PASSWD_NAME_MAP:
                self._last_run = 0
                break
            return (
             group_map,
             group_name_map,
             group_dn2id_map,
             group_member_map,
             role_groups,
             all_user_names)

    def _get_passwd_maps(self, ldap_conn, group_dn2id_map, role_groups):
        passwd_map = {CFG.aehost_vaccount_t[2]: CFG.aehost_vaccount_t}
        passwd_name_map = {CFG.aehost_vaccount_t[0]: CFG.aehost_vaccount_t[2]}
        user_group_dn_list = group_dn2id_map.keys()
        if not user_group_dn_list:
            self._log(logging.WARN, 'No visible groups at all => skip searching users')
            return (
             passwd_map, passwd_name_map)
        else:
            full_user_refresh = role_groups['aeVisibleGroups'] != self._last_role_groups['aeVisibleGroups'] or 
            if full_user_refresh:
                user_from_timestamp = 0
            else:
                user_from_timestamp = self._last_run
        user_filter = '(&{memberof}(modifyTimestamp>={timestamp}))'.format(memberof=(ldap0.filter.compose_filter('|', ldap0.filter.map_filter_parts('memberOf', user_group_dn_list))),
          timestamp=(strf_secs(user_from_timestamp)))
        self._log(logging.DEBUG, 'Search users with filter %r', user_filter)
        msg_id = ldap_conn.search((ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          filterstr=user_filter,
          attrlist=(self.posix_account_attrs))
        if msg_id is None:
            self._log(logging.WARN, 'Searching users with filter %r failed (msg_id = %r)', user_filter, msg_id)
            return (
             passwd_map, passwd_name_map)
        sshkeys_usernames = set()
        for res in ldap_conn.results(msg_id, timeout=(CFG.timelimit)):
            for user in res.rdata:
                self._log(logging.DEBUG, 'Found user entry %r : %r', user.dn_s, user.entry_s)
                user_name = user.dn_s.split(',', 1)[0][4:]
                user.entry_s['uid'] = [user_name]
                uid_number = int(user.entry_s['uidNumber'][0])
                passwd_map[uid_number] = UsersUpdater._passwd_convert(user.entry_s)
                passwd_name_map[user_name] = uid_number
                if CFG.sshkeys_dir:
                    if 'sshPublicKey' in user.entry_s:
                        self._store_ssh_key(user)
                        sshkeys_usernames.add(user_name)
                    else:
                        self._delete_ssh_key(user_name)

            if CFG.sshkeys_dir:
                if full_user_refresh:
                    self._delete_obsolete_keys(sshkeys_usernames)
            return (
             passwd_map, passwd_name_map)

    def _delete_ssh_key(self, user_name):
        sshkey_filename = os.path.join(CFG.sshkeys_dir, user_name)
        if not os.path.exists(sshkey_filename):
            self._log(logging.DEBUG, 'No SSH key file %r found', sshkey_filename)
            return
        self._log(logging.INFO, 'Removing SSH key file %r', sshkey_filename)
        try:
            os.remove(sshkey_filename)
        except OSError as os_error:
            try:
                self._log(logging.ERROR, 'Error removing SSH key file %r: %r', sshkey_filename, os_error)
            finally:
                os_error = None
                del os_error

    def _delete_obsolete_keys--- This code section failed: ---

 L. 562         0  LOAD_GLOBAL              glob
                2  LOAD_METHOD              glob
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              join
               10  LOAD_GLOBAL              CFG
               12  LOAD_ATTR                sshkeys_dir
               14  LOAD_STR                 '*'
               16  CALL_METHOD_2         2  ''
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'existing_ssh_key_files'

 L. 563        22  LOAD_GLOBAL              len
               24  LOAD_GLOBAL              CFG
               26  LOAD_ATTR                sshkeys_dir
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  BINARY_ADD       
               34  STORE_DEREF              'path_prefix_len'

 L. 564        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _log

 L. 565        40  LOAD_GLOBAL              logging
               42  LOAD_ATTR                DEBUG

 L. 566        44  LOAD_STR                 '%d existing SSH key files found: %r'

 L. 567        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'existing_ssh_key_files'
               50  CALL_FUNCTION_1       1  ''

 L. 568        52  LOAD_FAST                'existing_ssh_key_files'

 L. 564        54  CALL_METHOD_4         4  ''
               56  POP_TOP          

 L. 570        58  LOAD_CLOSURE             'path_prefix_len'
               60  BUILD_TUPLE_1         1 
               62  LOAD_SETCOMP             '<code_object <setcomp>>'
               64  LOAD_STR                 'UsersUpdater._delete_obsolete_keys.<locals>.<setcomp>'
               66  MAKE_FUNCTION_8          'closure'

 L. 572        68  LOAD_FAST                'existing_ssh_key_files'

 L. 570        70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'old_userid_set'

 L. 574        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _log

 L. 575        80  LOAD_GLOBAL              logging
               82  LOAD_ATTR                DEBUG

 L. 576        84  LOAD_STR                 '%d existing user IDs: %s'

 L. 577        86  LOAD_GLOBAL              len
               88  LOAD_FAST                'old_userid_set'
               90  CALL_FUNCTION_1       1  ''

 L. 578        92  LOAD_STR                 ', '
               94  LOAD_METHOD              join
               96  LOAD_GLOBAL              map
               98  LOAD_GLOBAL              str
              100  LOAD_FAST                'old_userid_set'
              102  CALL_FUNCTION_2       2  ''
              104  CALL_METHOD_1         1  ''

 L. 574       106  CALL_METHOD_4         4  ''
              108  POP_TOP          

 L. 580       110  LOAD_FAST                'old_userid_set'
              112  LOAD_FAST                'active_userid_set'
              114  BINARY_SUBTRACT  
              116  STORE_FAST               'to_be_removed'

 L. 581       118  LOAD_FAST                'to_be_removed'
              120  POP_JUMP_IF_FALSE   176  'to 176'

 L. 582       122  LOAD_FAST                'self'
              124  LOAD_METHOD              _log

 L. 583       126  LOAD_GLOBAL              logging
              128  LOAD_ATTR                INFO

 L. 584       130  LOAD_STR                 '%d existing files to be removed: %s'

 L. 585       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'to_be_removed'
              136  CALL_FUNCTION_1       1  ''

 L. 586       138  LOAD_STR                 ', '
              140  LOAD_METHOD              join
              142  LOAD_GLOBAL              map
              144  LOAD_GLOBAL              str
              146  LOAD_FAST                'to_be_removed'
              148  CALL_FUNCTION_2       2  ''
              150  CALL_METHOD_1         1  ''

 L. 582       152  CALL_METHOD_4         4  ''
              154  POP_TOP          

 L. 588       156  LOAD_FAST                'to_be_removed'
              158  GET_ITER         
              160  FOR_ITER            176  'to 176'
              162  STORE_FAST               'user_name'

 L. 589       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _delete_ssh_key
              168  LOAD_FAST                'user_name'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_BACK           160  'to 160'
            176_0  COME_FROM           120  '120'

Parse error at or near `LOAD_SETCOMP' instruction at offset 62

    def _refresh_task(self, ldap_conn):
        """
        Search users and groups
        """
        group_map, group_name_map, group_dn2id_map, group_member_map, role_groups, all_user_names = self._get_group_maps(ldap_conn)
        passwd_map, passwd_name_map = self._get_passwd_maps(ldap_conn, group_dn2id_map, role_groups)
        self._log(logging.DEBUG, 'all_user_names = %r', all_user_names)
        new_passwd_keys = set()
        for user_name in list(all_user_names):
            if user_name in passwd_name_map:
                new_passwd_keys.add(passwd_name_map[user_name])
            elif user_name in passwd.PASSWD_NAME_MAP:
                new_passwd_keys.add(passwd.PASSWD_NAME_MAP[user_name])
            else:
                self._log(logging.WARN, 'Could not map user name %r to UID', user_name)

        new_passwd_keys.add(CFG.aehost_vaccount_t[2])
        self._log(logging.DEBUG, 'new_passwd_keys = %r', new_passwd_keys)
        passwd_key_set = set(passwd.PASSWD_MAP)
        add_passwd_keys = new_passwd_keys - passwd_key_set
        remove_passwd_keys = passwd_key_set - new_passwd_keys
        passwd.PASSWD_MAP.update(passwd_map)
        passwd.PASSWD_NAME_MAP.update(passwd_name_map)
        group.GROUP_MEMBER_MAP.update(group_member_map)
        if add_passwd_keys:
            self._log(logging.INFO, '%d passwd entries added: %s', len(add_passwd_keys), ','.join([passwd.PASSWD_MAP[uid_number][0] for uid_number in add_passwd_keys]))
        if remove_passwd_keys:
            remove_passwd_names = ','.join([passwd.PASSWD_MAP[uid_number][0] for uid_number in remove_passwd_keys])
            for uid_number in remove_passwd_keys:
                self._log(logging.DEBUG, 'Removing %r from passwd map', passwd.PASSWD_MAP[uid_number][0])
                dict_del(passwd.PASSWD_NAME_MAP, passwd.PASSWD_MAP[uid_number][0])
                dict_del(group.GROUP_MEMBER_MAP, passwd.PASSWD_MAP[uid_number][0])
                del passwd.PASSWD_MAP[uid_number]

            self._log(logging.INFO, '%d passwd entries removed: %s', len(remove_passwd_keys), remove_passwd_names)
        self._log(logging.DEBUG, '%d passwd entries', len(passwd.PASSWD_MAP))
        if not len(passwd.PASSWD_MAP) == len(passwd.PASSWD_NAME_MAP) == len(group.GROUP_MEMBER_MAP):
            self._log(logging.WARN, 'Different map length! PASSWD_MAP=%d PASSWD_NAME_MAP=%d GROUP_MEMBER_MAP=%d', len(passwd.PASSWD_MAP), len(passwd.PASSWD_NAME_MAP), len(group.GROUP_MEMBER_MAP))
            self._log(logging.DEBUG, 'PASSWD_MAP = %s', pprint.pformat((passwd.PASSWD_MAP), indent=2))
            self._log(logging.DEBUG, 'PASSWD_NAME_MAP = %s', pprint.pformat((passwd.PASSWD_NAME_MAP), indent=2))
            self._log(logging.DEBUG, 'GROUP_MEMBER_MAP = %s', pprint.pformat((group.GROUP_MEMBER_MAP), indent=2))
        for uid_number in new_passwd_keys:
            pw_entry = passwd.PASSWD_MAP[uid_number]
            gid_number = pw_entry[2]
            if gid_number in group_map:
                pass
            else:
                group_name = ''.join((
                 CFG.vgroup_name_prefix,
                 pw_entry[0]))
                group_map[gid_number] = UsersUpdater._group_convert({'cn':[
                  group_name], 
                 'gidNumber':[
                  gid_number]})
                group_name_map[group_name] = gid_number
                self._log(logging.DEBUG, 'Primary user group entry for %d : %r', gid_number, group_map[gid_number])

        new_group_keys = set(group_map.keys())
        group_key_set = set(group.GROUP_MAP)
        add_group_keys = new_group_keys - group_key_set
        remove_group_keys = group_key_set - new_group_keys
        group.GROUP_MAP.update(group_map)
        group.GROUP_NAME_MAP.update(group_name_map)
        if add_group_keys:
            self._log(logging.INFO, '%d group entries added: %s', len(add_group_keys), ','.join([group.GROUP_MAP[group_dn][0] for group_dn in add_group_keys]))
        if remove_group_keys:
            remove_group_names = ','.join([group.GROUP_MAP[gid_number][0] for gid_number in remove_group_keys])
            for gid_number in remove_group_keys:
                dict_del(group.GROUP_NAME_MAP, group.GROUP_MAP[gid_number][0])
                del group.GROUP_MAP[gid_number]
                self._log(logging.DEBUG, 'Removed %d from group map', gid_number)

            self._log(logging.INFO, '%d group entries removed: %s', len(remove_group_keys), remove_group_names)
        self._log(logging.DEBUG, '%d group entries', len(group.GROUP_MAP))
        self._last_role_groups = role_groups

    def reset(self):
        """
        trigger next run, skips refresh sleep time
        """
        self._last_role_groups = {set():role_attr for role_attr in CFG.vgroup_role_map}
        RefreshThread.reset(self)

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        res = RefreshThread.get_monitor_data(self)
        res.update(dict(group_count=(len(group.GROUP_MAP)),
          group_member_count=(len(group.GROUP_MEMBER_MAP)),
          group_name_count=(len(group.GROUP_NAME_MAP)),
          passwd_count=(len(passwd.PASSWD_MAP)),
          passwd_name_count=(len(passwd.PASSWD_NAME_MAP))))
        return res


class NetworkAddrUpdater(RefreshThread):
    """NetworkAddrUpdater"""
    hosts_attrs = [
     'aeFqdn',
     'ipHostNumber',
     'macAddress']

    def _refresh_task--- This code section failed: ---

 L. 794         0  BUILD_MAP_0           0 
                2  STORE_FAST               'hosts_map'

 L. 795         4  BUILD_MAP_0           0 
                6  STORE_FAST               'hosts_name_map'

 L. 796         8  BUILD_MAP_0           0 
               10  STORE_FAST               'hosts_addr_map'

 L. 797        12  LOAD_GLOBAL              str
               14  LOAD_GLOBAL              DNObj
               16  LOAD_METHOD              from_str
               18  LOAD_FAST                'ldap_conn'
               20  LOAD_METHOD              get_whoami_dn
               22  CALL_METHOD_0         0  ''
               24  CALL_METHOD_1         1  ''
               26  LOAD_METHOD              slice
               28  LOAD_GLOBAL              CFG
               30  LOAD_ATTR                netaddr_level
               32  LOAD_CONST               None
               34  CALL_METHOD_2         2  ''
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'netaddr_base'

 L. 798        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _log
               44  LOAD_GLOBAL              logging
               46  LOAD_ATTR                DEBUG
               48  LOAD_STR                 'Searching network address entries beneath %r'
               50  LOAD_FAST                'netaddr_base'
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L. 799        56  LOAD_FAST                'ldap_conn'
               58  LOAD_ATTR                search_s

 L. 800        60  LOAD_FAST                'netaddr_base'

 L. 801        62  LOAD_GLOBAL              ldap0
               64  LOAD_ATTR                SCOPE_SUBTREE

 L. 802        66  LOAD_STR                 '(objectClass=aeNwDevice)'

 L. 803        68  LOAD_FAST                'self'
               70  LOAD_ATTR                hosts_attrs

 L. 799        72  LOAD_CONST               ('filterstr', 'attrlist')
               74  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               76  STORE_FAST               'ldap_results'

 L. 805        78  LOAD_FAST                'ldap_results'
               80  GET_ITER         
               82  FOR_ITER            152  'to 152'
               84  STORE_FAST               'nw_res'

 L. 806        86  LOAD_FAST                'nw_res'
               88  LOAD_ATTR                entry_s
               90  LOAD_FAST                'hosts_map'
               92  LOAD_FAST                'nw_res'
               94  LOAD_ATTR                dn_s
               96  STORE_SUBSCR     

 L. 807        98  LOAD_FAST                'nw_res'
              100  LOAD_ATTR                entry_s
              102  LOAD_STR                 'aeFqdn'
              104  BINARY_SUBSCR    
              106  GET_ITER         
              108  FOR_ITER            124  'to 124'
              110  STORE_FAST               'name'

 L. 808       112  LOAD_FAST                'nw_res'
              114  LOAD_ATTR                dn_s
              116  LOAD_FAST                'hosts_name_map'
              118  LOAD_FAST                'name'
              120  STORE_SUBSCR     
              122  JUMP_BACK           108  'to 108'

 L. 809       124  LOAD_FAST                'nw_res'
              126  LOAD_ATTR                entry_s
              128  LOAD_STR                 'ipHostNumber'
              130  BINARY_SUBSCR    
              132  GET_ITER         
              134  FOR_ITER            150  'to 150'
              136  STORE_FAST               'addr'

 L. 810       138  LOAD_FAST                'nw_res'
              140  LOAD_ATTR                dn_s
              142  LOAD_FAST                'hosts_addr_map'
              144  LOAD_FAST                'addr'
              146  STORE_SUBSCR     
              148  JUMP_BACK           134  'to 134'
              150  JUMP_BACK            82  'to 82'

 L. 812       152  LOAD_GLOBAL              set
              154  LOAD_GLOBAL              hosts
              156  LOAD_ATTR                HOSTS_MAP
              158  LOAD_METHOD              keys
              160  CALL_METHOD_0         0  ''
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'hosts_key_set'

 L. 813       166  LOAD_GLOBAL              set
              168  LOAD_FAST                'hosts_map'
              170  LOAD_METHOD              keys
              172  CALL_METHOD_0         0  ''
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'new_hosts_keys'

 L. 814       178  LOAD_FAST                'new_hosts_keys'
              180  LOAD_FAST                'hosts_key_set'
              182  BINARY_SUBTRACT  
              184  STORE_FAST               'add_hosts_keys'

 L. 815       186  LOAD_FAST                'hosts_key_set'
              188  LOAD_FAST                'new_hosts_keys'
              190  BINARY_SUBTRACT  
              192  STORE_FAST               'remove_hosts_keys'

 L. 816       194  LOAD_GLOBAL              hosts
              196  LOAD_ATTR                HOSTS_MAP
              198  LOAD_METHOD              update
              200  LOAD_FAST                'hosts_map'
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 817       206  LOAD_GLOBAL              hosts
              208  LOAD_ATTR                HOSTS_NAME_MAP
              210  LOAD_METHOD              update
              212  LOAD_FAST                'hosts_name_map'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          

 L. 818       218  LOAD_GLOBAL              hosts
              220  LOAD_ATTR                HOSTS_ADDR_MAP
              222  LOAD_METHOD              update
              224  LOAD_FAST                'hosts_addr_map'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 819       230  LOAD_FAST                'self'
              232  LOAD_METHOD              _log

 L. 820       234  LOAD_GLOBAL              logging
              236  LOAD_ATTR                DEBUG

 L. 821       238  LOAD_STR                 '%d hosts entries, added %d, removed %d'

 L. 822       240  LOAD_GLOBAL              len
              242  LOAD_GLOBAL              hosts
              244  LOAD_ATTR                HOSTS_MAP
              246  CALL_FUNCTION_1       1  ''

 L. 823       248  LOAD_GLOBAL              len
              250  LOAD_FAST                'add_hosts_keys'
              252  CALL_FUNCTION_1       1  ''

 L. 824       254  LOAD_GLOBAL              len
              256  LOAD_FAST                'remove_hosts_keys'
              258  CALL_FUNCTION_1       1  ''

 L. 819       260  CALL_METHOD_5         5  ''
              262  POP_TOP          

 L. 826       264  LOAD_FAST                'remove_hosts_keys'
          266_268  POP_JUMP_IF_FALSE   490  'to 490'

 L. 827       270  LOAD_FAST                'remove_hosts_keys'
              272  GET_ITER         
              274  FOR_ITER            468  'to 468'
              276  STORE_FAST               'nw_dn'

 L. 828       278  SETUP_FINALLY       318  'to 318'

 L. 829       280  LOAD_FAST                'ldap_conn'
              282  LOAD_ATTR                read_s
              284  LOAD_FAST                'nw_dn'
              286  LOAD_STR                 '1.1'
              288  BUILD_LIST_1          1 
              290  LOAD_CONST               ('attrlist',)
              292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              294  STORE_FAST               'ldap_res'

 L. 830       296  LOAD_FAST                'ldap_res'
              298  LOAD_CONST               None
              300  COMPARE_OP               is
          302_304  POP_JUMP_IF_FALSE   314  'to 314'

 L. 831       306  LOAD_GLOBAL              ldap0
              308  LOAD_METHOD              NO_SUCH_OBJECT
              310  CALL_METHOD_0         0  ''
              312  RAISE_VARARGS_1       1  ''
            314_0  COME_FROM           302  '302'
              314  POP_BLOCK        
              316  JUMP_FORWARD        440  'to 440'
            318_0  COME_FROM_FINALLY   278  '278'

 L. 832       318  DUP_TOP          
              320  LOAD_GLOBAL              ldap0
              322  LOAD_ATTR                NO_SUCH_OBJECT
              324  LOAD_GLOBAL              ldap0
              326  LOAD_ATTR                INSUFFICIENT_ACCESS
              328  BUILD_TUPLE_2         2 
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   438  'to 438'
              336  POP_TOP          
              338  POP_TOP          
              340  POP_TOP          

 L. 833       342  LOAD_GLOBAL              hosts
              344  LOAD_ATTR                HOSTS_MAP
              346  LOAD_FAST                'nw_dn'
              348  BINARY_SUBSCR    
              350  LOAD_STR                 'aeFqdn'
              352  BINARY_SUBSCR    
              354  GET_ITER         
              356  FOR_ITER            376  'to 376'
              358  STORE_FAST               'name'

 L. 834       360  LOAD_GLOBAL              dict_del
              362  LOAD_GLOBAL              hosts
              364  LOAD_ATTR                HOSTS_NAME_MAP
              366  LOAD_FAST                'name'
              368  CALL_FUNCTION_2       2  ''
              370  POP_TOP          
          372_374  JUMP_BACK           356  'to 356'

 L. 835       376  LOAD_GLOBAL              hosts
              378  LOAD_ATTR                HOSTS_MAP
              380  LOAD_FAST                'nw_dn'
              382  BINARY_SUBSCR    
              384  LOAD_STR                 'ipHostNumber'
              386  BINARY_SUBSCR    
              388  GET_ITER         
              390  FOR_ITER            410  'to 410'
              392  STORE_FAST               'addr'

 L. 836       394  LOAD_GLOBAL              dict_del
              396  LOAD_GLOBAL              hosts
              398  LOAD_ATTR                HOSTS_ADDR_MAP
              400  LOAD_FAST                'addr'
              402  CALL_FUNCTION_2       2  ''
              404  POP_TOP          
          406_408  JUMP_BACK           390  'to 390'

 L. 837       410  LOAD_GLOBAL              hosts
              412  LOAD_ATTR                HOSTS_MAP
              414  LOAD_FAST                'nw_dn'
              416  DELETE_SUBSCR    

 L. 838       418  LOAD_FAST                'self'
              420  LOAD_METHOD              _log
              422  LOAD_GLOBAL              logging
              424  LOAD_ATTR                DEBUG
              426  LOAD_STR                 'Removed %r from group map'
              428  LOAD_FAST                'nw_dn'
              430  CALL_METHOD_3         3  ''
              432  POP_TOP          
              434  POP_EXCEPT       
              436  JUMP_BACK           274  'to 274'
            438_0  COME_FROM           332  '332'
              438  END_FINALLY      
            440_0  COME_FROM           316  '316'

 L. 840       440  LOAD_FAST                'self'
              442  LOAD_METHOD              _log

 L. 841       444  LOAD_GLOBAL              logging
              446  LOAD_ATTR                WARN

 L. 842       448  LOAD_STR                 '%r marked to be deleted, but found %r => abort refresh'

 L. 843       450  LOAD_FAST                'nw_dn'

 L. 844       452  LOAD_FAST                'ldap_res'

 L. 840       454  CALL_METHOD_4         4  ''
              456  POP_TOP          

 L. 846       458  POP_TOP          
              460  LOAD_CONST               None
              462  RETURN_VALUE     
          464_466  JUMP_BACK           274  'to 274'

 L. 847       468  LOAD_FAST                'self'
              470  LOAD_METHOD              _log

 L. 848       472  LOAD_GLOBAL              logging
              474  LOAD_ATTR                DEBUG

 L. 849       476  LOAD_STR                 '%d hosts entries removed: %s'

 L. 850       478  LOAD_GLOBAL              len
              480  LOAD_FAST                'remove_hosts_keys'
              482  CALL_FUNCTION_1       1  ''

 L. 851       484  LOAD_FAST                'remove_hosts_keys'

 L. 847       486  CALL_METHOD_4         4  ''
              488  POP_TOP          
            490_0  COME_FROM           266  '266'

Parse error at or near `LOAD_CONST' instruction at offset 460

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        res = RefreshThread.get_monitor_data(self)
        res.update(dict(hosts_addr_count=(len(hosts.HOSTS_ADDR_MAP)),
          hosts_count=(len(hosts.HOSTS_MAP)),
          hosts_name_count=(len(hosts.HOSTS_NAME_MAP))))
        return res


USERSUPDATER_TASK = None