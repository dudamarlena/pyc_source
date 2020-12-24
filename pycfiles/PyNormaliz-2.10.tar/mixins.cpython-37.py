# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/models/mixins.py
# Compiled at: 2019-03-11 18:33:28
# Size of source mod 2**32: 8527 bytes
from sqlalchemy import Column, Integer, String, Text, exists, and_, TypeDecorator
import json, logging, traceback
logger = logging.getLogger(__name__)

def lazy_property(f):
    internal_property = '__lazy_' + f.__name__

    @property
    def lazy_property_wrapper(self):
        try:
            return getattr(self, internal_property)
        except AttributeError:
            v = f(self)
            setattr(self, internal_property, v)
            return v
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    return lazy_property_wrapper


class LazyMixin(object):

    def invalidate--- This code section failed: ---

 L.  34         0  LOAD_FAST                'property_name'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    52  'to 52'

 L.  35         8  LOAD_GENEXPR             '<code_object <genexpr>>'
               10  LOAD_STR                 'LazyMixin.invalidate.<locals>.<genexpr>'
               12  MAKE_FUNCTION_0          ''
               14  LOAD_GLOBAL              dir
               16  LOAD_FAST                'self'
               18  CALL_FUNCTION_1       1  ''
               20  GET_ITER         
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'lazy_properties'

 L.  36        26  SETUP_LOOP           80  'to 80'
               28  LOAD_FAST                'lazy_properties'
               30  GET_ITER         
               32  FOR_ITER             48  'to 48'
               34  STORE_FAST               'p'

 L.  37        36  LOAD_GLOBAL              delattr
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'p'
               42  CALL_FUNCTION_2       2  ''
               44  POP_TOP          
               46  JUMP_BACK            32  'to 32'
               48  POP_BLOCK        
               50  JUMP_FORWARD         80  'to 80'
             52_0  COME_FROM             6  '6'

 L.  39        52  LOAD_STR                 '__lazy_'
               54  LOAD_FAST                'property_name'
               56  BINARY_ADD       
               58  STORE_FAST               'lazy_property_name'

 L.  40        60  LOAD_GLOBAL              hasattr
               62  LOAD_FAST                'self'
               64  LOAD_FAST                'lazy_property_name'
               66  CALL_FUNCTION_2       2  ''
               68  POP_JUMP_IF_FALSE    80  'to 80'

 L.  41        70  LOAD_GLOBAL              delattr
               72  LOAD_FAST                'self'
               74  LOAD_FAST                'lazy_property_name'
               76  CALL_FUNCTION_2       2  ''
               78  POP_TOP          
             80_0  COME_FROM            68  '68'
             80_1  COME_FROM            50  '50'
             80_2  COME_FROM_LOOP       26  '26'

Parse error at or near `COME_FROM' instruction at offset 80_1


class register_parameter(object):
    PARAMETER_REGISTRY = '__parameter_defaults__'

    def __init__(self, section='main', name='', default='', parameter_type=None, description='', target_class=None):
        self.section = section
        self.name = name
        self.default = default
        if parameter_type is None:
            self.parameter_type = type(default)
        else:
            self.parameter_type = parameter_type
        self.description = description
        self.target_class = target_class

    def __call__(self, cls):
        if self.target_class is not None:
            tcls = self.target_class
        else:
            tcls = cls
        section = cls.__name__ + ':' + self.section
        field = '{}{}'.format(self.PARAMETER_REGISTRY, tcls.__name__)
        if not hasattr(tcls, field):
            parent_fields = [field for field in dir(cls) if field.startswith(register_parameter.PARAMETER_REGISTRY)]
            parent_param_names = set()
            parent_params = []
            for f in parent_fields:
                p_params = getattr(cls, f)
                parent_params.append([p for p in p_params if p['name'] not in parent_param_names])
                parent_param_names |= {p['name'] for p in p_params}

            parent_params = sum(parent_params, [])
            setattr(tcls, field, parent_params)
        params = getattr(tcls, field)
        found = [p for p in params if p['name'] == self.name]
        if found:
            msg = 'Parameter {} already defined in class {}'.format(self.name, found[0]['cls'])
            logger.error(msg)
            logger.debug(traceback.print_exc())
            raise ValueError(msg)
        params.append({'section':section,  'name':self.name, 
         'default':self.default, 
         'type':self.parameter_type, 
         'description':self.description, 
         'cls':tcls.__name__})
        return cls


class ParametrizedMixin(LazyMixin):
    params = Column(Text, default='{}')

    @lazy_property
    def parameters(self):
        if not self.params or self.params == '':
            return {}
        try:
            return json.loads(self.params)
        except:
            msg = 'Parameters {} can not be parsed as json'.format(self.params)
            logger.error(msg)
            logger.debug(traceback.print_exc())
            raise ValueError(msg)

    @classmethod
    def registered_parameters(cls):
        field = '{}{}'.format(register_parameter.PARAMETER_REGISTRY, cls.__name__)
        if not hasattr(cls, field):
            parent_fields = [field for field in dir(cls) if field.startswith(register_parameter.PARAMETER_REGISTRY)]
            parent_param_names = set()
            parent_params = sum([[p for p in getattr(cls, f) if p['name'] not in parent_param_names] for f in parent_fields], [])
            setattr(cls, field, parent_params)
        return getattr(cls, field)

    @classmethod
    def parameter_default(cls, name):
        """
        Get the default value for a parameter
        :param name: the name of the parameter
        :type name: str
        :return: the default value registered
        """
        for p in cls.registered_parameters():
            if p['name'] == name:
                return p['default']

    @classmethod
    def parameter_type(cls, name):
        """
        Get the type for a parameter
        :param name: the name of the parameter
        :type name: str
        :return: the type registered
        """
        for p in cls.registered_parameters():
            if p['name'] == name:
                return p['type']

    @classmethod
    def df_registered_parameters(cls, section=None):
        from pandas import DataFrame
        df = DataFrame(cls.registered_parameters())
        if section is None:
            return df
        return df.query('section=="{}"'.format(section))

    @classmethod
    def json_registered_parameters(cls, section=None):
        from pandas import DataFrame
        df = DataFrame(cls.registered_parameters())
        if df.empty:
            return '[]'
        df = df[['section', 'name', 'description', 'default']]
        if section is None:
            return df.to_json(orient='records')
        return df.query('section=="{}"'.format(section)).to_json(orient='records')

    @classmethod
    def markup_registered_parameters(cls, section=None):
        rp = cls.registered_parameters()
        if rp is None or len(rp) == 0:
            return '[]'
        html = '<table width=90%><tr><th>Section</th><th>Name</th><th>Default</th><th>Description</th></tr>'
        for row in rp:
            if section is None or row['section'] == section:
                html += '<tr><td>{}&nbsp;&nbsp;&nbsp;</td><td>{}&nbsp;&nbsp;&nbsp;</td><td>{}&nbsp;&nbsp;&nbsp;</td><td>{}&nbsp;&nbsp;&nbsp;</td></tr>'.format(row['section'], row['name'], row['default'], row['description'])

        html += '</table>'
        return html

    def get(self, name, default=None):
        """
        Get the value for a parameter by name
        :param name: the name of the parameter
        :type name: str
        :param default: a given overridden default value
        :return: the value
        """
        return self.parameters.get(name, default or )

    def set(self, name, value):
        """
        Set the value for a parameter
        :param name: the name of the parameter
        :type name: str
        :param value: the value to set
        :return: self
        """
        registered_type = self.parameter_type(name)
        if registered_type is None:
            msg = 'Parameter {} is not registered for class {}'.format(name, self.__class__.__name__)
            logger.error(msg)
            logger.debug(traceback.print_exc())
            raise ValueError(msg)
        if not isinstance(value, registered_type):
            if not isinstance(registered_type, type(None)):
                msg = 'The value {} is not the same type as registered {}'.format(value, registered_type)
                logger.error(msg)
                logger.debug(traceback.print_exc())
                raise ValueError(msg)
        self.parameters[name] = value
        self.invalidate(name)
        self.params = json.dumps(self.parameters)
        return self


class ARRAY(TypeDecorator):
    """ARRAY"""
    impl = String

    def __init__(self, intern=None):
        super().__init__()
        self.intern = intern

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ARRAY(self.impl.length)