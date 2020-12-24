# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynomer/nomer_utils.py
# Compiled at: 2019-12-06 12:38:03
# Size of source mod 2**32: 1326 bytes
import logging, subprocess, json, sys

def get_nomer_match_cmd(id='', name='', cmd='append', matcher='globi-taxon-cache', properties=None, output_format=None):
    if id == '':
        if name == '':
            raise ValueError('Id and name cannot be empty strings')
    query = "'{}\\t{}'".format(id, name)
    cmd = ' '.join(['echo -e', query, '|', 'nomer', cmd, matcher])
    if properties:
        cmd = ' '.join([cmd, '-p', properties])
    if output_format:
        cmd = ' '.join([cmd, '-o', output_format])
    return cmd


def get_nomer_simple_cmd(cmd='version', verbose=None, properties=None, output_format=None):
    cmd = ' '.join(['nomer', cmd])
    if properties:
        cmd = ' '.join([cmd, '-p', properties])
    if output_format:
        cmd = ' '.join([cmd, '-o', output_format])
    if verbose:
        cmd = ' '.join([cmd, '-v', verbose])
    return cmd


def get_docker_cmd(nomer_cmd):
    return 'docker run --rm nomer-docker {}'.format(nomer_cmd)


def run_nomer(nomer_cmd):
    docker_cmd = get_docker_cmd(nomer_cmd)
    p = subprocess.Popen(docker_cmd,
      stdout=(subprocess.PIPE), stderr=(subprocess.DEVNULL), shell=True)
    result = p.communicate()[0].decode('utf8')
    if result:
        return result.strip('\n')