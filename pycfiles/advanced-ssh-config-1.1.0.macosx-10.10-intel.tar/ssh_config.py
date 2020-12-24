# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/ssh_config.py
# Compiled at: 2015-03-20 16:29:12
import re
PROXY_REGEX = re.compile('^(proxycommand)\\s*=*\\s*(.*)', re.I)

def parse_ssh_config(file_obj):
    """
    Read an OpenSSH config from the given file object.

    Small adaptation of the paramiko.config.SSH_Config.parse method
    https://github.com/paramiko/paramiko/blob/master/paramiko/config.py

    @param file_obj: a file-like object to read the config file from
    @type file_obj: file
    """
    hosts = {}
    host = {'host': ['*'], 'config': {}}
    for line in file_obj:
        line = line.rstrip('\n').lstrip()
        if line == '' or line[0] == '#':
            continue
        if '=' in line:
            if line.lower().strip().startswith('proxycommand'):
                match = PROXY_REGEX.match(line)
                key, value = match.group(1).lower(), match.group(2)
            else:
                (key, value) = line.split('=', 1)
                key = key.strip().lower()
        else:
            i = 0
            while i < len(line) and not line[i].isspace():
                i += 1

            if i == len(line):
                raise Exception('Unparsable line: %r' % line)
            key = line[:i].lower()
            value = line[i:].lstrip()
        if key == 'host':
            hosts[host['host'][0]] = host['config']
            value = value.split()
            host = {key: value, 'config': {}}
        elif key in ('identityfile', 'localforward', 'remoteforward'):
            if key in host['config']:
                host['config'][key].append(value)
            else:
                host['config'][key] = [
                 value]
        elif key not in host['config']:
            host['config'].update({key: value})

    hosts[host['host'][0]] = host['config']
    return hosts