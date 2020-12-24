# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/inspector/inspectors/agent_info.py
# Compiled at: 2019-02-11 13:08:11
# Size of source mod 2**32: 612 bytes
import pkg_resources
from mercury_agent.inspector.inspectors import expose

@expose('agent_info')
def agent_inspector():
    _info = {'agent_version':pkg_resources.get_distribution('mercury-agent').version, 
     'mercury_version':pkg_resources.get_distribution('mercury-core').version}
    try:
        with open('/etc/hostname') as (fp):
            hostname = fp.read().strip()
    except (IOError, OSError):
        hostname = None

    _info['hostname'] = hostname
    return _info


if __name__ == '__main__':
    from pprint import pprint
    pprint(agent_inspector())