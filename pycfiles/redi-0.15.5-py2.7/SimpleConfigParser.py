# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/utils/SimpleConfigParser.py
# Compiled at: 2018-08-13 08:58:37
"""
SimpleConfigParser

Simple configuration file parser: Python module to parse configuration files
without sections. Based on ConfigParser from the standard library.

Author: Philippe Lagadec

Project website: http://www.decalage.info/python/configparser

Inspired from an idea posted by Fredrik Lundh:
http://mail.python.org/pipermail/python-dev/2002-November/029987.html

Usage: see end of source code and http://docs.python.org/library/configparser.html
"""
__author__ = 'Philippe Lagadec'
__version__ = '0.02'
import ConfigParser, StringIO, logging, os, sys
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
NOSECTION = 'NOSECTION'
DEFAULT_MESSAGE_NO_VALUE = "Required parameter '{0}' does not have a value in {1}."
DEFAULT_MESSAGE = '\nPlease set it with the appropriate value. Refer to config-example/settings.ini for assistance.\nProgram will now terminate...'
required_files_dict = {'raw_xml_file': '\nIt should specify the name of the file containing raw data. ', 
   'translation_table_file': '\nIt should specify the name of the required xml file containing translation table. ', 
   'form_events_file': '\nIt should specify the name of the required xml file containing empty form events. ', 
   'research_id_to_redcap_id': '\nIt should specify the name of the xml file containing mapping of research ids to redcap ids. ', 
   'component_to_loinc_code_xml': '\nIt should specify the name of the required xml file  containing a mapping of clinical component ids to loinc codes. '}
required_server_parameters_list = [
 'redcap_uri',
 'token',
 'redcap_support_receiver_email',
 'smtp_host_for_outbound_mail',
 'smtp_port_for_outbound_mail',
 'emr_sftp_server_hostname',
 'emr_sftp_server_username',
 'emr_sftp_project_name',
 'emr_data_file']
optional_parameters_dict = {'report_file_path': 'report.xml', 
   'input_date_format': '%Y-%m-%d %H:%M:%S', 
   'output_date_format': '%Y-%m-%d', 
   'report_file_path2': 'report.html', 
   'sender_email': 'please-do-not-reply@example.com', 
   'project': 'DEFAULT_PROJECT', 
   'rules': {}, 'preprocessors': {}, 'batch_warning_days': 13, 
   'rate_limiter_value_in_redcap': 600, 
   'batch_info_database': 'redi.db', 
   'send_email': 'N', 
   'receiver_email': 'test@example.com', 
   'verify_ssl': True, 
   'replace_fields_in_raw_data_xml': None, 
   'include_rule_errors_in_report': False, 
   'redcap_support_sender_email': 'please-do-not-reply@example.com', 
   'emr_sftp_server_port': 22, 
   'emr_sftp_server_password': None, 
   'emr_sftp_server_private_key': None, 
   'emr_sftp_server_private_key_pass': None, 
   'is_sort_by_lab_id': True, 
   'max_retry_count': 10}

class ConfigurationError(Exception):
    pass


class SimpleConfigParser(ConfigParser.RawConfigParser):
    """
    Simple configuration file parser: based on ConfigParser from the standard
    library, slightly modified to parse configuration files without sections.

    Inspired from an idea posted by Fredrik Lundh:
    http://mail.python.org/pipermail/python-dev/2002-November/029987.html
    """

    def read(self, filename):
        if not os.path.exists(filename):
            logger.exception(('Cannot find settings file: {0}. Program will now terminate...').format(filename))
            sys.exit()
        self.filename = filename
        text = open(filename).read()
        f = StringIO.StringIO('[%s]\n' % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        """get the value of an option"""
        opt_as_string = self.get(NOSECTION, option)
        try:
            opt_as_bool = to_bool(opt_as_string)
            return opt_as_bool
        except ValueError:
            pass

        return opt_as_string

    def getoptionslist(self):
        """get a list of available options"""
        return self.options(NOSECTION)

    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

    def set_attributes(self):
        if not self.getoptionslist():
            message = ("ERROR: Configuration file '{0}' is empty! Program will now terminate...").format(self.filename)
            logger.error(message)
            sys.exit()
        else:
            self.check_parameters()

    def check_parameters(self):
        """
        handle required and default optional_parameters_dict
        """
        for option in required_files_dict:
            if not self.hasoption(option) or self.getoption(option) == '':
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, self.filename) + required_files_dict[option] + DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()
            else:
                setattr(self, option, self.getoption(option))

        for option in required_server_parameters_list:
            if not self.hasoption(option) or self.getoption(option) == '':
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, self.filename) + DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()
            else:
                logger.debug(('Setting required parameter {} = {} ').format(option, self.getoption(option)))
                setattr(self, option, self.getoption(option))

        if self.hasoption('send_email') and self.getoption('send_email'):
            if not self.hasoption('receiver_email') or self.getoption('receiver_email') == '':
                message = DEFAULT_MESSAGE_NO_VALUE.format(option, self.filename) + DEFAULT_MESSAGE
                logger.error(message)
                sys.exit()
        for option in optional_parameters_dict:
            if not self.hasoption(option) or self.getoption(option) == '':
                logger.warn(("Parameter '{0}' in {1} does not have a value. Default value '{2}' applied.").format(option, self.filename, optional_parameters_dict[option]))
                setattr(self, option, optional_parameters_dict[option])
            else:
                setattr(self, option, self.getoption(option))


def to_bool(value):
    """
    Helper function for translating strings into booleans
    @see test/TestReadConfig.py
    """
    valid = {'true': True, 
       't': True, '1': True, 'y': True, 'false': False, 
       'f': False, '0': False, 'n': False}
    if not isinstance(value, str):
        raise ValueError('Cannot check boolean value. Not a string.')
    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    raise ValueError('Not a boolean string: "%s"' % value)


if __name__ == '__main__':
    print 'SimpleConfigParser tests:'
    filename = 'sample_config_no_section.ini'
    cp = SimpleConfigParser()
    print 'Parsing %s...' % filename
    cp.read(filename)
    print 'Sections:', cp.sections()
    print 'getoptionslist():', cp.getoptionslist()
    for option in cp.getoptionslist():
        print "getoption('%s') = '%s'" % (option, cp.getoption(option))

    print "hasoption('wrongname') =", cp.hasoption('wrongname')
    print
    print 'Print out options by attribute instead of recursing the list'
    cp.set_attributes()
    print cp.option1
    print cp.option2