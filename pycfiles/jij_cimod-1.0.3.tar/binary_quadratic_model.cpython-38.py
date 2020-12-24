# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/ssd/workspace/linux/workspace/Jij/cimod/cimod/model/binary_quadratic_model.py
# Compiled at: 2020-05-10 01:06:29
# Size of source mod 2**32: 12659 bytes
import cxxcimod
from cimod.vartype import to_cxxcimod
from cimod.utils.decolator import recalc
import dimod, numpy as np

def make_BinaryQuadraticModel(linear, quadratic):
    """BinaryQuadraticModel factory. 
       Generate BinaryQuadraticModel class with the base class specified by the arguments linear and quadratic
    Args:
        linear (dict): linear bias
        quadratic (dict): quadratic bias
    Returns:
        generated BinaryQuadraticModel class
    """
    index = set()
    base = None
    if linear != {}:
        index.add(next(iter(linear)))
    elif quadratic != {}:
        index.add(next(iter(quadratic))[0])
        index.add(next(iter(quadratic))[1])
    elif len(set((type(i) for i in index))) != 1:
        raise TypeError('invalid types of linear and quadratic')
    else:
        ind = next(iter(index))
        if isinstance(ind, int):
            base = cxxcimod.BinaryQuadraticModel
        else:
            if isinstance(ind, str):
                base = cxxcimod.BinaryQuadraticModel_str
            else:
                if isinstance(ind, tuple):
                    if len(ind) == 2:
                        base = cxxcimod.BinaryQuadraticModel_tuple2
                    else:
                        if len(ind) == 3:
                            base = cxxcimod.BinaryQuadraticModel_tuple3
                        else:
                            if len(ind) == 4:
                                base = cxxcimod.BinaryQuadraticModel_tuple4
                            else:
                                raise TypeError('invalid length of tuple')
                else:
                    raise TypeError('invalid types of linear and quadratic')

    class BinaryQuadraticModel(base):
        __doc__ = 'Represents Binary quadratic model. \n           Note that the indices are converted to the integers internally. \n           The dictionaries between indices and integers are self.ind_to_num (indices -> integers) and self.num_to_ind (integers -> indices).\n           Indices are listed in self._indices.\n        Attributes:\n            var_type (cimod.VariableType): variable type SPIN or BINARY\n            linear (dict): represents linear term\n            quadratic (dict): represents quadratic term\n            adj (dict): represents adjacency\n            indices (list): labels of each variables sorted by results variables\n            ind_to_num (list): map which specifies where the index is in self._indices\n            offset (float): represents constant energy term when convert to SPIN from BINARY\n        '

        def __init__(self, linear, quadratic, offset=0.0, var_type=dimod.SPIN, **kwargs):
            super().__init__(linear, quadratic, offset, to_cxxcimod(var_type))
            self._init_process()

        def _init_process(self):
            self._re_calculate = True
            self._re_calculate_indices = True
            self._interaction_matrix = None
            self._indices = None
            self._ind_to_num = None

        @property
        def linear(self):
            return self.get_linear()

        @property
        def quadratic(self):
            return self.get_quadratic()

        @property
        def adj(self):
            return self.get_adjacency()

        @property
        def vartype(self):
            vartype = super().get_vartype()
            if vartype == cxxcimod.Vartype.SPIN:
                return dimod.SPIN
            return dimod.BINARY

        @property
        def offset(self):
            return self.get_offset()

        @property
        def indices(self):
            ind, _ = self.update_indices()
            return ind

        def update_indices(self):
            """calculate self._indices and self.ind_to_num
            Returns:
                self._indices and self._ind_to_num
            """
            if self._re_calculate_indices is True:
                self._indices = self._generate_indices()
                self._ind_to_num = {num:ind for num, ind in enumerate(self._indices)}
                self._re_calculate_indices = False
            return (self._indices, self._ind_to_num)

        def interaction_matrix(self):
            if self._re_calculate is True:
                indices, ind_to_num = self.update_indices()
                self._interaction_matrix = super().interaction_matrix(indices)
                self._re_calculate = False
            return self._interaction_matrix

        def energy--- This code section failed: ---

 L. 169         0  LOAD_FAST                'self'
                2  LOAD_METHOD              update_indices
                4  CALL_METHOD_0         0  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_DEREF              'indices'
               10  STORE_FAST               'ind_to_num'

 L. 172        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'sample'
               16  LOAD_GLOBAL              list
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     34  'to 34'
               22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'sample'
               26  LOAD_GLOBAL              np
               28  LOAD_ATTR                ndarray
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    56  'to 56'
             34_0  COME_FROM            20  '20'

 L. 173        34  LOAD_CLOSURE             'indices'
               36  BUILD_TUPLE_1         1 
               38  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               40  LOAD_STR                 'make_BinaryQuadraticModel.<locals>.BinaryQuadraticModel.energy.<locals>.<dictcomp>'
               42  MAKE_FUNCTION_8          'closure'
               44  LOAD_GLOBAL              enumerate
               46  LOAD_FAST                'sample'
               48  CALL_FUNCTION_1       1  ''
               50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'sample'
             56_0  COME_FROM            32  '32'

 L. 176        56  LOAD_FAST                'convert_sample'
               58  POP_JUMP_IF_FALSE   138  'to 138'

 L. 177        60  LOAD_FAST                'sample'
               62  LOAD_METHOD              keys
               64  CALL_METHOD_0         0  ''
               66  GET_ITER         
             68_0  COME_FROM           126  '126'
             68_1  COME_FROM           114  '114'
               68  FOR_ITER            138  'to 138'
               70  STORE_FAST               'k'

 L. 178        72  LOAD_FAST                'sample'
               74  LOAD_FAST                'k'
               76  BINARY_SUBSCR    
               78  LOAD_CONST               -1
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   104  'to 104'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                vartype
               88  LOAD_GLOBAL              dimod
               90  LOAD_ATTR                BINARY
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 179        96  LOAD_CONST               0
               98  LOAD_FAST                'sample'
              100  LOAD_FAST                'k'
              102  STORE_SUBSCR     
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            82  '82'

 L. 180       104  LOAD_FAST                'sample'
              106  LOAD_FAST                'k'
              108  BINARY_SUBSCR    
              110  LOAD_CONST               0
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE    68  'to 68'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                vartype
              120  LOAD_GLOBAL              dimod
              122  LOAD_ATTR                SPIN
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE    68  'to 68'

 L. 181       128  LOAD_CONST               -1
              130  LOAD_FAST                'sample'
              132  LOAD_FAST                'k'
              134  STORE_SUBSCR     
              136  JUMP_BACK            68  'to 68'
            138_0  COME_FROM            58  '58'

 L. 183       138  LOAD_FAST                'sparse'
              140  POP_JUMP_IF_FALSE   154  'to 154'

 L. 184       142  LOAD_GLOBAL              super
              144  CALL_FUNCTION_0       0  ''
              146  LOAD_METHOD              energy
              148  LOAD_FAST                'sample'
              150  CALL_METHOD_1         1  ''
              152  RETURN_VALUE     
            154_0  COME_FROM           140  '140'

 L. 188       154  LOAD_GLOBAL              isinstance
              156  LOAD_FAST                'sample'
              158  LOAD_GLOBAL              dict
              160  CALL_FUNCTION_2       2  ''
              162  POP_JUMP_IF_FALSE   212  'to 212'

 L. 189       164  LOAD_CONST               0
              166  BUILD_LIST_1          1 
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'sample'
              172  CALL_FUNCTION_1       1  ''
              174  BINARY_MULTIPLY  
              176  STORE_FAST               'state'

 L. 190       178  LOAD_FAST                'sample'
              180  LOAD_METHOD              items
              182  CALL_METHOD_0         0  ''
              184  GET_ITER         
              186  FOR_ITER            208  'to 208'
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'k'
              192  STORE_FAST               'v'

 L. 191       194  LOAD_FAST                'v'
              196  LOAD_FAST                'state'
              198  LOAD_FAST                'ind_to_num'
              200  LOAD_FAST                'k'
              202  BINARY_SUBSCR    
              204  STORE_SUBSCR     
              206  JUMP_BACK           186  'to 186'

 L. 192       208  LOAD_FAST                'state'
              210  STORE_FAST               'sample'
            212_0  COME_FROM           162  '162'

 L. 194       212  LOAD_GLOBAL              np
              214  LOAD_METHOD              array
              216  LOAD_FAST                'sample'
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'sample'

 L. 196       222  LOAD_FAST                'self'
              224  LOAD_METHOD              interaction_matrix
              226  CALL_METHOD_0         0  ''
              228  STORE_FAST               'int_mat'

 L. 199       230  LOAD_FAST                'self'
              232  LOAD_ATTR                vartype
              234  LOAD_GLOBAL              dimod
              236  LOAD_ATTR                BINARY
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   278  'to 278'

 L. 200       244  LOAD_GLOBAL              np
              246  LOAD_METHOD              dot
              248  LOAD_FAST                'sample'
              250  LOAD_GLOBAL              np
              252  LOAD_METHOD              dot
              254  LOAD_GLOBAL              np
              256  LOAD_METHOD              triu
              258  LOAD_FAST                'int_mat'
              260  CALL_METHOD_1         1  ''
              262  LOAD_FAST                'sample'
              264  CALL_METHOD_2         2  ''
              266  CALL_METHOD_2         2  ''
              268  LOAD_FAST                'self'
              270  LOAD_METHOD              get_offset
              272  CALL_METHOD_0         0  ''
              274  BINARY_ADD       
              276  RETURN_VALUE     
            278_0  COME_FROM           240  '240'

 L. 201       278  LOAD_FAST                'self'
              280  LOAD_ATTR                vartype
              282  LOAD_GLOBAL              dimod
              284  LOAD_ATTR                SPIN
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   364  'to 364'

 L. 202       292  LOAD_GLOBAL              np
              294  LOAD_METHOD              diag
              296  LOAD_FAST                'int_mat'
              298  CALL_METHOD_1         1  ''
              300  STORE_FAST               'linear_term'

 L. 203       302  LOAD_GLOBAL              np
              304  LOAD_METHOD              dot
              306  LOAD_FAST                'sample'
              308  LOAD_GLOBAL              np
              310  LOAD_METHOD              dot
              312  LOAD_FAST                'int_mat'
              314  LOAD_FAST                'sample'
              316  CALL_METHOD_2         2  ''
              318  CALL_METHOD_2         2  ''

 L. 204       320  LOAD_GLOBAL              np
              322  LOAD_METHOD              sum
              324  LOAD_FAST                'linear_term'
              326  CALL_METHOD_1         1  ''

 L. 203       328  BINARY_SUBTRACT  

 L. 204       330  LOAD_CONST               2

 L. 203       332  BINARY_TRUE_DIVIDE
              334  STORE_FAST               'energy'

 L. 205       336  LOAD_FAST                'energy'
              338  LOAD_GLOBAL              np
              340  LOAD_METHOD              dot
              342  LOAD_FAST                'linear_term'
              344  LOAD_FAST                'sample'
              346  CALL_METHOD_2         2  ''
              348  INPLACE_ADD      
              350  STORE_FAST               'energy'

 L. 206       352  LOAD_FAST                'energy'
              354  LOAD_FAST                'self'
              356  LOAD_METHOD              get_offset
              358  CALL_METHOD_0         0  ''
              360  INPLACE_ADD      
              362  STORE_FAST               'energy'
            364_0  COME_FROM           288  '288'

 L. 207       364  LOAD_FAST                'energy'
              366  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 38

        def energies(self, samples_like, **kwargs):
            en_vec = []
            for elem in samples_like:
                en_vec.append((self.energy)(elem, **kwargs))
            else:
                return en_vec

        @recalc
        def empty(self, *args, **kwargs):
            return (super().empty)(*args, **kwargs)

        @recalc
        def add_variable(self, *args, **kwargs):
            return (super().add_variable)(*args, **kwargs)

        @recalc
        def add_variables_from(self, *args, **kwargs):
            return (super().add_variables_from)(*args, **kwargs)

        @recalc
        def add_interaction(self, *args, **kwargs):
            return (super().add_interaction)(*args, **kwargs)

        @recalc
        def add_interactions_from(self, *args, **kwargs):
            return (super().add_interactions_from)(*args, **kwargs)

        @recalc
        def remove_variable(self, *args, **kwargs):
            return (super().remove_variable)(*args, **kwargs)

        @recalc
        def remove_variables_from(self, *args, **kwargs):
            return (super().remove_variables_from)(*args, **kwargs)

        @recalc
        def remove_interaction(self, *args, **kwargs):
            return (super().remove_interaction)(*args, **kwargs)

        @recalc
        def remove_interactions_from(self, *args, **kwargs):
            return (super().remove_interactions_from)(*args, **kwargs)

        @recalc
        def add_offset(self, *args, **kwargs):
            return (super().add_offset)(*args, **kwargs)

        @recalc
        def remove_offset(self, *args, **kwargs):
            return (super().remove_offset)(*args, **kwargs)

        @recalc
        def scale(self, *args, **kwargs):
            return (super().scale)(*args, **kwargs)

        @recalc
        def normalize(self, *args, **kwargs):
            return (super().normalize)(*args, **kwargs)

        @recalc
        def fix_variable(self, *args, **kwargs):
            return (super().fix_variable)(*args, **kwargs)

        @recalc
        def fix_variables(self, *args, **kwargs):
            return (super().fix_variables)(*args, **kwargs)

        @recalc
        def flip_variable(self, *args, **kwargs):
            return (super().flip_variable)(*args, **kwargs)

        @recalc
        def update(self, *args, **kwargs):
            return (super().update)(*args, **kwargs)

        @recalc
        def contract_variables(self, *args, **kwargs):
            return (super().contract_variables)(*args, **kwargs)

        def change_vartype(self, vartype, inplace=True):
            """
            Create a binary quadratic model with the specified vartype
            Args:
                var_type (cimod.Vartype): SPIN or BINARY
            Returns:
                A new instance of the BinaryQuadraticModel class.
            """
            cxxvartype = to_cxxcimod(vartype)
            bqm = super().change_vartypecxxvartypeinplace
            self._re_calculate = True
            return BinaryQuadraticModel(bqm.get_linear(), bqm.get_quadratic(), bqm.get_offset(), vartype)

        @classmethod
        def from_qubo(cls, Q, offset=0.0, **kwargs):
            linear = {}
            quadratic = {}
            for (u, v), bias in Q.items():
                if u == v:
                    linear[u] = bias
                else:
                    quadratic[(u, v)] = bias
            else:
                return cls(linear, quadratic, offset, var_type=dimod.BINARY, **kwargs)

        @classmethod
        def from_ising(cls, linear, quadratic, offset=0.0, **kwargs):
            return cls(linear, quadratic, offset, var_type=dimod.SPIN, **kwargs)

        @classmethod
        def from_serializable(cls, obj):
            bqm = super().from_serializable(obj)
            return BinaryQuadraticModel(bqm.get_linear(), bqm.get_quadratic(), bqm.get_offset(), bqm.get_vartype())

    return BinaryQuadraticModel


def make_BinaryQuadraticModel_from_JSON(obj):
    label = obj['variable_labels'][0]
    if isinstance(label, list):
        label = tuple(label)
    mock_linear = {label: 1.0}
    return make_BinaryQuadraticModel(mock_linear, {})


def BinaryQuadraticModel(linear, quadratic, offset=0.0, var_type=dimod.SPIN, **kwargs):
    Model = make_BinaryQuadraticModel(linear, quadratic)
    return Model(linear, quadratic, offset, var_type, **kwargs)


BinaryQuadraticModel.from_qubo = lambda Q, offset=0.0, **kwargs: (make_BinaryQuadraticModel({}, Q).from_qubo)(Q, offset, **kwargs)
BinaryQuadraticModel.from_ising = lambda linear, quadratic, offset=0.0, **kwargs: (make_BinaryQuadraticModel(linear, quadratic).from_ising)(linear, quadratic, offset, **kwargs)
BinaryQuadraticModel.from_serializable = lambda obj: make_BinaryQuadraticModel_from_JSON(obj).from_serializable(obj)