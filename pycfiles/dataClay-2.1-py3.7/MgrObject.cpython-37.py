# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/MgrObject.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 19734 bytes
""" Class description goes here. """
import logging
from yaml import load, dump, Loader, Dumper
from dataclay.commonruntime.Initializer import size_tracking
import dataclay.serialization.DataClaySerializable as DataClaySerializable
import dataclay.serialization.python.lang.StringWrapper as StringWrapper
import six
logger = logging.getLogger(__name__)

class ManagementMetaClass(type):

    def __init__(cls, name, bases, kwds):
        if name != 'ManagementObject':
            yaml_tag = 'tag:yaml.org,2002:es.bsc.%s' % cls.__module__
            cls.yaml_loader = Loader
            cls.yaml_tag = yaml_tag
            logger.trace('YAML TAG : %s', yaml_tag)
            Loader.add_constructor(yaml_tag, cls.from_yaml)
            Dumper.add_representer(cls, cls.to_yaml)
        super(ManagementMetaClass, cls).__init__(name, bases, kwds)

    def __new__(cls, name, bases, dct):
        if '_fields' not in dct:
            raise AttributeError('All YAML structures must have a `_fields` list attribute')
        if name == 'ManagementObject':
            dct['__slots__'] = tuple()
            return super(ManagementMetaClass, cls).__new__(cls, name, bases, dct)
        if ManagementObject not in bases:
            full_fields = list()
            full_internal = list()
            for b in bases:
                if issubclass(b, ManagementObject):
                    try:
                        dct['_typed_fields'].update(b._typed_fields)
                    except KeyError:
                        pass

                    full_fields += b._fields
                    try:
                        full_internal += b._internal_fields
                    except AttributeError:
                        pass

            full_fields += dct['_fields']
            if '_internal_fields' in dct:
                full_internal += dct['_internal_fields']
            dct['_fields'] = full_fields
            dct['_internal_fields'] = full_internal
            all_fields = full_fields + full_internal
        else:
            all_fields = list(dct['_fields'])
            if '_internal_fields' in dct:
                all_fields += dct['_internal_fields']
            dct['__slots__'] = tuple(all_fields)
            return super(ManagementMetaClass, cls).__new__(cls, name, bases, dct)


@six.add_metaclass(ManagementMetaClass)
class ManagementObject(DataClaySerializable):
    _fields = list()
    _internal_fields = list()
    _typed_fields = dict()
    yaml_tag = None

    def __init__(self, **kwargs):
        super(ManagementObject, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_yaml(cls, loader, node):
        """See YAMLObject."""
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, dumper, data):
        """See YAMLObject."""
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls)

    def __getstate__(self):
        """This method is used both by Pickle and by YAML Dumper."""
        ret = {k:getattr(self, k, None) for k in self._fields}
        ret.update({k:getattr(self, k) for k in self._internal_fields if hasattr(self, k)})
        return ret

    def __setstate__(self, state):
        """This method is used both by Pickle and by YAML Loader."""
        setted_attrs = set()
        unsetted_attrs = set()
        for k, v in state.items():
            if isinstance(v, dict):
                if k in self._typed_fields:
                    typed_field = self._typed_fields[k]
                    new_attr = typed_field()
                    new_attr.__setstate__(v)
                    v = new_attr
            try:
                setattr(self, k, v)
                setted_attrs.add(k)
            except Exception:
                unsetted_attrs.add(k)

        missed_fields = set(self._fields) - setted_attrs
        if len(missed_fields) != 0:
            logger.error('WARNING -- __setstate__ on class %s called without this fields: %s', self.__class__, list(missed_fields))
        if len(unsetted_attrs) > 0:
            logger.error('WARNING -- Attributes %s are not setted -- Fields missing on class %s', unsetted_attrs, self.__class__)

    def __str__(self):
        lines = ['ManagementObject: %s' % self.__class__.__name__]
        for field_name in self._fields:
            try:
                lines.append('  - %s: %r' % (field_name, getattr(self, field_name)))
            except AttributeError:
                logger.debug('WARNING -- Missing attribute: %s', field_name)

        return '\n'.join(lines)

    def serialize(self, io_file):
        """Serialize this instance into a IO like (file, StringIO...)."""
        with size_tracking(io_file):
            dump(self, io_file, encoding='utf-16-be', Dumper=Dumper)

    @classmethod
    def deserialize(cls, io_file):
        """Deserialize the IO into a new instance."""
        value = StringWrapper().read(io_file)
        return load(value, Loader=Loader)

    read = deserialize

    @classmethod
    def write(cls, io_file, value):
        assert isinstance(value, cls), "Called `write` on class '%s' with an object of class '%s'" % (
         cls.__name__, type(value).__name__)
        value.serialize(io_file)

    @staticmethod
    def type_equal(deserialized, orig_val):
        ret_bool = True
        ret_list = []
        try:
            if deserialized.typeName == orig_val.typeName:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('typeName')

        try:
            if deserialized.languageDepInfos == orig_val.languageDepInfos:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('languageDepInfos')

        try:
            if deserialized.descriptor == orig_val.descriptor:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('descriptor')

        try:
            if deserialized.signature == orig_val.signature:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('signature')

        try:
            if deserialized.includes == orig_val.includes:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('includes')

        return (
         ret_bool, ret_list)

    @staticmethod
    def prop_equal--- This code section failed: ---

 L. 230         0  LOAD_CONST               True
                2  STORE_FAST               'ret_bool'

 L. 231         4  BUILD_LIST_0          0 
                6  STORE_FAST               'ret_list'

 L. 233         8  LOAD_FAST                'i'
               10  LOAD_CONST               None
               12  COMPARE_OP               is-not
            14_16  POP_JUMP_IF_FALSE   912  'to 912'

 L. 234        18  SETUP_EXCEPT         58  'to 58'

 L. 235        20  LOAD_FAST                'deserialized'
               22  LOAD_ATTR                namespace
               24  LOAD_FAST                'orig_val'
               26  LOAD_FAST                'i'
               28  BINARY_SUBSCR    
               30  LOAD_ATTR                namespace
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 236        36  LOAD_CONST               True
               38  STORE_FAST               'ret_bool'
               40  JUMP_FORWARD         54  'to 54'
             42_0  COME_FROM            34  '34'

 L. 238        42  LOAD_CONST               False
               44  STORE_FAST               'ret_bool'

 L. 239        46  LOAD_FAST                'ret_bool'
               48  LOAD_FAST                'ret_list'
               50  BUILD_TUPLE_2         2 
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  POP_BLOCK        
               56  JUMP_FORWARD         96  'to 96'
             58_0  COME_FROM_EXCEPT     18  '18'

 L. 241        58  DUP_TOP          
               60  LOAD_GLOBAL              AttributeError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    94  'to 94'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 242        72  LOAD_FAST                'ret_list'
               74  LOAD_METHOD              append
               76  LOAD_GLOBAL              str
               78  LOAD_FAST                'i'
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  LOAD_STR                 ' namespace'
               84  BINARY_ADD       
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_TOP          
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            64  '64'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            56  '56'

 L. 244        96  SETUP_EXCEPT        136  'to 136'

 L. 245        98  LOAD_FAST                'deserialized'
              100  LOAD_ATTR                className
              102  LOAD_FAST                'orig_val'
              104  LOAD_FAST                'i'
              106  BINARY_SUBSCR    
              108  LOAD_ATTR                className
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   120  'to 120'

 L. 246       114  LOAD_CONST               True
              116  STORE_FAST               'ret_bool'
              118  JUMP_FORWARD        132  'to 132'
            120_0  COME_FROM           112  '112'

 L. 248       120  LOAD_CONST               False
              122  STORE_FAST               'ret_bool'

 L. 249       124  LOAD_FAST                'ret_bool'
              126  LOAD_FAST                'ret_list'
              128  BUILD_TUPLE_2         2 
              130  RETURN_VALUE     
            132_0  COME_FROM           118  '118'
              132  POP_BLOCK        
              134  JUMP_FORWARD        174  'to 174'
            136_0  COME_FROM_EXCEPT     96  '96'

 L. 251       136  DUP_TOP          
              138  LOAD_GLOBAL              AttributeError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   172  'to 172'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 252       150  LOAD_FAST                'ret_list'
              152  LOAD_METHOD              append
              154  LOAD_GLOBAL              str
              156  LOAD_FAST                'i'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  LOAD_STR                 ' className'
              162  BINARY_ADD       
              164  CALL_METHOD_1         1  '1 positional argument'
              166  POP_TOP          
              168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
            172_0  COME_FROM           142  '142'
              172  END_FINALLY      
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           134  '134'

 L. 254       174  SETUP_EXCEPT        214  'to 214'

 L. 255       176  LOAD_FAST                'deserialized'
              178  LOAD_ATTR                getterImplementationID
              180  LOAD_FAST                'orig_val'
              182  LOAD_FAST                'i'
              184  BINARY_SUBSCR    
              186  LOAD_ATTR                getterImplementationID
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L. 256       192  LOAD_CONST               True
              194  STORE_FAST               'ret_bool'
              196  JUMP_FORWARD        210  'to 210'
            198_0  COME_FROM           190  '190'

 L. 258       198  LOAD_CONST               False
              200  STORE_FAST               'ret_bool'

 L. 259       202  LOAD_FAST                'ret_bool'
              204  LOAD_FAST                'ret_list'
              206  BUILD_TUPLE_2         2 
              208  RETURN_VALUE     
            210_0  COME_FROM           196  '196'
              210  POP_BLOCK        
              212  JUMP_FORWARD        252  'to 252'
            214_0  COME_FROM_EXCEPT    174  '174'

 L. 261       214  DUP_TOP          
              216  LOAD_GLOBAL              AttributeError
              218  COMPARE_OP               exception-match
              220  POP_JUMP_IF_FALSE   250  'to 250'
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 262       228  LOAD_FAST                'ret_list'
              230  LOAD_METHOD              append
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'i'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  LOAD_STR                 ' getterImplementationID'
              240  BINARY_ADD       
              242  CALL_METHOD_1         1  '1 positional argument'
              244  POP_TOP          
              246  POP_EXCEPT       
              248  JUMP_FORWARD        252  'to 252'
            250_0  COME_FROM           220  '220'
              250  END_FINALLY      
            252_0  COME_FROM           248  '248'
            252_1  COME_FROM           212  '212'

 L. 264       252  SETUP_EXCEPT        294  'to 294'

 L. 265       254  LOAD_FAST                'deserialized'
              256  LOAD_ATTR                setterImplementationID
              258  LOAD_FAST                'orig_val'
              260  LOAD_FAST                'i'
              262  BINARY_SUBSCR    
              264  LOAD_ATTR                setterImplementationID
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   278  'to 278'

 L. 266       272  LOAD_CONST               True
              274  STORE_FAST               'ret_bool'
              276  JUMP_FORWARD        290  'to 290'
            278_0  COME_FROM           268  '268'

 L. 268       278  LOAD_CONST               False
              280  STORE_FAST               'ret_bool'

 L. 269       282  LOAD_FAST                'ret_bool'
              284  LOAD_FAST                'ret_list'
              286  BUILD_TUPLE_2         2 
              288  RETURN_VALUE     
            290_0  COME_FROM           276  '276'
              290  POP_BLOCK        
              292  JUMP_FORWARD        334  'to 334'
            294_0  COME_FROM_EXCEPT    252  '252'

 L. 270       294  DUP_TOP          
              296  LOAD_GLOBAL              AttributeError
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   332  'to 332'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 271       310  LOAD_FAST                'ret_list'
              312  LOAD_METHOD              append
              314  LOAD_GLOBAL              str
              316  LOAD_FAST                'i'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  LOAD_STR                 ' setterImplementationID'
              322  BINARY_ADD       
              324  CALL_METHOD_1         1  '1 positional argument'
              326  POP_TOP          
              328  POP_EXCEPT       
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           300  '300'
              332  END_FINALLY      
            334_0  COME_FROM           330  '330'
            334_1  COME_FROM           292  '292'

 L. 273       334  SETUP_EXCEPT        376  'to 376'

 L. 274       336  LOAD_FAST                'deserialized'
              338  LOAD_ATTR                name
              340  LOAD_FAST                'orig_val'
              342  LOAD_FAST                'i'
              344  BINARY_SUBSCR    
              346  LOAD_ATTR                name
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   360  'to 360'

 L. 275       354  LOAD_CONST               True
              356  STORE_FAST               'ret_bool'
              358  JUMP_FORWARD        372  'to 372'
            360_0  COME_FROM           350  '350'

 L. 277       360  LOAD_CONST               False
              362  STORE_FAST               'ret_bool'

 L. 278       364  LOAD_FAST                'ret_bool'
              366  LOAD_FAST                'ret_list'
              368  BUILD_TUPLE_2         2 
              370  RETURN_VALUE     
            372_0  COME_FROM           358  '358'
              372  POP_BLOCK        
              374  JUMP_FORWARD        416  'to 416'
            376_0  COME_FROM_EXCEPT    334  '334'

 L. 279       376  DUP_TOP          
              378  LOAD_GLOBAL              AttributeError
              380  COMPARE_OP               exception-match
          382_384  POP_JUMP_IF_FALSE   414  'to 414'
              386  POP_TOP          
              388  POP_TOP          
              390  POP_TOP          

 L. 280       392  LOAD_FAST                'ret_list'
              394  LOAD_METHOD              append
              396  LOAD_GLOBAL              str
              398  LOAD_FAST                'i'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  LOAD_STR                 ' name'
              404  BINARY_ADD       
              406  CALL_METHOD_1         1  '1 positional argument'
              408  POP_TOP          
              410  POP_EXCEPT       
              412  JUMP_FORWARD        416  'to 416'
            414_0  COME_FROM           382  '382'
              414  END_FINALLY      
            416_0  COME_FROM           412  '412'
            416_1  COME_FROM           374  '374'

 L. 282       416  SETUP_EXCEPT        458  'to 458'

 L. 283       418  LOAD_FAST                'deserialized'
              420  LOAD_ATTR                position
              422  LOAD_FAST                'orig_val'
              424  LOAD_FAST                'i'
              426  BINARY_SUBSCR    
              428  LOAD_ATTR                position
              430  COMPARE_OP               ==
          432_434  POP_JUMP_IF_FALSE   442  'to 442'

 L. 284       436  LOAD_CONST               True
              438  STORE_FAST               'ret_bool'
              440  JUMP_FORWARD        454  'to 454'
            442_0  COME_FROM           432  '432'

 L. 286       442  LOAD_CONST               False
              444  STORE_FAST               'ret_bool'

 L. 287       446  LOAD_FAST                'ret_bool'
              448  LOAD_FAST                'ret_list'
              450  BUILD_TUPLE_2         2 
              452  RETURN_VALUE     
            454_0  COME_FROM           440  '440'
              454  POP_BLOCK        
              456  JUMP_FORWARD        498  'to 498'
            458_0  COME_FROM_EXCEPT    416  '416'

 L. 288       458  DUP_TOP          
              460  LOAD_GLOBAL              AttributeError
              462  COMPARE_OP               exception-match
          464_466  POP_JUMP_IF_FALSE   496  'to 496'
              468  POP_TOP          
              470  POP_TOP          
              472  POP_TOP          

 L. 289       474  LOAD_FAST                'ret_list'
              476  LOAD_METHOD              append
              478  LOAD_GLOBAL              str
              480  LOAD_FAST                'i'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  LOAD_STR                 ' position'
              486  BINARY_ADD       
              488  CALL_METHOD_1         1  '1 positional argument'
              490  POP_TOP          
              492  POP_EXCEPT       
              494  JUMP_FORWARD        498  'to 498'
            496_0  COME_FROM           464  '464'
              496  END_FINALLY      
            498_0  COME_FROM           494  '494'
            498_1  COME_FROM           456  '456'

 L. 291       498  SETUP_EXCEPT        540  'to 540'

 L. 292       500  LOAD_FAST                'deserialized'
              502  LOAD_ATTR                getterOperationID
              504  LOAD_FAST                'orig_val'
              506  LOAD_FAST                'i'
              508  BINARY_SUBSCR    
              510  LOAD_ATTR                getterOperationID
              512  COMPARE_OP               ==
          514_516  POP_JUMP_IF_FALSE   524  'to 524'

 L. 293       518  LOAD_CONST               True
              520  STORE_FAST               'ret_bool'
              522  JUMP_FORWARD        536  'to 536'
            524_0  COME_FROM           514  '514'

 L. 295       524  LOAD_CONST               False
              526  STORE_FAST               'ret_bool'

 L. 296       528  LOAD_FAST                'ret_bool'
              530  LOAD_FAST                'ret_list'
              532  BUILD_TUPLE_2         2 
              534  RETURN_VALUE     
            536_0  COME_FROM           522  '522'
              536  POP_BLOCK        
              538  JUMP_FORWARD        580  'to 580'
            540_0  COME_FROM_EXCEPT    498  '498'

 L. 297       540  DUP_TOP          
              542  LOAD_GLOBAL              AttributeError
              544  COMPARE_OP               exception-match
          546_548  POP_JUMP_IF_FALSE   578  'to 578'
              550  POP_TOP          
              552  POP_TOP          
              554  POP_TOP          

 L. 298       556  LOAD_FAST                'ret_list'
              558  LOAD_METHOD              append
              560  LOAD_GLOBAL              str
              562  LOAD_FAST                'i'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  LOAD_STR                 ' getterOperationID'
              568  BINARY_ADD       
              570  CALL_METHOD_1         1  '1 positional argument'
              572  POP_TOP          
              574  POP_EXCEPT       
              576  JUMP_FORWARD        580  'to 580'
            578_0  COME_FROM           546  '546'
              578  END_FINALLY      
            580_0  COME_FROM           576  '576'
            580_1  COME_FROM           538  '538'

 L. 300       580  SETUP_EXCEPT        622  'to 622'

 L. 301       582  LOAD_FAST                'deserialized'
              584  LOAD_ATTR                setterOperationID
              586  LOAD_FAST                'orig_val'
              588  LOAD_FAST                'i'
              590  BINARY_SUBSCR    
              592  LOAD_ATTR                setterOperationID
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_FALSE   606  'to 606'

 L. 302       600  LOAD_CONST               True
              602  STORE_FAST               'ret_bool'
              604  JUMP_FORWARD        618  'to 618'
            606_0  COME_FROM           596  '596'

 L. 304       606  LOAD_CONST               False
              608  STORE_FAST               'ret_bool'

 L. 305       610  LOAD_FAST                'ret_bool'
              612  LOAD_FAST                'ret_list'
              614  BUILD_TUPLE_2         2 
              616  RETURN_VALUE     
            618_0  COME_FROM           604  '604'
              618  POP_BLOCK        
              620  JUMP_FORWARD        662  'to 662'
            622_0  COME_FROM_EXCEPT    580  '580'

 L. 306       622  DUP_TOP          
              624  LOAD_GLOBAL              AttributeError
              626  COMPARE_OP               exception-match
          628_630  POP_JUMP_IF_FALSE   660  'to 660'
              632  POP_TOP          
              634  POP_TOP          
              636  POP_TOP          

 L. 307       638  LOAD_FAST                'ret_list'
              640  LOAD_METHOD              append
              642  LOAD_GLOBAL              str
              644  LOAD_FAST                'i'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  LOAD_STR                 ' setterOperationID'
              650  BINARY_ADD       
              652  CALL_METHOD_1         1  '1 positional argument'
              654  POP_TOP          
              656  POP_EXCEPT       
              658  JUMP_FORWARD        662  'to 662'
            660_0  COME_FROM           628  '628'
              660  END_FINALLY      
            662_0  COME_FROM           658  '658'
            662_1  COME_FROM           620  '620'

 L. 309       662  SETUP_EXCEPT        704  'to 704'

 L. 310       664  LOAD_FAST                'deserialized'
              666  LOAD_ATTR                metaClassID
              668  LOAD_FAST                'orig_val'
              670  LOAD_FAST                'i'
              672  BINARY_SUBSCR    
              674  LOAD_ATTR                metaClassID
              676  COMPARE_OP               ==
          678_680  POP_JUMP_IF_FALSE   688  'to 688'

 L. 311       682  LOAD_CONST               True
              684  STORE_FAST               'ret_bool'
              686  JUMP_FORWARD        700  'to 700'
            688_0  COME_FROM           678  '678'

 L. 313       688  LOAD_CONST               False
              690  STORE_FAST               'ret_bool'

 L. 314       692  LOAD_FAST                'ret_bool'
              694  LOAD_FAST                'ret_list'
              696  BUILD_TUPLE_2         2 
              698  RETURN_VALUE     
            700_0  COME_FROM           686  '686'
              700  POP_BLOCK        
              702  JUMP_FORWARD        744  'to 744'
            704_0  COME_FROM_EXCEPT    662  '662'

 L. 315       704  DUP_TOP          
              706  LOAD_GLOBAL              AttributeError
              708  COMPARE_OP               exception-match
          710_712  POP_JUMP_IF_FALSE   742  'to 742'
              714  POP_TOP          
              716  POP_TOP          
              718  POP_TOP          

 L. 316       720  LOAD_FAST                'ret_list'
              722  LOAD_METHOD              append
              724  LOAD_GLOBAL              str
              726  LOAD_FAST                'i'
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  LOAD_STR                 ' metaClassID'
              732  BINARY_ADD       
              734  CALL_METHOD_1         1  '1 positional argument'
              736  POP_TOP          
              738  POP_EXCEPT       
              740  JUMP_FORWARD        744  'to 744'
            742_0  COME_FROM           710  '710'
              742  END_FINALLY      
            744_0  COME_FROM           740  '740'
            744_1  COME_FROM           702  '702'

 L. 318       744  SETUP_EXCEPT        786  'to 786'

 L. 319       746  LOAD_FAST                'deserialized'
              748  LOAD_ATTR                namespaceID
              750  LOAD_FAST                'orig_val'
              752  LOAD_FAST                'i'
              754  BINARY_SUBSCR    
              756  LOAD_ATTR                namespaceID
              758  COMPARE_OP               ==
          760_762  POP_JUMP_IF_FALSE   770  'to 770'

 L. 320       764  LOAD_CONST               True
              766  STORE_FAST               'ret_bool'
              768  JUMP_FORWARD        782  'to 782'
            770_0  COME_FROM           760  '760'

 L. 322       770  LOAD_CONST               False
              772  STORE_FAST               'ret_bool'

 L. 323       774  LOAD_FAST                'ret_bool'
              776  LOAD_FAST                'ret_list'
              778  BUILD_TUPLE_2         2 
              780  RETURN_VALUE     
            782_0  COME_FROM           768  '768'
              782  POP_BLOCK        
              784  JUMP_FORWARD        826  'to 826'
            786_0  COME_FROM_EXCEPT    744  '744'

 L. 324       786  DUP_TOP          
              788  LOAD_GLOBAL              AttributeError
              790  COMPARE_OP               exception-match
          792_794  POP_JUMP_IF_FALSE   824  'to 824'
              796  POP_TOP          
              798  POP_TOP          
              800  POP_TOP          

 L. 325       802  LOAD_FAST                'ret_list'
              804  LOAD_METHOD              append
              806  LOAD_GLOBAL              str
              808  LOAD_FAST                'i'
              810  CALL_FUNCTION_1       1  '1 positional argument'
              812  LOAD_STR                 ' namespaceID'
              814  BINARY_ADD       
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          
              820  POP_EXCEPT       
              822  JUMP_FORWARD        826  'to 826'
            824_0  COME_FROM           792  '792'
              824  END_FINALLY      
            826_0  COME_FROM           822  '822'
            826_1  COME_FROM           784  '784'

 L. 327       826  SETUP_EXCEPT        868  'to 868'

 L. 328       828  LOAD_FAST                'deserialized'
              830  LOAD_ATTR                languageDepInfos
              832  LOAD_FAST                'orig_val'
              834  LOAD_FAST                'i'
              836  BINARY_SUBSCR    
              838  LOAD_ATTR                languageDepInfos
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE   852  'to 852'

 L. 329       846  LOAD_CONST               True
              848  STORE_FAST               'ret_bool'
              850  JUMP_FORWARD        864  'to 864'
            852_0  COME_FROM           842  '842'

 L. 331       852  LOAD_CONST               False
              854  STORE_FAST               'ret_bool'

 L. 332       856  LOAD_FAST                'ret_bool'
              858  LOAD_FAST                'ret_list'
              860  BUILD_TUPLE_2         2 
              862  RETURN_VALUE     
            864_0  COME_FROM           850  '850'
              864  POP_BLOCK        
              866  JUMP_FORWARD       1682  'to 1682'
            868_0  COME_FROM_EXCEPT    826  '826'

 L. 334       868  DUP_TOP          
              870  LOAD_GLOBAL              AttributeError
              872  COMPARE_OP               exception-match
          874_876  POP_JUMP_IF_FALSE   906  'to 906'
              878  POP_TOP          
              880  POP_TOP          
              882  POP_TOP          

 L. 335       884  LOAD_FAST                'ret_list'
              886  LOAD_METHOD              append
              888  LOAD_GLOBAL              str
              890  LOAD_FAST                'i'
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  LOAD_STR                 ' languageDepInfos'
              896  BINARY_ADD       
              898  CALL_METHOD_1         1  '1 positional argument'
              900  POP_TOP          
              902  POP_EXCEPT       
              904  JUMP_FORWARD       1682  'to 1682'
            906_0  COME_FROM           874  '874'
              906  END_FINALLY      
          908_910  JUMP_FORWARD       1682  'to 1682'
            912_0  COME_FROM            14  '14'

 L. 338       912  SETUP_EXCEPT        950  'to 950'

 L. 339       914  LOAD_FAST                'deserialized'
              916  LOAD_ATTR                namespace
              918  LOAD_FAST                'orig_val'
              920  LOAD_ATTR                namespace
              922  COMPARE_OP               ==
          924_926  POP_JUMP_IF_FALSE   934  'to 934'

 L. 340       928  LOAD_CONST               True
              930  STORE_FAST               'ret_bool'
              932  JUMP_FORWARD        946  'to 946'
            934_0  COME_FROM           924  '924'

 L. 342       934  LOAD_CONST               False
              936  STORE_FAST               'ret_bool'

 L. 343       938  LOAD_FAST                'ret_bool'
              940  LOAD_FAST                'ret_list'
              942  BUILD_TUPLE_2         2 
              944  RETURN_VALUE     
            946_0  COME_FROM           932  '932'
              946  POP_BLOCK        
              948  JUMP_FORWARD        982  'to 982'
            950_0  COME_FROM_EXCEPT    912  '912'

 L. 345       950  DUP_TOP          
              952  LOAD_GLOBAL              AttributeError
              954  COMPARE_OP               exception-match
          956_958  POP_JUMP_IF_FALSE   980  'to 980'
              960  POP_TOP          
              962  POP_TOP          
              964  POP_TOP          

 L. 346       966  LOAD_FAST                'ret_list'
              968  LOAD_METHOD              append
              970  LOAD_STR                 'namespace'
              972  CALL_METHOD_1         1  '1 positional argument'
              974  POP_TOP          
              976  POP_EXCEPT       
              978  JUMP_FORWARD        982  'to 982'
            980_0  COME_FROM           956  '956'
              980  END_FINALLY      
            982_0  COME_FROM           978  '978'
            982_1  COME_FROM           948  '948'

 L. 348       982  SETUP_EXCEPT       1020  'to 1020'

 L. 349       984  LOAD_FAST                'deserialized'
              986  LOAD_ATTR                className
              988  LOAD_FAST                'orig_val'
              990  LOAD_ATTR                className
              992  COMPARE_OP               ==
          994_996  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 350       998  LOAD_CONST               True
             1000  STORE_FAST               'ret_bool'
             1002  JUMP_FORWARD       1016  'to 1016'
           1004_0  COME_FROM           994  '994'

 L. 352      1004  LOAD_CONST               False
             1006  STORE_FAST               'ret_bool'

 L. 353      1008  LOAD_FAST                'ret_bool'
             1010  LOAD_FAST                'ret_list'
             1012  BUILD_TUPLE_2         2 
             1014  RETURN_VALUE     
           1016_0  COME_FROM          1002  '1002'
             1016  POP_BLOCK        
             1018  JUMP_FORWARD       1052  'to 1052'
           1020_0  COME_FROM_EXCEPT    982  '982'

 L. 355      1020  DUP_TOP          
             1022  LOAD_GLOBAL              AttributeError
             1024  COMPARE_OP               exception-match
         1026_1028  POP_JUMP_IF_FALSE  1050  'to 1050'
             1030  POP_TOP          
             1032  POP_TOP          
             1034  POP_TOP          

 L. 356      1036  LOAD_FAST                'ret_list'
             1038  LOAD_METHOD              append
             1040  LOAD_STR                 'className'
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  POP_TOP          
             1046  POP_EXCEPT       
             1048  JUMP_FORWARD       1052  'to 1052'
           1050_0  COME_FROM          1026  '1026'
             1050  END_FINALLY      
           1052_0  COME_FROM          1048  '1048'
           1052_1  COME_FROM          1018  '1018'

 L. 358      1052  SETUP_EXCEPT       1090  'to 1090'

 L. 359      1054  LOAD_FAST                'deserialized'
             1056  LOAD_ATTR                getterImplementationID
             1058  LOAD_FAST                'orig_val'
             1060  LOAD_ATTR                getterImplementationID
             1062  COMPARE_OP               ==
         1064_1066  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 360      1068  LOAD_CONST               True
             1070  STORE_FAST               'ret_bool'
             1072  JUMP_FORWARD       1086  'to 1086'
           1074_0  COME_FROM          1064  '1064'

 L. 362      1074  LOAD_CONST               False
             1076  STORE_FAST               'ret_bool'

 L. 363      1078  LOAD_FAST                'ret_bool'
             1080  LOAD_FAST                'ret_list'
             1082  BUILD_TUPLE_2         2 
             1084  RETURN_VALUE     
           1086_0  COME_FROM          1072  '1072'
             1086  POP_BLOCK        
             1088  JUMP_FORWARD       1122  'to 1122'
           1090_0  COME_FROM_EXCEPT   1052  '1052'

 L. 365      1090  DUP_TOP          
             1092  LOAD_GLOBAL              AttributeError
             1094  COMPARE_OP               exception-match
         1096_1098  POP_JUMP_IF_FALSE  1120  'to 1120'
             1100  POP_TOP          
             1102  POP_TOP          
             1104  POP_TOP          

 L. 366      1106  LOAD_FAST                'ret_list'
             1108  LOAD_METHOD              append
             1110  LOAD_STR                 'getterImplementationID'
             1112  CALL_METHOD_1         1  '1 positional argument'
             1114  POP_TOP          
             1116  POP_EXCEPT       
             1118  JUMP_FORWARD       1122  'to 1122'
           1120_0  COME_FROM          1096  '1096'
             1120  END_FINALLY      
           1122_0  COME_FROM          1118  '1118'
           1122_1  COME_FROM          1088  '1088'

 L. 368      1122  SETUP_EXCEPT       1160  'to 1160'

 L. 369      1124  LOAD_FAST                'deserialized'
             1126  LOAD_ATTR                setterImplementationID
             1128  LOAD_FAST                'orig_val'
             1130  LOAD_ATTR                setterImplementationID
             1132  COMPARE_OP               ==
         1134_1136  POP_JUMP_IF_FALSE  1144  'to 1144'

 L. 370      1138  LOAD_CONST               True
             1140  STORE_FAST               'ret_bool'
             1142  JUMP_FORWARD       1156  'to 1156'
           1144_0  COME_FROM          1134  '1134'

 L. 372      1144  LOAD_CONST               False
             1146  STORE_FAST               'ret_bool'

 L. 373      1148  LOAD_FAST                'ret_bool'
             1150  LOAD_FAST                'ret_list'
             1152  BUILD_TUPLE_2         2 
             1154  RETURN_VALUE     
           1156_0  COME_FROM          1142  '1142'
             1156  POP_BLOCK        
             1158  JUMP_FORWARD       1192  'to 1192'
           1160_0  COME_FROM_EXCEPT   1122  '1122'

 L. 374      1160  DUP_TOP          
             1162  LOAD_GLOBAL              AttributeError
             1164  COMPARE_OP               exception-match
         1166_1168  POP_JUMP_IF_FALSE  1190  'to 1190'
             1170  POP_TOP          
             1172  POP_TOP          
             1174  POP_TOP          

 L. 375      1176  LOAD_FAST                'ret_list'
             1178  LOAD_METHOD              append
             1180  LOAD_STR                 'setterImplementationID'
             1182  CALL_METHOD_1         1  '1 positional argument'
             1184  POP_TOP          
             1186  POP_EXCEPT       
             1188  JUMP_FORWARD       1192  'to 1192'
           1190_0  COME_FROM          1166  '1166'
             1190  END_FINALLY      
           1192_0  COME_FROM          1188  '1188'
           1192_1  COME_FROM          1158  '1158'

 L. 377      1192  SETUP_EXCEPT       1230  'to 1230'

 L. 378      1194  LOAD_FAST                'deserialized'
             1196  LOAD_ATTR                name
             1198  LOAD_FAST                'orig_val'
             1200  LOAD_ATTR                name
             1202  COMPARE_OP               ==
         1204_1206  POP_JUMP_IF_FALSE  1214  'to 1214'

 L. 379      1208  LOAD_CONST               True
             1210  STORE_FAST               'ret_bool'
             1212  JUMP_FORWARD       1226  'to 1226'
           1214_0  COME_FROM          1204  '1204'

 L. 381      1214  LOAD_CONST               False
             1216  STORE_FAST               'ret_bool'

 L. 382      1218  LOAD_FAST                'ret_bool'
             1220  LOAD_FAST                'ret_list'
             1222  BUILD_TUPLE_2         2 
             1224  RETURN_VALUE     
           1226_0  COME_FROM          1212  '1212'
             1226  POP_BLOCK        
             1228  JUMP_FORWARD       1262  'to 1262'
           1230_0  COME_FROM_EXCEPT   1192  '1192'

 L. 383      1230  DUP_TOP          
             1232  LOAD_GLOBAL              AttributeError
             1234  COMPARE_OP               exception-match
         1236_1238  POP_JUMP_IF_FALSE  1260  'to 1260'
             1240  POP_TOP          
             1242  POP_TOP          
             1244  POP_TOP          

 L. 384      1246  LOAD_FAST                'ret_list'
             1248  LOAD_METHOD              append
             1250  LOAD_STR                 'name'
             1252  CALL_METHOD_1         1  '1 positional argument'
             1254  POP_TOP          
             1256  POP_EXCEPT       
             1258  JUMP_FORWARD       1262  'to 1262'
           1260_0  COME_FROM          1236  '1236'
             1260  END_FINALLY      
           1262_0  COME_FROM          1258  '1258'
           1262_1  COME_FROM          1228  '1228'

 L. 386      1262  SETUP_EXCEPT       1300  'to 1300'

 L. 387      1264  LOAD_FAST                'deserialized'
             1266  LOAD_ATTR                position
             1268  LOAD_FAST                'orig_val'
             1270  LOAD_ATTR                position
             1272  COMPARE_OP               ==
         1274_1276  POP_JUMP_IF_FALSE  1284  'to 1284'

 L. 388      1278  LOAD_CONST               True
             1280  STORE_FAST               'ret_bool'
             1282  JUMP_FORWARD       1296  'to 1296'
           1284_0  COME_FROM          1274  '1274'

 L. 390      1284  LOAD_CONST               False
             1286  STORE_FAST               'ret_bool'

 L. 391      1288  LOAD_FAST                'ret_bool'
             1290  LOAD_FAST                'ret_list'
             1292  BUILD_TUPLE_2         2 
             1294  RETURN_VALUE     
           1296_0  COME_FROM          1282  '1282'
             1296  POP_BLOCK        
             1298  JUMP_FORWARD       1332  'to 1332'
           1300_0  COME_FROM_EXCEPT   1262  '1262'

 L. 392      1300  DUP_TOP          
             1302  LOAD_GLOBAL              AttributeError
             1304  COMPARE_OP               exception-match
         1306_1308  POP_JUMP_IF_FALSE  1330  'to 1330'
             1310  POP_TOP          
             1312  POP_TOP          
             1314  POP_TOP          

 L. 393      1316  LOAD_FAST                'ret_list'
             1318  LOAD_METHOD              append
             1320  LOAD_STR                 'position'
             1322  CALL_METHOD_1         1  '1 positional argument'
             1324  POP_TOP          
             1326  POP_EXCEPT       
             1328  JUMP_FORWARD       1332  'to 1332'
           1330_0  COME_FROM          1306  '1306'
             1330  END_FINALLY      
           1332_0  COME_FROM          1328  '1328'
           1332_1  COME_FROM          1298  '1298'

 L. 395      1332  SETUP_EXCEPT       1370  'to 1370'

 L. 396      1334  LOAD_FAST                'deserialized'
             1336  LOAD_ATTR                getterOperationID
             1338  LOAD_FAST                'orig_val'
             1340  LOAD_ATTR                getterOperationID
             1342  COMPARE_OP               ==
         1344_1346  POP_JUMP_IF_FALSE  1354  'to 1354'

 L. 397      1348  LOAD_CONST               True
             1350  STORE_FAST               'ret_bool'
             1352  JUMP_FORWARD       1366  'to 1366'
           1354_0  COME_FROM          1344  '1344'

 L. 399      1354  LOAD_CONST               False
             1356  STORE_FAST               'ret_bool'

 L. 400      1358  LOAD_FAST                'ret_bool'
             1360  LOAD_FAST                'ret_list'
             1362  BUILD_TUPLE_2         2 
             1364  RETURN_VALUE     
           1366_0  COME_FROM          1352  '1352'
             1366  POP_BLOCK        
             1368  JUMP_FORWARD       1402  'to 1402'
           1370_0  COME_FROM_EXCEPT   1332  '1332'

 L. 401      1370  DUP_TOP          
             1372  LOAD_GLOBAL              AttributeError
             1374  COMPARE_OP               exception-match
         1376_1378  POP_JUMP_IF_FALSE  1400  'to 1400'
             1380  POP_TOP          
             1382  POP_TOP          
             1384  POP_TOP          

 L. 402      1386  LOAD_FAST                'ret_list'
             1388  LOAD_METHOD              append
             1390  LOAD_STR                 'getterOperationID'
             1392  CALL_METHOD_1         1  '1 positional argument'
             1394  POP_TOP          
             1396  POP_EXCEPT       
             1398  JUMP_FORWARD       1402  'to 1402'
           1400_0  COME_FROM          1376  '1376'
             1400  END_FINALLY      
           1402_0  COME_FROM          1398  '1398'
           1402_1  COME_FROM          1368  '1368'

 L. 404      1402  SETUP_EXCEPT       1440  'to 1440'

 L. 405      1404  LOAD_FAST                'deserialized'
             1406  LOAD_ATTR                setterOperationID
             1408  LOAD_FAST                'orig_val'
             1410  LOAD_ATTR                setterOperationID
             1412  COMPARE_OP               ==
         1414_1416  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 406      1418  LOAD_CONST               True
             1420  STORE_FAST               'ret_bool'
             1422  JUMP_FORWARD       1436  'to 1436'
           1424_0  COME_FROM          1414  '1414'

 L. 408      1424  LOAD_CONST               False
             1426  STORE_FAST               'ret_bool'

 L. 409      1428  LOAD_FAST                'ret_bool'
             1430  LOAD_FAST                'ret_list'
             1432  BUILD_TUPLE_2         2 
             1434  RETURN_VALUE     
           1436_0  COME_FROM          1422  '1422'
             1436  POP_BLOCK        
             1438  JUMP_FORWARD       1472  'to 1472'
           1440_0  COME_FROM_EXCEPT   1402  '1402'

 L. 410      1440  DUP_TOP          
             1442  LOAD_GLOBAL              AttributeError
             1444  COMPARE_OP               exception-match
         1446_1448  POP_JUMP_IF_FALSE  1470  'to 1470'
             1450  POP_TOP          
             1452  POP_TOP          
             1454  POP_TOP          

 L. 411      1456  LOAD_FAST                'ret_list'
             1458  LOAD_METHOD              append
             1460  LOAD_STR                 'setterOperationID'
             1462  CALL_METHOD_1         1  '1 positional argument'
             1464  POP_TOP          
             1466  POP_EXCEPT       
             1468  JUMP_FORWARD       1472  'to 1472'
           1470_0  COME_FROM          1446  '1446'
             1470  END_FINALLY      
           1472_0  COME_FROM          1468  '1468'
           1472_1  COME_FROM          1438  '1438'

 L. 413      1472  SETUP_EXCEPT       1510  'to 1510'

 L. 414      1474  LOAD_FAST                'deserialized'
             1476  LOAD_ATTR                metaClassID
             1478  LOAD_FAST                'orig_val'
             1480  LOAD_ATTR                metaClassID
             1482  COMPARE_OP               ==
         1484_1486  POP_JUMP_IF_FALSE  1494  'to 1494'

 L. 415      1488  LOAD_CONST               True
             1490  STORE_FAST               'ret_bool'
             1492  JUMP_FORWARD       1506  'to 1506'
           1494_0  COME_FROM          1484  '1484'

 L. 417      1494  LOAD_CONST               False
             1496  STORE_FAST               'ret_bool'

 L. 418      1498  LOAD_FAST                'ret_bool'
             1500  LOAD_FAST                'ret_list'
             1502  BUILD_TUPLE_2         2 
             1504  RETURN_VALUE     
           1506_0  COME_FROM          1492  '1492'
             1506  POP_BLOCK        
             1508  JUMP_FORWARD       1542  'to 1542'
           1510_0  COME_FROM_EXCEPT   1472  '1472'

 L. 419      1510  DUP_TOP          
             1512  LOAD_GLOBAL              AttributeError
             1514  COMPARE_OP               exception-match
         1516_1518  POP_JUMP_IF_FALSE  1540  'to 1540'
             1520  POP_TOP          
             1522  POP_TOP          
             1524  POP_TOP          

 L. 420      1526  LOAD_FAST                'ret_list'
             1528  LOAD_METHOD              append
             1530  LOAD_STR                 'metaClassID'
             1532  CALL_METHOD_1         1  '1 positional argument'
             1534  POP_TOP          
             1536  POP_EXCEPT       
             1538  JUMP_FORWARD       1542  'to 1542'
           1540_0  COME_FROM          1516  '1516'
             1540  END_FINALLY      
           1542_0  COME_FROM          1538  '1538'
           1542_1  COME_FROM          1508  '1508'

 L. 422      1542  SETUP_EXCEPT       1580  'to 1580'

 L. 423      1544  LOAD_FAST                'deserialized'
             1546  LOAD_ATTR                namespaceID
             1548  LOAD_FAST                'orig_val'
             1550  LOAD_ATTR                namespaceID
             1552  COMPARE_OP               ==
         1554_1556  POP_JUMP_IF_FALSE  1564  'to 1564'

 L. 424      1558  LOAD_CONST               True
             1560  STORE_FAST               'ret_bool'
             1562  JUMP_FORWARD       1576  'to 1576'
           1564_0  COME_FROM          1554  '1554'

 L. 426      1564  LOAD_CONST               False
             1566  STORE_FAST               'ret_bool'

 L. 427      1568  LOAD_FAST                'ret_bool'
             1570  LOAD_FAST                'ret_list'
             1572  BUILD_TUPLE_2         2 
             1574  RETURN_VALUE     
           1576_0  COME_FROM          1562  '1562'
             1576  POP_BLOCK        
             1578  JUMP_FORWARD       1612  'to 1612'
           1580_0  COME_FROM_EXCEPT   1542  '1542'

 L. 428      1580  DUP_TOP          
             1582  LOAD_GLOBAL              AttributeError
             1584  COMPARE_OP               exception-match
         1586_1588  POP_JUMP_IF_FALSE  1610  'to 1610'
             1590  POP_TOP          
             1592  POP_TOP          
             1594  POP_TOP          

 L. 429      1596  LOAD_FAST                'ret_list'
             1598  LOAD_METHOD              append
             1600  LOAD_STR                 'namespaceID'
             1602  CALL_METHOD_1         1  '1 positional argument'
             1604  POP_TOP          
             1606  POP_EXCEPT       
             1608  JUMP_FORWARD       1612  'to 1612'
           1610_0  COME_FROM          1586  '1586'
             1610  END_FINALLY      
           1612_0  COME_FROM          1608  '1608'
           1612_1  COME_FROM          1578  '1578'

 L. 431      1612  SETUP_EXCEPT       1650  'to 1650'

 L. 432      1614  LOAD_FAST                'deserialized'
             1616  LOAD_ATTR                languageDepInfos
             1618  LOAD_FAST                'orig_val'
             1620  LOAD_ATTR                languageDepInfos
             1622  COMPARE_OP               ==
         1624_1626  POP_JUMP_IF_FALSE  1634  'to 1634'

 L. 433      1628  LOAD_CONST               True
             1630  STORE_FAST               'ret_bool'
             1632  JUMP_FORWARD       1646  'to 1646'
           1634_0  COME_FROM          1624  '1624'

 L. 435      1634  LOAD_CONST               False
             1636  STORE_FAST               'ret_bool'
           1638_0  COME_FROM           866  '866'

 L. 436      1638  LOAD_FAST                'ret_bool'
             1640  LOAD_FAST                'ret_list'
             1642  BUILD_TUPLE_2         2 
             1644  RETURN_VALUE     
           1646_0  COME_FROM          1632  '1632'
             1646  POP_BLOCK        
             1648  JUMP_FORWARD       1682  'to 1682'
           1650_0  COME_FROM_EXCEPT   1612  '1612'

 L. 438      1650  DUP_TOP          
             1652  LOAD_GLOBAL              AttributeError
             1654  COMPARE_OP               exception-match
         1656_1658  POP_JUMP_IF_FALSE  1680  'to 1680'
             1660  POP_TOP          
             1662  POP_TOP          
             1664  POP_TOP          

 L. 439      1666  LOAD_FAST                'ret_list'
             1668  LOAD_METHOD              append
             1670  LOAD_STR                 'languageDepInfos'
             1672  CALL_METHOD_1         1  '1 positional argument'
             1674  POP_TOP          
           1676_0  COME_FROM           904  '904'
             1676  POP_EXCEPT       
             1678  JUMP_FORWARD       1682  'to 1682'
           1680_0  COME_FROM          1656  '1656'
             1680  END_FINALLY      
           1682_0  COME_FROM          1678  '1678'
           1682_1  COME_FROM          1648  '1648'
           1682_2  COME_FROM           908  '908'

 L. 441      1682  LOAD_FAST                'ret_bool'
             1684  LOAD_FAST                'ret_list'
             1686  BUILD_TUPLE_2         2 
             1688  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 1646

    @staticmethod
    def op_equal(deserialized, orig_val, b_par=False):
        ret_bool = True
        ret_list = []
        try:
            if deserialized.namespace == orig_val.namespace:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('namespace')

        try:
            if deserialized.className == orig_val.className:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('className')

        try:
            if deserialized.descriptor == orig_val.descriptor:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('descriptor')

        try:
            if deserialized.signature == orig_val.signature:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('signature')

        try:
            if deserialized.name == orig_val.name:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('name')

        try:
            if deserialized.nameAndDescriptor == orig_val.nameAndDescriptor:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('nameAndDescriptor')

        if b_par:
            try:
                if deserialized.params == orig_val.params:
                    ret_bool = True
                else:
                    ret_bool = False
                    return (ret_bool, ret_list)
            except AttributeError:
                ret_list.append('params')

            try:
                if deserialized.returnType == orig_val.returnType:
                    ret_bool = True
                else:
                    ret_bool = False
                    return (ret_bool, ret_list)
            except AttributeError:
                ret_list.append('returnType')

            try:
                if deserialized.implementations == orig_val.implementations:
                    ret_bool = True
                else:
                    ret_bool = False
                    return (ret_bool, ret_list)
            except AttributeError:
                ret_list.append('implementations')

        try:
            if deserialized.paramsOrder == orig_val.paramsOrder:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('paramsOrder')

        try:
            if deserialized.isAbstract == orig_val.isAbstract:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('isAbstract')

        try:
            if deserialized.isStaticConstructor == orig_val.isStaticConstructor:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('isStaticConstructor')

        try:
            if deserialized.metaClassID == orig_val.metaClassID:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('metaClassID')

        try:
            if deserialized.namespaceID == orig_val.namespaceID:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('namespaceID')

        try:
            if deserialized.languageDepInfos == orig_val.languageDepInfos:
                ret_bool = True
            else:
                ret_bool = False
                return (ret_bool, ret_list)
        except AttributeError:
            ret_list.append('languageDepInfos')

        return (ret_bool, ret_list)