# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/manager/network.py
# Compiled at: 2011-05-23 09:48:35
__doc__ = ' A network-style manager.\nThe Network object sets up nodes and relation between them from a dictionnary\nrepresentation.\nThe nodes object do prelink and link from the bottom up (consumers to producers)\nThe Network can then set up a status handler and furnish\na final iterator over statuses.\n'
from pyf.dataflow.core import runner, BYPASS_VALS
from pyf.dataflow.components import linear_merging, splitm, all_true_longest, izip_longest, status_lookup
from operator import attrgetter, itemgetter
import operator, collections, Queue, logging, inspect
from pickle import PicklingError
import time
logger = logging.getLogger('pyf.manager.network')

class CustEllipsis(object):
    pass


BYPASS_VALS.append(CustEllipsis)

class FlowEnd(object):
    pass


class FlowComplete(object):
    pass


class SerializedContainer(object):

    def __init__(self, obj):
        if hasattr(obj, 'serialized'):
            self.serialized_obj = obj.serialized
        elif hasattr(obj, 'serialize'):
            self.serialized_obj = obj.serialize()
        else:
            raise ValueError, 'object is not serializable'
        self.obj_class = obj.__class__

    def deserialize(self):
        return self.obj_class.deserialize(self.serialized_obj)

    @classmethod
    def is_serializable(cls, obj):
        return (hasattr(obj, 'serialized') or hasattr(obj, 'serialize')) and hasattr(obj.__class__, 'deserialize')


def subprocess_output_adapter(flow, queue):
    try:
        try:
            for item in flow:
                if item in BYPASS_VALS:
                    item = CustEllipsis
                elif SerializedContainer.is_serializable(item):
                    item = SerializedContainer(item)
                try:
                    queue.put(item)
                except PicklingError:
                    raise

            queue.put(FlowComplete)
        except Exception, e:
            if isinstance(e, StopIteration):
                raise
            else:
                queue.put(e)
                raise

    finally:
        queue.put(FlowEnd)


class DataJunction(object):
    """ A DataJunction is an object specialised in taking multiple sources,
    setting up a joiner runner and permitting to get a generator output.
    
    It handles BYPASS_VALS constants to pass them to the output
    (only one if there are many). """

    def __init__(self, joiner=None, strip_bypass=True, node=None):
        self.input_sources = list()
        self.joiner = joiner or linear_merging
        self.runner = None
        if joiner is None:
            self.strip_bypass = False
        else:
            self.strip_bypass = strip_bypass
        self.queue = collections.deque()
        self.node = node
        return

    def add_input_source(self, source, name):
        """ Appends a named input source """
        if source not in self.input_sources:
            self.input_sources.append((source, name))

    def continuation_stripper(self, values):
        """ Removes the continuation values (values defined in BYPASS_VALS)
        and puts them in the queue. Returns an iterator over non bypassed values
        
        This is done so the joiner runner doesn't have to handle the
        bypassing values.
        """
        for value in values:
            if value not in BYPASS_VALS:
                yield value
            else:
                self.queue.append(value)

    def output_checker(self, values):
        """ Outputs the values passed in, and if there is something
        in the queue, pass it, but discard all other objects in the queue
        until next input data.
        (If there is a continuation, just pass one, and not the others...
        It's usefull if there is a split then a merge with continuation vals,
        to avoid duplication of sync packets)
        """
        for value in values:
            yield value
            if self.queue:
                yield self.queue.popleft()
            self.queue.clear()

    def get_generator(self):
        """ Sets up all the sources in the runner and returns an iterator over
        the output port of the junction runner.
        
        Warning, this function shouldn't be called twice !
        """
        if self.runner is None:
            extra_args = {'ports': map(itemgetter(1), self.input_sources)}
            func_spec = inspect.getargspec(self.joiner)
            func_kwargs = func_spec[0][len(func_spec[3]) * -1:]
            if 'metadata' in func_kwargs:
                extra_args['metadata'] = {'get_buffer_state': self.node.get_buffer_state, 'get_input_buffer': self.node.get_input_buffer}
            self.runner = runner(self.joiner, extra_args, handle_bypass=False)
        for (input_source, name) in self.input_sources:
            generator = input_source
            if self.strip_bypass:
                generator = self.continuation_stripper(generator)
            self.runner.connect_in('sources', generator)

        if self.strip_bypass:
            return self.output_checker(self.runner('out'))
        else:
            return self.runner('out')
            return

    __iter__ = get_generator


class GeneratorAdapter(object):

    def __init__(self, queue):
        self.queue = queue

    def __iter__(self):
        import Queue
        queue = self.queue
        finished = False
        complete = False
        i = 0
        while True:
            if self.queue.empty() and i < 10:
                if finished:
                    if complete:
                        raise StopIteration
                    else:
                        raise Exception, 'Bad ending in flow. Corrupted connection ?'
                yield Ellipsis
                i += 1
            else:
                i = 0
                item = queue.get()
                if isinstance(item, Exception):
                    raise item
                elif item is FlowEnd:
                    finished = True
                elif item is FlowComplete:
                    complete = True
                elif isinstance(item, SerializedContainer):
                    yield item.deserialize()
                else:
                    yield item


class Node(object):
    """ Object that is here to be linked to other nodes.
    Requires a node_id and a runner object (orunner).
    
    First step is to prelink, then to link.
    Order is from consumers up to producers :

        * Consumers take output from up nodes than themselves take sources up...
        * If there is multiple source, the joiner argument is used (or a default)
          and encapsulated in a DataJunction
        * If there is multiple output, the splitter argument is used (or a default)
    """

    def __init__(self, node_id, orunner, in_port=None, out_port=None, joiner=None, splitter=None, joiner_strip_bypass=True, deffer_to_process=False):
        self._id = node_id
        self.input_ports = list()
        self.output_ports = list()
        self.in_port_name = in_port or 'values'
        self.out_port_name = out_port or 'out'
        self.joiner = joiner
        self.joiner_strip_bypass = joiner_strip_bypass
        if deffer_to_process is True:
            try:
                import multiprocessing
            except ImportError:
                logger.warning('Asked to deffer to process, but multiprocessing is not available. Ignoring.')
                deffer_to_process = False

        self.deffer_to_process = deffer_to_process
        self.junction = None
        self.splitter = splitter
        self.linked = False
        self.inited = False
        self.iterator = None
        self.runner = orunner
        self.current_output = 0
        self.bypass_buffer = collections.deque()
        self.input_buffer = None
        self.output_generators = list()
        return

    @property
    def name(self):
        """ Returns the name (id) of the current node """
        return self._id

    def add_input(self, node):
        """ Adds a node as an input """
        if node not in self.input_ports:
            self.input_ports.append(node)

    def add_output(self, node):
        """ Adds a node as an output """
        if node not in self.output_ports:
            self.output_ports.append(node)

    @property
    def is_consumer(self):
        """ Returns true if there are no output ports """
        return len(self.output_ports) == 0

    @property
    def is_producer(self):
        """ Returns true if there are no input ports """
        return len(self.input_ports) == 0

    def prepare_splitter(self, splitter_function, size):
        args = inspect.getargspec(splitter_function).args
        kwargs = dict()
        if 'size' in args:
            kwargs['size'] = size
        if 'ports' in args:
            kwargs['ports'] = map(operator.attrgetter('name'), self.output_ports)
        return runner(splitter_function, kwargs, handle_bypass=False)

    def get_default_splitter(self, size):
        """ Returns a default splitter (basically the same than
        an itertools tee: pass the same data in all outputs) """
        return runner(splitm, dict(size=size), handle_bypass=False)

    def link_up(self):
        """ Link to the input nodes. (ask up to do the same)
        If not inited yet, init the current node """
        if not self.is_producer:
            for up_node in self.input_ports:
                up_node.link_up()

        if not self.inited:
            self.init_component()

    def prelink_up(self):
        """
        If there is a splitter needed, initialize it.
        If there is a junction needed, initialize it.
        
        Prelinks the input nodes... (ask up to do the same)
        """
        self.linked = True
        if not self.is_producer:
            for up_node in self.input_ports:
                if not up_node.linked:
                    up_node.prelink_up()

            if len(self.input_ports) > 1:
                self.junction = DataJunction(self.joiner, strip_bypass=self.joiner_strip_bypass, node=self)
        if len(self.output_ports) > 1:
            if self.splitter:
                if inspect.isfunction(self.splitter):
                    self.splitter = self.prepare_splitter(self.splitter, len(self.output_ports))
            else:
                self.splitter = self.get_default_splitter(len(self.output_ports))

    def prepare_input_flow(self):
        while True:
            if self.input_buffer is not None and self.input_buffer:
                value = self.input_buffer.popleft()
            else:
                value = self.input_flow.next()
            if value in BYPASS_VALS:
                self.bypass_buffer.append(value)
            elif isinstance(value, SerializedContainer):
                yield value.deserialize()
            else:
                yield value

        return

    def prepare_output_flow(self, flow):
        if self.deffer_to_process:
            import multiprocessing
            from multiprocessing.queues import SimpleQueue
            output_queue = SimpleQueue()
            process = multiprocessing.Process(target=subprocess_output_adapter, args=(
             self.__prepare_output_flow(flow), output_queue))
            process.start()
            for itemm in iter(GeneratorAdapter(output_queue)):
                yield itemm

        for itemm in self.__prepare_output_flow(flow):
            yield itemm

    def __prepare_output_flow(self, flow):
        while True:
            if not self.is_producer:
                if self.input_buffer is None:
                    self.input_buffer = collections.deque()
                while self.input_buffer:
                    yield flow.next()

                try:
                    up_val = self.input_flow.next()
                    if up_val in BYPASS_VALS:
                        yield up_val
                    else:
                        self.input_buffer.append(up_val)
                        if self.bypass_buffer:
                            yield self.bypass_buffer.popleft()
                        else:
                            yield flow.next()
                except StopIteration:
                    yield flow.next()

            else:
                yield flow.next()

        return

    def init_component(self):
        """ Connect data inputs in the main runner or in a junction
        connected to the main runner.
        If needed, connect output in the splitter. """
        if not self.is_producer:
            if self.junction:
                for up_node in self.input_ports:
                    self.junction.add_input_source(up_node.get_output(self), up_node.name)

                self.input_flow = self.junction.get_generator()
            else:
                self.input_flow = self.input_ports[0].get_output(self)
            self.runner.connect_in(self.in_port_name, self.prepare_input_flow())
        if not self.is_consumer:
            if self.splitter:
                flow = self.runner(self.out_port_name)
                self.splitter.connect_in('source', self.prepare_output_flow(flow))
        self.inited = True

    def get_output(self, node=None):
        """ Returns an output generator.
        If there is one output, return the main runner out port,
        else, return a free port from the splitter """
        if self.splitter:
            flow = self.splitter('out', self.output_ports.index(node))
        else:
            flow = self.prepare_output_flow(self.runner(self.out_port_name))
        self.output_generators.append(flow)
        return flow

    def get_output_port_position(self, generator):
        return self.output_generators.index(generator)

    def get_input_buffer(self, recursive=True, separate=False):
        if not self.is_producer:
            if len(self.input_ports) > 1:
                in_buffers = list()
                for (i, up_node) in enumerate(self.input_ports):
                    (source, name) = self.junction.input_sources[i]
                    in_buffers.append((name, up_node.get_buffer_state(source)))

                if separate:
                    return dict(in_buffers)
                return sum(map(itemgetter(1), in_buffers))
            else:
                up_node = self.input_ports[0]
                return up_node.get_buffer_state(self.input_flow, recursive=recursive)
        return 0

    def get_output_buffers(self):
        if not self.is_consumer:
            if len(self.output_ports) > 1 and 'out' in self.splitter.out_array_lookup:
                return map(len, self.splitter.out_array_lookup['out'])
        return list()

    def get_buffer_state(self, flow, recursive=True):
        position = self.get_output_port_position(flow)
        if not self.is_consumer and len(self.output_ports) > 1:
            if 'out' in self.splitter.out_array_lookup:
                return len(self.splitter.out_array_lookup['out'][position])
            else:
                return 0
        else:
            if recursive:
                return self.get_input_buffer()
            else:
                return 0


class Network(object):
    r""" Initialises a network of nodes from a dictionary structure.
    Once the nodes have been set up, you can either get the consumer iterators,
    or get a status handler checking that all the outputs resolve to True.
    
    .. code-block::
    
            [node1]
               |
            [node2]
             /            [node3]  [node4]
             \   /
            [node5]
    
    .. code-block:: python        
        nodes => {'node1': {component=my_producer, after=['node2']},
                  'node2': {component=tata, after=['node4']},
                  'node3': {component=titi, after=['node5'], before=['node2']},
                  'node4': {component=tutu, after=['node5']},
                  'node5': {component=my_consumer}}
    """

    def __init__(self, nodes=None):
        self.ids = list()
        self.nodes = nodes or dict()
        self.node_objects = dict()
        self.entry_points = list()

    def add_node(self, node):
        """ Adds a node to the main node dictionnary """
        node_id = node['id']
        self.nodes[node_id] = node

    @property
    def consumer_nodes(self):
        """ Returns the consumers Node objects """
        return filter(attrgetter('is_consumer'), self.node_objects.values())

    @property
    def consumers(self):
        """ Return the outputs from the consumer Node objects """
        return map(lambda node: node.get_output(), self.consumer_nodes)

    @property
    def producer_nodes(self):
        """ Return the producers Node objects """
        return filter(attrgetter('is_producer'), self.node_objects.values())

    def initialize(self):
        """ Creates the Node objects from the dictionnary data structure,
        set up the links between them and prelink_up then link_up the consumers.
        """
        for (node_id, node_data) in self.nodes.iteritems():
            self.node_objects[node_id] = Node(node_id, runner(node_data['component'], node_data.get('args', dict()), handle_bypass=False), in_port=node_data.get('in_port'), out_port=node_data.get('out_port'), joiner=node_data.get('joiner'), splitter=node_data.get('splitter'), joiner_strip_bypass=node_data.get('joiner_strip_bypass', True), deffer_to_process=node_data.get('deffer_to_process', False))

        for (node_id, node_data) in self.nodes.iteritems():
            node = self.node_objects[node_id]
            for in_node in node_data.get('before', list()):
                node.add_input(self.node_objects.get(in_node))
                self.node_objects.get(in_node).add_output(node)

            for out_node in node_data.get('after', list()):
                node.add_output(self.node_objects.get(out_node))
                self.node_objects.get(out_node).add_input(node)

        for node in self.consumer_nodes:
            node.prelink_up()

        for node in self.consumer_nodes:
            node.link_up()

    def get_status_handler(self, advanced=False):
        """ Returns a status handler that returns True
        each time it receives a True from parents.
        
        Experimental: if "advanced" is set to True,
        uses an intelligent status handler that looks for parent nodes
        until it finds a splitting node and consumes
        all the buffer on each branch to avoid high memory usage """
        if advanced:
            buffer_num_getters = [ node.get_input_buffer for node in self.consumer_nodes
                                 ]
            final_consumer = runner(status_lookup, dict(buffer_num_getters=buffer_num_getters))
            for consumer in self.consumers:
                final_consumer.connect_in('sources', consumer)

            return final_consumer('out')
        else:
            final_consumer = runner(all_true_longest)
            for (num, consumer) in enumerate(self.consumers):
                final_consumer.connect_in('sources', consumer)

            return final_consumer('out')