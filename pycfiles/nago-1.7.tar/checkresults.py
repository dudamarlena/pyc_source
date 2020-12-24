# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/nago/nago/extensions/checkresults.py
# Compiled at: 2013-11-27 07:41:53
""" Get and post nagios checkresults between nago instances

This extension allows to get status data from a local nagios server.

Also pushing checkresults into a local nagios server, therefore updating nagios status.
"""
from pynag.Parsers import mk_livestatus, config
import time, os, os.path, tempfile
from nago.core import nago_access
import nago.extensions.settings

@nago_access()
def get():
    """ Get all nagios status information from a local nagios instance
    """
    livestatus = mk_livestatus()
    hosts = livestatus.get_hosts()
    services = livestatus.get_services()
    result = {}
    result['hosts'] = hosts
    result['services'] = services
    return result


@nago_access()
def post(hosts=None, services=None, check_existance=True, create_services=True, create_hosts=False):
    """ Puts a list of hosts into local instance of nagios checkresults
    Arguments:
      hosts               -- list of dicts, like one obtained from get_checkresults
      services            -- list of dicts, like one obtained from get_checkresults
      check_existance     -- If True, check (and log) if objects already exist before posting
      create_services -- If True, autocreate non-existing services (where the host already exists)
      create_hosts    -- If True, autocreate non-existing hosts
    """
    nagios_config = config()
    nagios_config.parse_maincfg()
    check_result_path = nagios_config.get_cfg_value('check_result_path')
    fd, filename = tempfile.mkstemp(prefix='c', dir=check_result_path)
    if not hosts:
        hosts = []
    if not services:
        services = []
    if check_existance:
        checkresults_overhaul(hosts, services, create_services=create_services, create_hosts=create_hosts)
    checkresults = '### Active Check Result File Made by Nago ###\n'
    checkresults += 'file_time=%s' % int(time.time())
    checkresults = ''
    for host in hosts:
        checkresults += _format_checkresult(**host)

    for service in services:
        checkresults += _format_checkresult(**service)

    os.write(fd, checkresults)
    os.close(fd)
    os.chmod(filename, 420)
    file('%s.ok' % filename, 'w')


@nago_access()
def send(remote_host=None):
    """ Send local nagios data to a remote nago instance """
    my_data = get()
    if not remote_host:
        remote_host = nago.extensions.settings.get('server')
    remote_node = nago.core.get_node(remote_host)
    remote_node.send_command('checkresults', 'post', **my_data)
    return 'checkresults sent to %s' % remote_host


def checkresults_overhaul(hosts, services, create_services, create_hosts):
    """ Iterates through hosts and services, and filters out those who do not exist in our local monitoring core

    If create_services or create_hosts are defined, then
    """
    pass


def _format_checkresult(**kwargs):
    """ Returns a string in a nagios "checkresults" compatible format """
    o = {}
    o['check_type'] = '1'
    o['check_options'] = '0'
    o['scheduled_check'] = '1'
    o['reschedule_check'] = '1'
    o['latency'] = '0.0'
    o['start_time'] = '%5f' % time.time()
    o['finish_time'] = '%5f' % time.time()
    o['early_timeout'] = '0'
    o['exited_ok'] = '1'
    o['long_plugin_output'] = ''
    o['performance_data'] = ''
    o.update(locals())
    o.update(kwargs)
    del o['kwargs']
    del o['o']
    template = _host_check_result
    for k, v in o.items():
        if isinstance(v, basestring) and '\n' in v:
            o[k] = v.replace('\n', '\\n')

    if 'name' in o and 'host_name' not in o:
        o['host_name'] = o['name']
    if 'state' in o and 'return_code' not in o:
        o['return_code'] = o['state']
    if 'description' in o and 'service_description' not in o:
        o['service_description'] = o['description']
    if not o['performance_data'] and 'perf_data' in o:
        o['performance_data'] = o['perf_data']
    if 'service_description' in o:
        template += 'service_description={service_description}\n'
    if not o['performance_data'].endswith('\\n'):
        o['performance_data'] += '\\n'
    return template.format(**o) + '\n'


_host_check_result = '\nhost_name={host_name}\ncheck_type={check_type}\ncheck_options=0\nscheduled_check=1\nreschedule_check=1\nlatency=0.0\nstart_time={start_time}\nfinish_time={finish_time}\nearly_timeout=0\nexited_ok=1\nreturn_code={return_code}\noutput={plugin_output}{long_plugin_output} | {performance_data}\n'