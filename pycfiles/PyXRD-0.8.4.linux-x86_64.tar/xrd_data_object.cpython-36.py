# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/xrd_data_object.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2229 bytes
from io import StringIO
from ..data_object import DataObject
from pyxrd.generic.utils import not_none

class XRDDataObject(DataObject):
    __doc__ = '\n        A generic class holding all the information retrieved from an XRD data\n        file using an XRD-parser class.\n    '
    name = None
    date = None
    twotheta_min = None
    twotheta_max = None
    twotheta_count = None
    twotheta_step = None
    target_type = None
    alpha1 = None
    alpha2 = None
    alpha_average = None
    beta = None
    alpha_factor = None
    radius = None
    soller1 = None
    soller2 = None
    divergence = None
    data = None

    def create_gon_file(self):
        output = '        {\n            "type": "Goniometer", \n            "properties": {\n                "radius": %(radius)f, \n                "divergence": %(divergence)f, \n                "soller1": %(soller1)f, \n                "soller2": %(soller2)f, \n                "min_2theta": %(twotheta_min)f, \n                "max_2theta": %(twotheta_max)f, \n                "steps": %(twotheta_count)f, \n                "wavelength": %(alpha_average)f, \n                "has_ads": false, \n                "ads_fact": 1.0, \n                "ads_phase_fact": 1.0, \n                "ads_phase_shift": 0.0, \n                "ads_const": 0.0\n            }\n        }' % dict(radius=(float(not_none(self.radius, 25))),
          divergence=(float(not_none(self.divergence, 0.5))),
          soller1=(float(not_none(self.soller1, 2.5))),
          soller2=(float(not_none(self.soller2, 2.5))),
          twotheta_min=(float(not_none(self.twotheta_min, 3.0))),
          twotheta_max=(float(not_none(self.twotheta_max, 45.0))),
          twotheta_count=(float(not_none(self.twotheta_count, 2500))),
          alpha_average=(float(not_none(self.alpha_average, 0.154056))))
        f = StringIO(output)
        f.flush()
        return f