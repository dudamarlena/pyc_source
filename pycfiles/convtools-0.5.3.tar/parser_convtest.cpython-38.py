# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\convtest\parser_convtest.py
# Compiled at: 2020-02-27 14:23:34
# Size of source mod 2**32: 11676 bytes
import os, re, warnings, numpy as np

def input_parser--- This code section failed: ---

 L.  13         0  LOAD_CONST               0
                2  LOAD_STR                 'ALL'
                4  LOAD_CONST               0
                6  LOAD_CONST               ('VASPRUN', 'KEEPRESULT', 'ISTEST')
                8  BUILD_CONST_KEY_MAP_3     3 
               10  STORE_FAST               'dict_input'

 L.  14        12  BUILD_MAP_0           0 
               14  STORE_FAST               'dict_param'

 L.  15        16  LOAD_CONST               0
               18  STORE_FAST               'flag_multi'

 L.  16        20  LOAD_CONST               0
               22  STORE_FAST               'flag_param_start'

 L.  17        24  LOAD_GLOBAL              kwlist_parser
               26  CALL_FUNCTION_0       0  ''
               28  STORE_FAST               'list_kw'

 L.  18        30  LOAD_GLOBAL              open
               32  LOAD_FAST                'INPUT'
               34  LOAD_STR                 'r'
               36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'fopen'

 L.  19        40  LOAD_FAST                'fopen'
               42  GET_ITER         
             44_0  COME_FROM            66  '66'
            44_46  FOR_ITER            480  'to 480'
               48  STORE_FAST               'eachline'

 L.  20        50  LOAD_FAST                'eachline'
               52  LOAD_METHOD              strip
               54  LOAD_STR                 '\n'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'eachline'

 L.  22        60  LOAD_GLOBAL              is_blank_comments
               62  LOAD_FAST                'eachline'
               64  CALL_FUNCTION_1       1  ''
               66  POP_JUMP_IF_TRUE     44  'to 44'

 L.  23        68  LOAD_FAST                'eachline'
               70  LOAD_METHOD              split
               72  LOAD_STR                 '#'
               74  CALL_METHOD_1         1  ''
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  LOAD_METHOD              strip
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'eachline'

 L.  24        86  LOAD_GLOBAL              re
               88  LOAD_METHOD              split
               90  LOAD_STR                 '\\[|\\]'
               92  LOAD_FAST                'eachline'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'filename'

 L.  25        98  LOAD_GLOBAL              len
              100  LOAD_FAST                'filename'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_CONST               1
              106  COMPARE_OP               >
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L.  27       110  LOAD_FAST                'filename'
              112  LOAD_CONST               1
              114  BINARY_SUBSCR    
              116  STORE_FAST               'filename'
              118  JUMP_BACK            44  'to 44'
            120_0  COME_FROM           108  '108'

 L.  30       120  LOAD_GLOBAL              re
              122  LOAD_METHOD              split
              124  LOAD_STR                 '\\s+'
              126  LOAD_FAST                'eachline'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'params'

 L.  31       132  LOAD_FAST                'params'
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  LOAD_METHOD              upper
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'tag'

 L.  32       144  LOAD_FAST                'tag'
              146  LOAD_STR                 'PARAM'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_TRUE    170  'to 170'
              152  LOAD_FAST                'tag'
              154  LOAD_STR                 'PARAMLIST'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_TRUE    170  'to 170'
              160  LOAD_FAST                'tag'
              162  LOAD_STR                 'END_PARAMLIST'
              164  COMPARE_OP               ==
          166_168  POP_JUMP_IF_FALSE   400  'to 400'
            170_0  COME_FROM           158  '158'
            170_1  COME_FROM           150  '150'

 L.  35       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'params'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_CONST               1
              178  COMPARE_OP               >
          180_182  POP_JUMP_IF_FALSE   298  'to 298'

 L.  37       184  LOAD_FAST                'tag'
              186  LOAD_STR                 'PARAM'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   236  'to 236'

 L.  39       192  LOAD_FAST                'flag_param_start'
              194  LOAD_CONST               1
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   208  'to 208'

 L.  40       200  LOAD_GLOBAL              IOError
              202  LOAD_STR                 'No PARAMLIST after PARAM'
              204  CALL_FUNCTION_1       1  ''
              206  RAISE_VARARGS_1       1  ''
            208_0  COME_FROM           198  '198'

 L.  41       208  LOAD_FAST                'params'
              210  LOAD_CONST               1
              212  BINARY_SUBSCR    
              214  LOAD_METHOD              upper
              216  CALL_METHOD_0         0  ''
              218  STORE_FAST               'tag_key'

 L.  42       220  LOAD_GLOBAL              is_in_kwlist
              222  LOAD_FAST                'tag_key'
              224  LOAD_FAST                'list_kw'
              226  CALL_FUNCTION_2       2  ''
              228  POP_JUMP_IF_FALSE   234  'to 234'

 L.  43       230  LOAD_CONST               1
              232  STORE_FAST               'flag_param_start'
            234_0  COME_FROM           228  '228'
              234  JUMP_FORWARD        296  'to 296'
            236_0  COME_FROM           190  '190'

 L.  45       236  LOAD_FAST                'tag'
              238  LOAD_STR                 'PARAMLIST'
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   398  'to 398'

 L.  47       246  LOAD_FAST                'flag_param_start'
              248  LOAD_CONST               0
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   264  'to 264'

 L.  48       256  LOAD_GLOBAL              IOError
              258  LOAD_STR                 'Multi PARAMLISTs for current PARAM'
              260  CALL_FUNCTION_1       1  ''
              262  RAISE_VARARGS_1       1  ''
            264_0  COME_FROM           252  '252'

 L.  49       264  LOAD_FAST                'params'
              266  LOAD_CONST               1
              268  LOAD_CONST               None
              270  BUILD_SLICE_2         2 
              272  BINARY_SUBSCR    
              274  STORE_FAST               'tag_val_tmp'

 L.  50       276  LOAD_GLOBAL              paramlist_parser
              278  LOAD_FAST                'tag_val_tmp'
              280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'tag_val'

 L.  52       284  LOAD_FAST                'tag_val'
              286  LOAD_FAST                'dict_param'
              288  LOAD_FAST                'tag_key'
              290  STORE_SUBSCR     

 L.  53       292  LOAD_CONST               0
              294  STORE_FAST               'flag_param_start'
            296_0  COME_FROM           234  '234'
              296  JUMP_FORWARD        398  'to 398'
            298_0  COME_FROM           180  '180'

 L.  57       298  LOAD_FAST                'tag'
              300  LOAD_STR                 'PARAMLIST'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   354  'to 354'

 L.  58       308  LOAD_FAST                'flag_param_start'
              310  LOAD_CONST               0
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   326  'to 326'

 L.  59       318  LOAD_GLOBAL              IOError
              320  LOAD_STR                 'Multi PARAMLISTs for current PARAM'
              322  CALL_FUNCTION_1       1  ''
              324  RAISE_VARARGS_1       1  ''
            326_0  COME_FROM           314  '314'

 L.  60       326  LOAD_FAST                'flag_multi'
              328  LOAD_CONST               1
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   344  'to 344'

 L.  61       336  LOAD_GLOBAL              IOError
              338  LOAD_STR                 'No end mark for current PARAMLIST'
              340  CALL_FUNCTION_1       1  ''
              342  RAISE_VARARGS_1       1  ''
            344_0  COME_FROM           332  '332'

 L.  62       344  LOAD_CONST               1
              346  STORE_FAST               'flag_multi'

 L.  63       348  BUILD_LIST_0          0 
              350  STORE_FAST               'tag_val'
              352  JUMP_FORWARD        398  'to 398'
            354_0  COME_FROM           304  '304'

 L.  64       354  LOAD_FAST                'tag'
              356  LOAD_STR                 'END_PARAMLIST'
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   478  'to 478'

 L.  65       364  LOAD_FAST                'flag_multi'
              366  LOAD_CONST               0
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   382  'to 382'

 L.  66       374  LOAD_GLOBAL              IOError
              376  LOAD_STR                 'redundent end mark for current PARAMLIST'
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  ''
            382_0  COME_FROM           370  '370'

 L.  67       382  LOAD_CONST               0
              384  STORE_FAST               'flag_multi'

 L.  68       386  LOAD_FAST                'tag_val'
              388  LOAD_FAST                'dict_param'
              390  LOAD_FAST                'tag_key'
              392  STORE_SUBSCR     

 L.  69       394  LOAD_CONST               0
              396  STORE_FAST               'flag_param_start'
            398_0  COME_FROM           352  '352'
            398_1  COME_FROM           296  '296'
            398_2  COME_FROM           242  '242'
              398  JUMP_BACK            44  'to 44'
            400_0  COME_FROM           166  '166'

 L.  71       400  LOAD_FAST                'flag_multi'
          402_404  POP_JUMP_IF_FALSE   418  'to 418'

 L.  73       406  LOAD_FAST                'tag_val'
              408  LOAD_METHOD              append
              410  LOAD_FAST                'params'
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          
              416  JUMP_BACK            44  'to 44'
            418_0  COME_FROM           402  '402'

 L.  79       418  LOAD_FAST                'tag'
              420  LOAD_FAST                'list_kw'
              422  COMPARE_OP               in
          424_426  POP_JUMP_IF_FALSE   466  'to 466'

 L.  80       428  LOAD_FAST                'tag'
              430  LOAD_METHOD              upper
              432  CALL_METHOD_0         0  ''
              434  STORE_FAST               'tag_key'

 L.  81       436  LOAD_FAST                'params'
              438  LOAD_CONST               1
              440  LOAD_CONST               None
              442  BUILD_SLICE_2         2 
              444  BINARY_SUBSCR    
              446  STORE_FAST               'tag_val_tmp'

 L.  82       448  LOAD_GLOBAL              paramlist_parser
              450  LOAD_FAST                'tag_val_tmp'
              452  CALL_FUNCTION_1       1  ''
              454  STORE_FAST               'tag_val'

 L.  83       456  LOAD_FAST                'tag_val'
              458  LOAD_FAST                'dict_param'
              460  LOAD_FAST                'tag_key'
              462  STORE_SUBSCR     
              464  JUMP_BACK            44  'to 44'
            466_0  COME_FROM           424  '424'

 L.  87       466  LOAD_FAST                'params'
              468  LOAD_CONST               1
              470  BINARY_SUBSCR    
              472  LOAD_FAST                'dict_input'
              474  LOAD_FAST                'tag'
              476  STORE_SUBSCR     
            478_0  COME_FROM           360  '360'
              478  JUMP_BACK            44  'to 44'

 L.  88       480  LOAD_FAST                'dict_param'
              482  LOAD_FAST                'dict_input'
              484  BUILD_TUPLE_2         2 
              486  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 480


def incar_parser(INCAR='./template/INCAR'):
    """
    The test INCAR file is taken from https://cms.mpi.univie.ac.at/vasp/guide/node91.html
    Input: INCAR
        Requires: the value can't contain space, for example the value for the SYSTEM
    Output :
        INCAR_dict : A dict contains all the parameters(key) in the INCAR file and corresponding settings(value)
        key_order : A list contains all the parameters as the order of the original INCAR file
    """
    INCAR_dict = {}
    key_order = []
    fopen = openINCAR'r'
    for eachline in fopen:
        eachline = eachline.strip'\n'
        eachline = is_blank_comments(eachline) or eachline.split'#'[0].strip
        linei = eachline.split';'
        for tags in linei:
            tagsi = tags.split'='
            if len(tagsi) > 1:
                incar_key = re.split'\\s+'tagsi[0].strip[0]
                incar_val = re.split'\\s+'tagsi[1].strip[0]
                INCAR_dict[incar_key] = incar_val
                key_order.appendincar_key

        return (
         INCAR_dict, key_order)


def incar_write(INCAR_dict, key_order, dst_folder='.'):
    incar = open(dst_folder + '/INCAR')'w+'
    for keys in key_order:
        incar.write('%s  =  %s\n' % (keys, INCAR_dict[keys]))

    incar.close


def kpoint_update(kpoints, kpoint_folder='.'):
    if type(kpoints) is int or type(kpoints) is float:
        kpoints = str(int(kpoints))
        kpoints = [kpoints, kpoints, kpoints]
    elif type(kpoints) is str:
        try:
            kpoints = str(int(float(kpoints)))
            kpoints = [kpoints, kpoints, kpoints]
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    elif type(kpoints) is list and len(kpoints) == 3:
        pass
    else:
        raise IOError('The input of the type of length of kpoints is not correct')
    kp_template = open(kpoint_folder + '/KPOINTS')'r'
    kp_file = open(kpoint_folder + '/KPOINTStmp')'w+'
    k_count = 0
    for eachline in kp_template:
        if k_count == 3:
            kp_file.write('  %d  %d  %d\n' % (int(kpoints[0]), int(kpoints[1]), int(kpoints[2])))
        else:
            kp_file.writeeachline
        k_count = k_count + 1

    kp_template.close
    kp_file.close
    os.remove(kpoint_folder + '/KPOINTS')
    os.rename(kpoint_folder + '/KPOINTStmp')(kpoint_folder + '/KPOINTS')


def poscar_update(scale_factor, poscar_folder='.', scale_type='v'):
    pos_template = open(poscar_folder + '/POSCAR')'r'
    pos_file = open(poscar_folder + '/postmp')'w+'
    pos_count = 0
    for eachline in pos_template:
        if pos_count == 1:
            if scale_type == 'v':
                scale_factor = float(1.0 + float(scale_factor) / 100.0) ** 0.3333333333333333
            else:
                scale_factor = float(1.0 + float(scale_factor) / 100.0)
            scale_factor_new = float(eachline.strip'\n'.strip) * scale_factor
            pos_file.write('%f\n' % scale_factor_new)
        else:
            pos_file.writeeachline
        pos_count = pos_count + 1

    pos_template.close
    pos_file.close
    os.remove(poscar_folder + '/POSCAR')
    os.rename(poscar_folder + '/postmp')(poscar_folder + '/POSCAR')


def get_base_vec(poscar_folder='.'):
    BaseVec = np.zeros(3, 3)
    FileName = 'POSCAR'
    fopen = openFileName'r'
    pos_count = 0
    scale_factor = 1.0
    for eachline in fopen:
        if pos_count == 1:
            scale_factor = float(eachline.strip'\n'.strip)
        if pos_count > 1:
            linei = eachline.strip'\n'.strip
            linei = re.split'\\s+'linei
            for j in range03:
                BaseVec[(pos_count - 2)][j] = float(linei[j])

        else:
            if pos_count > 3:
                return (BaseVec, scale_factor)
            pos_count = pos_count + 1

    return (
     BaseVec, scale_factor)


def get_vol(poscar_folder='.'):
    basevec, scale_factor = get_base_vec(poscar_folder)
    V = np.powerscale_factor3 * np.linalg.detbasevec
    return V


def kwlist_parser(KWLIST='kwlist'):
    kwPath = os.path.dirname__file__
    list_kw = []
    fopen = open(kwPath + '/' + KWLIST)'r'
    for eachline in fopen:
        eachline = eachline.strip'\n'
        if not is_blank_comments(eachline):
            list_kw.appendeachline
        return list_kw


def is_blank_comments(line):
    flag = 0
    if len(line) < 1:
        flag = 1
    elif line[0] == '#':
        flag = 1
    return flag


def is_in_kwlist(kw, kwlist):
    flag = 0
    if kw in kwlist:
        flag = 1
    else:
        warnings.warn('Warning: The keyword ' + kw + ' is not in the keyword list, and it is neglected.')
    return flag


def paramlist_parser(paramlist):
    if len(paramlist) > 1:
        tag_val = paramlist
    else:
        range_param = paramlist[0].split'..'
        range_param = [float(x) for x in range_param]
        range_param = np.arange(range_param[0], range_param[2] + range_param[1], range_param[1])
        tag_val = [str(x) for x in range_param]
    return tag_val


def get_energy(folder_name='.'):
    FileName = folder_name + '/OSZICAR'
    fopen = openFileName'r'
    for eachline in fopen:
        linei = eachline.split'='
        if len(linei) > 2:
            energy = linei[2].strip.split' '[0]
        fopen.close
        energy = float(energy)
        return energy


def code_run():
    runstr = 'mpirun vasp_std'
    return runstr


def gen_sc():
    pass