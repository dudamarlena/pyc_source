# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\convtest\convtest_prl.py
# Compiled at: 2020-02-27 14:18:35
# Size of source mod 2**32: 6911 bytes
from sys import argv
import random, warnings, shutil, os, re, numpy as np
import convtest.parser_convtest as cnvt

def write_head(filename, flag_pbs, pbs_file):
    if flag_pbs:
        os.system('cp ' + pbs_file + ' ' + filename)
    else:
        fid = open(filename, 'w+')
        fid.write('#!sh\n')
        fid.close()


def update_file(param='EOS', param_val=0, template_folder='.'):
    if param == 'KPOINTS':
        cnvt.kpoint_update(param_val, kpoint_folder=template_folder)
    else:
        if param == 'EOS':
            cnvt.poscar_update(param_val, poscar_folder=template_folder)
        else:
            INCAR_dict, key_order = cnvt.incar_parser(INCAR=(template_folder + '/INCAR'))
            INCAR_dict[param] = param_val
            cnvt.incar_write(INCAR_dict, key_order, dst_folder=template_folder)


def convtest(template_folder='template', input_file='INPUT.convtest', pbs_file='convtest.pbs'):
    pbs_file = template_folder + '/' + pbs_file
    if input_file == '.':
        input_file = 'INPUT.convtest'
    else:
        if not os.path.exists(input_file):
            raise IOError("The input file doesn't exist.")
        dict_param, dict_input = cnvt.input_parser(INPUT=input_file)
        VASPRUN = int(dict_input['VASPRUN'])
        KPRESULT = dict_input['KEEPRESULT']
        flag_test = int(dict_input['ISTEST'])
        if not os.path.exists(pbs_file):
            if not VASPRUN:
                warnings.warn("pbs file doesn't exist. Shell scripts will be generated.")
            script_ext = '.sh'
            flag_pbs = 0
        else:
            script_ext = '.pbs'
        flag_pbs = 1
    for PARAM in dict_param:
        name_fileout = 'ConvTest_' + PARAM + '.txt'
        os.mkdir(PARAM)
        paramlist = dict_param[PARAM]
        list_convtest = []
        param_val_count = 0
        for param_val in paramlist:
            if type(param_val) is list:
                name_subfolder = PARAM + '/' + '-'.join(param_val)
            else:
                name_subfolder = PARAM + '/' + param_val
            os.mkdir(name_subfolder)
            os.system('cp ' + template_folder + '/* ' + name_subfolder)
            if VASPRUN == 1:
                if PARAM != 'EOS':
                    if param_val_count > 0:
                        os.system('cp ' + name_prefolder + '/CONTCAR ' + name_subfolder + '/POSCAR')
                    name_prefolder = name_subfolder
                    param_val_count = param_val_count + 1
                print(param_val)
                update_file(PARAM, param_val, name_subfolder)
                if VASPRUN == 1:
                    os.chdir(name_subfolder)
                    if flag_test:
                        energy = random.random()
                    else:
                        os.system(cnvt.code_run())
                        os.system('rm WAVECAR CHG* vasprun.xml')
                        energy = cnvt.get_energy()
                    if PARAM == 'EOS':
                        V = cnvt.get_vol()
                        list_convtest.append([param_val, V, str(energy)])
                    else:
                        list_convtest.append([param_val, str(energy)])
                    os.chdir('../../')
                if VASPRUN == 0:
                    name_script = 'script_' + PARAM + script_ext
                    write_head(name_script, flag_pbs, pbs_file)
                    fid = open(name_script, 'a+')
                    fid.write('for param in ' + ' '.join(paramlist) + ';\n')
                    fid.write('do\n')
                    fid.write('cd ' + PARAM + '/$param\n')
                    fid.write(cnvt.code_run() + '\n')
                    fid.write('E=`tail -1 OSZICAR | awk \'{printf "%12.6f \\n", $5}\'`\n')
                    fid.write('cd ../../\n')
                    fid.write('echo $param $E >> ' + name_fileout + '\n')
                    fid.write('done\n')
                    fid.close()
            else:
                fid = open(name_fileout, 'w')
                for i in range(0, len(list_convtest)):
                    for x in list_convtest[i]:
                        fid.write(str(x))
                        fid.write('\t')
                    else:
                        fid.write('\n')

                else:
                    fid.close()

                if KPRESULT == 'MIN':
                    os.system('rm -rf ' + PARAM)