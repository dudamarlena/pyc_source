# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/fill.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 5194 bytes
"""
Fill in missing parts of a project and cleans up its sections
so they have exactly the right constructor.
"""
import copy
from . import aliases, construct, merge
from .. import layout
from ..util import deprecated, exception, log
from ..colors import make, palettes, tables
from ..animation.strip import Strip
DEFAULT_DRIVERS = [
 construct.to_type('simpixel')]

def fill(desc):
    desc = _fill_aliases(desc)
    desc = _fill_colors(desc)
    desc = _fill_palettes(desc)
    desc = _fill_animation(desc)
    desc = _fill_drivers(desc)
    desc = _fill_shape(desc)
    desc = _fill_numbers(desc)
    desc = _fill_controls(desc)
    return desc


def fill_layout(animation):
    datatype = animation['datatype']
    args = getattr(datatype, 'LAYOUT_ARGS', Strip.LAYOUT_ARGS)
    layout_cl = getattr(datatype, 'LAYOUT_CLASS', Strip.LAYOUT_CLASS)
    args = {k:animation[k] for k in args if k in animation}
    return dict(args, datatype=layout_cl)


def _fill_aliases(desc):

    def unalias(k):
        if any(k.startswith(m) for m in aliases.ALIAS_MARKERS):
            return k[1:]
        else:
            return k

    al = desc.pop('aliases', {})
    aliases.PROJECT_ALIASES = {unalias(k):v for k, v in al.items()}
    return desc


def _fill_colors(desc):
    tables.set_user_colors(desc.pop('colors', {}))
    return desc


def _fill_palettes(desc):
    p = desc.pop('palettes', None)
    if p:
        default = p.pop('default', None)
        with exception.add('Error in "palettes" Section'):
            pp = {k:make.colors(v) for k, v in p.items()}
        palettes.PROJECT_PALETTES = pp
        if default:
            try:
                palettes.set_default(default)
            except:
                log.error('Unable to set default palette to be %s', default)

    return desc


def _fill_animation--- This code section failed: ---

 L.  73         0  LOAD_FAST                'desc'
                2  LOAD_STR                 'animation'
                4  BINARY_SUBSCR    
                6  JUMP_IF_TRUE_OR_POP    14  'to 14'
                8  LOAD_STR                 'typename'
               10  LOAD_STR                 'animation'
               12  BUILD_MAP_1           1 
             14_0  COME_FROM             6  '6'
               14  STORE_FAST               'da'

 L.  74        16  LOAD_GLOBAL              construct
               18  LOAD_ATTR                to_type_constructor
               20  LOAD_FAST                'da'
               22  LOAD_STR                 'bibliopixel.animation'
               24  CALL_FUNCTION_2       2  '2 positional arguments'
               26  STORE_FAST               'da'

 L.  75        28  LOAD_FAST                'da'
               30  LOAD_ATTR                get
               32  LOAD_STR                 'datatype'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  STORE_FAST               'datatype'

 L.  76        38  LOAD_FAST                'datatype'
               40  POP_JUMP_IF_TRUE     64  'to 64'

 L.  77        42  LOAD_FAST                'da'
               44  LOAD_ATTR                get
               46  LOAD_STR                 '_exception'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'e'

 L.  78        52  LOAD_FAST                'e'
               54  JUMP_IF_TRUE_OR_POP    62  'to 62'
               56  LOAD_GLOBAL              ValueError
               58  LOAD_STR                 'Missing "datatype" in "animation" Section'
               60  CALL_FUNCTION_1       1  '1 positional argument'
             62_0  COME_FROM            54  '54'
               62  RAISE_VARARGS_1       1  'exception'
             64_0  COME_FROM            40  '40'

 L.  80        64  LOAD_FAST                'da'
               66  LOAD_ATTR                setdefault
               68  LOAD_STR                 'name'
               70  LOAD_FAST                'datatype'
               72  LOAD_ATTR                __name__
               74  CALL_FUNCTION_2       2  '2 positional arguments'
               76  POP_TOP          

 L.  82        78  LOAD_CONST               2
               80  LOAD_CONST               ('sequence',)
               82  IMPORT_NAME              animation
               84  IMPORT_FROM              sequence
               86  STORE_FAST               'sequence'
               88  POP_TOP          

 L.  83        90  LOAD_GLOBAL              issubclass
               92  LOAD_FAST                'datatype'
               94  LOAD_FAST                'sequence'
               96  LOAD_ATTR                Sequence
               98  CALL_FUNCTION_2       2  '2 positional arguments'
              100  POP_JUMP_IF_TRUE    138  'to 138'

 L.  85       102  LOAD_FAST                'da'
              104  LOAD_ATTR                pop
              106  LOAD_STR                 'length'
              108  BUILD_LIST_0          0 
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  STORE_FAST               'length'

 L.  86       114  LOAD_FAST                'length'
              116  POP_JUMP_IF_FALSE   138  'to 138'

 L.  87       118  LOAD_FAST                'length'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  LOAD_FAST                'desc'
              126  LOAD_ATTR                setdefault
              128  LOAD_STR                 'run'
              130  BUILD_MAP_0           0 
              132  CALL_FUNCTION_2       2  '2 positional arguments'
              134  LOAD_STR                 'seconds'
              136  STORE_SUBSCR     
            138_0  COME_FROM           116  '116'
            138_1  COME_FROM           100  '100'

 L.  89       138  LOAD_GLOBAL              merge
              140  LOAD_ATTR                merge
              142  LOAD_GLOBAL              getattr
              144  LOAD_FAST                'datatype'
              146  LOAD_STR                 'PROJECT'
              148  BUILD_MAP_0           0 
              150  CALL_FUNCTION_3       3  '3 positional arguments'
              152  LOAD_FAST                'desc'
              154  CALL_FUNCTION_2       2  '2 positional arguments'
              156  STORE_FAST               'desc'

 L.  91       158  LOAD_GLOBAL              dict
              160  LOAD_FAST                'desc'
              162  LOAD_ATTR                pop
              164  LOAD_STR                 'run'
              166  BUILD_MAP_0           0 
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  BUILD_TUPLE_1         1 
              172  LOAD_FAST                'da'
              174  LOAD_ATTR                get
              176  LOAD_STR                 'run'
              178  BUILD_MAP_0           0 
              180  CALL_FUNCTION_2       2  '2 positional arguments'
              182  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              184  LOAD_FAST                'da'
              186  LOAD_STR                 'run'
              188  STORE_SUBSCR     

 L.  92       190  LOAD_FAST                'da'
              192  LOAD_FAST                'desc'
              194  LOAD_STR                 'animation'
              196  STORE_SUBSCR     

 L.  93       198  LOAD_FAST                'desc'
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RAISE_VARARGS_1' instruction at offset 62


def _fill_drivers(desc):
    driver = construct.to_type(desc.pop('driver', {}))
    drivers = [construct.to_type(d) for d in desc['drivers']]
    if driver:
        drivers = [dict(driver, **d) for d in drivers or [{}]]
    desc['drivers'] = drivers or DEFAULT_DRIVERS
    return desc


def _fill_shape(desc):
    desc = copy.deepcopy(desc)
    dimensions = desc.pop('dimensions', None)
    if dimensions:
        deprecated.deprecated('Project Section "dimensions"')
    shape = desc.pop('shape', None) or dimensions
    if not shape:
        return desc
    else:
        if len(desc['drivers']) != 1:
            raise ValueError('Cannot use dimensions with more than one driver')
        else:
            if isinstance(shape, int):
                shape = [
                 shape]
            else:
                if isinstance(shape, str):
                    shape = shape.strip()
                    if shape.startswith('('):
                        if shape.endswith(')'):
                            shape = shape[1:-1]
                    try:
                        shape = [int(s) for s in shape.split(',')]
                    except:
                        raise ValueError('Cannot parse shape %s' % shape)

                elif not isinstance(shape, (list, tuple)):
                    raise ValueError('`shape` must be a number or a list, was "%s" (%s)' % (
                     shape, type(shape)))
                else:
                    ldesc = construct.to_type_constructor((desc.get('layout') or {}), python_path='bibliopixel.layout')
                    driver = desc['drivers'][0]
                    if len(shape) == 1:
                        driver['num'] = shape[0]
                        ldesc.setdefault('datatype', layout.strip.Strip)
                    else:
                        if len(shape) == 2:
                            driver['num'] = shape[0] * shape[1]
                            ldesc.setdefault('datatype', layout.matrix.Matrix)
                            ldesc.update(width=(shape[0]), height=(shape[1]))
                        else:
                            if len(shape) == 3:
                                driver['num'] = shape[0] * shape[1] * shape[2]
                                ldesc.setdefault('datatype', layout.cube.Cube)
                                ldesc.update(x=(shape[0]), y=(shape[1]), z=(shape[2]))
                            else:
                                raise ValueError('Dimension %s > 3' % len(shape))
        desc['layout'] = ldesc
        return desc


def _fill_numbers(desc):
    numbers = desc.pop('numbers', None) or 'python'
    if numbers != 'python':
        desc.setdefault('maker', {})['numpy_dtype'] = numbers
    return desc


def _fill_controls(desc):
    controls = desc.get('controls', None)
    if isinstance(controls, (str, dict)):
        desc['controls'] = [
         controls]
    return desc