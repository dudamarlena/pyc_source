# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/conf/settings.py
# Compiled at: 2011-01-23 16:28:11
import os
MINPYVERSION = '2.4'
MODE = 'TEST'
SKIP_VALIDATION_TEST = False
GUI = False
DB_DATABASE = 'password_here'
DB_USER = 'username_here'
DB_PASSWD = 'password'
DB_PORT = 5432
DB_HOST = 'localhost'
SVCPT_VERSION = '406'
BASE_PATH = '/home/username_here/synthesis_install_location/synthesis/synthesis'
print 'BASE_PATH is: ', BASE_PATH
PATH_TO_GPG = '/usr/bin/gpg'
PGPHOMEDIR = ''
PASSPHRASE = ''
JFCS_SOURCE_ID = 734
JFCS_AGENCY_ID = 711
JFCS_SERVICE_ID = 705
INPUTFILES_PATH = [
 BASE_PATH + '/input_files']
WEB_SERVICE_INPUTFILES_PATH = [
 BASE_PATH + '/ws_input_files']
XSD_PATH = 'xsd'
OUTPUTFILES_PATH = os.path.join(BASE_PATH, 'output_files')
if not os.path.exists(OUTPUTFILES_PATH):
    os.mkdir(OUTPUTFILES_PATH)
USEDFILES_PATH = os.path.join(BASE_PATH, 'used_files')
if not os.path.exists(USEDFILES_PATH):
    os.mkdir(USEDFILES_PATH)
FAILEDFILES_PATH = os.path.join(BASE_PATH, 'failed_files')
if not os.path.exists(FAILEDFILES_PATH):
    os.mkdir(FAILEDFILES_PATH)
logging_ini_file_name = 'logging.ini'
relative_logging_ini_filepath = os.path.join(BASE_PATH, logging_ini_file_name)
logging_ini_filepath = os.path.abspath(relative_logging_ini_filepath)
print 'logging.ini filepath is at: ', logging_ini_filepath
if not os.path.isfile(logging_ini_filepath):
    print 'no logging.ini found'
LOGGING_INI = logging_ini_filepath
LOGS = os.path.join(BASE_PATH, 'logs')
if not os.path.exists(LOGS):
    os.mkdir(LOGS)
PROCESSED_PATH = ''
SCHEMA_DOCS = {'hud_hmis_xml_2_8': os.path.join(BASE_PATH, XSD_PATH, 'versions', 'HMISXML', '28', 'HUD_HMIS.xsd'), 
   'hud_hmis_xml_3_0': os.path.join(BASE_PATH, XSD_PATH, 'versions', 'HMISXML', '30', 'HUD_HMIS.xsd'), 
   'svcpoint_2_0_xml': os.path.join(BASE_PATH, XSD_PATH, 'versions', 'SVCPT', SVCPT_VERSION, 'sp.xsd'), 
   'jfcs_service_event_xml': os.path.join(BASE_PATH, XSD_PATH, 'JFCS_SERVICE_EVENT.xsd'), 
   'jfcs_client_xml': os.path.join(BASE_PATH, XSD_PATH, 'JFCS_CLIENT.xsd'), 
   'operation_par_xml': os.path.join(BASE_PATH, XSD_PATH, 'Operation_PAR_Extend_HUD_HMIS_2_8.xsd'), 
   'occ_hud_hmis_xml_3_0': os.path.join(BASE_PATH, XSD_PATH, 'OCC_Extend_HUD_HMIS.xsd')}
DEBUG = True
DEBUG_ALCHEMY = False
DEBUG_DB = False
SMTPSERVER = 'localhost'
SMTPPORT = 25
SMTPSENDER = 'me@localhost'
SMTPSENDERPWD = 'mysecret'
SMTPRECIPIENTS = {'/home/username_here/synthesis_install_location/synthesis/synthesis/input_files': {'VENDOR_NAME': 'SomeVendor', 
                                                                                      'SMTPTOADDRESS': [
                                                                                                      'someone@somedomain.com'], 
                                                                                      'SMTPTOADDRESSCC': [], 'SMTPTOADDRESSBCC': [], 'FINGERPRINT': '', 
                                                                                      'USES_ENCRYPTION': False}, 
   '~/workspace/synthesis/installer/build/InputFiles2': {'VENDOR_NAME': 'SomeVendor2', 
                                                         'SMTPTOADDRESS': [
                                                                         'admin@superhost.com'], 
                                                         'SMTPTOADDRESSCC': [], 'SMTPTOADDRESSBCC': [], 'FINGERPRINT': '', 
                                                         'USES_ENCRYPTION': True}, 
   '~/workspace/synthesis/installer/build/InputFiles3': {'VENDOR_NAME': '', 
                                                         'SMTPTOADDRESS': [
                                                                         'sammy.davis@jr.com'], 
                                                         'SMTPTOADDRESSCC': [], 'SMTPTOADDRESSBCC': [], 'FINGERPRINT': '', 
                                                         'USES_ENCRYPTION': False}, 
   '~/workspace/synthesis/installer/build/OutputFiles': {'VENDOR_NAME': '', 
                                                         'SMTPTOADDRESS': [
                                                                         'user@host.com'], 
                                                         'SMTPTOADDRESSCC': [], 'SMTPTOADDRESSBCC': [], 'FINGERPRINT': '', 
                                                         'USES_ENCRYPTION': False}, 
   '~/workspace/synthesis/installer/build/OutputFiles2': {'VENDOR_NAME': '', 
                                                          'SMTPTOADDRESS': [
                                                                          'admin@somehost.com'], 
                                                          'SMTPTOADDRESSCC': [], 'SMTPTOADDRESSBCC': [], 'FINGERPRINT': '', 
                                                          'USES_ENCRYPTION': True}}
try:
    from local_settings import *
except ImportError:
    pass