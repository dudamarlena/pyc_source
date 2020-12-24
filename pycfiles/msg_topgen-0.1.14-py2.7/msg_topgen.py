# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/msg_topgen/msg_topgen.py
# Compiled at: 2018-01-29 07:18:47
import json, os
from arg_parser import Config
from generate import get_conf
from topology import Topology

def generate_output(config, generated, topology):
    """
    Function for generate final output (variables for ansible deployment, topology picture, etc.)
    :param config: object of parsed arguments with data for filename
    :param generated: generated variables
    :param topology: object of created topology
    """
    basename = '%s_R%s_B%s' % (config.graph_type, config.routers, config.brokers)
    directory = os.path.join(config.out_dir, basename)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, 'router_confs.json')
    topology.export_graph(os.path.join(directory, 'topology.svg'), basename, config.graph_type)
    with open(filename, 'w') as (f):
        f.write(json.dumps({'confs': generated.values()}))


def main():
    """
    Main
    """
    config = Config()
    config.args_parse()
    topology = Topology()
    if config.graph_file:
        topology.load_graph_from_json(config.graph_file)
    else:
        topology.create_graph(config.router_names, config.broker_names, config.graph_type)
    generated = get_conf(topology.graph)
    generate_output(config, generated, topology)