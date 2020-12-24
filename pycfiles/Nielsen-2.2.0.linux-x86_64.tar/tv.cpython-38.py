# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/nielsen/tv.py
# Compiled at: 2020-05-04 00:36:33
# Size of source mod 2**32: 2810 bytes
"""
Episode title module for Nielsen.
Fetches information from TVmaze.
"""
import logging, requests
from nielsen.config import CONFIG

def select_series--- This code section failed: ---

 L.  14         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'results'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               1
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    28  'to 28'

 L.  16        12  LOAD_FAST                'results'
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  LOAD_STR                 'show'
               20  BINARY_SUBSCR    
               22  LOAD_STR                 'id'
               24  BINARY_SUBSCR    
               26  RETURN_VALUE     
             28_0  COME_FROM            10  '10'

 L.  18        28  LOAD_GLOBAL              print
               30  LOAD_STR                 "Search results for '{0}'"
               32  LOAD_METHOD              format
               34  LOAD_FAST                'series'
               36  CALL_METHOD_1         1  ''
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L.  19        42  LOAD_GLOBAL              enumerate
               44  LOAD_FAST                'results'
               46  CALL_FUNCTION_1       1  ''
               48  GET_ITER         
               50  FOR_ITER            104  'to 104'
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'i'
               56  STORE_FAST               'result'

 L.  20        58  LOAD_GLOBAL              print
               60  LOAD_STR                 '{0}. {1} ({2}) - {3}'
               62  LOAD_METHOD              format
               64  LOAD_FAST                'i'
               66  LOAD_FAST                'result'
               68  LOAD_STR                 'show'
               70  BINARY_SUBSCR    
               72  LOAD_STR                 'name'
               74  BINARY_SUBSCR    

 L.  21        76  LOAD_FAST                'result'
               78  LOAD_STR                 'show'
               80  BINARY_SUBSCR    
               82  LOAD_STR                 'premiered'
               84  BINARY_SUBSCR    

 L.  21        86  LOAD_FAST                'result'
               88  LOAD_STR                 'show'
               90  BINARY_SUBSCR    
               92  LOAD_STR                 'id'
               94  BINARY_SUBSCR    

 L.  20        96  CALL_METHOD_4         4  ''
               98  CALL_FUNCTION_1       1  ''
              100  POP_TOP          
              102  JUMP_BACK            50  'to 50'

 L.  23       104  LOAD_GLOBAL              print
              106  LOAD_STR                 'Other input cancels without selection.'
              108  CALL_FUNCTION_1       1  ''
              110  POP_TOP          

 L.  25       112  SETUP_FINALLY       148  'to 148'

 L.  26       114  LOAD_GLOBAL              int
              116  LOAD_GLOBAL              input
              118  LOAD_STR                 'Select series: '
              120  CALL_FUNCTION_1       1  ''
              122  CALL_FUNCTION_1       1  ''
              124  STORE_FAST               'selection'

 L.  27       126  LOAD_FAST                'results'
              128  LOAD_GLOBAL              int
              130  LOAD_FAST                'selection'
              132  CALL_FUNCTION_1       1  ''
              134  BINARY_SUBSCR    
              136  LOAD_STR                 'show'
              138  BINARY_SUBSCR    
              140  LOAD_STR                 'id'
              142  BINARY_SUBSCR    
              144  POP_BLOCK        
              146  RETURN_VALUE     
            148_0  COME_FROM_FINALLY   112  '112'

 L.  28       148  DUP_TOP          
              150  LOAD_GLOBAL              ValueError
              152  LOAD_GLOBAL              IndexError
              154  LOAD_GLOBAL              EOFError
              156  BUILD_TUPLE_3         3 
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   204  'to 204'
              162  POP_TOP          
              164  STORE_FAST               'e'
              166  POP_TOP          
              168  SETUP_FINALLY       192  'to 192'

 L.  29       170  LOAD_GLOBAL              logging
              172  LOAD_METHOD              error
              174  LOAD_STR                 'Caught exception: %s'
              176  LOAD_FAST                'e'
              178  CALL_METHOD_2         2  ''
              180  POP_TOP          

 L.  30       182  POP_BLOCK        
              184  POP_EXCEPT       
              186  CALL_FINALLY        192  'to 192'
              188  LOAD_CONST               None
              190  RETURN_VALUE     
            192_0  COME_FROM           186  '186'
            192_1  COME_FROM_FINALLY   168  '168'
              192  LOAD_CONST               None
              194  STORE_FAST               'e'
              196  DELETE_FAST              'e'
              198  END_FINALLY      
              200  POP_EXCEPT       
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           160  '160'
              204  END_FINALLY      
            206_0  COME_FROM           202  '202'

Parse error at or near `POP_EXCEPT' instruction at offset 184


def get_series_id(series, interactive=CONFIG.get('Options', 'Interactive')):
    """Return a unique ID for a given series.
        If an ID isn't found in the config, allow the user to select a match from
        search results."""
    series_id = CONFIG.get('IDs', series, fallback=None)
    if not series_id:
        if interactive:
            endpoint = '{0}/search/shows?q={1}'
        else:
            endpoint = '{0}/singlesearch/shows?q={1}'
        endpoint = endpoint.format(CONFIG['Options']['ServiceURI'], series)
        try:
            response = requests.getendpoint
        except IOError as e:
            try:
                logging.error'Unable to retrieve series names.'
                logging.debuge
                exit()
            finally:
                e = None
                del e

        else:
            results = response.json()
            if response.status_code == 200:
                if interactive:
                    series_id = select_series(series, results)
                else:
                    series_id = results['id']
    logging.info("Show ID for '%s': %s", series, series_id)
    CONFIG.set('IDs', series, str(series_id))
    return series_id


def get_episode_title(season, episode, series_id=None, series=None):
    """Return the episode title using the series name or ID, season, and
        episode number."""
    if series_id is None:
        if series:
            series_id = get_series_id(series)
    if series_id:
        logging.info'Series ID: %s, Season: %s, Episode: %s'series_idseasonepisode
        try:
            response = requests.get'{0}shows/{1}/episodebynumber?season={2}&number={3}'.formatCONFIG['Options']['ServiceURI']series_idseasonepisode
            title = response.json()['name']
            logging.info('Title: %s', title)
            return title
            except IOError as e:
            try:
                logging.error'Unable to retrieve episode title.'
                logging.debuge
            finally:
                e = None
                del e

    return str()