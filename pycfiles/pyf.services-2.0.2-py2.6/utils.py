# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/controllers/utils.py
# Compiled at: 2010-05-21 08:57:50
from pyf.services.model import DBSession, Tube, Descriptor

def tube_select_getter(needs_source=None):

    def get_tubes_id_name():
        tubes = DBSession.query(Tube)
        if needs_source is not None:
            tubes = tubes.filter(Tube.needs_source == needs_source)
        tubes = tubes.order_by(Tube.display_name)
        return [ (tube.id, tube.display_name) for tube in tubes ]

    return get_tubes_id_name


def descriptor_select_getter(needs_source=None):
    descriptors = DBSession.query(Descriptor)
    descriptors = descriptors.order_by(Descriptor.display_name)
    return [ (descriptor.id, descriptor.display_name) for descriptor in descriptors ]