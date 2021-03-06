# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mcosta/Dropbox/SPICE/SPICE_CROSS_MISSION/spiops/spiops/utils/naif.py
# Compiled at: 2019-01-15 05:16:20
# Size of source mod 2**32: 2869 bytes
from spiops.utils import get_latest_kernel
from spiops.utils import get_sc
import subprocess

def brief(kernel, utc=False):
    utility = 'brief'
    option = '-c'
    skd_path = '/'.join(kernel.split('/')[:-2])
    try:
        lsk = get_latest_kernel('lsk', skd_path, 'naif????.tls')
    except:
        lsk = get_latest_kernel('lsk', skd_path, 'NAIF????.TLS')

    if utc:
        option += ' -utc'
        kernel += ' ' + skd_path + '/lsk/' + lsk
    command_line_process = subprocess.Popen([utility, option, kernel], stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT))
    process_output, _ = command_line_process.communicate()
    return process_output.decode('utf-8')


def ckbrief(kernel, utc=False):
    utility = 'ckbrief'
    option = '-rel -n'
    skd_path = '/'.join(kernel.split('/')[:-2])
    sc = get_sc(kernel)
    try:
        lsk = get_latest_kernel('lsk', skd_path, 'naif????.tls')
    except:
        lsk = get_latest_kernel('lsk', skd_path, 'NAIF????.TLS')

    try:
        sclk = get_latest_kernel('sclk', skd_path, '{}_step_????????.tsc'.format(sc))
    except:
        sclk = get_latest_kernel('lsk', skd_path, '{}_STEP_????????.TSC'.format(sc.upper()))

    try:
        fk = get_latest_kernel('fk', skd_path, '{}_v??.tf'.format(sc))
    except:
        fk = get_latest_kernel('fk', skd_path, '{}_V??.TF'.format(sc.upper()))

    if utc:
        option += ' -utc'
    kernel += ' ' + skd_path + '/lsk/' + lsk
    kernel += ' ' + skd_path + '/sclk/' + sclk
    kernel += ' ' + skd_path + '/fk/' + fk
    command_line_process = subprocess.Popen([utility, option, kernel], stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT))
    process_output, _ = command_line_process.communicate()
    return process_output.decode('utf-8')


def optiks(mkernel, utc=False):
    if 'MEX' in mkernel:
        mission = 'MEX'
    else:
        if 'VEX' in mkernel:
            mission = 'VEX'
        else:
            if 'ROS' in mkernel:
                mission = 'ROS'
            else:
                if 'em16' in mkernel:
                    mission = 'TGO'
                else:
                    if 'bc' in mkernel:
                        mission = 'MPO'
                    else:
                        if 'JUICE' in mkernel:
                            mission = 'JUICE'
                        else:
                            raise ValueError('OPTIKS utility could not run')
    utility = 'optiks'
    option = '-half -units degrees -frame {}_SPACECRAFT -showfovframes'.format(mission)
    if utc:
        option += ' -epoch {}'.format(utc)
    print(option)
    command_line_process = subprocess.Popen([utility, option, mkernel], stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT))
    process_output, _ = command_line_process.communicate()
    return process_output.decode('utf-8')