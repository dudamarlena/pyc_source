# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/pwd/expreset.py
# Compiled at: 2020-02-05 10:20:59
# Size of source mod 2**32: 4635 bytes
__doc__ = '\naedir_pproc.pwd.expreset - Remove expired msPwdResetObject attributes\n'
import time
from socket import getfqdn
import ldap0, ldap0.functions, aedir.process
from aedirpwd_cnf import FILTERSTR_EXPIRE, NOTIFY_OLDEST_TIMESPAN, PWD_ADMIN_LEN, SERVER_ID
from ..__about__ import __version__, __author__, __license__

class AEDIRPwdJob(aedir.process.AEProcess):
    """AEDIRPwdJob"""
    script_version = __version__
    notify_oldest_timespan = NOTIFY_OLDEST_TIMESPAN
    user_attrs = [
     'objectClass',
     'uid',
     'cn',
     'displayName',
     'description',
     'mail',
     'creatorsName']
    admin_attrs = [
     'objectClass',
     'uid',
     'cn',
     'mail']

    def __init__(self, server_id):
        aedir.process.AEProcess.__init__(self)
        self.host_fqdn = getfqdn()
        self.server_id = server_id
        self.notification_counter = 0
        self._smtp_conn = None
        self.logger.debug('running on %r with (serverID %r)', self.host_fqdn, self.server_id)

    def _get_time_strings(self):
        """
        Determine
        1. oldest possible last timestamp (sounds strange, yeah!)
        2. and current time
        """
        current_time = time.time()
        return (
         ldap0.functions.strf_secs(current_time - self.notify_oldest_timespan),
         ldap0.functions.strf_secs(current_time))

    def _expire_pwd_reset(self, last_run_timestr, current_run_timestr):
        """
        Remove expired msPwdResetObject attributes
        """
        expired_pwreset_filter = FILTERSTR_EXPIRE.format(currenttime=current_run_timestr)
        ldap_results = self.ldap_conn.search_s((self.ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          filterstr=expired_pwreset_filter,
          attrlist=[
         'objectClass',
         'msPwdResetExpirationTime',
         'msPwdResetTimestamp',
         'msPwdResetAdminPw'])
        self.logger.debug('%d expired password resets found with %r', len(ldap_results), expired_pwreset_filter)
        for res in ldap_results:
            self.logger.debug('Found %r: %r', res.dn_s, res.entry_as)
            ldap_mod_list = [
             (
              ldap0.MOD_DELETE, b'objectClass', [b'msPwdResetObject']),
             (
              ldap0.MOD_DELETE,
              b'msPwdResetTimestamp',
              [
               res.entry_as['msPwdResetTimestamp'][0]]),
             (
              ldap0.MOD_DELETE,
              b'msPwdResetExpirationTime',
              [
               res.entry_as['msPwdResetExpirationTime'][0]]),
             (
              ldap0.MOD_DELETE, b'msPwdResetEnabled', None),
             (
              ldap0.MOD_DELETE, b'msPwdResetPasswordHash', None)]
            if not PWD_ADMIN_LEN:
                if 'msPwdResetAdminPw' in res.entry_as:
                    ldap_mod_list.append((
                     ldap0.MOD_DELETE, b'msPwdResetAdminPw', None))
                try:
                    self.ldap_conn.modify_s(res.dn_s, ldap_mod_list)
                except ldap0.LDAPError as ldap_error:
                    try:
                        self.logger.warning('LDAPError removing msPwdResetObject attrs in %r: %s', res.dn_s, ldap_error)
                    finally:
                        ldap_error = None
                        del ldap_error

                else:
                    self.logger.info('Removed msPwdResetObject attributes from %r', res.dn_s)

    def run_worker(self, state):
        """
        Run the job
        """
        last_run_timestr, current_run_timestr = self._get_time_strings()
        self._expire_pwd_reset(last_run_timestr, current_run_timestr)
        return current_run_timestr


def main--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL              AEDIRPwdJob
                2  LOAD_GLOBAL              SERVER_ID
                4  CALL_FUNCTION_1       1  ''
                6  SETUP_WITH           26  'to 26'
                8  STORE_FAST               'ae_process'

 L. 147        10  LOAD_FAST                'ae_process'
               12  LOAD_ATTR                run
               14  LOAD_CONST               1
               16  LOAD_CONST               ('max_runs',)
               18  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        6  '6'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 24


if __name__ == '__main__':
    main()