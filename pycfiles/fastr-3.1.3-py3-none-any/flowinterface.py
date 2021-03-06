# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/interfaceplugins/flowinterface.py
# Compiled at: 2019-06-04 03:03:06
from abc import abstractmethod
import os
from collections import OrderedDict
import fastr
from fastr import exceptions
from fastr.core.baseplugin import Plugin
from fastr.core.pluginmanager import PluginSubManager
from fastr.core.interface import Interface, InterfaceResult, InputSpec, OutputSpec

class FlowPlugin(Plugin):
    """
    Plugin that can manage an advanced data flow. The plugins override the
    execution of node. The execution receives all data of a node in one go,
    so not split per sample combination, but all data on all inputs in one
    large payload. The flow plugin can then re-order the data and create
    resulting samples as it sees fits. This can be used for all kinds of
    specialized data flows, e.g. cross validation.

    To create a new FlowPlugin there is only one method that needs to be
    implemented: :py:meth:`execute <fastr.plugins.FlowInterface.flow_plugin_type.execute>`.
    """

    @abstractmethod
    def execute(payload):
        result_data = None
        log_data = None
        return (result_data, log_data)


class FlowPluginManager(PluginSubManager):
    """
    Container holding all the CollectorPlugins
    """

    def __init__(self):
        """
        Create the Coll
        :param path:
        :param recursive:
        :return:
        """
        super(FlowPluginManager, self).__init__(parent=fastr.plugin_manager, plugin_class=FlowPlugin)

    @property
    def _instantiate(self):
        """
        Indicate that the plugins should instantiated before stored
        """
        return False


class FlowInterface(Interface):
    """
    The Interface use for AdvancedFlowNodes to create the advanced data flows
    that are not implemented in the fastr. This allows nodes to implement
    new data flows using the plugin system.

    The definition of ``FlowInterfaces`` are very similar to the default
    ``FastrInterfaces``.

    .. note::

        A flow interface should be using a specific FlowPlugin
    """
    __dataschemafile__ = 'FastrInterface.schema.json'
    flow_plugins = FlowPluginManager()
    flow_plugin_type = FlowPlugin

    def __init__(self, id_, document):
        super(FlowInterface, self).__init__()
        if not isinstance(document, dict):
            fastr.log.debug(('Trying to load file: {}').format(document))
            filename = os.path.expanduser(document)
            filename = os.path.abspath(filename)
            document = self._loadf(filename)
        else:
            document = self.get_serializer().instantiate(document)
        self.id = id_
        self._inputs = OrderedDict((v['id'], InputSpec(id_=v['id'], cardinality=v.get('cardinality', 1), datatype=v['datatype'] if 'datatype' in v else fastr.typelist.create_enumtype(('__{}__{}__Enum__').format(self.id, v['id']), tuple(v['enum'])).id, required=v.get('required', True), description=v.get('description', ''), default=v.get('default', None), hidden=v.get('hidden', False))) for v in document['inputs'])
        self._outputs = OrderedDict((v['id'], OutputSpec(id_=v['id'], cardinality=v.get('cardinality', 1), datatype=v['datatype'] if 'datatype' in v else fastr.typelist.create_enumtype(('__{}__{}__Enum__').format(self.id, v['id']), tuple(v['enum'])).id, automatic=v.get('automatic', False), required=v.get('required', True), description=v.get('description', ''), hidden=v.get('hidden', False))) for v in document['outputs'])

    def __eq__(self, other):
        if not isinstance(other, FlowInterface):
            return NotImplemented
        return vars(self) == vars(other)

    def __getstate__(self):
        """
        Get the state of the FastrInterface object.

        :return: state of interface
        :rtype: dict
        """
        state = {'id': self.id, 
           'class': type(self).__name__, 
           'inputs': self.inputs.values(), 
           'outputs': self.outputs.values()}
        return state

    def __setstate__(self, state):
        """
        Set the state of the Interface
        """
        self.id = state['id']
        self._inputs = OrderedDict((v['id'], InputSpec(id_=v['id'], cardinality=v.get('cardinality', 1), datatype=v['datatype'] if 'datatype' in v else fastr.typelist.create_enumtype(('__{}__{}__Enum__').format(self.id, v['id']), tuple(v['enum'])).id, required=v.get('required', True), description=v.get('description', ''), default=v.get('default', None), hidden=v.get('hidden', False))) for v in state['inputs'])
        self._outputs = OrderedDict((v['id'], OutputSpec(id_=v['id'], cardinality=v.get('cardinality', 1), datatype=v['datatype'] if 'datatype' in v else fastr.typelist.create_enumtype(('__{}__{}__Enum__').format(self.id, v['id']), tuple(v['enum'])).id, automatic=v.get('automatic', False), required=v.get('required', True), description=v.get('description', ''), hidden=v.get('hidden', False))) for v in state['outputs'])

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def expanding(self):
        return 1

    def execute(self, target, payload):
        try:
            flow_plugin = self.flow_plugins[target.binary]
        except KeyError:
            raise exceptions.FastrKeyError(('Could not find {} in {} (options {})').format(target.binary, self.flow_plugins, self.flow_plugins.keys()))

        result = InterfaceResult(result_data=None, log_data=None, payload=payload)
        result.result_data, result.log_data = flow_plugin.execute(payload)
        return result