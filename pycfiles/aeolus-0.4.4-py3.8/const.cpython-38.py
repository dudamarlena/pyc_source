# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/const/const.py
# Compiled at: 2020-01-07 11:04:49
# Size of source mod 2**32: 5185 bytes
"""Main interface to the physical constants store."""
import json
from dataclasses import make_dataclass
from pathlib import Path
from warnings import warn
import iris, numpy as np
from ..exceptions import AeolusWarning, ArgumentError, LoadError
__all__ = ('init_const', 'get_planet_radius')
CONST_DIR = Path(__file__).parent / 'store'

class ScalarCube(iris.cube.Cube):
    __doc__ = 'Cube without coordinates.'

    def __repr__(self):
        """Repr of this class."""
        return f"<ScalarCube of {self.long_name} [{self.units}]>"

    def __deepcopy__(self, memo):
        """Deep copy of a scalar cube."""
        return self.from_cube(self._deepcopy(memo))

    @property
    def asc(self):
        """Convert cube to AuxCoord for math ops."""
        return iris.coords.AuxCoord((np.asarray(self.data)),
          units=(self.units), long_name=(self.long_name))

    @classmethod
    def from_cube--- This code section failed: ---

 L.  41         0  LOAD_FAST                'cls'
                2  BUILD_TUPLE_0         0 
                4  LOAD_CLOSURE             'cube'
                6  BUILD_TUPLE_1         1 
                8  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               10  LOAD_STR                 'ScalarCube.from_cube.<locals>.<dictcomp>'
               12  MAKE_FUNCTION_8          'closure'
               14  LOAD_CONST               ('data', 'units', 'long_name')
               16  GET_ITER         
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class ConstContainer:
    __doc__ = 'Base class for creating dataclasses and storing planetary constants.'

    def __repr__(self):
        """Create custom repr."""
        cubes_str = ', '.join([f"{getattr(self, _field).long_name} [{getattr(self, _field).units}]" for _field in self.__dataclass_fields__])
        return f"{self.__class__.__name__}({cubes_str})"

    def __post_init__(self):
        """Do things automatically after __init__()."""
        self._convert_to_iris_cubes()
        self._derive_const()

    def _convert_to_iris_cubes(self):
        """Loop through fields and convert each of them to `iris.cube.Cube`."""
        for name in self.__dataclass_fields__:
            _field = getattr(self, name)
            cube = ScalarCube(data=(_field.get('value')),
              units=(_field.get('units', 1)),
              long_name=name)
            object.__setattr__(self, name, cube)

    def _derive_const(self):
        """Not fully implemented yet."""
        derivatives = {'dry_air_gas_constant': lambda slf: slf.molar_gas_constant / slf.dry_air_molecular_weight}
        for name, func in derivatives.items():
            try:
                cube = ScalarCube.from_cube(func(self))
                cube.rename(name)
                object.__setattr__(self, name, cube)
            except AttributeError:
                pass


def _read_const_file--- This code section failed: ---

 L.  88         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'directory'
                4  LOAD_GLOBAL              Path
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L.  89        10  LOAD_GLOBAL              ArgumentError
               12  LOAD_STR                 'directory must be a pathlib.Path object'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  90        18  SETUP_FINALLY       108  'to 108'

 L.  91        20  LOAD_FAST                'directory'
               22  LOAD_FAST                'name'
               24  BINARY_TRUE_DIVIDE
               26  LOAD_METHOD              with_suffix
               28  LOAD_STR                 '.json'
               30  CALL_METHOD_1         1  ''
               32  LOAD_METHOD              open
               34  LOAD_STR                 'r'
               36  CALL_METHOD_1         1  ''
               38  SETUP_WITH           56  'to 56'
               40  STORE_FAST               'fp'

 L.  92        42  LOAD_GLOBAL              json
               44  LOAD_METHOD              load
               46  LOAD_FAST                'fp'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'list_of_dicts'
               52  POP_BLOCK        
               54  BEGIN_FINALLY    
             56_0  COME_FROM_WITH       38  '38'
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      

 L.  94        62  BUILD_MAP_0           0 
               64  STORE_FAST               'const_dict'

 L.  95        66  LOAD_FAST                'list_of_dicts'
               68  GET_ITER         
               70  FOR_ITER            102  'to 102'
               72  STORE_FAST               'vardict'

 L.  96        74  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               76  LOAD_STR                 '_read_const_file.<locals>.<dictcomp>'
               78  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  97        80  LOAD_FAST                'vardict'
               82  LOAD_METHOD              items
               84  CALL_METHOD_0         0  ''

 L.  96        86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_FAST                'const_dict'
               92  LOAD_FAST                'vardict'
               94  LOAD_STR                 'name'
               96  BINARY_SUBSCR    
               98  STORE_SUBSCR     
              100  JUMP_BACK            70  'to 70'

 L.  99       102  LOAD_FAST                'const_dict'
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM_FINALLY    18  '18'

 L. 100       108  DUP_TOP          
              110  LOAD_GLOBAL              FileNotFoundError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   146  'to 146'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 101       122  LOAD_GLOBAL              LoadError

 L. 102       124  LOAD_STR                 'JSON file for '
              126  LOAD_FAST                'name'
              128  FORMAT_VALUE          0  ''
              130  LOAD_STR                 ' configuration not found, check the directory: '
              132  LOAD_FAST                'directory'
              134  FORMAT_VALUE          0  ''
              136  BUILD_STRING_4        4 

 L. 101       138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           114  '114'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'

Parse error at or near `POP_TOP' instruction at offset 118


def init_const(name='general', directory=None):
    """
    Create a dataclass with a given set of constants.

    Parameters
    ----------
    name: str, optional
        Name of the constants set.
        Should be identical to the JSON file name (without the .json extension).
        If not given, only general physical constants are returned.
    directory: pathlib.Path, optional
        Path to a folder with JSON files containing constants for a specific planet.

    Returns
    -------
    Dataclass with constants as iris cubes.

    Examples
    --------
    >>> c = init_const('earth')
    >>> c
    EarthConstants(gravity [m s-2], radius [m], day [s], solar_constant [W m-2], ...)
    >>> c.gravity
    <iris 'Cube' of gravity / (m s-2) (scalar cube)>
    """
    cls_name = f"{name.capitalize()}Constants"
    if directory is None:
        kw = {}
    else:
        kw = {'directory': directory}
    const_dict = _read_const_file('general')
    if name != 'general':
        const_dict.update(_read_const_file(name, **kw))
    kls = make_dataclass(cls_name,
      fields=[
     *const_dict.keys()],
      bases=(
     ConstContainer,),
      frozen=True,
      repr=False)
    return kls(**const_dict)


def get_planet_radius(cube, default=iris.fileformats.pp.EARTH_RADIUS):
    """Get planet radius in metres from cube attributes or coordinate system."""
    cs = cube.coord_system('CoordSystem')
    if cs is not None:
        r = cs.semi_major_axis
    else:
        try:
            r = cube.attributes['planet_conf'].radius.copy()
            r.convert_units('m')
            r = float(r.data)
        except (KeyError, LoadError):
            warn('Using default radius', AeolusWarning)
            r = default
        else:
            return r