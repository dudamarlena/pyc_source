# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir/process.py
# Compiled at: 2020-02-10 05:37:23
# Size of source mod 2**32: 6504 bytes
"""
Basic boilerplate code for maintenance processes and tools etc.
"""
import socket, sys, os, time, smtplib, ldap0, ldap0.functions, aedir
__all__ = [
 'AEProcess',
 'TimestampStateMixin']
CatchAllException = Exception
ldap0._trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))

class AEProcess:
    __doc__ = '\n    Base process class\n    '
    initial_state = None
    script_version = '(no version)'
    ldap_url = None
    ldap0_trace_level = ldap0._trace_level

    def __init__(self):
        self.script_name = os.path.basename(sys.argv[0])
        self.host_fqdn = socket.getfqdn()
        self.logger = aedir.init_logger(self.__class__.__name__)
        if 'LOG_LEVEL' in os.environ:
            self.logger.setLevel(os.environ['LOG_LEVEL'].upper())
        self.logger.debug('Starting %s %s on %s', sys.argv[0], self.script_version, self.host_fqdn)
        self.start_time = None
        self.run_counter = None
        self._ldap_conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._ldap_conn is not None:
            try:
                self.logger.debug('Close LDAP connection to %r', self._ldap_conn.ldap_url_obj.connect_uri())
                self._ldap_conn.unbind_s()
            except (ldap0.LDAPError, AttributeError):
                pass

    @property
    def ldap_conn(self):
        """
        return a LDAP connection to Æ-DIR server
        """
        if self._ldap_conn is None:
            self.logger.debug('Connecting to %r...', self.ldap_url)
            self._ldap_conn = aedir.AEDirObject((self.ldap_url), trace_level=(self.ldap0_trace_level))
            self.logger.debug('Conntected to %r bound as %r', self._ldap_conn.ldap_url_obj.connect_uri(), self._ldap_conn.whoami_s())
        return self._ldap_conn

    def smtp_connection(self, url, local_hostname=None, ca_certs=None, debug_level=0):
        """
        Open SMTP connection if not yet done before
        """
        import mailutil
        local_hostname = local_hostname or self.host_fqdn
        self.logger.debug('Opening SMTP connection to %r from %r ...', url, local_hostname)
        smtp_conn = mailutil.smtp_connection(url,
          local_hostname=local_hostname,
          ca_certs=ca_certs,
          debug_level=debug_level)
        return smtp_conn

    def get_state(self):
        """
        get current state (to be overloaded by derived classes)
        """
        return self.initial_state

    def set_state(self, state):
        """
        set current state (to be overloaded by derived classes)
        """
        pass

    def run_worker(self, state):
        """
        one iteration of worker run (to be overloaded by derived classes)

        must return next state to be passed to set_state()
        """
        self.logger.info('Nothing done in %s.run_worker()', self.__class__.__name__)

    def exit(self):
        """
        method called on exit
        (to be overloaded by derived classes, e.g. for logging a summary)
        """
        self.logger.debug('Exiting %s', self.__class__.__name__)

    def run(self, max_runs=1, run_sleep=60.0):
        """
        the main program
        """
        self.start_time = time.time()
        self.run_counter = 0
        try:
            self.set_state(self.run_worker(self.get_state()))
            self.run_counter += 1
            while not self.run_counter < max_runs:
                if max_runs is None:
                    self.set_state(self.run_worker(self.get_state()))
                    self.run_counter += 1
                    time.sleep(run_sleep)

        except KeyboardInterrupt:
            self.logger.info('Exit on keyboard interrupt')
            self.exit()
        except CatchAllException as err:
            try:
                self.logger.error('Unhandled exception %s: %s',
                  ('.'.join((err.__class__.__module__, err.__class__.__name__))),
                  err,
                  exc_info=True)
            finally:
                err = None
                del err

        else:
            self.exit()


class TimestampStateMixin(object):
    __doc__ = '\n    Mix-in class for AEProcess which implements timestamp-based\n    state strings in a file\n    '
    initial_state = '19700101000000Z'

    def get_state(self):
        """
        Read the timestamp of last run from file `sync_state_filename'
        """
        try:
            with open(self.state_filename, 'rb') as (file_obj):
                last_run_timestr = file_obj.read().strip().decode('utf-8') or self.initial_state
            ldap0.functions.strp_secs(last_run_timestr)
        except CatchAllException as err:
            try:
                self.logger.warning('Error reading timestamp from file %r: %s', self.state_filename, err)
                last_run_timestr = self.initial_state
            finally:
                err = None
                del err

        else:
            self.logger.debug('Read last run timestamp %r from file %r', last_run_timestr, self.state_filename)
        return last_run_timestr

    def set_state(self, current_time_str):
        """
        Write the current state
        """
        if not current_time_str:
            current_time_str = self.initial_state
        try:
            with open(self.state_filename, 'wb') as (file_obj):
                file_obj.write(current_time_str.encode('utf-8'))
        except CatchAllException as err:
            try:
                self.logger.warning('Could not write %r: %s', self.state_filename, err)
            finally:
                err = None
                del err

        else:
            self.logger.debug('Wrote %r to %r', current_time_str, self.state_filename)