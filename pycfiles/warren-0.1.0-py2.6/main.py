# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/warren/main.py
# Compiled at: 2014-03-05 17:19:46
import sys, re, subprocess, logging
from socket import getfqdn
from optparse import OptionParser
from warren import __version__

class RabbitMQCtl(object):

    def __init__(self, rabbitmqctl='rabbitmqctl'):
        super(RabbitMQCtl, self).__init__()
        self.ctl = rabbitmqctl

    def _run_rabbitmqctl(self, args, run_on=None):
        proc_args = [self.ctl] + (['-n', run_on] if run_on else []) + args
        logging.debug(('Executing: {0!r}').format((' ').join(proc_args)))
        proc = subprocess.Popen(proc_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0:
            msg = ('Unexpected return code: {0}\n    Stdout: {1!r}\n    Stderr: {2!r}\n').format(proc.returncode, stdout, stderr)
            raise Exception(msg)
        return stdout.splitlines()

    def _trim_quotes(self, node):
        if node.startswith("'") and node.endswith("'"):
            return node[1:-1]
        else:
            return node

    def get_cluster_status(self):
        output = self._run_rabbitmqctl(['cluster_status'])
        match = re.match('^Cluster status of node (.*) ...$', output[0])
        if match:
            local_node = self._trim_quotes(match.group(1))
        else:
            raise Exception(('Unexpected header line: {0!r}').format(output[0]))
        match = re.match('^...done', output[(-1)])
        if not match:
            raise Exception(('Unexpected footer line: {0!r}').format(output[(-1)]))
        cluster_info = ('').join(output[1:-1])
        match = re.search('{nodes,\\[((?:{.*?\\[.*?\\]},?)+)\\]}', cluster_info)
        if not match:
            msg = ('Could not parse cluster info: {0!r}').format(cluster_info)
            raise Exception(msg)
        node_info = match.group(1)
        nodes = set()
        for match in re.finditer('{.*?,\\[(.*?)\\]}', node_info):
            for node_name in match.group(1).split(','):
                nodes.add(self._trim_quotes(node_name))

        return (
         local_node, nodes)

    def join_cluster(self, node_name):
        try:
            self._run_rabbitmqctl(['stop_app'])
            self._run_rabbitmqctl(['join_cluster', node_name])
        finally:
            self._run_rabbitmqctl(['start_app'])

    def forget_cluster_node(self, node_name):
        try:
            self._run_rabbitmqctl(['stop_app'], node_name)
        except Exception, exc:
            logging.error(str(exc))

        args = [
         'forget_cluster_node', node_name]
        self._run_rabbitmqctl(['forget_cluster_node', node_name])
        try:
            self._run_rabbitmqctl(['reset'], node_name)
            self._run_rabbitmqctl(['start_app'], node_name)
        except Exception, exc:
            logging.error(str(exc))


def main():
    usage = 'Usage: %prog <nodes...>'
    version = '%prog ' + __version__
    description = 'Checks the current cluster status of the RabbitMQ node. If the node is unclustered, warren attempts to cluster with the given list of RabbitMQ nodes.'
    parser = OptionParser(usage=usage, description=description, version=version)
    parser.add_option('--verbose', action='store_true', help='Enable verbose output.')
    (options, extra) = parser.parse_args()
    known_nodes = set(extra)
    if options.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    ctl = RabbitMQCtl()
    try:
        (local_node, cluster_nodes) = ctl.get_cluster_status()
    except Exception, exc:
        logging.error(str(exc))
        sys.exit(2)

    known_nodes.add(local_node)
    logging.info(('Local cluster node: {0}').format(local_node))
    logging.info(('Current cluster nodes: {0}').format((', ').join(cluster_nodes)))
    logging.info(('Known cluster nodes: {0}').format((', ').join(known_nodes)))
    if cluster_nodes == known_nodes:
        logging.info('This node is clustered correctly.')
    elif len(cluster_nodes) == 1:
        for node_name in known_nodes:
            if node_name != local_node:
                logging.info(('Attempting to join with: {0}').format(node_name))
                try:
                    ctl.join_cluster(node_name)
                    break
                except Exception, exc:
                    logging.error(str(exc))

        else:
            logging.warning('Node could not be clustered.')
            sys.exit(2)