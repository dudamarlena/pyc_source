# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\convtest\update_files.py
# Compiled at: 2020-01-27 18:33:39
# Size of source mod 2**32: 917 bytes
import parser_convtest as genstr

def update_file(param='EOS', param_val=0, template_folder='.'):
    if param == 'KPOINTS':
        genstr.kpoint_update(param_val, kpoint_folder=template_folder)
    elif param == 'EOS':
        genstr.poscar_update(param_val, poscar_folder=template_folder)
    else:
        INCAR_dict, key_order = genstr.incar_parser(INCAR=(template_folder + '/INCAR'))
        INCAR_dict[param] = param_val
        genstr.incar_write(INCAR_dict, key_order, dst_folder=template_folder)