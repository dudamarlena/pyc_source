# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeaubin/ge/pypi/pypi/genielibs/pkgs/sdk-pkg/src/genie/libs/sdk/genie_yamls/__init__.py
# Compiled at: 2019-08-26 20:40:03
# Size of source mod 2**32: 1688 bytes
import os
curr_dir = os.path.dirname(os.path.abspath(__file__))
trigger_datafiles = {}
trigger_datafiles['main'] = os.path.join(curr_dir, 'trigger_datafile.yaml')
trigger_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/trigger_datafile_nxos.yaml')
trigger_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/trigger_datafile_iosxe.yaml')
trigger_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/trigger_datafile_xr.yaml')
trigger_datafiles['junos'] = os.path.join(curr_dir, 'junos/trigger_datafile_junos.yaml')
trigger_datafiles['virl'] = os.path.join(curr_dir, 'virl/trigger_datafile_virl.yaml')
verification_datafiles = {}
verification_datafiles['main'] = os.path.join(curr_dir, 'verification_datafile.yaml')
verification_datafiles['nxos'] = os.path.join(curr_dir, 'nxos/verification_datafile_nxos.yaml')
verification_datafiles['iosxe'] = os.path.join(curr_dir, 'iosxe/verification_datafile_iosxe.yaml')
verification_datafiles['iosxr'] = os.path.join(curr_dir, 'iosxr/verification_datafile_xr.yaml')
verification_datafiles['junos'] = os.path.join(curr_dir, 'junos/verification_datafile_junos.yaml')
subsection_datafile = os.path.join(curr_dir, 'subsection_datafile.yaml')
pts_datafile = os.path.join(curr_dir, 'pts_datafile.yaml')

def datafile(mode, os='main'):
    if mode == 'trigger':
        return trigger_datafiles[os]
    else:
        if mode == 'verification':
            return verification_datafiles[os]
        if mode == 'subsection':
            return subsection_datafile
        if mode == 'pts':
            return pts_datafile
    raise Exception('{m} is not a valid datafile mode - valid: trigger, verification, subsection pts'.format(m=mode))