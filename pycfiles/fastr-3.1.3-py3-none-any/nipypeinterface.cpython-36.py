# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/interfaceplugins/nipypeinterface.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 9122 bytes
from collections import OrderedDict, Mapping
try:
    import nipype, traits
    IMPORT_SUCCESS = True
    IMPORT_ERROR = ''
except ImportError as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = e.msg

import fastr
from fastr import exceptions
from fastr.abc.baseplugin import PluginState
from fastr.core.interface import Interface, InterfaceResult, InputSpec, OutputSpec

class HiddenFieldMap(Mapping):

    def __init__(self, *args, **kwargs):
        self._data = OrderedDict(*args, **kwargs)

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        for key, value in self._data.items():
            if not (hasattr(value, 'hidden') and value.hidden):
                yield key


if IMPORT_SUCCESS:
    DATATYPE_MAP = {traits.trait_types.Int: 'Int', 
     traits.trait_types.Long: 'Int', 
     traits.trait_types.Float: 'Float', 
     traits.trait_types.Bool: 'Boolean', 
     traits.trait_types.Str: 'String', 
     traits.trait_types.String: 'String', 
     traits.trait_types.Unicode: 'String', 
     traits.trait_types.List: None}
else:
    DATATYPE_MAP = {}

class NipypeInterface(Interface):
    __doc__ = '\n    Experimental interfaces to using ``nipype`` interfaces directly in fastr\n    tools, only using a simple reference.\n\n    To create a tool using a nipype interface just create an interface with\n    the correct type and set the ``nipype`` argument to the correct class.\n    For example in an xml tool this would become::\n\n        <interface class="NipypeInterface">\n          <nipype_class>nipype.interfaces.elastix.Registration</nipype_class>\n        </interface>\n\n    .. note::\n\n        To use these interfaces ``nipype`` should be installed on the system.\n\n    .. warning::\n\n        This interface plugin is basically functional, but highly experimental!\n    '
    if IMPORT_ERROR:
        _status = (
         PluginState.failed, 'nipype could not be found!')

    def __init__(self, id_, nipype_cls=None, document=None):
        super(NipypeInterface, self).__init__()
        if nipype_cls is None:
            if document is None:
                raise exceptions.FastrValueError('Need to have at Nipype class set in either the nipype_cls or document argument')
        if nipype_cls is not None and document is not None:
            raise exceptions.FastrValueError('Need to have at Nipype class set in either the nipype_cls or the document argument, not both!')
        else:
            if document is not None:
                nipype_cls = document['nipype_class']
        if isinstance(nipype_cls, str):
            if '.' in nipype_cls:
                module, cls = nipype_cls.rsplit('.', 1)
                _temp = __import__(module, globals(), locals(), [cls], -1)
                nipype_cls = getattr(_temp, cls)
            else:
                raise ValueError('If a string is given, it should be a full class specification (in the form of nipype.interfaces.something.Class), got "{}"'.format(nipype_cls))
        self.nipype_class = nipype_cls
        self.id = id_
        self._create_inputs_outputs()

    def _create_inputs_outputs(self):
        nipype_object = self.nipype_class()
        ignore_inputs = ['args', 'environ', 'ignore_exception', 'terminal_output']
        inputs = []
        for id_, input_ in nipype_object.input_spec().items():
            default = input_.default
            if default == '':
                default = None
            inputs.append(InputSpec(id_=id_, cardinality=(1 if not input_.is_trait_type(traits.trait_types.List) else '1-*'),
              datatype=(self.get_type(input_)),
              required=(input_.mandatory and default is None),
              description=(input_.desc),
              default=default,
              hidden=(id_ in ignore_inputs)))

        outputs = []
        for id_, output in nipype_object.output_spec().items():
            outputs.append(OutputSpec(id_=id_, cardinality=(1 if not output.is_trait_type(traits.trait_types.List) else 'unknown'),
              datatype=(self.get_type(output)),
              automatic=True,
              required=False,
              description=(output.desc),
              hidden=False))

        self._inputs = HiddenFieldMap((input_.id, input_) for input_ in inputs)
        self._outputs = HiddenFieldMap((output_.id, output_) for output_ in outputs)

    def __getstate__(self):
        state = {'id':self.id, 
         'class':type(self).__name__, 
         'nipype_class':self.nipype_class}
        return state

    def __setstate__(self, state):
        del state['class']
        self.__dict__.update(state)
        nipype_cls = self.nipype_class
        if isinstance(nipype_cls, str):
            if '.' in nipype_cls:
                module, cls = nipype_cls.rsplit('.', 1)
                _temp = __import__(module, globals(), locals(), [cls], -1)
                nipype_cls = getattr(_temp, cls)
            else:
                raise ValueError('If a string is given, it should be a full class specification (in the form of nipype.interfaces.something.Class), got "{}"'.format(nipype_cls))
        self.nipype_class = nipype_cls
        self._create_inputs_outputs()

    def __eq__(self, other):
        if not isinstance(other, NipypeInterface):
            return NotImplemented
        else:
            return vars(self) == vars(other)

    def get_type(self, trait):
        datatype = DATATYPE_MAP.get(trait.trait_type, 'AnyFile')
        if datatype is None:
            new_trait = trait.inner_traits[0]
            return self.get_type(new_trait)
        else:
            return datatype

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def expanding(self):
        return 0

    def execute(self, target, payload):
        """
        Execute the interface using a specific target and payload (containing
        a set of values for the arguments)

        :param target: the target to use
        :type target: :py:class:`SampleId <fastr.core.target.Target>`
        :param dict payload: the values for the arguments
        :return: result of the execution
        :rtype: InterfaceResult
        """
        nipype_object = self.nipype_class()
        for id_, input_value in payload['inputs'].items():
            if len(input_value) == 0:
                fastr.log.info('Skipping non-valued input {}'.format(id_))
            else:
                value = [x.value if isinstance(x, fastr.datatypes.DataType) else x for x in input_value]
                if self.inputs[id_].cardinality == 1:
                    if len(value) > 1:
                        raise exceptions.FastrValueError('Expected cardinality 1, got {}'.format(len(value)))
                    value = value[0]
                else:
                    value = list(value)
                setattr(nipype_object.inputs, id_, value)

        nipype_result = nipype_object.run()
        result_data = nipype_result.outputs.get()
        fastr.log.info('NIPYPE RESULT: {}'.format(result_data))
        for key, value in result_data.items():
            if isinstance(value, list):
                value = tuple(value)
            else:
                value = (
                 value,)
            result_data[key] = value

        fastr.log.info('RESULT DATA: {}'.format(result_data))
        result = InterfaceResult(result_data, nipype_result.runtime.dictcopy(), payload)
        return result

    @classmethod
    def test(cls):
        if not IMPORT_SUCCESS:
            raise ImportError('Could not load required module: {}'.format(IMPORT_ERROR))