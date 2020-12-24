# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/calc/metpy.py
# Compiled at: 2019-12-03 10:30:30
# Size of source mod 2**32: 3115 bytes
__doc__ = 'Interface to metpy calc functions.'
import functools, cf_units, iris
import metpy.units as metunits
import numpy as np, pint, xarray as xr
from ..exceptions import UnitFormatError
__all__ = ('preprocess_iris', )

def preprocess_iris(f):
    """
    Wrap a function from `metpy.calc` for it to accept iris cubes as arguments.

    In addition, this decorator converts `metpy.calc` output by using the first input argument
    as a 'donor' cube.
    Note this works only for functions that preserve dimensions and may not work with some units.
    Now that metpy has xarray preprocessor, this decorator depends on it.
    """

    def to_xarray(cube):
        """Convert `iris.cube.Cube` to `xarray.DataArray` and format units correctly."""
        _unit = None
        for ut_format in set(cf_units.UT_FORMATS):
            try:
                _unit = metunits.units(cube.units.format(ut_format))
            except pint.errors.DimensionalityError:
                pass

        if _unit is None:
            raise UnitFormatError(f"Unable to convert cube units of\n{repr(cube)}\nto metpy units")
        arr = xr.DataArray.from_iris(cube)
        arr.attrs['units'] = str(_unit)
        return arr

    def to_iris(donor_cube, arr, name):
        """Convert metpy calc result to `iris.cube.Cube`."""
        try:
            data = arr.magnitude
            units = str(arr.units).replace(' ** ', '^').replace(' * ', ' ')
        except AttributeError:
            data = np.asarray(arr)
            units = '1'
        else:
            cube_out = donor_cube.copy(data=data)
            try:
                cube_out.units = units
            except ValueError:
                cube_out.units = 'unknown'
            else:
                cube_out.rename(name)
                cube_out.attributes.pop('STASH', None)
                return cube_out

    @functools.wraps(f)
    def wrapper--- This code section failed: ---

 L.  66         0  BUILD_LIST_0          0 
                2  STORE_FAST               'nargs'

 L.  67         4  LOAD_CONST               None
                6  STORE_FAST               '_cube'

 L.  70         8  LOAD_FAST                'args'
               10  GET_ITER         
               12  FOR_ITER             86  'to 86'
               14  STORE_FAST               'arg'

 L.  71        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'arg'
               20  LOAD_GLOBAL              iris
               22  LOAD_ATTR                cube
               24  LOAD_ATTR                Cube
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    74  'to 74'

 L.  72        30  LOAD_FAST                'arg'
               32  LOAD_ATTR                ndim
               34  LOAD_CONST               0
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L.  74        40  LOAD_FAST                'arg'
               42  STORE_FAST               '_cube'
               44  JUMP_FORWARD         58  'to 58'
             46_0  COME_FROM            38  '38'

 L.  75        46  LOAD_FAST                '_cube'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.  76        54  LOAD_FAST                'arg'
               56  STORE_FAST               '_cube'
             58_0  COME_FROM            52  '52'
             58_1  COME_FROM            44  '44'

 L.  78        58  LOAD_FAST                'nargs'
               60  LOAD_METHOD              append
               62  LOAD_DEREF               'to_xarray'
               64  LOAD_FAST                'arg'
               66  CALL_FUNCTION_1       1  ''
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  JUMP_BACK            12  'to 12'
             74_0  COME_FROM            28  '28'

 L.  80        74  LOAD_FAST                'nargs'
               76  LOAD_METHOD              append
               78  LOAD_FAST                'arg'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            12  'to 12'

 L.  82        86  LOAD_CLOSURE             'to_xarray'
               88  BUILD_TUPLE_1         1 
               90  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               92  LOAD_STR                 'preprocess_iris.<locals>.wrapper.<locals>.<dictcomp>'
               94  MAKE_FUNCTION_8          'closure'

 L.  83        96  LOAD_FAST                'kwargs'
               98  LOAD_METHOD              items
              100  CALL_METHOD_0         0  ''

 L.  82       102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'kwargs'

 L.  87       108  LOAD_DEREF               'f'
              110  LOAD_FAST                'nargs'
              112  LOAD_FAST                'kwargs'
              114  CALL_FUNCTION_EX_KW     1  'keyword args'
              116  STORE_FAST               'out'

 L.  88       118  LOAD_FAST                '_cube'
              120  LOAD_CONST               None
              122  COMPARE_OP               is
              124  POP_JUMP_IF_FALSE   130  'to 130'

 L.  90       126  LOAD_FAST                'out'
              128  RETURN_VALUE     
            130_0  COME_FROM           124  '124'

 L.  94       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'out'
              134  LOAD_GLOBAL              tuple
              136  LOAD_GLOBAL              list
              138  LOAD_GLOBAL              set
              140  BUILD_TUPLE_3         3 
              142  CALL_FUNCTION_2       2  ''
              144  POP_JUMP_IF_FALSE   208  'to 208'

 L.  95       146  BUILD_LIST_0          0 
              148  STORE_FAST               'res'

 L.  96       150  LOAD_GLOBAL              enumerate
              152  LOAD_FAST                'out'
              154  CALL_FUNCTION_1       1  ''
              156  GET_ITER         
              158  FOR_ITER            198  'to 198'
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST               'i'
              164  STORE_FAST               'iout'

 L.  97       166  LOAD_FAST                'res'
              168  LOAD_METHOD              append
              170  LOAD_DEREF               'to_iris'
              172  LOAD_FAST                '_cube'
              174  LOAD_FAST                'iout'
              176  LOAD_DEREF               'f'
              178  LOAD_ATTR                __name__
              180  FORMAT_VALUE          0  ''
              182  LOAD_STR                 '_output_'
              184  LOAD_FAST                'i'
              186  FORMAT_VALUE          0  ''
              188  BUILD_STRING_3        3 
              190  CALL_FUNCTION_3       3  ''
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_BACK           158  'to 158'

 L.  98       198  LOAD_GLOBAL              tuple
              200  LOAD_FAST                'res'
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'res'
              206  JUMP_FORWARD        222  'to 222'
            208_0  COME_FROM           144  '144'

 L. 100       208  LOAD_DEREF               'to_iris'
              210  LOAD_FAST                '_cube'
              212  LOAD_FAST                'out'
              214  LOAD_DEREF               'f'
              216  LOAD_ATTR                __name__
              218  CALL_FUNCTION_3       3  ''
              220  STORE_FAST               'res'
            222_0  COME_FROM           206  '206'

 L. 101       222  LOAD_FAST                'res'
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 90

    return wrapper