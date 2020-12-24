# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/honza/code/my/physt/tests/../physt/io/json.py
# Compiled at: 2019-08-28 04:52:53
# Size of source mod 2**32: 1677 bytes
"""JSON I/O"""
import json
from typing import Optional, Union
from physt.io import CURRENT_VERSION, create_from_dict, VersionError
from physt.histogram_base import HistogramBase
from physt.histogram_collection import HistogramCollection
COMPATIBLE_VERSION = '0.3.20'
COLLECTION_COMPATIBLE_VERSION = '0.4.5'

def save_json(histogram: Union[(HistogramBase, HistogramCollection)], path: Optional[str]=None, **kwargs) -> str:
    """Save histogram to JSON format.

    Parameters
    ----------
    histogram : Any histogram
    path : If set, also writes to the path.

    Returns
    -------
    json : The JSON representation of the histogram
    """
    data = histogram.to_dict()
    data['physt_version'] = CURRENT_VERSION
    if isinstance(histogram, HistogramBase):
        data['physt_compatible'] = COMPATIBLE_VERSION
    else:
        if isinstance(histogram, HistogramCollection):
            data['physt_compatible'] = COLLECTION_COMPATIBLE_VERSION
        else:
            raise TypeError('Cannot save unknown type: {0}'.format(type(histogram)))
    text = (json.dumps)(data, **kwargs)
    if path:
        with open(path, 'w', encoding='utf-8') as (f):
            f.write(text)
    return text


def load_json--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'path'
                4  LOAD_STR                 'r'
                6  LOAD_FAST                'encoding'
                8  LOAD_CONST               ('encoding',)
               10  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               12  SETUP_WITH           44  'to 44'
               14  STORE_FAST               'f'

 L.  46        16  LOAD_FAST                'f'
               18  LOAD_METHOD              read
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'text'

 L.  47        24  LOAD_GLOBAL              parse_json
               26  LOAD_FAST                'text'
               28  CALL_FUNCTION_1       1  ''
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  POP_FINALLY           0  ''
               42  RETURN_VALUE     
             44_0  COME_FROM_WITH       12  '12'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 32


def parse_json(text: str, encoding: str='utf-8') -> HistogramBase:
    """Create histogram from a JSON string."""
    data = json.loads(text, encoding=encoding)
    return create_from_dict(data, format_name='JSON')