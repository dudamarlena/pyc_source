# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/utils/credentials.py
# Compiled at: 2020-05-13 17:11:01
# Size of source mod 2**32: 4007 bytes
"""
Package for interacting with the PredictiveGrid credentials file.
"""
import os, yaml
from functools import wraps
from btrdb.exceptions import ProfileNotFound, CredentialsFileNotFound
CONFIG_DIR = '.predictivegrid'
CREDENTIALS_FILENAME = 'credentials.yaml'
CREDENTIALS_PATH = os.path.join(os.environ['HOME'], CONFIG_DIR, CREDENTIALS_FILENAME)

def filter_none(f):
    """
    decorator for removing dict items with None as value
    """

    @wraps(f)
    def inner(*args, **kwargs):
        return {v:k for k, v in f(*args, **kwargs).items() if v is not None if v is not None}

    return inner


def load_credentials_from_file--- This code section failed: ---

 L.  54         0  SETUP_FINALLY        48  'to 48'

 L.  55         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              CREDENTIALS_PATH
                6  LOAD_STR                 'r'
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           38  'to 38'
               12  STORE_FAST               'stream'

 L.  56        14  LOAD_GLOBAL              yaml
               16  LOAD_METHOD              safe_load
               18  LOAD_FAST                'stream'
               20  CALL_METHOD_1         1  ''
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       10  '10'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      
               44  POP_BLOCK        
               46  JUMP_FORWARD         98  'to 98'
             48_0  COME_FROM_FINALLY     0  '0'

 L.  57        48  DUP_TOP          
               50  LOAD_GLOBAL              FileNotFoundError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    96  'to 96'
               56  POP_TOP          
               58  STORE_FAST               'exc'
               60  POP_TOP          
               62  SETUP_FINALLY        84  'to 84'

 L.  58        64  LOAD_GLOBAL              CredentialsFileNotFound
               66  LOAD_STR                 'Cound not find `{}`'
               68  LOAD_METHOD              format
               70  LOAD_GLOBAL              CREDENTIALS_PATH
               72  CALL_METHOD_1         1  ''
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'exc'
               78  RAISE_VARARGS_2       2  'exception instance with __cause__'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_FINALLY    62  '62'
               84  LOAD_CONST               None
               86  STORE_FAST               'exc'
               88  DELETE_FAST              'exc'
               90  END_FINALLY      
               92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
             96_0  COME_FROM            54  '54'
               96  END_FINALLY      
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            46  '46'

Parse error at or near `ROT_TWO' instruction at offset 24


@filter_none
def credentials_by_profile(name=None):
    """
    Returns the BTrDB connection information (as dict) for a requested profile
    from the user's credentials file.

    Parameters
    ----------
    name: str
        The name of the profile to retrieve

    Returns
    -------
    dict
        A dictionary of the requested profile's connection information

    Raises
    ------
    CredentialsFileNotFound
        The expected credentials file `~/.predictivegrid/credentials.yaml` could not be found.

    ProfileNotFound
        The requested profile could not be found in the credentials file
    """
    if not name:
        name = os.environ.get('BTRDB_PROFILE', 'default')
    creds = load_credentials_from_file()
    if name not in creds.keys():
        if name == 'default':
            return {}
        raise ProfileNotFound('Profile `{}` not found in credentials file.'.formatname)
    fragment = creds[name].get('btrdb', {})
    if 'api_key' in fragment:
        fragment['apikey'] = fragment.pop'api_key'
    return fragment


@filter_none
def credentials_by_env():
    """
    Returns the BTrDB connection information (as dict) using BTRDB_ENDPOINTS and
    BTRDB_API_KEY ENV variables.

    Returns
    -------
    dict
        A dictionary containing connection information
    """
    return {'endpoints':os.environ.get('BTRDB_ENDPOINTS', None), 
     'apikey':os.environ.get('BTRDB_API_KEY', None)}


def credentials(endpoints=None, apikey=None):
    """
    Returns the BTrDB connection information (as dict) for a requested profile
    from the user's credentials file.

    Parameters
    ----------
    name: str
        The name of the profile to retrieve

    Returns
    -------
    dict
        A dictionary of the requested profile's connection information

    """
    creds = {}
    credentials_by_arg = filter_none(lambda : {'endpoints':endpoints,  'apikey':apikey})
    pipeline = [credentials_by_env, credentials_by_arg]
    if os.path.existsCREDENTIALS_PATH:
        pipeline.insert(0, credentials_by_profile)
    [creds.updatefunc() for func in pipeline]
    return creds