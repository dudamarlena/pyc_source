# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-6brxc_kc/websockets/websockets/typing.py
# Compiled at: 2020-03-24 13:42:06
# Size of source mod 2**32: 1305 bytes
from typing import List, NewType, Optional, Tuple, Union
__all__ = [
 'Data', 'Origin', 'ExtensionHeader', 'ExtensionParameter', 'Subprotocol']
Data = Union[(str, bytes)]
Data__doc__ = '\nTypes supported in a WebSocket message:\n\n- :class:`str` for text messages\n- :class:`bytes` for binary messages\n\n'
try:
    Data.__doc__ = Data__doc__
except AttributeError:
    pass

Origin = NewType('Origin', str)
Origin.__doc__ = 'Value of a Origin header'
ExtensionName = NewType('ExtensionName', str)
ExtensionName.__doc__ = 'Name of a WebSocket extension'
ExtensionParameter = Tuple[(str, Optional[str])]
ExtensionParameter__doc__ = 'Parameter of a WebSocket extension'
try:
    ExtensionParameter.__doc__ = ExtensionParameter__doc__
except AttributeError:
    pass

ExtensionHeader = Tuple[(ExtensionName, List[ExtensionParameter])]
ExtensionHeader__doc__ = 'Item parsed in a Sec-WebSocket-Extensions header'
try:
    ExtensionHeader.__doc__ = ExtensionHeader__doc__
except AttributeError:
    pass

Subprotocol = NewType('Subprotocol', str)
Subprotocol.__doc__ = 'Items parsed in a Sec-WebSocket-Protocol header'