# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ethankeller/edx/xblock_development/onshape_xblock/onshape_xblock/checks/check_element_type.py
# Compiled at: 2019-05-22 15:26:23
from onshape_xblock.check_imports import *

class CheckElementType(CheckBase):
    """An element type check

    This element type check checks whether or not the specified Onshape element is the correct element type. """
    failure_message_template = 'The element you passed in is a {{ actual_element_type }} rather than the expected {{ expected_element_type }}.'
    success_message_template = 'Element type check passed!'
    additional_form_properties = {'expected_element_type': {'title': 'The expected element type.', 
                                 'type': 'string', 
                                 'default': 'List', 
                                 'enum': [
                                        'PartStudio',
                                        'Assembly',
                                        'Drawing',
                                        'Blob'], 
                                 'uniqueItems': True}}

    def __init__(self, expected_element_type=None, **kwargs):
        super(CheckElementType, self).__init__(name='Check Element Type', **kwargs)

    def execute_check(self):
        part_id = self.get_part_id(self.part_number)
        mass_properties = self.get_mass_properties(part_id)
        self.volume = quantify(mass_properties.bodies['-all-'].volume[0], default_units=u.m ** 3)
        self.passed = self.min_volume < self.volume < self.max_volume