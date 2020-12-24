# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\service\_docker_utils.py
# Compiled at: 2017-09-20 13:50:34
"""
Utilities to work with docker.

"""
import base64, json, os, traceback, docker, re
from azure.cli.core.util import CLIError

def get_docker_client(verb=False):
    try:
        client = docker.from_env()
    except docker.errors.DockerException as exc:
        msg = ('Failed to create Docker client: {}').format(exc)
        raise CLIError(msg)

    try:
        client.containers.list()
    except docker.errors.APIError as exc:
        api_regex = 'server API version: (?P<server_version>[^\\)]+)'
        s = re.search(api_regex, str(exc))
        if s:
            client = docker.DockerClient()
            client.api = docker.APIClient(base_url='unix://var/run/docker.sock', version=s.group('server_version'))
        else:
            if verb:
                print traceback.format_exc()
            raise CLIError('Docker not configured properly. Please check you docker installation.')
    except Exception as ex:
        if verb:
            print traceback.format_exc()
        raise CLIError('Docker not configured properly. Please check you docker installation.')

    return client