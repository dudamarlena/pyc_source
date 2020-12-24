# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir/process.py
# Compiled at: 2020-02-10 05:37:23
# Size of source mod 2**32: 6504 bytes
__doc__ = '\nBasic boilerplate code for maintenance processes and tools etc.\n'
import socket, sys, os, time, smtplib, ldap0, ldap0.functions, aedir
__all__ = [
 'AEProcess',
 'TimestampStateMixin']
CatchAllException = Exception
ldap0._trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))

class AEProcess:
    """AEProcess"""
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
        local_hostname = local_hostname or 
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
    """TimestampStateMixin"""
    initial_state = '19700101000000Z'

    def get_state--- This code section failed: ---

 L. 180         0  SETUP_FINALLY        66  'to 66'

 L. 181         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                state_filename
                8  LOAD_STR                 'rb'
               10  CALL_FUNCTION_2       2  ''
               12  SETUP_WITH           44  'to 44'
               14  STORE_FAST               'file_obj'

 L. 182        16  LOAD_FAST                'file_obj'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  LOAD_METHOD              strip
               24  CALL_METHOD_0         0  ''
               26  LOAD_METHOD              decode
               28  LOAD_STR                 'utf-8'
               30  CALL_METHOD_1         1  ''
               32  JUMP_IF_TRUE_OR_POP    38  'to 38'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                initial_state
             38_0  COME_FROM            32  '32'
               38  STORE_FAST               'last_run_timestr'
               40  POP_BLOCK        
               42  BEGIN_FINALLY    
             44_0  COME_FROM_WITH       12  '12'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

 L. 184        50  LOAD_GLOBAL              ldap0
               52  LOAD_ATTR                functions
               54  LOAD_METHOD              strp_secs
               56  LOAD_FAST                'last_run_timestr'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  POP_BLOCK        
               64  JUMP_FORWARD        124  'to 124'
             66_0  COME_FROM_FINALLY     0  '0'

 L. 185        66  DUP_TOP          
               68  LOAD_GLOBAL              CatchAllException
               70  COMPARE_OP               exception-match
               72  POP_JUMP_IF_FALSE   122  'to 122'
               74  POP_TOP          
               76  STORE_FAST               'err'
               78  POP_TOP          
               80  SETUP_FINALLY       110  'to 110'

 L. 186        82  LOAD_FAST                'self'
               84  LOAD_ATTR                logger
               86  LOAD_METHOD              warning

 L. 187        88  LOAD_STR                 'Error reading timestamp from file %r: %s'

 L. 188        90  LOAD_FAST                'self'
               92  LOAD_ATTR                state_filename

 L. 189        94  LOAD_FAST                'err'

 L. 186        96  CALL_METHOD_3         3  ''
               98  POP_TOP          

 L. 191       100  LOAD_FAST                'self'
              102  LOAD_ATTR                initial_state
              104  STORE_FAST               'last_run_timestr'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM_FINALLY    80  '80'
              110  LOAD_CONST               None
              112  STORE_FAST               'err'
              114  DELETE_FAST              'err'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_FORWARD        142  'to 142'
            122_0  COME_FROM            72  '72'
              122  END_FINALLY      
            124_0  COME_FROM            64  '64'

 L. 193       124  LOAD_FAST                'self'
              126  LOAD_ATTR                logger
              128  LOAD_METHOD              debug

 L. 194       130  LOAD_STR                 'Read last run timestamp %r from file %r'

 L. 195       132  LOAD_FAST                'last_run_timestr'

 L. 196       134  LOAD_FAST                'self'
              136  LOAD_ATTR                state_filename

 L. 193       138  CALL_METHOD_3         3  ''
              140  POP_TOP          
            142_0  COME_FROM           120  '120'

 L. 198       142  LOAD_FAST                'last_run_timestr'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 42

    def set_state--- This code section failed: ---

 L. 204         0  LOAD_FAST                'current_time_str'
                2  POP_JUMP_IF_TRUE     10  'to 10'

 L. 205         4  LOAD_FAST                'self'
                6  LOAD_ATTR                initial_state
                8  STORE_FAST               'current_time_str'
             10_0  COME_FROM             2  '2'

 L. 206        10  SETUP_FINALLY        56  'to 56'

 L. 208        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                state_filename
               18  LOAD_STR                 'wb'
               20  CALL_FUNCTION_2       2  ''
               22  SETUP_WITH           46  'to 46'
               24  STORE_FAST               'file_obj'

 L. 209        26  LOAD_FAST                'file_obj'
               28  LOAD_METHOD              write
               30  LOAD_FAST                'current_time_str'
               32  LOAD_METHOD              encode
               34  LOAD_STR                 'utf-8'
               36  CALL_METHOD_1         1  ''
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  BEGIN_FINALLY    
             46_0  COME_FROM_WITH       22  '22'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      
               52  POP_BLOCK        
               54  JUMP_FORWARD        108  'to 108'
             56_0  COME_FROM_FINALLY    10  '10'

 L. 210        56  DUP_TOP          
               58  LOAD_GLOBAL              CatchAllException
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   106  'to 106'
               64  POP_TOP          
               66  STORE_FAST               'err'
               68  POP_TOP          
               70  SETUP_FINALLY        94  'to 94'

 L. 211        72  LOAD_FAST                'self'
               74  LOAD_ATTR                logger
               76  LOAD_METHOD              warning
               78  LOAD_STR                 'Could not write %r: %s'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                state_filename
               84  LOAD_FAST                'err'
               86  CALL_METHOD_3         3  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_FINALLY    70  '70'
               94  LOAD_CONST               None
               96  STORE_FAST               'err'
               98  DELETE_FAST              'err'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        126  'to 126'
            106_0  COME_FROM            62  '62'
              106  END_FINALLY      
            108_0  COME_FROM            54  '54'

 L. 213       108  LOAD_FAST                'self'
              110  LOAD_ATTR                logger
              112  LOAD_METHOD              debug
              114  LOAD_STR                 'Wrote %r to %r'
              116  LOAD_FAST                'current_time_str'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                state_filename
              122  CALL_METHOD_3         3  ''
              124  POP_TOP          
            126_0  COME_FROM           104  '104'

Parse error at or near `BEGIN_FINALLY' instruction at offset 44