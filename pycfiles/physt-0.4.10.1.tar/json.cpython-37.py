# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
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


def load_json(path: str, encoding: str='utf-8') -> HistogramBase:
    """Load histogram from a JSON file."""
    with open(path, 'r', encoding=encoding) as (f):
        text = f.read()
        return parse_json(text)


def parse_json(text: str, encoding: str='utf-8') -> HistogramBase:
    """Create histogram from a JSON string."""
    data = json.loads(text, encoding=encoding)
    return create_from_dict(data, format_name='JSON')