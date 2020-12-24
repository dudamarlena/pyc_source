# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir_pproc/persattrs.py
# Compiled at: 2020-02-05 10:31:56
# Size of source mod 2**32: 6548 bytes
__doc__ = '\naedir_pproc.persattrs - Sync the personnel attributes (cn, sn, givenName, mail)\nfrom aePerson to aeUser entries\n'
import sys, time, ldap0, ldap0.modlist, ldap0.functions, ldap0.filter
from ldap0.base import encode_list
import aedir, aedir.process
from .__about__ import __version__, __author__, __license__
AEDIR_AEPERSON_ATTRS = [
 'cn',
 'givenName',
 'sn',
 'mail',
 'aeStatus']
aedir.process.CatchAllException = Exception

class SyncProcess(aedir.process.TimestampStateMixin, aedir.process.AEProcess):
    """SyncProcess"""
    script_version = __version__

    def __init__(self, state_filename):
        aedir.process.AEProcess.__init__(self)
        self.state_filename = state_filename
        self.aeperson_counter = 0
        self.modify_counter = 0
        self.error_counter = 0
        self.deactivate_counter = 0

    def exit(self):
        """
        Log a summary of actions and errors, mainly counters
        """
        self.logger.debug('Found %d aePerson entries', self.aeperson_counter)
        if self.modify_counter:
            self.logger.info('Updated %d AE-DIR entries (%d deactivated).', self.modify_counter, self.deactivate_counter)
        else:
            self.logger.debug('No modifications.')
        if self.error_counter:
            self.logger.error('%d errors.', self.error_counter)

    def run_worker(self, last_run_timestr):
        """
        the main worker part
        """
        current_time_str = ldap0.functions.strf_secs(time.time())
        self.logger.debug('current_time_str=%r last_run_timestr=%r', current_time_str, last_run_timestr)
        aeperson_filterstr = '(&(objectClass=aePerson)(modifyTimestamp>={0})(!(modifyTimestamp>={1})))'.format(last_run_timestr, current_time_str)
        self.logger.debug('Searching in %r with filter %r', self.ldap_conn.search_base, aeperson_filterstr)
        msg_id = self.ldap_conn.search((self.ldap_conn.search_base),
          (ldap0.SCOPE_SUBTREE),
          aeperson_filterstr,
          attrlist=AEDIR_AEPERSON_ATTRS)
        for ldap_res in self.ldap_conn.results(msg_id):
            for aeperson in ldap_res.rdata:
                self.aeperson_counter += 1
                aeuser_results = self.ldap_conn.search_s((self.ldap_conn.search_base),
                  (ldap0.SCOPE_SUBTREE),
                  ('(&(objectClass=aeUser)(aePerson=%s))' % ldap0.filter.escape_str(aeperson.dn_s)),
                  attrlist=(AEDIR_AEPERSON_ATTRS + ['uid', 'uidNumber', 'displayName']))
                for aeuser in aeuser_results:
                    new_aeuser_entry = {}
                    new_aeuser_entry.update(aeperson.entry_s)
                    del new_aeuser_entry['aeStatus']
                    new_aeuser_entry['displayName'] = [
                     '{cn} ({uid}/{uidNumber})'.format(cn=(aeperson.entry_s['cn'][0]),
                       uid=(aeuser.entry_s['uid'][0]),
                       uidNumber=(aeuser.entry_s['uidNumber'][0]))]
                    aeperson_status = int(aeperson.entry_s['aeStatus'][0])
                    aeuser_status = int(aeuser.entry_s['aeStatus'][0])
                    if aeperson_status > 0:
                        if aeuser_status <= 0:
                            new_aeuser_entry['aeStatus'] = [
                             '1']
                            self.deactivate_counter += 1
                        else:
                            new_aeuser_entry['aeStatus'] = aeuser.entry_s['aeStatus']
                        modlist = ldap0.modlist.modify_modlist((aeuser.entry_as),
                          {encode_list(avs):at for at, avs in new_aeuser_entry.items()},
                          ignore_attr_types=[
                         'uid', 'uidNumber'])
                        if not modlist:
                            self.logger.debug('Nothing to do in %r => skipped', aeuser.dn_s)
                    else:
                        self.logger.debug('Update existing entry %r: %r', aeuser.dn_s, modlist)
                        try:
                            self.ldap_conn.modify_s(aeuser.dn_s, modlist)
                        except ldap0.LDAPError as ldap_err:
                            try:
                                self.logger.error('LDAP error modifying %r with %r: %s', aeuser.dn_s, modlist, ldap_err)
                                self.error_counter += 1
                            finally:
                                ldap_err = None
                                del ldap_err

                        else:
                            self.logger.info('Updated entry %r: %r', aeuser.dn_s, modlist)
                            self.modify_counter += 1

            return current_time_str


def main--- This code section failed: ---

 L. 194         0  LOAD_GLOBAL              SyncProcess
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                argv
                6  LOAD_CONST               1
                8  BINARY_SUBSCR    
               10  CALL_FUNCTION_1       1  ''
               12  SETUP_WITH           32  'to 32'
               14  STORE_FAST               'ae_process'

 L. 195        16  LOAD_FAST                'ae_process'
               18  LOAD_ATTR                run
               20  LOAD_CONST               1
               22  LOAD_CONST               ('max_runs',)
               24  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               26  POP_TOP          
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH       12  '12'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 30


if __name__ == '__main__':
    main()