# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/manager/path.py
# Compiled at: 2010-09-24 04:35:32
""" A datapath-style manager.
It is now deprecated (not used in upper level libs anymore) in favor of the network-style manager, but is still here if you want to do pure data path without networking system (faster).
"""
from pyf.dataflow import runner
from pyf.dataflow.components import splitm, all_true_longest, status_lookup, linear_merging
from pyf.dataflow.core import BYPASS_VALS

class DataPath(object):
    """
    root_node = dict(content=None,
                     children=[
                             dict(content=[dict(component=toto), dict(component=tata)],
                                  children=[
                                            dict(content=[dict(component=titi)])
                                            ]),
                             dict(content=DataRoad(dict(component=huhu),
                                                   dict(component=hoho),
                                                   dict(component=hehe)))
                             ]
                   )
    """

    def __init__(self, root_node):
        self.root_node = root_node
        self.consumers = list()
        self.consumers_runners = list()

    def setup(self, values):
        flow = self.setup_node(self.root_node, values)

    def get_nodes(self):
        return self.root_node

    def setup_node(self, node, values, parent_runner=None, parent_runner_port=None):
        if not isinstance(node, dict):
            if not isinstance(node, DataPath):
                raise ValueError('Nodes should be dicts or paths')
            content = node.get('content')
            if isinstance(content, DataPath):
                node = node.get_nodes()
            children = node.get('children')
            children_source = None
            children_source_runner = None
            if content:
                if isinstance(content, DataRoad):
                    content_road = content
                elif isinstance(content, list):
                    content_road = DataRoad(content)
                else:
                    raise ValueError('Content should be of type DataRoad or list')
                content_road.setup(values, parent_runner=parent_runner, parent_runner_port=parent_runner_port)
                children_source = content_road.launch()
                (children_source_runner, port) = content_road.out_port
            else:
                children_source = values
            if children:
                splitter_size = len(children)
                splitter = node.get('splitter')
                splitter = splitter or self.get_default_splitter(splitter_size)
            else:
                splitter = runner(splitter)
            setattr(splitter, 'is_splitter', True)
            if not isinstance(children, list):
                raise ValueError('Children should be a list of dicts')
            splitter.connect_in('source', children_source)
            for (num, child_node) in enumerate(children):
                self.setup_node(child_node, splitter('out', num), parent_runner=splitter, parent_runner_port=num)

        else:
            self.consumers.append(children_source)
            self.consumers_runners.append(children_source_runner)
        return

    def get_default_splitter(self, size):
        return runner(splitm, dict(size=size))

    def get_status_handler(self, advanced=True):
        """ Returns a status handler that returns True
        each time it receives a True from parents.
        
        Experimental: if "advanced" is set to True,
        uses an intelligent status handler that looks for parent nodes
        until it finds a splitting node and consumes
        all the buffer on each branch to avoid high memory usage """
        if advanced:

            def find_first_buffer_container(node, child_port=None):
                if hasattr(node, 'is_splitter') and node.is_splitter is True:

                    def return_func():
                        if 'out' in node.out_array_lookup:
                            return len(node.out_array_lookup['out'][child_port])
                        else:
                            return 0

                    return return_func
                else:
                    if hasattr(node, 'parent_runner') and node.parent_runner is not None:
                        parent = node.parent_runner
                        if hasattr(node, 'parent_port') and node.parent_port is not None:
                            return find_first_buffer_container(parent, node.parent_port)
                        return find_first_buffer_container(parent)
                    else:
                        return
                    return

            buffer_num_getters = list()
            final_consumer = runner(status_lookup, dict(buffer_num_getters=buffer_num_getters))
            for (num, consumer) in enumerate(self.consumers):
                final_consumer.connect_in('sources', consumer)
                buffer_container = find_first_buffer_container(self.consumers_runners[num])
                buffer_num_getters.append(buffer_container)

            return final_consumer('out')
        else:
            final_consumer = runner(all_true_longest)
            for (num, consumer) in enumerate(self.consumers):
                final_consumer.connect_in('sources', consumer)

            return final_consumer('out')
            return


class DataRoad(object):
    """ Data Road gets list of items and sets up a data road with them.
    To launch the road, pass items in the init, run road.setup(in_generator),
    then road.launch() returns an iterator of results."""

    def __init__(self, *items):
        """ @params: a list of dict with {component: component,
                                         in_port: string,
                                         out_port: string,
                                         kwargs: dict}"""
        if isinstance(items[0], list):
            items = items[0]
        self.items = items
        self.runners = None
        self.out_port = None
        return

    def split(self, position):
        """ Splits the data road at the specified position.
        Usefull to plug data in the flow at a specific position """
        return (
         DataRoad(self.items[:position]), DataRoad(self.items[position:]))

    def setup(self, values, parent_runner=None, parent_runner_port=None):
        self.runners = list()
        for (num, item) in enumerate(self.items):
            self.runners.append(runner(item.get('component'), item.get('kwargs', dict())))
            if num > 0:
                self.runners[num].connect_in(item.get('in_port', 'values'), self.runners[(num - 1)](self.items[(num - 1)].get('out_port', 'out')))
                setattr(self.runners[num], 'parent_runner', self.runners[(num - 1)])
                setattr(self.runners[num], 'is_splitter', False)
            else:
                self.runners[num].connect_in(item.get('in_port', 'values'), values)
                setattr(self.runners[num], 'parent_runner', parent_runner)
                setattr(self.runners[num], 'parent_port', parent_runner_port)
                setattr(self.runners[num], 'is_splitter', False)
            if num + 1 == len(self.items):
                self.out_port = (self.runners[num], item.get('out_port', 'out'))

    def launch(self):
        if self.out_port:
            (runner, port) = self.out_port
            return runner(port)
        else:
            return
            return

    def __iter__(self):
        return self.items.__iter__()

    def append(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)


class DataJunction(object):

    def __init__(self, output_route):
        self.input_routes = list()
        self.output_route = output_route
        self.runner = None
        self.consumer = None
        return

    def add_input_route(self, route):
        self.input_route.append(route)

    def continuation_stripper(self, values):
        for value in values:
            if value not in BYPASS_VALS:
                yield value

    def setup(self, merging_runner=None):
        pass