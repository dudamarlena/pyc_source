# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\toolboxes\iolidfiles\io_lid_files.py
# Compiled at: 2019-01-25 08:29:59
# Size of source mod 2**32: 19585 bytes
"""
Module for reading / writing LID data from IES and LDT files.
=============================================================

 :read_lamp_data: Read in light intensity distribution and other lamp data from LDT or IES files.

    Notes:
        1.Only basic support. Writing is not yet implemented.
        2.Reading IES files is based on Blender's ies2cycles.py
        3.This was implemented to build some uv-texture maps for rendering and only tested for a few files.
        4. Use at own risk. No warranties.
     
.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, os
__all__ = [
 'read_lamp_data']

def read_lamp_data(filename, multiplier=1.0, verbosity=0, normalize='I0', only_common_keys=False):
    """
    Read in light intensity distribution and other lamp data from LDT or IES files.
    
    Args:
        :filename:
            | Filename of IES file.
        :multiplier:
            | 1.0, optional
            | Scaler for candela values.
        :verbosity:
            | 0, optional
            | Display messages while reading file.
        :normalize:
            | 'I0', optional
            | If 'I0': normalize LID to intensity at (theta,phi) = (0,0)
            | If 'max': normalize to max = 1.
        :only_common_keys:
            | False, optional
            | If True, output only common dict keys related to angles, values
            | and such of LID.
            | read_lid_lamp_data(?) for print of common keys and return
            |                       empty dict with common keys.
   
    Returns:
        :lid: dict with IES or LDT file data.
            |
            | If file_ext == 'ies':
            |    dict_keys(
            | ['filename', 'version', 'lamps_num', 'lumens_per_lamp',
            | 'candela_mult', 'v_angles_num', 'h_angles_num', 'photometric_type',
            | 'units_type', 'width', 'length', 'height', 'ballast_factor', 
            | 'future_use', 'input_watts', 'v_angs', 'h_angs', 'lamp_cone_type',
            | 'lamp_h_type', 'candela_values', 'candela_2d', 'v_same', 'h_same',
            | 'intensity', 'theta', 'values', 'phi', 'map','Iv0']
            |
            | If file_ext == 'ldt':
            |    dict_keys(
            | ['filename', 'version', 'manufacturer', 'Ityp','Isym',
            | 'Mc', 'Dc', 'Ng', 'name', Dg', 'cct/cri', 'tflux', 'lumens_per_lamp',
            | 'candela_mult', 'tilt', lamps_num',
            | 'cangles', 'tangles','candela_values', 'candela_2d',
            | 'intensity', 'theta', 'values', 'phi', 'map', 'Iv0']
            | )
            
    """
    common_keys = [
     'filename', 'version', 'intensity', 'theta', 'phi',
     'values', 'map', 'Iv0', 'candela_values', 'candela_2d']
    if filename == '?':
        print(common_keys)
        return dict(zip(common_keys, [np.nan] * len(common_keys)))
    else:
        file_ext = filename[-3:].lower()
        if file_ext == 'ies':
            lid = read_IES_lamp_data(filename, multiplier=multiplier, verbosity=verbosity,
              normalize=normalize)
        else:
            if file_ext == 'ldt':
                lid = read_ldt_lamp_data(filename, multiplier=multiplier, normalize=normalize)
            else:
                raise Exception("read_lid_lamp_data(): {:s} --> unsupported file type/extension (only 'ies' or 'ldt': ".format(file_ext))
    if only_common_keys == True:
        return {key:value for key, value in lid.items() if key in common_keys}
    return lid


def displaymsg(code, message, verbosity=1):
    """
    Display messages (used by read_IES_lamp_data).  
    """
    if verbosity > 0:
        print('{}: {}'.format(code, message))


def read_IES_lamp_data(filename, multiplier=1.0, verbosity=0, normalize='I0'):
    """
    Read in IES files (adapted from Blender's ies2cycles.py).
    
    Args:
        :filename:
            | Filename of IES file.
        :multiplier:
            | 1.0, optional
            | Scaler for candela values.
        :verbosity:
            | 0, optional
            | Display messages while reading file.
        :normalize:
            | 'I0', optional
            | If 'I0': normalize LID to intensity at (theta,phi) = (0,0)
            | If 'max': normalize to max = 1.
            
    Returns:
        :IES: dict with IES file data.
            |
            | dict_keys(
            | ['filename', 'version', 'lamps_num', 'lumens_per_lamp',
            | 'candela_mult', 'v_angles_num', 'h_angles_num', 'photometric_type',
            | 'units_type', 'width', 'length', 'height', 'ballast_factor', 
            | 'future_use', 'input_watts', 'v_angs', 'h_angs', 'lamp_cone_type',
            | 'lamp_h_type', 'candela_values', 'candela_2d', 'v_same', 'h_same',
            | 'intensity', 'theta', 'values', 'phi', 'map','Iv0']
            | )
    """
    version_table = {'IESNA:LM-63-1986':1986, 
     'IESNA:LM-63-1991':1991, 
     'IESNA91':1991, 
     'IESNA:LM-63-1995':1995, 
     'IESNA:LM-63-2002':2002}
    name = os.path.splitext(os.path.split(filename)[1])[0]
    file = open(filename, 'rt', encoding='cp1252')
    content = file.read()
    file.close()
    s, content = content.split('\n', 1)
    if s in version_table:
        version = version_table[s]
    else:
        displaymsg('INFO', 'IES file does not specify any version', verbosity=verbosity)
        version = None
    keywords = dict()
    while content:
        s, content = content.startswith('TILT=') or content.split('\n', 1)
        if s.startswith('['):
            endbracket = s.find(']')
            if endbracket != -1:
                keywords[s[1:endbracket]] = s[endbracket + 1:].strip()

    s, content = content.split('\n', 1)
    if not s.startswith('TILT'):
        displaymsg('ERRORTILT keyword not found, check your IES file', verbosity=verbosity)
        return
    file_data = content.replace(',', ' ').split()
    lamps_num = int(file_data[0])
    if lamps_num != 1:
        displaymsg('INFO', ('Only 1 lamp is supported, %d in IES file' % lamps_num), verbosity=verbosity)
    lumens_per_lamp = float(file_data[1])
    candela_mult = float(file_data[2])
    v_angles_num = int(file_data[3])
    h_angles_num = int(file_data[4])
    if not (v_angles_num and h_angles_num):
        displaymsg('ERROR', 'TILT keyword not found, check your IES file', verbosity=verbosity)
        return
    photometric_type = int(file_data[5])
    units_type = int(file_data[6])
    if units_type not in (1, 2):
        displaymsg('INFO', 'Units type should be either 1 (feet) or 2 (meters)', verbosity=verbosity)
    width, length, height = map(float, file_data[7:10])
    ballast_factor = float(file_data[10])
    future_use = float(file_data[11])
    if future_use != 1.0:
        displaymsg('INFO', 'Invalid future use field', verbosity=verbosity)
    input_watts = float(file_data[12])
    v_angs = [float(s) for s in file_data[13:13 + v_angles_num]]
    h_angs = [float(s) for s in file_data[13 + v_angles_num:13 + v_angles_num + h_angles_num]]
    if v_angs[0] == 0 and v_angs[(-1)] == 90:
        lamp_cone_type = 'TYPE90'
    else:
        if v_angs[0] == 0:
            if v_angs[(-1)] == 180:
                lamp_cone_type = 'TYPE180'
            else:
                displaymsg('INFO', ('Lamps with vertical angles (%d-%d) are not supported' % (
                 v_angs[0], v_angs[(-1)])),
                  verbosity=verbosity)
                lamp_cone_type = 'TYPE180'
        elif len(h_angs) == 1 or abs(h_angs[0] - h_angs[(-1)]) == 360:
            lamp_h_type = 'TYPE360'
        else:
            if abs(h_angs[0] - h_angs[(-1)]) == 180:
                lamp_h_type = 'TYPE180'
            else:
                if abs(h_angs[0] - h_angs[(-1)]) == 90:
                    lamp_h_type = 'TYPE90'
                else:
                    displaymsg('INFO', ('Lamps with horizontal angles (%d-%d) are not supported' % (
                     h_angs[0], h_angs[(-1)])),
                      verbosity=verbosity)
                    lamp_h_type = 'TYPE360'
        offset = 13 + len(v_angs) + len(h_angs)
        candela_num = len(v_angs) * len(h_angs)
        candela_values = [float(s) for s in file_data[offset:offset + candela_num]]
        candela_2d = list(zip(*[iter(candela_values)] * len(v_angs)))
        v_d = [v_angs[i] - v_angs[(i - 1)] for i in range(1, len(v_angs))]
        h_d = [h_angs[i] - h_angs[(i - 1)] for i in range(1, len(h_angs))]
        v_same = all((abs(v_d[i] - v_d[(i - 1)]) < 0.001 for i in range(1, len(v_d))))
        h_same = all((abs(h_d[i] - h_d[(i - 1)]) < 0.001 for i in range(1, len(h_d))))
        if not h_same:
            displaymsg('INFO', 'Different offsets for horizontal angles!', verbosity=verbosity)
        maxval = max([max(row) for row in candela_2d])
        candela_2d = [[val / maxval for val in row] for row in candela_2d]
        intensity = maxval * multiplier * candela_mult
        IES = {'filename': filename}
        IES['name'] = name
        IES['version'] = version
        IES['lamps_num'] = lamps_num
        IES['lumens_per_lamp'] = lumens_per_lamp
        IES['candela_mult'] = candela_mult
        IES['v_angles_num'] = v_angles_num
        IES['h_angles_num'] = h_angles_num
        IES['photometric_type'] = photometric_type
        IES['units_type'] = units_type
        IES['width'], IES['length'], IES['height'] = width, length, height
        IES['ballast_factor'] = ballast_factor
        IES['future_use'] = future_use
        IES['input_watts'] = input_watts
        IES['v_angs'] = np.asarray(v_angs)
        IES['h_angs'] = np.asarray(h_angs)
        IES['lamp_cone_type'] = lamp_cone_type
        IES['lamp_h_type'] = np.asarray(lamp_h_type)
        IES['candela_values'] = np.asarray(candela_values)
        IES['candela_2d'] = np.asarray(candela_2d)
        IES['v_same'] = v_same
        IES['h_same'] = h_same
        IES['intensity'] = intensity
        IES = _normalize_candela_2d(IES, normalize=normalize, multiplier=multiplier)
        IES = _complete_ies_lid(IES, lamp_h_type=(IES['lamp_h_type']))
        IES['Iv0'] = IES['intensity'] / 1000 * IES['lumens_per_lamp']
        return IES


def _complete_ies_lid(IES, lamp_h_type='TYPE90'):
    """
    Convert IES LID map with lamp_h_type symmetry to a 'full' map with phi: [0,360] and theta: [0,180].
    """
    IES['theta'] = IES['v_angs']
    if IES['lamp_h_type'] == 'TYPE90':
        IES['values'] = np.matlib.repmat(IES['candela_2d'], 4, 1)
        IES['phi'] = np.hstack((IES['h_angs'], IES['h_angs'] + 90, IES['h_angs'] + 180, IES['h_angs'] + 270))
    else:
        if IES['lamp_h_type'] == 'TYPE180':
            IES['values'] = np.matlib.repmat(IES['candela_2d'], 2, 1)
            IES['phi'] = np.hstack((IES['h_angs'], IES['h_angs'] + 180))
        else:
            IES['values'] = IES['candela_2d']
            IES['phi'] = IES['h_angs']
    IES['map']['thetas'] = IES['theta']
    IES['map']['phis'] = IES['phi']
    IES['map']['values'] = IES['values']
    return IES


def read_ldt_lamp_data--- This code section failed: ---

 L. 346         0  LOAD_STR                 'filename'
                2  LOAD_FAST                'filename'
                4  BUILD_MAP_1           1 
                6  STORE_FAST               'LDT'

 L. 347         8  LOAD_CONST               None
               10  LOAD_FAST                'LDT'
               12  LOAD_STR                 'version'
               14  STORE_SUBSCR     

 L. 348        16  LOAD_GLOBAL              open
               18  LOAD_FAST                'filename'
               20  CALL_FUNCTION_1       1  '1 positional argument'
            22_24  SETUP_WITH          966  'to 966'
               26  STORE_FAST               'file'

 L. 349        28  LOAD_CONST               0
               30  STORE_FAST               'c'

 L. 350        32  BUILD_LIST_0          0 
               34  STORE_FAST               'cangles'

 L. 351        36  BUILD_LIST_0          0 
               38  STORE_FAST               'tangles'

 L. 352        40  BUILD_LIST_0          0 
               42  STORE_FAST               'candela_values'

 L. 353     44_46  SETUP_LOOP          794  'to 794'
               48  LOAD_FAST                'file'
               50  GET_ITER         
            52_54  FOR_ITER            792  'to 792'
               56  STORE_FAST               'line'

 L. 354        58  LOAD_FAST                'c'
               60  LOAD_CONST               0
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L. 355        66  LOAD_FAST                'line'
               68  LOAD_METHOD              rstrip
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  LOAD_FAST                'LDT'
               74  LOAD_STR                 'manufacturer'
               76  STORE_SUBSCR     
            78_80  JUMP_FORWARD        782  'to 782'
             82_0  COME_FROM            64  '64'

 L. 356        82  LOAD_FAST                'c'
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   164  'to 164'

 L. 357        90  LOAD_GLOBAL              np
               92  LOAD_METHOD              float
               94  LOAD_FAST                'line'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  LOAD_CONST               1.0
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 358       104  LOAD_STR                 'point source with symm. around vert. axis'
              106  LOAD_FAST                'LDT'
              108  LOAD_STR                 'Ityp'
              110  STORE_SUBSCR     
              112  JUMP_FORWARD        782  'to 782'
            114_0  COME_FROM           102  '102'

 L. 359       114  LOAD_GLOBAL              np
              116  LOAD_METHOD              float
              118  LOAD_FAST                'line'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  LOAD_CONST               2.0
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L. 360       128  LOAD_STR                 'line luminaire'
              130  LOAD_FAST                'LDT'
              132  LOAD_STR                 'Ityp'
              134  STORE_SUBSCR     
              136  JUMP_FORWARD        782  'to 782'
            138_0  COME_FROM           126  '126'

 L. 361       138  LOAD_GLOBAL              np
              140  LOAD_METHOD              float
              142  LOAD_FAST                'line'
              144  CALL_METHOD_1         1  '1 positional argument'
              146  LOAD_CONST               3.0
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   160  'to 160'

 L. 362       152  LOAD_STR                 'point source with other symm.'
              154  LOAD_FAST                'LDT'
              156  LOAD_STR                 'Ityp'
              158  STORE_SUBSCR     
            160_0  COME_FROM           150  '150'
          160_162  JUMP_FORWARD        782  'to 782'
            164_0  COME_FROM            88  '88'

 L. 363       164  LOAD_FAST                'c'
              166  LOAD_CONST               2
              168  COMPARE_OP               ==
          170_172  POP_JUMP_IF_FALSE   300  'to 300'

 L. 364       174  LOAD_GLOBAL              np
              176  LOAD_METHOD              float
              178  LOAD_FAST                'line'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  LOAD_CONST               0.0
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 365       188  LOAD_CONST               (0, 'no symmetry')
              190  LOAD_FAST                'LDT'
              192  LOAD_STR                 'Isym'
              194  STORE_SUBSCR     
              196  JUMP_FORWARD        782  'to 782'
            198_0  COME_FROM           186  '186'

 L. 366       198  LOAD_GLOBAL              np
              200  LOAD_METHOD              float
              202  LOAD_FAST                'line'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  LOAD_CONST               1.0
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   222  'to 222'

 L. 367       212  LOAD_CONST               (1, 'symmetry about the vertical axis')
              214  LOAD_FAST                'LDT'
              216  LOAD_STR                 'Isym'
              218  STORE_SUBSCR     
              220  JUMP_FORWARD        782  'to 782'
            222_0  COME_FROM           210  '210'

 L. 368       222  LOAD_GLOBAL              np
              224  LOAD_METHOD              float
              226  LOAD_FAST                'line'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  LOAD_CONST               2.0
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   246  'to 246'

 L. 369       236  LOAD_CONST               (2, 'symmetry to plane C0-C180')
              238  LOAD_FAST                'LDT'
              240  LOAD_STR                 'Isym'
              242  STORE_SUBSCR     
              244  JUMP_FORWARD        782  'to 782'
            246_0  COME_FROM           234  '234'

 L. 370       246  LOAD_GLOBAL              np
              248  LOAD_METHOD              float
              250  LOAD_FAST                'line'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  LOAD_CONST               3.0
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   272  'to 272'

 L. 371       262  LOAD_CONST               (3, 'symmetry to plane C90-C270')
              264  LOAD_FAST                'LDT'
              266  LOAD_STR                 'Isym'
              268  STORE_SUBSCR     
              270  JUMP_FORWARD        782  'to 782'
            272_0  COME_FROM           258  '258'

 L. 372       272  LOAD_GLOBAL              np
              274  LOAD_METHOD              float
              276  LOAD_FAST                'line'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  LOAD_CONST               4.0
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   782  'to 782'

 L. 373       288  LOAD_CONST               (4, 'symmetry to plane C0-C180 and to plane C90-C270')
              290  LOAD_FAST                'LDT'
              292  LOAD_STR                 'Isym'
              294  STORE_SUBSCR     
          296_298  JUMP_FORWARD        782  'to 782'
            300_0  COME_FROM           170  '170'

 L. 374       300  LOAD_FAST                'c'
              302  LOAD_CONST               3
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   328  'to 328'

 L. 375       310  LOAD_GLOBAL              np
              312  LOAD_METHOD              float
              314  LOAD_FAST                'line'
              316  CALL_METHOD_1         1  '1 positional argument'
              318  LOAD_FAST                'LDT'
              320  LOAD_STR                 'Mc'
              322  STORE_SUBSCR     
          324_326  JUMP_FORWARD        782  'to 782'
            328_0  COME_FROM           306  '306'

 L. 376       328  LOAD_FAST                'c'
              330  LOAD_CONST               4
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   356  'to 356'

 L. 377       338  LOAD_GLOBAL              np
              340  LOAD_METHOD              float
              342  LOAD_FAST                'line'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  LOAD_FAST                'LDT'
              348  LOAD_STR                 'Dc'
              350  STORE_SUBSCR     
          352_354  JUMP_FORWARD        782  'to 782'
            356_0  COME_FROM           334  '334'

 L. 378       356  LOAD_FAST                'c'
              358  LOAD_CONST               5
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   384  'to 384'

 L. 379       366  LOAD_GLOBAL              np
              368  LOAD_METHOD              float
              370  LOAD_FAST                'line'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  LOAD_FAST                'LDT'
              376  LOAD_STR                 'Ng'
              378  STORE_SUBSCR     
          380_382  JUMP_FORWARD        782  'to 782'
            384_0  COME_FROM           362  '362'

 L. 380       384  LOAD_FAST                'c'
              386  LOAD_CONST               6
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   412  'to 412'

 L. 381       394  LOAD_GLOBAL              np
              396  LOAD_METHOD              float
              398  LOAD_FAST                'line'
              400  CALL_METHOD_1         1  '1 positional argument'
              402  LOAD_FAST                'LDT'
              404  LOAD_STR                 'Dg'
              406  STORE_SUBSCR     
          408_410  JUMP_FORWARD        782  'to 782'
            412_0  COME_FROM           390  '390'

 L. 382       412  LOAD_FAST                'c'
              414  LOAD_CONST               8
              416  COMPARE_OP               ==
          418_420  POP_JUMP_IF_FALSE   438  'to 438'

 L. 383       422  LOAD_FAST                'line'
              424  LOAD_METHOD              rstrip
              426  CALL_METHOD_0         0  '0 positional arguments'
              428  LOAD_FAST                'LDT'
              430  LOAD_STR                 'name'
              432  STORE_SUBSCR     
          434_436  JUMP_FORWARD        782  'to 782'
            438_0  COME_FROM           418  '418'

 L. 384       438  LOAD_FAST                'c'
              440  LOAD_CONST               23
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_FALSE   466  'to 466'

 L. 385       448  LOAD_GLOBAL              np
              450  LOAD_METHOD              float
              452  LOAD_FAST                'line'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  LOAD_FAST                'LDT'
              458  LOAD_STR                 'candela_mult'
              460  STORE_SUBSCR     
          462_464  JUMP_FORWARD        782  'to 782'
            466_0  COME_FROM           444  '444'

 L. 386       466  LOAD_FAST                'c'
              468  LOAD_CONST               24
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   494  'to 494'

 L. 387       476  LOAD_GLOBAL              np
              478  LOAD_METHOD              float
              480  LOAD_FAST                'line'
              482  CALL_METHOD_1         1  '1 positional argument'
              484  LOAD_FAST                'LDT'
              486  LOAD_STR                 'tilt'
              488  STORE_SUBSCR     
          490_492  JUMP_FORWARD        782  'to 782'
            494_0  COME_FROM           472  '472'

 L. 388       494  LOAD_FAST                'c'
              496  LOAD_CONST               26
              498  COMPARE_OP               ==
          500_502  POP_JUMP_IF_FALSE   522  'to 522'

 L. 389       504  LOAD_GLOBAL              np
              506  LOAD_METHOD              float
              508  LOAD_FAST                'line'
              510  CALL_METHOD_1         1  '1 positional argument'
              512  LOAD_FAST                'LDT'
              514  LOAD_STR                 'lamps_num'
              516  STORE_SUBSCR     
          518_520  JUMP_FORWARD        782  'to 782'
            522_0  COME_FROM           500  '500'

 L. 390       522  LOAD_FAST                'c'
              524  LOAD_CONST               28
              526  COMPARE_OP               ==
          528_530  POP_JUMP_IF_FALSE   560  'to 560'

 L. 391       532  LOAD_GLOBAL              np
              534  LOAD_METHOD              float
              536  LOAD_FAST                'line'
              538  CALL_METHOD_1         1  '1 positional argument'
              540  LOAD_FAST                'LDT'
              542  LOAD_STR                 'tflux'
              544  STORE_SUBSCR     

 L. 392       546  LOAD_FAST                'LDT'
              548  LOAD_STR                 'tflux'
              550  BINARY_SUBSCR    
              552  LOAD_FAST                'LDT'
              554  LOAD_STR                 'lumens_per_lamp'
              556  STORE_SUBSCR     
              558  JUMP_FORWARD        782  'to 782'
            560_0  COME_FROM           528  '528'

 L. 393       560  LOAD_FAST                'c'
              562  LOAD_CONST               29
              564  COMPARE_OP               ==
          566_568  POP_JUMP_IF_FALSE   584  'to 584'

 L. 394       570  LOAD_FAST                'line'
              572  LOAD_METHOD              rstrip
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  LOAD_FAST                'LDT'
              578  LOAD_STR                 'cct/cri'
              580  STORE_SUBSCR     
              582  JUMP_FORWARD        782  'to 782'
            584_0  COME_FROM           566  '566'

 L. 395       584  LOAD_FAST                'c'
              586  LOAD_CONST               42
              588  COMPARE_OP               >=
              590  LOAD_FAST                'c'
              592  LOAD_CONST               42
              594  LOAD_FAST                'LDT'
              596  LOAD_STR                 'Mc'
              598  BINARY_SUBSCR    
              600  BINARY_ADD       
              602  LOAD_CONST               1
              604  BINARY_SUBTRACT  
              606  COMPARE_OP               <=
              608  BINARY_AND       
          610_612  POP_JUMP_IF_FALSE   632  'to 632'

 L. 396       614  LOAD_FAST                'cangles'
              616  LOAD_METHOD              append
              618  LOAD_GLOBAL              np
              620  LOAD_METHOD              float
              622  LOAD_FAST                'line'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  POP_TOP          
              630  JUMP_FORWARD        782  'to 782'
            632_0  COME_FROM           610  '610'

 L. 397       632  LOAD_FAST                'c'
              634  LOAD_CONST               42
              636  LOAD_FAST                'LDT'
              638  LOAD_STR                 'Mc'
              640  BINARY_SUBSCR    
              642  BINARY_ADD       
              644  COMPARE_OP               >=
              646  LOAD_FAST                'c'
              648  LOAD_CONST               42
              650  LOAD_FAST                'LDT'
              652  LOAD_STR                 'Mc'
              654  BINARY_SUBSCR    
              656  BINARY_ADD       
              658  LOAD_FAST                'LDT'
              660  LOAD_STR                 'Ng'
              662  BINARY_SUBSCR    
              664  BINARY_ADD       
              666  LOAD_CONST               1
              668  BINARY_SUBTRACT  
              670  COMPARE_OP               <=
              672  BINARY_AND       
          674_676  POP_JUMP_IF_FALSE   696  'to 696'

 L. 398       678  LOAD_FAST                'tangles'
            680_0  COME_FROM           196  '196'
              680  LOAD_METHOD              append
              682  LOAD_GLOBAL              np
              684  LOAD_METHOD              float
              686  LOAD_FAST                'line'
              688  CALL_METHOD_1         1  '1 positional argument'
              690  CALL_METHOD_1         1  '1 positional argument'
              692  POP_TOP          
              694  JUMP_FORWARD        782  'to 782'
            696_0  COME_FROM           674  '674'

 L. 399       696  LOAD_FAST                'c'
              698  LOAD_CONST               42
              700  LOAD_FAST                'LDT'
              702  LOAD_STR                 'Mc'
            704_0  COME_FROM           220  '220'
              704  BINARY_SUBSCR    
              706  BINARY_ADD       
              708  LOAD_FAST                'LDT'
              710  LOAD_STR                 'Ng'
              712  BINARY_SUBSCR    
              714  BINARY_ADD       
              716  COMPARE_OP               >=
              718  LOAD_FAST                'c'
              720  LOAD_CONST               42
              722  LOAD_FAST                'LDT'
              724  LOAD_STR                 'Mc'
              726  BINARY_SUBSCR    
            728_0  COME_FROM           244  '244'
              728  BINARY_ADD       
              730  LOAD_FAST                'LDT'
            732_0  COME_FROM           112  '112'
              732  LOAD_STR                 'Ng'
              734  BINARY_SUBSCR    
              736  BINARY_ADD       
              738  LOAD_FAST                'LDT'
              740  LOAD_STR                 'Mc'
              742  BINARY_SUBSCR    
              744  LOAD_FAST                'LDT'
              746  LOAD_STR                 'Ng'
              748  BINARY_SUBSCR    
              750  BINARY_MULTIPLY  
              752  BINARY_ADD       
            754_0  COME_FROM           270  '270'
              754  LOAD_CONST               1
            756_0  COME_FROM           136  '136'
              756  BINARY_SUBTRACT  
              758  COMPARE_OP               <=
              760  BINARY_AND       
          762_764  POP_JUMP_IF_FALSE   782  'to 782'

 L. 400       766  LOAD_FAST                'candela_values'
              768  LOAD_METHOD              append
              770  LOAD_GLOBAL              np
              772  LOAD_METHOD              float
              774  LOAD_FAST                'line'
              776  CALL_METHOD_1         1  '1 positional argument'
              778  CALL_METHOD_1         1  '1 positional argument'
              780  POP_TOP          
            782_0  COME_FROM           762  '762'
            782_1  COME_FROM           694  '694'
            782_2  COME_FROM           630  '630'
            782_3  COME_FROM           582  '582'
            782_4  COME_FROM           558  '558'
            782_5  COME_FROM           518  '518'
            782_6  COME_FROM           490  '490'
            782_7  COME_FROM           462  '462'
            782_8  COME_FROM           434  '434'
            782_9  COME_FROM           408  '408'
           782_10  COME_FROM           380  '380'
           782_11  COME_FROM           352  '352'
           782_12  COME_FROM           324  '324'
           782_13  COME_FROM           296  '296'
           782_14  COME_FROM           284  '284'
           782_15  COME_FROM           160  '160'
           782_16  COME_FROM            78  '78'

 L. 401       782  LOAD_FAST                'c'
              784  LOAD_CONST               1
              786  INPLACE_ADD      
              788  STORE_FAST               'c'
              790  JUMP_BACK            52  'to 52'
              792  POP_BLOCK        
            794_0  COME_FROM_LOOP       44  '44'

 L. 403       794  LOAD_GLOBAL              np
              796  LOAD_METHOD              array
              798  LOAD_FAST                'candela_values'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  STORE_FAST               'candela_values'

 L. 404       804  LOAD_GLOBAL              np
              806  LOAD_METHOD              array
              808  LOAD_FAST                'candela_values'
              810  CALL_METHOD_1         1  '1 positional argument'
              812  LOAD_FAST                'LDT'
              814  LOAD_STR                 'candela_values'
              816  STORE_SUBSCR     

 L. 405       818  LOAD_GLOBAL              np
              820  LOAD_METHOD              array
              822  LOAD_FAST                'candela_values'
              824  CALL_METHOD_1         1  '1 positional argument'
              826  LOAD_METHOD              reshape
              828  LOAD_CONST               -1
              830  LOAD_GLOBAL              np
              832  LOAD_METHOD              int
              834  LOAD_FAST                'LDT'
              836  LOAD_STR                 'Ng'
              838  BINARY_SUBSCR    
              840  CALL_METHOD_1         1  '1 positional argument'
              842  BUILD_TUPLE_2         2 
              844  CALL_METHOD_1         1  '1 positional argument'
              846  STORE_FAST               'candela_2d'

 L. 406       848  LOAD_GLOBAL              np
              850  LOAD_METHOD              array
              852  LOAD_FAST                'cangles'
              854  CALL_METHOD_1         1  '1 positional argument'
              856  LOAD_CONST               None
              858  LOAD_FAST                'candela_2d'
              860  LOAD_ATTR                shape
              862  LOAD_CONST               0
              864  BINARY_SUBSCR    
              866  BUILD_SLICE_2         2 
              868  BINARY_SUBSCR    
              870  LOAD_FAST                'LDT'
              872  LOAD_STR                 'h_angs'
              874  STORE_SUBSCR     

 L. 407       876  LOAD_GLOBAL              np
              878  LOAD_METHOD              array
              880  LOAD_FAST                'tangles'
              882  CALL_METHOD_1         1  '1 positional argument'
              884  LOAD_FAST                'LDT'
              886  LOAD_STR                 'v_angs'
              888  STORE_SUBSCR     

 L. 408       890  LOAD_GLOBAL              np
              892  LOAD_METHOD              array
              894  LOAD_FAST                'candela_2d'
              896  CALL_METHOD_1         1  '1 positional argument'
              898  LOAD_FAST                'LDT'
              900  LOAD_STR                 'candela_2d'
              902  STORE_SUBSCR     

 L. 411       904  LOAD_GLOBAL              _normalize_candela_2d
              906  LOAD_FAST                'LDT'
              908  LOAD_FAST                'normalize'
              910  LOAD_FAST                'multiplier'
              912  LOAD_CONST               ('normalize', 'multiplier')
              914  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              916  STORE_FAST               'LDT'

 L. 414       918  LOAD_GLOBAL              _complete_ldt_lid
              920  LOAD_FAST                'LDT'
              922  LOAD_FAST                'LDT'
              924  LOAD_STR                 'Isym'
              926  BINARY_SUBSCR    
              928  LOAD_CONST               0
              930  BINARY_SUBSCR    
              932  LOAD_CONST               ('Isym',)
              934  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              936  STORE_FAST               'LDT'

 L. 416       938  LOAD_FAST                'LDT'
              940  LOAD_STR                 'intensity'
              942  BINARY_SUBSCR    
              944  LOAD_CONST               1000
              946  BINARY_TRUE_DIVIDE
              948  LOAD_FAST                'LDT'
              950  LOAD_STR                 'tflux'
              952  BINARY_SUBSCR    
              954  BINARY_MULTIPLY  
              956  LOAD_FAST                'LDT'
              958  LOAD_STR                 'Iv0'
              960  STORE_SUBSCR     

 L. 417       962  LOAD_FAST                'LDT'
              964  RETURN_VALUE     
            966_0  COME_FROM_WITH       22  '22'
              966  WITH_CLEANUP_START
              968  WITH_CLEANUP_FINISH
              970  END_FINALLY      

Parse error at or near `LOAD_METHOD' instruction at offset 680


def _complete_ldt_lid(LDT, Isym=4):
    """
    Convert LDT LID map with Isym symmetry to a 'full' map with phi: [0,360] and theta: [0,180].
    """
    cangles = LDT['h_angs']
    tangles = LDT['v_angs']
    candela_2d = LDT['candela_2d']
    if Isym == 4:
        a = candela_2d.copy().T
        b = np.hstack((a, a[:, a.shape[1] - 2::-1]))
        c = np.hstack((b, b[:, b.shape[1] - 2:0:-1]))
        candela_2d_0C360 = np.hstack((c, c[:, :1]))
        cangles = np.hstack((cangles, cangles[1:] + 90, cangles[1:] + 180, cangles[1:] + 270))
        a = candela_2d_0C360.copy()
        b = np.vstack((a, np.zeros(a.shape)[1:, :]))
        tangles = np.hstack((tangles, tangles[1:] + 90))
        candela_2d = b
    else:
        if Isym == -4:
            a = candela_2d.copy().T
            b = np.hstack((a, a[:, a.shape[1] - 2::-1]))
            c = np.hstack((b, b[:, b.shape[1] - 2:0:-1]))
            candela_2d_0C360 = np.hstack((c, c[:, :1]))
            cangles = np.hstack((cangles, -cangles[cangles.shape[0] - 2::-1] + 180))
            cangles = np.hstack((cangles, -cangles[cangles.shape[0] - 2:0:-1] + 360))
            cangles = np.hstack((cangles, cangles[:1]))
            a = candela_2d_0C360.copy()
            b = np.vstack((a, np.zeros(a.shape)[1:, :]))
            tangles = np.hstack((tangles, -tangles[tangles.shape[0] - 2::-1] + 180))
            candela_2d = b
        else:
            raise Exception('complete_ldt_lid(): Other "Isym" than "4", not yet implemented (31/10/2018).')
    LDT['map'] = {'thetas': tangles}
    LDT['map']['phis'] = cangles
    LDT['map']['values'] = candela_2d.T
    return LDT


def _normalize_candela_2d(LID, normalize='I0', multiplier=1):
    candela_2d = LID['candela_2d']
    if normalize == 'max':
        maxval = candela_2d.max()
        norm = maxval
    else:
        if normalize == 'I0':
            I0 = candela_2d[(LID['h_angs'] == 0.0, LID['v_angs'] == 0.0)]
            norm = I0[0]
    candela_2d = candela_2d / norm
    candela_mult = LID['candela_mult']
    intensity = norm * multiplier * candela_mult
    LID['candela_2d'] = candela_2d
    LID['intensity'] = intensity
    return LID