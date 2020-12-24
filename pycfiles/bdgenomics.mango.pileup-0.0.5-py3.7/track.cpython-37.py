# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/pileup/track.py
# Compiled at: 2019-08-09 11:11:10
# Size of source mod 2**32: 5152 bytes
"""
=====
Track
=====
.. currentmodule:: bdgenomics.mango.pileup.track

Tracks specify what visualization will be drawn. 

.. autosummary::
    :toctree: _generate/

    Track
    track_to_json
    track_from_json
    tracks_to_json
    tracks_from_json
"""
from traitlets import TraitType
import six
from .sources import *

class Track(TraitType):
    __doc__ = 'A trait for a pileupTrack, requires a viz string of (coverage, pileup, features, variants, genome, genes, scale, or location)\n    and a DataSource.\n    '
    info_text = 'a pileup track (requires names for pileup.viz, pileup.source, pileup.source, and optional pileup.label)'
    viz = None
    source = None
    sourceOptions = None
    label = None

    def __init__(self, **kwargs):
        """ Initializes track. 

        Args:
            :param kwargs: Should contain viz, optional source, optional label.

        """
        for key, value in kwargs.items():
            if key == 'viz':
                if value not in vizNames.keys():
                    raise RuntimeError('Invalid track visualization %s. Available tracks include %s' % (value, vizNames.keys()))
                setattr(self, key, value)
            elif key == 'source':
                if value.name not in vizNames[kwargs['viz']]:
                    raise RuntimeError('Invalid data source %s for track %s' % (
                     value.name, kwargs['viz']))
                self.source = kwargs['source'].name
                self.sourceOptions = kwargs['source'].dict_
            else:
                setattr(self, key, value)


def track_to_json(pyTrack, manager):
    """Serialize a Track.
    Attributes of this dictionary are to be passed to the JavaScript Date
    constructor.

    Args:
        :param Track: Track object
        :param any: manager. Used for widget serialization.

    Returns:
        dict of Track elements (viz, source, sourceOptions and label)

    """
    if pyTrack is None:
        return
    return dict(viz=(pyTrack.viz),
      source=(pyTrack.source),
      sourceOptions=(pyTrack.sourceOptions),
      label=(pyTrack.label))


def track_from_json(js, manager):
    """Deserialize a Track from JSON.

    Args:
        :param (str): json for Track containing viz, source, sourceOptions and label
        :param (any): manager. Used for widget serialization.

    Returns:
        Track: pileup Track built from json

    """
    if js is None:
        return
    return Track(viz=(js['viz']),
      source=(sourceNames[js['source']]),
      sourceOptions=(js['sourceOptions']),
      label=(js['label']))


def tracks_to_json(pyTracks, manager):
    """Serialize a Python date object.
    Attributes of this dictionary are to be passed to the JavaScript Date
    constructor.

    Args:
        :param (List): List of Tracks
        :param (any): manager. Used for widget serialization.

    Returns:
        List of dict of Track elements (viz, source, sourceOptions and label)

    """
    if pyTracks is None:
        return
    return [track_to_json(x, manager) for x in pyTracks]


def tracks_from_json(js, manager):
    """Deserialize a list of Tracks from JSON.

    Args:
        :param (str): json for list of Tracks containing viz, source, sourceOptions and label
        :param (any): manager. Used for widget serialization.

    Returns:
        List: List of pileup Track built from json

    """
    if js is None:
        return
    return [track_from_json(j, manager) for j in js]


track_serialization = {'from_json':track_from_json, 
 'to_json':track_to_json}
track_list_serialization = {'from_json':tracks_from_json, 
 'to_json':tracks_to_json}