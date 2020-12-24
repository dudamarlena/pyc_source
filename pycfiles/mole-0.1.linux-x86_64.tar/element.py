# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/element.py
# Compiled at: 2012-07-13 03:38:02
from mole.helper import AttrDict

class Element(AttrDict):
    """Models an element.
    """

    @classmethod
    def from_config(cls, config, base):
        """Create a new :class:`Element` object from a configuration object
        and a base ones (which acts as default values).

        :param `config`: A :class:`MoleConfig` object which contains
            a configuration object.
        :param `base`: A :class:`MoleConfig` object which contains default
            values for the element.
        """
        for element, values in config:
            x = Element()
            for key in values:
                if key in base:
                    if values[key] in base[key]:
                        x[key] = base[key][values[key]]

            yield (
             element, x)