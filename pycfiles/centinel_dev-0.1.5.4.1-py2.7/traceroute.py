# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/primitives/traceroute.py
# Compiled at: 2015-10-26 01:10:45
import copy, logging, threading, time, trparse
from sys import platform
from centinel import command

def traceroute(domain, method='udp', cmd_arguments=None, external=None, log_prefix=''):
    """This function uses centinel.command to issue
    a traceroute command, wait for it to finish execution and
    parse the results out to a dictionary.

    Params:
    domain-        the domain to be queried
    method-        the packet type used for traceroute, ICMP by default
    cmd_arguments- the list of arguments that need to be passed
                   to traceroute.

    """
    _cmd_arguments = []
    logging.debug('%sRunning traceroute for %s using %s probes.' % (
     log_prefix, domain, method))
    if cmd_arguments is not None:
        _cmd_arguments = copy.deepcopy(cmd_arguments)
    if method == 'tcp':
        if platform in ('linux', 'linux2'):
            _cmd_arguments.append('-T')
        elif platform == 'darwin':
            _cmd_arguments.append('-P')
            _cmd_arguments.append('tcp')
    elif method == 'udp':
        if platform in ('linux', 'linux2'):
            _cmd_arguments.append('-U')
        elif platform == 'darwin':
            _cmd_arguments.append('-P')
            _cmd_arguments.append('udp')
    elif method == 'icmp':
        if platform in ('linux', 'linux2'):
            _cmd_arguments.append('-I')
        elif platform == 'darwin':
            _cmd_arguments.append('-P')
            _cmd_arguments.append('icmp')
    cmd = [
     'traceroute'] + _cmd_arguments + [domain]
    caller = command.Command(cmd, _traceroute_callback)
    caller.start()
    message = caller.started or ''
    if caller.exception is not None:
        if 'No such file or directory' in caller.exception:
            message = 'traceroute not found or not installed'
        else:
            message = 'traceroute thread threw an exception: %s'(caller.exception)
    else:
        if 'enough privileges' in caller.notifications:
            message = 'not enough privileges'
        else:
            if 'not known' in caller.notifications:
                message = 'name or service not known'
            else:
                message = caller.notifications
            results = {}
            results['domain'] = domain
            results['method'] = method
            results['error'] = message
            if external is not None and type(external) is dict:
                external[domain] = results
            return results
        forcefully_terminated = False
        timeout = 60
        start_time = time.time()
        while caller.thread.isAlive():
            if time.time() - start_time > timeout:
                caller.stop()
                forcefully_terminated = True
                break
            time.sleep(1)

        time_elapsed = int(time.time() - start_time)
        output_string = caller.notifications
        try:
            parsed_output = trparse.loads(output_string)
        except Exception as exc:
            results = {}
            results['domain'] = domain
            results['method'] = method
            results['error'] = str(exc)
            results['raw'] = output_string
            if external is not None and type(external) is dict:
                external[domain] = results
            return results

        hops = list()
        for hop in parsed_output.hops:
            hop_json = {'index': hop.idx, 'asn': hop.asn}
            probes_json = []
            for probe in hop.probes:
                probes_json.append({'name': probe.name, 'ip': probe.ip, 
                   'rtt': probe.rtt, 
                   'anno': probe.anno})

            hop_json['probes'] = probes_json
            hops.append(hop_json)

    results = {}
    results['dest_name'] = parsed_output.dest_name
    results['dest_ip'] = parsed_output.dest_ip
    results['method'] = method
    results['hops'] = hops
    results['forcefully_terminated'] = forcefully_terminated
    results['time_elapsed'] = time_elapsed
    if external is not None and type(external) is dict:
        external[domain] = results
    return results


def traceroute_batch(input_list, method='udp', cmd_arguments=[], delay_time=0.1, max_threads=100):
    """
    This is a parallel version of the traceroute primitive.

    Params:
    input_list-    the input is a list of domain names
    method-        the packet type used for traceroute, ICMP by default
    cmd_arguments- the list of arguments that need to be passed
                   to traceroute.
    delay_time-    delay before starting each thread
    max_threads-   maximum number of concurrent threads

    """
    results = {}
    threads = []
    thread_error = False
    thread_wait_timeout = 200
    ind = 1
    total_item_count = len(input_list)
    for domain in input_list:
        wait_time = 0
        while threading.active_count() > max_threads:
            time.sleep(1)
            wait_time += 1
            if wait_time > thread_wait_timeout:
                thread_error = True
                break

        if thread_error:
            results['error'] = 'Threads took too long to finish.'
            break
        time.sleep(delay_time)
        log_prefix = '%d/%d: ' % (ind, total_item_count)
        thread = threading.Thread(target=traceroute, args=(
         domain, method, cmd_arguments,
         results, log_prefix))
        ind += 1
        thread.setDaemon(1)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join(thread_wait_timeout)

    return results


def _traceroute_callback(self, line, kill_switch):
    """Callback function to handle traceroute.
    """
    line = line.lower()
    if 'traceroute to' in line:
        self.started = True
    if 'enough privileges' in line:
        self.error = True
        self.kill_switch()
        self.stopped = True
    if 'service not known' in line:
        self.error = True
        self.kill_switch()
        self.stopped = True