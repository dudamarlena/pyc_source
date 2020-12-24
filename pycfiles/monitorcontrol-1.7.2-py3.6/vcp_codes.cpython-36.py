# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monitorcontrol/vcp/vcp_codes.py
# Compiled at: 2020-02-29 14:25:34
# Size of source mod 2**32: 4188 bytes
from typing import Type

class VCPCode:
    __doc__ = '\n    Virtual Control Panel code.  Simple container for the control\n    codes defined by the VESA Monitor Control Command Set (MCSS).\n\n    This should be used by getting the code from\n    :py:meth:`get_vcp_code_definition()`\n\n    Args:\n        definition: code definition dictionary\n    '
    _VCP_CODE_DEFINTIONS = {'image_factory_default':{'name':'restore factory default image', 
      'value':4, 
      'type':'wo', 
      'function':'nc'}, 
     'image_luminance':{'name':'image luminance', 
      'value':16, 
      'type':'rw', 
      'function':'c'}, 
     'image_contrast':{'name':'image contrast', 
      'value':18, 
      'type':'rw', 
      'function':'c'}, 
     'active_control':{'name':'active control', 
      'value':82, 
      'type':'ro', 
      'function':'nc'}, 
     'image_orientation':{'name':'image orientation', 
      'value':170, 
      'type':'ro', 
      'function':'nc'}, 
     'display_power_mode':{'name':'display power mode', 
      'value':214, 
      'type':'rw', 
      'function':'nc'}}

    def __init__(self, definition: dict):
        self.definition = definition

    def __repr__(self) -> str:
        return f"virtual control panel code definition. value: {self.value} type: {self.type}function: {self.function}"

    @property
    def name(self) -> int:
        """ Friendly name of the code. """
        return self.definition['name']

    @property
    def value(self) -> int:
        """ Value of the code. """
        return self.definition['value']

    @property
    def type(self) -> str:
        """ Type of the code. """
        return self.definition['type']

    @property
    def function(self) -> str:
        """ Function of the code. """
        return self.definition['function']

    @property
    def readable(self) -> bool:
        """ Returns true if the code can be read. """
        if self.type == 'wo':
            return False
        else:
            return True

    @property
    def writeable(self) -> bool:
        """ Returns true if the code can be written. """
        if self.type == 'ro':
            return False
        else:
            return True


def get_vcp_code_definition(name: str) -> Type[VCPCode]:
    """
    Gets a code from the dictionary.

    Args:
        name: name of the VCP code definition

    Returns:
        Associated :py:meth:`VCPCode`

    Raises:
        KeyError: unable to locate VCP code
    """
    return VCPCode(VCPCode._VCP_CODE_DEFINTIONS[name])