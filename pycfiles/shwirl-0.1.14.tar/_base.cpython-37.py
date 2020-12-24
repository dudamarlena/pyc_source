# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/scene/cameras/_base.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 1263 bytes
from .base_camera import BaseCamera
from .perspective import PerspectiveCamera
from .panzoom import PanZoomCamera
from .arcball import ArcballCamera
from .turntable import TurntableCamera
from .fly import FlyCamera

def make_camera(cam_type, *args, **kwargs):
    """ Factory function for creating new cameras using a string name.

    Parameters
    ----------
    cam_type : str
        May be one of:

            * 'panzoom' : Creates :class:`PanZoomCamera`
            * 'turntable' : Creates :class:`TurntableCamera`
            * None : Creates :class:`Camera`

    Notes
    -----
    All extra arguments are passed to the __init__ method of the selected
    Camera class.
    """
    cam_types = {None: BaseCamera}
    for camType in (BaseCamera, PanZoomCamera, PerspectiveCamera,
     TurntableCamera, FlyCamera, ArcballCamera):
        cam_types[camType.__name__[:-6].lower()] = camType

    try:
        return (cam_types[cam_type])(*args, **kwargs)
    except KeyError:
        raise KeyError('Unknown camera type "%s". Options are: %s' % (
         cam_type, cam_types.keys()))