# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/splunk/modules/cofense.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 15959 bytes
"""
Copyright 2013-2015 Cofense, Inc.  All rights reserved.

This software is provided by Cofense, Inc. ("Cofense") on an "as is" basis and any express or implied warranties,
including but not limited to the implied warranties of merchantability and fitness for a particular purpose, are
disclaimed in all aspects.  In no event will Cofense be liable for any direct, indirect, special, incidental or
consequential damages relating to the use of this software, even if advised of the possibility of such damage. Use of
this software is pursuant to, and permitted only in accordance with, the agreement between you and Cofense.

Cofense Base Module (for both Python 2.x & Python 3.x)
Author: Josh Larkins/Kevin Stilwell/Robert McMahon
Support: support@cofense.com
ChangesetID: CHANGESETID_VERSION_STRING

"""
try:
    from configparser import ConfigParser
    PYTHON_MAJOR_VERSION = 3
except ImportError:
    from ConfigParser import SafeConfigParser
    PYTHON_MAJOR_VERSION = 2

from calendar import timegm
from datetime import datetime
import time, json, logging, os, sys, argparse, requests
LOGGER = logging.getLogger('cofense')

class CofenseConnectionType:
    THREAT_SEARCH = 1
    THREAT_UPDATES = 2
    T3_CEF = 3
    T3_STIX = 4


def connect_to_cofense--- This code section failed: ---

 L.  61         0  LOAD_CONST               3
                2  STORE_FAST               'max_attempts'

 L.  63       4_6  SETUP_LOOP          664  'to 664'
                8  LOAD_GLOBAL              range
               10  LOAD_FAST                'max_attempts'
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  GET_ITER         
            16_18  FOR_ITER            630  'to 630'
               20  STORE_FAST               'attempt'

 L.  64     22_24  SETUP_EXCEPT        310  'to 310'

 L.  65        26  LOAD_GLOBAL              LOGGER
               28  LOAD_METHOD              debug
               30  LOAD_STR                 'Requesting data from ThreatHQ'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  POP_TOP          

 L.  66        36  LOAD_FAST                'verb'
               38  LOAD_STR                 'GET'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    66  'to 66'

 L.  67        44  LOAD_GLOBAL              requests
               46  LOAD_ATTR                get
               48  LOAD_FAST                'url'
               50  LOAD_FAST                'params'
               52  LOAD_FAST                'auth'
               54  LOAD_FAST                'proxies'
               56  LOAD_FAST                'headers'
               58  LOAD_CONST               ('url', 'params', 'auth', 'proxies', 'headers')
               60  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               62  STORE_FAST               'response'
               64  JUMP_FORWARD        108  'to 108'
             66_0  COME_FROM            42  '42'

 L.  68        66  LOAD_FAST                'verb'
               68  LOAD_STR                 'POST'
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    96  'to 96'

 L.  69        74  LOAD_GLOBAL              requests
               76  LOAD_ATTR                post
               78  LOAD_FAST                'url'
               80  LOAD_FAST                'params'
               82  LOAD_FAST                'auth'
               84  LOAD_FAST                'proxies'
               86  LOAD_FAST                'headers'
               88  LOAD_CONST               ('url', 'params', 'auth', 'proxies', 'headers')
               90  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               92  STORE_FAST               'response'
               94  JUMP_FORWARD        108  'to 108'
             96_0  COME_FROM            72  '72'

 L.  71        96  LOAD_GLOBAL              ValueError
               98  LOAD_STR                 'The HTTP verb must be GET or POST not: %s'
              100  LOAD_FAST                'verb'
              102  BINARY_MODULO    
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            94  '94'
            108_1  COME_FROM            64  '64'

 L.  73       108  LOAD_GLOBAL              LOGGER
              110  LOAD_METHOD              debug
              112  LOAD_STR                 'Got a %d response'
              114  LOAD_FAST                'response'
              116  LOAD_ATTR                status_code
              118  BINARY_MODULO    
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          

 L.  75       124  LOAD_FAST                'response'
              126  LOAD_ATTR                status_code
              128  LOAD_CONST               400
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   158  'to 158'

 L.  76       134  LOAD_GLOBAL              ValueError
              136  LOAD_STR                 'HTTP Status: '
              138  LOAD_GLOBAL              str
              140  LOAD_FAST                'response'
              142  LOAD_ATTR                status_code
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  BINARY_ADD       
              148  LOAD_STR                 '  Message: Bad request due to malformed syntax.'
              150  BINARY_ADD       
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  RAISE_VARARGS_1       1  'exception instance'
              156  JUMP_FORWARD        304  'to 304'
            158_0  COME_FROM           132  '132'

 L.  77       158  LOAD_FAST                'response'
              160  LOAD_ATTR                status_code
              162  LOAD_CONST               401
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   192  'to 192'

 L.  78       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'HTTP Status: '
              172  LOAD_GLOBAL              str
              174  LOAD_FAST                'response'
              176  LOAD_ATTR                status_code
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  BINARY_ADD       
              182  LOAD_STR                 '  Message: Failed to authorize.'
              184  BINARY_ADD       
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  RAISE_VARARGS_1       1  'exception instance'
              190  JUMP_FORWARD        304  'to 304'
            192_0  COME_FROM           166  '166'

 L.  79       192  LOAD_FAST                'response'
              194  LOAD_ATTR                status_code
              196  LOAD_CONST               404
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   226  'to 226'

 L.  80       202  LOAD_GLOBAL              ValueError
              204  LOAD_STR                 'HTTP Status: '
              206  LOAD_GLOBAL              str
              208  LOAD_FAST                'response'
              210  LOAD_ATTR                status_code
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  BINARY_ADD       
              216  LOAD_STR                 '  Message: Requested data not found.'
              218  BINARY_ADD       
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  RAISE_VARARGS_1       1  'exception instance'
              224  JUMP_FORWARD        304  'to 304'
            226_0  COME_FROM           200  '200'

 L.  81       226  LOAD_GLOBAL              str
              228  LOAD_FAST                'response'
              230  LOAD_ATTR                status_code
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  LOAD_METHOD              startswith
              236  LOAD_STR                 '5'
              238  CALL_METHOD_1         1  '1 positional argument'
          240_242  POP_JUMP_IF_FALSE   268  'to 268'

 L.  82       244  LOAD_GLOBAL              ValueError
              246  LOAD_STR                 'HTTP Status: '
              248  LOAD_GLOBAL              str
              250  LOAD_FAST                'response'
              252  LOAD_ATTR                status_code
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  BINARY_ADD       
              258  LOAD_STR                 '  Message: Server error.'
              260  BINARY_ADD       
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  RAISE_VARARGS_1       1  'exception instance'
              266  JUMP_FORWARD        304  'to 304'
            268_0  COME_FROM           240  '240'

 L.  83       268  LOAD_FAST                'response'
              270  LOAD_ATTR                status_code
              272  LOAD_CONST               200
              274  COMPARE_OP               !=
          276_278  POP_JUMP_IF_FALSE   304  'to 304'

 L.  84       280  LOAD_GLOBAL              ValueError
              282  LOAD_STR                 'HTTP Status: '
              284  LOAD_GLOBAL              str
              286  LOAD_FAST                'response'
              288  LOAD_ATTR                status_code
              290  CALL_FUNCTION_1       1  '1 positional argument'
              292  BINARY_ADD       
              294  LOAD_STR                 '  Message: Connection error.'
              296  BINARY_ADD       
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  RAISE_VARARGS_1       1  'exception instance'
              302  JUMP_FORWARD        304  'to 304'
            304_0  COME_FROM           302  '302'
            304_1  COME_FROM           276  '276'
            304_2  COME_FROM           266  '266'
            304_3  COME_FROM           224  '224'
            304_4  COME_FROM           190  '190'
            304_5  COME_FROM           156  '156'

 L.  86       304  POP_BLOCK        
          306_308  JUMP_FORWARD        612  'to 612'
            310_0  COME_FROM_EXCEPT     22  '22'

 L.  88       310  DUP_TOP          
              312  LOAD_GLOBAL              requests
              314  LOAD_ATTR                exceptions
              316  LOAD_ATTR                ChunkedEncodingError
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   368  'to 368'
              324  POP_TOP          
              326  STORE_FAST               'exception'
              328  POP_TOP          
              330  SETUP_FINALLY       356  'to 356'

 L.  89       332  LOAD_GLOBAL              LOGGER
              334  LOAD_METHOD              error
              336  LOAD_STR                 'An error occurred during the previous request. Results are as follows:  Message: Chunked Encoding Error.'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  POP_TOP          

 L.  90       342  LOAD_GLOBAL              remove_lock_and_exit
              344  LOAD_FAST                'config'
              346  LOAD_CONST               1
              348  CALL_FUNCTION_2       2  '2 positional arguments'
              350  POP_TOP          
              352  POP_BLOCK        
              354  LOAD_CONST               None
            356_0  COME_FROM_FINALLY   330  '330'
              356  LOAD_CONST               None
              358  STORE_FAST               'exception'
              360  DELETE_FAST              'exception'
              362  END_FINALLY      
              364  POP_EXCEPT       
              366  JUMP_BACK            16  'to 16'
            368_0  COME_FROM           320  '320'

 L.  92       368  DUP_TOP          
              370  LOAD_GLOBAL              requests
              372  LOAD_ATTR                exceptions
              374  LOAD_ATTR                Timeout
              376  COMPARE_OP               exception-match
          378_380  POP_JUMP_IF_FALSE   426  'to 426'
              382  POP_TOP          
              384  STORE_FAST               'exception'
              386  POP_TOP          
              388  SETUP_FINALLY       414  'to 414'

 L.  93       390  LOAD_GLOBAL              LOGGER
              392  LOAD_METHOD              error
              394  LOAD_STR                 'An error occurred during the previous request. Results are as follows:  Message: Request timeout.'
              396  CALL_METHOD_1         1  '1 positional argument'
              398  POP_TOP          

 L.  94       400  LOAD_GLOBAL              remove_lock_and_exit
              402  LOAD_FAST                'config'
              404  LOAD_CONST               2
              406  CALL_FUNCTION_2       2  '2 positional arguments'
              408  POP_TOP          
              410  POP_BLOCK        
              412  LOAD_CONST               None
            414_0  COME_FROM_FINALLY   388  '388'
              414  LOAD_CONST               None
              416  STORE_FAST               'exception'
              418  DELETE_FAST              'exception'
              420  END_FINALLY      
              422  POP_EXCEPT       
              424  JUMP_BACK            16  'to 16'
            426_0  COME_FROM           378  '378'

 L.  96       426  DUP_TOP          
              428  LOAD_GLOBAL              requests
              430  LOAD_ATTR                exceptions
              432  LOAD_ATTR                TooManyRedirects
              434  COMPARE_OP               exception-match
          436_438  POP_JUMP_IF_FALSE   484  'to 484'
              440  POP_TOP          
              442  STORE_FAST               'exception'
              444  POP_TOP          
              446  SETUP_FINALLY       472  'to 472'

 L.  97       448  LOAD_GLOBAL              LOGGER
              450  LOAD_METHOD              error
              452  LOAD_STR                 'An error occurred during the previous request. Results are as follows:  Message: Too many requests.'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  POP_TOP          

 L.  98       458  LOAD_GLOBAL              remove_lock_and_exit
              460  LOAD_FAST                'config'
              462  LOAD_CONST               3
              464  CALL_FUNCTION_2       2  '2 positional arguments'
              466  POP_TOP          
              468  POP_BLOCK        
              470  LOAD_CONST               None
            472_0  COME_FROM_FINALLY   446  '446'
              472  LOAD_CONST               None
              474  STORE_FAST               'exception'
              476  DELETE_FAST              'exception'
              478  END_FINALLY      
              480  POP_EXCEPT       
              482  JUMP_BACK            16  'to 16'
            484_0  COME_FROM           436  '436'

 L. 100       484  DUP_TOP          
              486  LOAD_GLOBAL              requests
              488  LOAD_ATTR                exceptions
              490  LOAD_ATTR                RequestException
              492  COMPARE_OP               exception-match
          494_496  POP_JUMP_IF_FALSE   546  'to 546'
              498  POP_TOP          
              500  STORE_FAST               'exception'
              502  POP_TOP          
              504  SETUP_FINALLY       534  'to 534'

 L. 101       506  LOAD_GLOBAL              LOGGER
              508  LOAD_METHOD              error
              510  LOAD_STR                 'An error occurred during the previous request. Results are as follows: Message: Request exception. %s'
              512  LOAD_FAST                'exception'
              514  BINARY_MODULO    
              516  CALL_METHOD_1         1  '1 positional argument'
              518  POP_TOP          

 L. 102       520  LOAD_GLOBAL              remove_lock_and_exit
              522  LOAD_FAST                'config'
              524  LOAD_CONST               4
              526  CALL_FUNCTION_2       2  '2 positional arguments'
              528  POP_TOP          
              530  POP_BLOCK        
              532  LOAD_CONST               None
            534_0  COME_FROM_FINALLY   504  '504'
              534  LOAD_CONST               None
              536  STORE_FAST               'exception'
              538  DELETE_FAST              'exception'
              540  END_FINALLY      
              542  POP_EXCEPT       
              544  JUMP_BACK            16  'to 16'
            546_0  COME_FROM           494  '494'

 L. 104       546  DUP_TOP          
              548  LOAD_GLOBAL              ValueError
              550  COMPARE_OP               exception-match
          552_554  POP_JUMP_IF_FALSE   610  'to 610'
              556  POP_TOP          
              558  STORE_FAST               'exception'
              560  POP_TOP          
              562  SETUP_FINALLY       598  'to 598'

 L. 105       564  LOAD_GLOBAL              LOGGER
              566  LOAD_METHOD              error
              568  LOAD_STR                 'An error occurred during the previous request. Results are as follows: '
              570  LOAD_FAST                'exception'
              572  LOAD_ATTR                args
              574  LOAD_CONST               0
              576  BINARY_SUBSCR    
              578  BINARY_ADD       
              580  CALL_METHOD_1         1  '1 positional argument'
              582  POP_TOP          

 L. 106       584  LOAD_GLOBAL              remove_lock_and_exit
              586  LOAD_FAST                'config'
              588  LOAD_CONST               5
              590  CALL_FUNCTION_2       2  '2 positional arguments'
              592  POP_TOP          
              594  POP_BLOCK        
              596  LOAD_CONST               None
            598_0  COME_FROM_FINALLY   562  '562'
              598  LOAD_CONST               None
              600  STORE_FAST               'exception'
              602  DELETE_FAST              'exception'
              604  END_FINALLY      
              606  POP_EXCEPT       
              608  JUMP_BACK            16  'to 16'
            610_0  COME_FROM           552  '552'
              610  END_FINALLY      
            612_0  COME_FROM           306  '306'

 L. 109       612  LOAD_GLOBAL              LOGGER
              614  LOAD_METHOD              debug
              616  LOAD_STR                 'Request was successful.'
              618  CALL_METHOD_1         1  '1 positional argument'
              620  POP_TOP          

 L. 110       622  LOAD_FAST                'response'
              624  LOAD_ATTR                content
              626  RETURN_VALUE     
              628  JUMP_BACK            16  'to 16'
              630  POP_BLOCK        

 L. 113       632  LOAD_GLOBAL              LOGGER
              634  LOAD_METHOD              error
              636  LOAD_STR                 'An error occurred. Tried to complete request '
              638  LOAD_GLOBAL              str
              640  LOAD_FAST                'max_attempts'
              642  CALL_FUNCTION_1       1  '1 positional argument'
              644  BINARY_ADD       
              646  LOAD_STR                 ' times and all failed.'
              648  BINARY_ADD       
              650  CALL_METHOD_1         1  '1 positional argument'
              652  POP_TOP          

 L. 114       654  LOAD_GLOBAL              remove_lock_and_exit
              656  LOAD_FAST                'config'
              658  LOAD_CONST               6
              660  CALL_FUNCTION_2       2  '2 positional arguments'
              662  POP_TOP          
            664_0  COME_FROM_LOOP        4  '4'

Parse error at or near `POP_BLOCK' instruction at offset 304


def retrieve_from_threat_updates(config, end_timestamp, headers=None):
    """
    Handle output from Cofense's /threat/updates
    """
    auth, url, proxies, headers = setup_cofense_connection(CofenseConnectionType.THREAT_UPDATES, config)
    if config.get('cofense', 'position'):
        payload = {'position': config.get('cofense', 'position')}
    else:
        payload = {'timestamp': end_timestamp}
    if config.get('cofense', 'position'):
        LOGGER.debug('Retrieving ' + url + ' with position: ' + payload.get('position'))
    else:
        LOGGER.debug('Retrieving ' + url + ' with end_timestamp: ' + str(end_timestamp))
    response = connect_to_cofense(config=config, auth=auth, url=url, params=payload, proxies=proxies, verb='POST', headers=headers)
    LOGGER.debug('Results retrieved.')
    if PYTHON_MAJOR_VERSION == 3:
        result = json.loads(response.decode())
    else:
        result = json.loads(response)
    changelog = result.get('data').get('changelog')
    changelog_size = len(changelog)
    next_position = result.get('data').get('nextPosition')
    malware_add_set = set()
    phish_add_set = set()
    malware_remove_set = set()
    phish_remove_set = set()
    LOGGER.debug('Changelog size: %d' % len(changelog))
    for update in changelog:
        threat_id = str(update.get('threatId'))
        threat_type = update.get('threatType')
        deleted = update.get('deleted')
        LOGGER.debug('Processing threat_id: %s, threat_type: %s, deleted: %s' % (threat_id, threat_type, deleted))
        if not deleted:
            if threat_type == 'malware':
                LOGGER.debug('Adding threat_id: %s to the malware_add_set' % threat_id)
                malware_add_set.add(threat_id)
            else:
                if threat_type == 'phish':
                    LOGGER.debug('Adding threat_id: %s to the phish_add_set' % threat_id)
                    phish_add_set.add(threat_id)
                else:
                    LOGGER.debug('Not adding entry with threat type %s' % threat_type)
        elif threat_type == 'malware':
            LOGGER.debug('Adding malware to malware_remove_set threat_id:%s' % threat_id)
            malware_remove_set.add(threat_id)
        elif threat_type == 'phish':
            LOGGER.debug('Adding phish to phish_remove_set threat_id: %s' % threat_id)
            phish_remove_set.add(threat_id)
        else:
            LOGGER.debug('Not adding entry with threat type %s' % threat_type)

    LOGGER.debug('changelog_size: %d, malware_add_size: %d, phish_add_size: %d, malware_remove_size: %d, phish_remove_size: %s' % (changelog_size, len(malware_add_set), len(phish_add_set), len(malware_remove_set), len(phish_remove_set)))
    return (next_position, changelog_size, malware_add_set, phish_add_set, malware_remove_set, phish_remove_set)


def retrieve_from_t3_cef(config, payload=None, threat_type=None, threat_id=None):
    """
    Handle output from Cofense's /t3/{threat_type}/{threat_id}/cef.
    """
    auth, url, proxies, headers = setup_cofense_connection(CofenseConnectionType.T3_CEF, config, threat_type, threat_id)
    LOGGER.debug('Retrieving ' + url)
    if payload:
        response = connect_to_cofense(config=config, auth=auth, url=url, params=payload, proxies=proxies, verb='POST', headers=headers)
    else:
        response = connect_to_cofense(config=config, auth=auth, url=url, proxies=proxies, verb='GET', headers=headers)
    return response


def retrieve_from_t3_stix(config, threat_type=None, threat_id=None):
    """
    Handle output from Cofense's /t3/{threat_type}/{threat_id}/stix.
    """
    auth, url, proxies, headers = setup_cofense_connection(CofenseConnectionType.T3_STIX, config, threat_type, threat_id)
    LOGGER.debug('Retrieving STIX from ' + url)
    response = connect_to_cofense(config=config, auth=auth, url=url, proxies=proxies, verb='GET', headers=headers)
    return response


def retrieve_from_threat_search(config, payload):
    """
    Handle output from Cofense's /threat/search
    """
    LOGGER.debug('Searching ThreatHQ for %s' % str(payload))
    auth, url, proxies, headers = setup_cofense_connection(CofenseConnectionType.THREAT_SEARCH, config)
    if payload.get('page') and payload.get('beginTimestamp') and payload.get('endTimestamp'):
        LOGGER.debug('Retrieving JSON from ' + url + ' for window from ' + str(datetime.fromtimestamp(payload.get('beginTimestamp'))) + ' to ' + str(datetime.fromtimestamp(payload.get('endTimestamp'))) + '. Retrieving page ' + str(payload.get('page')) + '...')
    else:
        if payload.get('beginTimestamp'):
            if payload.get('endTimestamp'):
                LOGGER.debug('Retrieving JSON from ' + url + ' for window from ' + str(datetime.fromtimestamp(payload.get('beginTimestamp', ''))) + ' to ' + str(datetime.fromtimestamp(payload.get('endTimestamp', ''))))
            else:
                if PYTHON_MAJOR_VERSION == 3:
                    LOGGER.debug('Retrieving JSON from ' + url + ' for ' + str(len(payload.get('threatId'))) + ' Threat ID(s).')
                else:
                    LOGGER.debug('Retrieving JSON from ' + url + ' for 1 Threat ID.')
        else:
            response = connect_to_cofense(config=config, auth=auth, url=url, params=payload, proxies=proxies, verb='POST', headers=headers)
            if PYTHON_MAJOR_VERSION == 3:
                result = json.loads(response.decode())
            else:
                result = json.loads(response)
        if result.get('success'):
            LOGGER.debug('Retrieved ' + str(len(result.get('data').get('threats'))) + ' threats, processing.')
            return (result.get('data').get('page').get('totalPages'), result.get('data').get('threats'))
        remove_lock_and_exit(config, 7)


def setup_cofense_connection(connection_type, config, threat_type=None, threat_id=None):
    """
    This method will handle connection setup tasks for the various types of queries
    :param connection_type: CofenseConnectionType
    :param config: connection configuration
    :param threat_type: Type of threat to search for (Threat Search and Threat Updates only)
    :param threat_id: ID of threat to search for (Threat Search and Threat Updates only)
    :return:
    """
    if connection_type is CofenseConnectionType.THREAT_SEARCH:
        url_values = '/threat/search'
    else:
        if connection_type is CofenseConnectionType.THREAT_UPDATES:
            url_values = '/threat/updates'
        else:
            if connection_type is CofenseConnectionType.T3_CEF:
                if threat_type and threat_id:
                    url_values = '/t3/' + threat_type + '/' + threat_id + '/cef'
                else:
                    url_values = '/t3/cef'
            elif connection_type is CofenseConnectionType.T3_STIX:
                if threat_type and threat_id:
                    url_values = '/t3/' + threat_type + '/' + threat_id + '/stix'
            else:
                raise Exception('Connection type not one of THREAT_SEARCH, THREAT_UPDATES, T3_CEF, or T3_STIX')
    url = config.get('cofense', 'base_url') + url_values
    auth = (config.get('cofense', 'user'), config.get('cofense', 'pass'))
    proxies = {}
    if config.has_option('proxy', 'http'):
        proxies['http'] = config.get('proxy', 'http')
    if config.has_option('proxy', 'https'):
        proxies['https'] = config.get('proxy', 'https')
    user_agent = 'Cofense Intelligence Splunk Integration'
    if config.has_option('integration', 'version'):
        user_agent += ' v{}'.format(config.get('integration', 'version'))
    headers = {'User-Agent': user_agent}
    return (
     auth, url, proxies, headers)


def initial_time_window(num_days):
    """
    Return a time window in seconds based on the input number of days.
    """
    now = time.time()
    if PYTHON_MAJOR_VERSION == 3:
        return (
         round(now - num_days * 24 * 60 * 60), round(now))
    return (int(now - num_days * 24 * 60 * 60), int(now))


def date_to_epoch(date):
    """

    :param num_days:
    :return:
    """
    utc_time = time.strptime(date, '%Y-%m-%d')
    epoch_time = timegm(utc_time)
    return (int(epoch_time), int(time.time()))


def read_args(script_description):
    """ Parse all input arguments.
    """
    parser = argparse.ArgumentParser(description=script_description)
    parser.add_argument('-conf', '--config_file', help="Config location. By default, config file is assumed to be in the same directory and named 'config.ini'.", required=False, default='config.ini')
    parser.add_argument('-type', '--threat_type', help="Type of threats to retrieve. Choices are 'all', 'malware', or 'phish'.", required=False, default='all', choices=['all', 'malware', 'phish'])
    return parser.parse_args()


def read_config(config_file):
    """
    Read configuration file.
    """
    if PYTHON_MAJOR_VERSION == 3:
        config = ConfigParser()
    else:
        config = SafeConfigParser()
    config.read(config_file)
    return config


def add_lock(config):
    """
    Create lock file if it does not exit; exit if lock file already exists.
    """
    if config.getboolean('concurrency', 'use') is True:
        lock_file_full_path = config.get('concurrency', 'lock_file')
        try:
            dummy = open(lock_file_full_path)
            LOGGER.warning('File locked: ' + lock_file_full_path + '. This instance will exit.')
            return False
        except (IOError, OSError):
            try:
                with open(lock_file_full_path, 'w+') as (dummy):
                    return True
            except (IOError, OSError):
                LOGGER.error('Could not create lock file at: ' + lock_file_full_path + '. This is most likely a permissions issue.')
                return False

    else:
        return True


def remove_lock_and_exit(config, exit_code=0):
    """
    Remove lock file and exit.
    """
    if config.getboolean('concurrency', 'use') is True:
        lock_file_full_path = config.get('concurrency', 'lock_file')
        os.remove(lock_file_full_path)
        if exit_code == 0:
            LOGGER.warn('Exiting.\n\n')
        else:
            LOGGER.warn('Exiting due to failure.\n\n')
        sys.exit(exit_code)