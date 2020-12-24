# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/subset.py
# Compiled at: 2020-04-28 06:34:04
# Size of source mod 2**32: 2390 bytes
"""Subset cubes using iris constraints."""
from datetime import timedelta
import iris
from .coord import UM_HGT, UM_LATLON, UM_LEV, UM_TIME, get_cube_datetimes
__all__ = ('CM_MEAN_CONSTR', 'DIM_CONSTR_TMYX', 'DIM_CONSTR_TZYX', 'DIM_CONSTR_TYX',
           'DIM_CONSTR_MYX', 'DIM_CONSTR_ZYX', 'DIM_CONSTR_YX', 'DIM_CONSTR_YX_R',
           'extract_last_month', 'extract_last_year', 'l_range_constr')

def _select_mean--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        20  'to 20'

 L.  27         2  LOAD_FAST                'cube'
                4  LOAD_ATTR                cell_methods
                6  LOAD_CONST               0
                8  BINARY_SUBSCR    
               10  LOAD_ATTR                method
               12  LOAD_STR                 'mean'
               14  COMPARE_OP               ==
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  28        20  DUP_TOP          
               22  LOAD_GLOBAL              IndexError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  29        34  POP_EXCEPT       
               36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 30


def _dim_constr(*coords, strict=True):
    """Make an `iris.Constraint` from given dimensional coordinates."""
    coord_set = set(coords)

    def __cube_func(cube):
        cube_dimcoords = {dc.name() for dc in cube.dim_coords}
        if strict:
            return cube_dimcoords == coord_set
        return coord_set.issubset(cube_dimcoords)

    return iris.Constraint(cube_func=__cube_func)


def l_range_constr(h_min, h_max, units='km', coord=UM_HGT):
    """Make a constraint on length range."""
    if units == 'km':
        factor = 0.001
    else:
        factor = 1
    return (iris.Constraint)(**{coord: lambda x: h_min <= x.point * factor <= h_max})


def extract_last_month(cube):
    """Extract time slices within the last months of a cube."""
    dt = get_cube_datetimes(cube)[(-1)]
    return cube.extract((iris.Constraint)(**{UM_TIME: lambda x: x.point.year == dt.year and x.point.month == dt.month}))


def extract_last_year(cube):
    """Extract time slices within the last year of a cube."""
    dt = get_cube_datetimes(cube)[(-1)]
    yr_before = dt - timedelta(days=365)
    return cube.extract((iris.Constraint)(**{UM_TIME: lambda t: t.point > yr_before}))


CM_MEAN_CONSTR = iris.Constraint(cube_func=_select_mean)
DIM_CONSTR_TMYX = _dim_constr(UM_TIME, UM_LEV, *UM_LATLON)
DIM_CONSTR_TZYX = _dim_constr(UM_TIME, UM_HGT, *UM_LATLON)
DIM_CONSTR_TYX = _dim_constr(UM_TIME, *UM_LATLON)
DIM_CONSTR_MYX = _dim_constr(UM_LEV, *UM_LATLON)
DIM_CONSTR_ZYX = _dim_constr(UM_HGT, *UM_LATLON)
DIM_CONSTR_YX = _dim_constr(*UM_LATLON)
DIM_CONSTR_YX_R = _dim_constr(*UM_LATLON, **{'strict': False})