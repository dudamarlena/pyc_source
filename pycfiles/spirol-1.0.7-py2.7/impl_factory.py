# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spirol/impl_factory.py
# Compiled at: 2015-01-09 08:35:26
from spirol.errors import UnknownImplementation, NonSpirolInterface
from spirol.impls import spirol_interface
from spirol.impls.spirol_array_iter import spirol_array_iter
from spirol.utils import SpirolType

def spirol_factory(spirol_type):
    """
    A factory the return <type>spirol iterators.
    :param spirol_type: str
    :see: 'SpirolType'.
    :return:
    """
    _mapping = {SpirolType.SPIRAL_CIRCULAR_OUTSIDE_IN: spirol_array_iter}
    try:
        interface = _mapping[spirol_type]
    except KeyError:
        raise UnknownImplementation(spirol_type)
    else:
        if spirol_interface not in interface.__bases__:
            raise NonSpirolInterface(interface)
        return interface


if __name__ == '__main__':
    pass