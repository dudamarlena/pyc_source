# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/configuration_parameters/all_configuration_parameters.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 462 bytes
from exactly_lib.help.entities.configuration_parameters.objects import actor, test_case_status, hds_act_directory, hds_case_directory, timeout

def all_configuration_parameters() -> list:
    """
    :rtype [ConfigurationParameterDocumentation]
    """
    return [
     actor.DOCUMENTATION,
     test_case_status.DOCUMENTATION,
     hds_case_directory.DOCUMENTATION,
     hds_act_directory.DOCUMENTATION,
     timeout.DOCUMENTATION]