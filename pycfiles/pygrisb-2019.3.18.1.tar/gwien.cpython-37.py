# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/run/gwien.py
# Compiled at: 2019-02-25 22:36:44
# Size of source mod 2**32: 27507 bytes
import os, sys, glob, h5py, socket, shutil, time, re, subprocess, warnings, numpy as np
from collections import deque
from subprocess import Popen, PIPE
from pygrisb.io.fio import file_exists
import pygrisb.run.environ as env

def get_file_info(fname, unit, idmf, case, scratch, so, para, cmplx, _band, updn, dnup):
    """help function to setup informations in def file.
    """
    if 'in2' == fname:
        return [
         unit, "'{}.in2{}'".format(case, cmplx), "'old'",
         "'formatted'", 0]
        if 'inso' == fname:
            return [
             unit, "'{}.inso'".format(case), "'unknown'", "'formatted'", 0]
        if 'indmfl' == fname:
            return [
             unit, "'{}.indmfl'".format(case), "'old'", "'formatted'", 0]
        if 'outputdmfupdn' == fname:
            return [
             unit, "'{}.outputdmf{}{}'".format(case, idmf, updn),
             "'unknown'", "'formatted'", 0]
        if 'in1c' == fname:
            return [
             unit, "'{}.in1c'".format(case), "'unknown'", "'formatted'", 0]
        if 'vectorupdn' == fname:
            return [
             unit,
             "'{}/{}.vector{}{}{}'".format(scratch, case, so, updn, para), "'unknown'", "'unformatted'", 9000]
        if 'vectordnup' == fname:
            return [
             unit,
             "'{}/{}.vector{}{}{}'".format(scratch, case, so, dnup, para), "'unknown'", "'unformatted'", 9000]
        if 'klist' == fname:
            return [
             unit, "'{}.klist{}'".format(case, _band), "'old'",
             "'formatted'", 0]
        if 'kgen' == fname:
            return [
             unit, "'{}.kgen'".format(case), "'unknown'", "'formatted'", 0]
        if 'vspupdn' == fname:
            return [
             unit, "'{}.vsp{}'".format(case, updn), "'old'",
             "'formatted'", 0]
        if 'vspdnup' == fname:
            return [
             unit, "'{}.vsp{}'".format(case, dnup), "'unknown'",
             "'formatted'", 0]
        if 'struct' == fname:
            return [
             unit, "'{}.struct'".format(case), "'old'", "'formatted'", 0]
        if 'rotlm' == fname:
            return [
             unit, "'{}.rotlm'".format(case), "'unknown'", "'formatted'", 0]
        if 'energysodum' == fname:
            if so == 'so':
                sodum = 'dum'
            else:
                sodum = dnup
            return [
             unit, "'{}.energy{}'".format(case, sodum),
             "'unknown'", "'formatted'", 0]
        if 'energyupdn' == fname:
            return [
             unit, "'{}.energy{}{}{}'".format(case, so, updn, para),
             "'unknown'", "'formatted'", 0]
        if 'energydnup' == fname:
            return [
             unit, "'{}.energy{}{}{}'".format(case, so, dnup, para),
             "'unknown'", "'formatted'", 0]
        if 'clmval' == fname:
            return [
             unit, "'{}.clmval{}'".format(case, updn), "'unknown'",
             "'formatted'", 0]
        if 'recprlist' == fname:
            return [
             unit, "'{}.recprlist'".format(case), "'unknown'",
             "'formatted'", 9000]
    else:
        if 'scf2updn' == fname:
            return [
             unit, "'{}.scf2{}'".format(case, updn),
             "'unknown'", "'formatted'", 0]
            if 'normupdn' == fname:
                if so == 'so' and updn == '':
                    _updn = 'up'
        else:
            _updn = updn
        return [
         unit, "'{}.norm{}{}{}'".format(case, so, _updn, para),
         "'unknown'", "'formatted'", 0]
    if 'normdnup' == fname:
        return [
         unit, "'{}.norm{}{}{}'".format(case, so, dnup, para),
         "'unknown'", "'formatted'", 0]
    raise ValueError('No matching file name {}!'.format(fname))


def fcreate_def_gwien(case, scratch='.', so='', para='', idmf='1', cmplx='', _band='', updn='', dnup='dn'):
    """create gwien1/2.def file.
    """
    fdef = open('gwien{}{}.def'.format(idmf, updn), 'w')
    if idmf == '1':
        fname_list = [
         'in2', 'inso', 'indmfl', 'outputdmfupdn',
         'in1c', 'vectorupdn', 'vectordnup', 'klist',
         'kgen', 'vspupdn', 'vspdnup', 'struct',
         'rotlm', 'energydnup', 'energyupdn', 'normupdn',
         'normdnup']
        unit_list = [3, 4, 5, 6,
         7, 9, 10, 13,
         14, 18, 19, 20,
         22, 59, 60, 12,
         11]
    else:
        if idmf == '2':
            fname_list = [
             'in1c', 'inso', 'in2', 'outputdmfupdn', 'indmfl',
             'clmval', 'vectorupdn', 'vectordnup', 'recprlist', 'kgen',
             'vspupdn', 'struct', 'scf2updn', 'rotlm', 'energyupdn',
             'normupdn', 'normdnup']
            unit_list = [3, 4, 5, 6, 7,
             8, 9, 10, 13, 14,
             18, 20, 21, 22, 30,
             12, 11]
    for fname, unit in zip(fname_list, unit_list):
        fdef.write(('{:3d}, {:<15s}, {:<10s}, {:<13s}, {:<4d}\n'.format)(*get_file_info(fname, unit, idmf, case, scratch, so, para, cmplx, _band, updn, dnup)))

    fdef.close()


def onestep(fday, case, exec_name, w_root, para='', so='', band=None, updn=None):
    """wien2k steps.
    """
    time_start = time.strftime('%H:%M:%S')
    cmd = ['{}/x'.format(w_root), exec_name, '-f', case]
    if para != '':
        cmd.append(para)
    if band == '-band':
        cmd.append(band)
        if not os.path.isfile('EFLDA.INP'):
            shutil.copy2('EFLDA.OUT', 'EFLDA.INP')
    if updn in ('-up', '-dn'):
        cmd.append(updn)
    if so == 'so':
        cmd.extend(['-c', '-so'])
    print(' '.join((x for x in cmd)))
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    fday.write('>{:<10s} ({}) {}\n'.format(exec_name, time_start, out[:-1].decode()))
    fday.flush()
    for f in glob.glob('{}.error*'.format(exec_name)):
        if os.path.getsize(f) > 0:
            print('error in {} from file: {}'.format(f, open(f, 'r').readlines()))
            sys.exit(1)


def gonestep(fday, exec_name, mpi, updn='', gpath=os.environ['WIEN_GUTZ_ROOT']):
    """gwien1, CyGutz and gwien2 steps.
    """
    time_start = time.strftime('%H:%M:%S')
    with open(':log', 'a') as (f):
        f.write('{}>   {}\n'.format(time.strftime('%a %b %d %H:%M:%S %Z %Y'), exec_name))
    cmd = ['/usr/bin/time']
    if mpi != '':
        cmd.extend(mpi)
    cmd.append('{}'.format(exec_name))
    if 'gwien' in exec_name:
        cmd.append('{}{}.def'.format(exec_name, updn))
    if 'CyGutz' in exec_name:
        cmd += ['-p', gpath]
    print(' '.join((x for x in cmd)))
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    with open('{}_info.out'.format(exec_name), 'w') as (f):
        f.write(out.decode())
    fday.write('>{:<10s} ({}) {}\n'.format(exec_name, time_start, err.splitlines()[(-2)].decode()))
    fday.flush()
    for f in glob.glob('{}.error*'.format(exec_name)):
        if os.path.getsize(f) > 0:
            print('error in {} from file: {}'.format(f, open(f, 'r').readlines()))
            sys.exit(1)


def get_file_content(fname):
    if os.path.exists(fname):
        data = '\n------- {} --------\n'.format(fname)
        with open(fname, 'r') as (f):
            data += f.read()
        return data
    return ''


def scf(case, spinpol):
    if spinpol:
        f_list = ['{}.scf{}'.format(case, i) for i in ('0', '1up', '1dn', 'so', '2up',
                                                       '2dn', '1s', '2s', 'cup',
                                                       'cdn')]
    else:
        f_list = ['{}.scf{}'.format(case, i) for i in ('0', '1', 'so', '2', '1s', '2s',
                                                       'c')]
    data = ''.join((get_file_content(f) for f in f_list))
    with open('{}.scf'.format(case), 'a') as (f):
        f.write(data)
    if spinpol:
        f_list = [
         'clmsum', 'vspup', 'vspdn', 'vnsup', 'vnsdn', 'vrespsum',
         'clmdn', 'clmup']
    else:
        f_list = [
         'clmsum', 'vsp', 'vns', 'vrespsum']
    for i in f_list:
        name = '{}.{}'.format(case, i)
        if file_exists(name):
            shutil.copy2(name, '{}_old'.format(name))


def scfm(case):
    f_scf = '{}.scfm'.format(case)
    data = get_file_content(f_scf)
    with open('{}.scf'.format(case), 'a') as (f):
        f.write(data)


def diff(fday, case, mix_dc, avg_dc, gskip):
    e_que = deque([], 2)
    with open('{}.scf'.format(case), 'r') as (f):
        for line in f:
            if ':DIS' in line:
                d_rho = float(line.split()[(-1)])
            if ':ENE' in line:
                e_que.append(float(line.split()[(-1)]))

    if len(e_que) == 2:
        d_etot = np.abs(e_que[1] - e_que[0])
    else:
        d_etot = 0.0
    dcv_err = 0.0
    if not gskip:
        with h5py.File('GPARAM.h5', 'a') as (f):
            ldc = f['/dc_mode'][0]
            if os.path.isfile('GDC_NELF_OUT.h5'):
                with h5py.File('GDC_NELF_OUT.h5', 'r') as (fp):
                    nelf_list_inp = fp['/dc_nelf_list_inp'][()]
                    nelf_list_out = fp['/dc_nelf_list_out'][()]
                nelf_diff_list = nelf_list_out - nelf_list_inp
                nelf_list_mix = nelf_list_inp + mix_dc * nelf_diff_list
                if avg_dc:
                    valup = np.sum(nelf_list_mix[:, 0]) / nelf_list_mix.shape[0]
                    valdn = np.sum(nelf_list_mix[:, 1]) / nelf_list_mix.shape[0]
                    nelf_list_mix = [[valup, valdn] for x in nelf_list_inp]
                if ldc == 12:
                    if avg_dc:
                        dcv_err = np.sum(nelf_diff_list) / len(nelf_list_mix)
                    else:
                        dcv_err = np.max(np.abs(nelf_diff_list))
                    if '/dc_nelf_list' in f:
                        f['/dc_nelf_list'][()] = nelf_list_mix
                    else:
                        f['/dc_nelf_list'] = nelf_list_mix
    fday.write(':ENERGY convergence: {}\n'.format(d_etot))
    fday.write(':CHARGE convergence: {}\n'.format(d_rho))
    fday.write(':VDC convergence: {}\n'.format(dcv_err))
    return (d_rho, d_etot, dcv_err)


def processes_convert(so, updn):
    if not file_exists('.processes'):
        print('.processes file not present. It must be a serial run.')
        return
    lines = open('.processes', 'r').readlines()
    work = {}
    nkstart = 0
    for line in lines:
        data = line.split(':')
        if data[0].strip().isdigit():
            vecn = ['emmanuel' for i in range(6)]
            i, nkp, nprc = map(int, data[::2])
            if not so:
                fdef = open('{}lapw1_{}.def'.format(updn, i), 'r')
                for line in fdef:
                    data = line.split(',')
                    data0 = int(data[0])
                    if not data0 == 10:
                        if data0 == 11:
                            data0 = data0 % 10
                            m = re.search('.*[\'|"](.*)_(\\d+)', data[1])
                            if not m is not None:
                                raise AssertionError('vector file to macth  lapw1.def not found!')
                        vecn[data0 * 2] = '{}_{}'.format(m.group(1), m.group(2))
                        vecn[data0 * 2 + 1] = '{}dn_{}'.format(m.group(1), m.group(2))

                fdef.close()
            else:
                fdef = open('{}lapwso_{}.def'.format(updn, i), 'r')
                for line in fdef:
                    data = line.split(',')
                    if int(data[0]) == 42:
                        vecn[0] = data[1].split("'")[1]
                    elif int(data[0]) == 41:
                        vecn[1] = data[1].split("'")[1]
                    elif int(data[0]) == 52:
                        vecn[2] = data[1].split("'")[1]
                    elif int(data[0]) == 51:
                        vecn[3] = data[1].split("'")[1]
                    elif int(data[0]) == 46:
                        vecn[4] = data[1].split("'")[1]
                    elif int(data[0]) == 45:
                        vecn[5] = data[1].split("'")[1]

                fdef.close()
            if work.has_key(nprc):
                work[nprc].append((i, nkp, nkstart, vecn))
            else:
                work[nprc] = [
                 (
                  i, nkp, nkstart, vecn)]
            nkstart += nkp

    for prc in sorted(work.keys()):
        fo = open('_processes_{}'.format(prc - 1), 'w')
        for i, nkp, nkstart, vecn in work[prc]:
            fo.write(('{} {} {} "{}" "{}" "{}" "{}" "{}" "{}"\n'.format)(i, nkp, nkstart, *vecn))


def create_gomp_file():
    """
    Create GOMP.h5 file based on GMPI_X.h5 for openMP execution.
    """
    with h5py.File('GMPI_0.h5', 'r') as (f):
        num_procs = f['/nprocs'][0]
    nvec = 0
    kvec1 = []
    kvec2 = []
    for iproc in range(num_procs):
        with h5py.File('GMPI_' + str(iproc) + '.h5', 'r') as (f):
            nvec += f['/nvec'][0]
            kvec = f['/KVEC'][()].T
            kvec1.append(kvec[0])
            if kvec.shape[1] == 2:
                kvec2.append(kvec[1])

    kvec = np.asarray(kvec1 + kvec2)
    with h5py.File('GOMP.h5', 'w') as (f):
        f['/nvec'] = np.asarray([nvec])
        f['/KVEC'] = kvec.T


def run_gwien--- This code section failed: ---

 L. 355         0  LOAD_STR                 '-s'
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                argv
                6  COMPARE_OP               in
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 356        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                argv
               14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                argv
               18  LOAD_METHOD              index
               20  LOAD_STR                 '-s'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  LOAD_CONST               1
               26  BINARY_ADD       
               28  BINARY_SUBSCR    
               30  STORE_FAST               'startp'
             32_0  COME_FROM             8  '8'

 L. 357        32  LOAD_STR                 '-e'
               34  LOAD_GLOBAL              sys
               36  LOAD_ATTR                argv
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    64  'to 64'

 L. 358        42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                argv
               46  LOAD_GLOBAL              sys
               48  LOAD_ATTR                argv
               50  LOAD_METHOD              index
               52  LOAD_STR                 '-e'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  LOAD_CONST               1
               58  BINARY_ADD       
               60  BINARY_SUBSCR    
               62  STORE_FAST               'endp'
             64_0  COME_FROM            40  '40'

 L. 359        64  LOAD_STR                 '-cc'
               66  LOAD_GLOBAL              sys
               68  LOAD_ATTR                argv
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE   100  'to 100'

 L. 360        74  LOAD_GLOBAL              float
               76  LOAD_GLOBAL              sys
               78  LOAD_ATTR                argv
               80  LOAD_GLOBAL              sys
               82  LOAD_ATTR                argv
               84  LOAD_METHOD              index
               86  LOAD_STR                 '-cc'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  BINARY_SUBSCR    
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  STORE_FAST               'cc'
            100_0  COME_FROM            72  '72'

 L. 361       100  LOAD_STR                 '-ec'
              102  LOAD_GLOBAL              sys
              104  LOAD_ATTR                argv
              106  COMPARE_OP               in
              108  POP_JUMP_IF_FALSE   136  'to 136'

 L. 362       110  LOAD_GLOBAL              float
              112  LOAD_GLOBAL              sys
              114  LOAD_ATTR                argv
              116  LOAD_GLOBAL              sys
              118  LOAD_ATTR                argv
              120  LOAD_METHOD              index
              122  LOAD_STR                 '-ec'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  LOAD_CONST               1
              128  BINARY_ADD       
              130  BINARY_SUBSCR    
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  STORE_FAST               'ec'
            136_0  COME_FROM           108  '108'

 L. 363       136  LOAD_STR                 '-vc'
              138  LOAD_GLOBAL              sys
              140  LOAD_ATTR                argv
              142  COMPARE_OP               in
              144  POP_JUMP_IF_FALSE   172  'to 172'

 L. 364       146  LOAD_GLOBAL              float
              148  LOAD_GLOBAL              sys
              150  LOAD_ATTR                argv
              152  LOAD_GLOBAL              sys
              154  LOAD_ATTR                argv
              156  LOAD_METHOD              index
              158  LOAD_STR                 '-vc'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  LOAD_CONST               1
              164  BINARY_ADD       
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  STORE_FAST               'vc'
            172_0  COME_FROM           144  '144'

 L. 365       172  LOAD_STR                 '-n'
              174  LOAD_GLOBAL              sys
              176  LOAD_ATTR                argv
              178  COMPARE_OP               in
              180  POP_JUMP_IF_FALSE   208  'to 208'

 L. 366       182  LOAD_GLOBAL              int
              184  LOAD_GLOBAL              sys
              186  LOAD_ATTR                argv
              188  LOAD_GLOBAL              sys
              190  LOAD_ATTR                argv
              192  LOAD_METHOD              index
              194  LOAD_STR                 '-n'
              196  CALL_METHOD_1         1  '1 positional argument'
              198  LOAD_CONST               1
              200  BINARY_ADD       
              202  BINARY_SUBSCR    
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  STORE_FAST               'nmaxiter'
            208_0  COME_FROM           180  '180'

 L. 367       208  LOAD_STR                 '-omp'
              210  LOAD_GLOBAL              sys
              212  LOAD_ATTR                argv
              214  COMPARE_OP               in
              216  POP_JUMP_IF_FALSE   230  'to 230'

 L. 368       218  LOAD_CONST               True
              220  STORE_FAST               'openmp'

 L. 369       222  LOAD_GLOBAL              print
              224  LOAD_STR                 'Using Open-MP instead of MPI of CyGutz.'
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  POP_TOP          
            230_0  COME_FROM           216  '216'

 L. 370       230  LOAD_STR                 '-amix'
              232  LOAD_GLOBAL              sys
              234  LOAD_ATTR                argv
              236  COMPARE_OP               in
          238_240  POP_JUMP_IF_FALSE   268  'to 268'

 L. 371       242  LOAD_GLOBAL              float
              244  LOAD_GLOBAL              sys
              246  LOAD_ATTR                argv
              248  LOAD_GLOBAL              sys
              250  LOAD_ATTR                argv
              252  LOAD_METHOD              index
              254  LOAD_STR                 '-amix'
              256  CALL_METHOD_1         1  '1 positional argument'
              258  LOAD_CONST               1
              260  BINARY_ADD       
              262  BINARY_SUBSCR    
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  STORE_FAST               'mix_dc'
            268_0  COME_FROM           238  '238'

 L. 372       268  LOAD_STR                 '-band'
              270  LOAD_GLOBAL              sys
              272  LOAD_ATTR                argv
              274  COMPARE_OP               in
          276_278  POP_JUMP_IF_FALSE   284  'to 284'

 L. 373       280  LOAD_STR                 '-band'
              282  STORE_FAST               'band'
            284_0  COME_FROM           276  '276'

 L. 374       284  LOAD_STR                 '-dos'
              286  LOAD_GLOBAL              sys
              288  LOAD_ATTR                argv
              290  COMPARE_OP               in
          292_294  POP_JUMP_IF_FALSE   300  'to 300'

 L. 375       296  LOAD_STR                 '-dos'
              298  STORE_FAST               'dos'
            300_0  COME_FROM           292  '292'

 L. 376       300  LOAD_STR                 '-nrl'
              302  LOAD_GLOBAL              sys
              304  LOAD_ATTR                argv
              306  COMPARE_OP               in
          308_310  POP_JUMP_IF_FALSE   316  'to 316'

 L. 377       312  LOAD_CONST               False
              314  STORE_FAST               'recycle_rl'
            316_0  COME_FROM           308  '308'

 L. 378       316  LOAD_STR                 '-navg_dc'
              318  LOAD_GLOBAL              sys
              320  LOAD_ATTR                argv
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   332  'to 332'

 L. 379       328  LOAD_CONST               False
              330  STORE_FAST               'avg_dc'
            332_0  COME_FROM           324  '324'

 L. 380       332  LOAD_STR                 '-sp'
              334  LOAD_GLOBAL              sys
              336  LOAD_ATTR                argv
              338  COMPARE_OP               in
          340_342  POP_JUMP_IF_FALSE   348  'to 348'

 L. 381       344  LOAD_CONST               True
              346  STORE_FAST               'spinpol'
            348_0  COME_FROM           340  '340'

 L. 382       348  LOAD_STR                 '-so'
              350  LOAD_GLOBAL              sys
              352  LOAD_ATTR                argv
              354  COMPARE_OP               in
          356_358  POP_JUMP_IF_FALSE   364  'to 364'

 L. 383       360  LOAD_CONST               True
              362  STORE_FAST               'p_so'
            364_0  COME_FROM           356  '356'

 L. 384       364  LOAD_STR                 '-dft'
              366  LOAD_GLOBAL              sys
              368  LOAD_ATTR                argv
              370  COMPARE_OP               in
          372_374  POP_JUMP_IF_FALSE   380  'to 380'

 L. 385       376  LOAD_CONST               True
              378  STORE_FAST               'gskip'
            380_0  COME_FROM           372  '372'

 L. 386       380  LOAD_FAST                'band'
              382  LOAD_STR                 '-band'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   400  'to 400'

 L. 387       390  LOAD_STR                 '_band'
              392  STORE_FAST               '_band'

 L. 388       394  LOAD_CONST               1
              396  STORE_FAST               'nmaxiter'
              398  JUMP_FORWARD        404  'to 404'
            400_0  COME_FROM           386  '386'

 L. 390       400  LOAD_STR                 ''
              402  STORE_FAST               '_band'
            404_0  COME_FROM           398  '398'

 L. 391       404  LOAD_FAST                'band'
              406  LOAD_STR                 '-band'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_TRUE    424  'to 424'
              414  LOAD_FAST                'dos'
              416  LOAD_STR                 '-dos'
              418  COMPARE_OP               ==
          420_422  POP_JUMP_IF_FALSE   428  'to 428'
            424_0  COME_FROM           410  '410'

 L. 392       424  LOAD_STR                 'CyGutzB'
              426  STORE_FAST               'cygutz'
            428_0  COME_FROM           420  '420'

 L. 394       428  LOAD_GLOBAL              len
              430  LOAD_GLOBAL              sys
              432  LOAD_ATTR                argv
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  LOAD_CONST               1
              438  COMPARE_OP               >
          440_442  POP_JUMP_IF_FALSE   482  'to 482'
              444  LOAD_GLOBAL              sys
              446  LOAD_ATTR                argv
              448  LOAD_CONST               1
              450  BINARY_SUBSCR    
              452  LOAD_CONST               ('-h', '--help')
              454  COMPARE_OP               in
          456_458  POP_JUMP_IF_FALSE   482  'to 482'

 L. 422       460  LOAD_STR                 "\n    The script is a wrapper to run Wien2k + Gutzwiller.\n    It usually loops over the following steps:\n\n        x lapw0   : computes LDA potential with current DFT+G-RISB charge\n        x lapw1   : solves LDA eigenvalue equations\n        [x lapwso]: second variational treatment of spin-orbit coupling\n        x gwien1  : compute the local projector in the basis of DFT bands\n        x cygutz  : solve the generic KS-Hubbard model using G-RISB\n        x gwien2  : computes DFT+G-RISB valence charge\n        x lcore   : computes DFT core charge\n        x mixer   : mixes new charge density with the previous result\n\n    The parameters with default values are as follows:\n\n        name     default  inline-argument  help\n        --------------------------------------------------------------------\n        nmaxiter 100      -n 100           max charge mixing steps\n        mix_dc   0.2      -amix            D.C. potential mxing param\n        cc       1.e-3    -cc 1.e-3        charge density cutoff to exit\n        ec       1.e-5    -ec 1.e-5        total energy cutoff to exit\n        startp   'lapw0'  -s lapw0         start program\n        endp     ''       -e ''            end program\n        openmp   False    -omp             use openMP instead of openMPI\n        rl       True     -nrl             start from previous GA solutions\n        avg_dc   True     -navg_dc         average dc among atoms or not\n        spinpol  False    -sp              spin-symmetry breaking at DFT level\n        "
              462  STORE_FAST               'help'

 L. 423       464  LOAD_GLOBAL              print
              466  LOAD_FAST                'help'
              468  CALL_FUNCTION_1       1  '1 positional argument'
              470  POP_TOP          

 L. 424       472  LOAD_GLOBAL              sys
              474  LOAD_METHOD              exit
              476  LOAD_CONST               0
              478  CALL_METHOD_1         1  '1 positional argument'
              480  POP_TOP          
            482_0  COME_FROM           456  '456'
            482_1  COME_FROM           440  '440'

 L. 426       482  LOAD_STR                 ''
              484  STORE_FAST               'para'

 L. 427       486  LOAD_STR                 ''
              488  STORE_FAST               '_para'

 L. 428       490  LOAD_GLOBAL              file_exists
              492  LOAD_STR                 '.machines'
              494  CALL_FUNCTION_1       1  '1 positional argument'
          496_498  POP_JUMP_IF_FALSE   508  'to 508'

 L. 429       500  LOAD_STR                 ' -p'
              502  STORE_FAST               'para'

 L. 430       504  LOAD_STR                 '_x'
              506  STORE_FAST               '_para'
            508_0  COME_FROM           496  '496'

 L. 433       508  LOAD_GLOBAL              glob
              510  LOAD_METHOD              glob
              512  LOAD_STR                 '*.scf*'
              514  CALL_METHOD_1         1  '1 positional argument'
              516  LOAD_GLOBAL              glob
              518  LOAD_METHOD              glob
              520  LOAD_STR                 '*.error*'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  BINARY_ADD       
              526  LOAD_GLOBAL              glob
              528  LOAD_METHOD              glob
              530  LOAD_STR                 '*.outputdmf?.*'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  BINARY_ADD       
              536  LOAD_GLOBAL              glob
              538  LOAD_METHOD              glob
              540  LOAD_STR                 'EMBED_HAMIL_RES*'
              542  CALL_METHOD_1         1  '1 positional argument'
              544  BINARY_ADD       
              546  STORE_FAST               'toclean'

 L. 434       548  SETUP_LOOP          574  'to 574'
              550  LOAD_FAST                'toclean'
              552  GET_ITER         
              554  FOR_ITER            572  'to 572'
              556  STORE_FAST               'f'

 L. 435       558  LOAD_GLOBAL              os
              560  LOAD_METHOD              remove
              562  LOAD_FAST                'f'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          
          568_570  JUMP_BACK           554  'to 554'
              572  POP_BLOCK        
            574_0  COME_FROM_LOOP      548  '548'

 L. 437       574  LOAD_GLOBAL              glob
              576  LOAD_METHOD              glob
              578  LOAD_STR                 '*.struct'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               'struct_file'

 L. 438       584  LOAD_GLOBAL              len
              586  LOAD_FAST                'struct_file'
              588  CALL_FUNCTION_1       1  '1 positional argument'
              590  LOAD_CONST               1
              592  COMPARE_OP               !=
          594_596  POP_JUMP_IF_FALSE   616  'to 616'

 L. 439       598  LOAD_GLOBAL              ValueError
              600  LOAD_STR                 '{} struct files present while only one must exist!'
              602  LOAD_METHOD              format

 L. 440       604  LOAD_GLOBAL              len
              606  LOAD_FAST                'struct_file'
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  CALL_METHOD_1         1  '1 positional argument'
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  RAISE_VARARGS_1       1  'exception instance'
            616_0  COME_FROM           594  '594'

 L. 441       616  LOAD_FAST                'struct_file'
              618  LOAD_CONST               0
              620  BINARY_SUBSCR    
              622  LOAD_METHOD              split
              624  LOAD_STR                 '.'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  LOAD_CONST               0
              630  BINARY_SUBSCR    
              632  STORE_FAST               'w_case'

 L. 442       634  LOAD_GLOBAL              os
              636  LOAD_ATTR                environ
              638  LOAD_STR                 'WIENROOT'
              640  BINARY_SUBSCR    
              642  STORE_FAST               'w_root'

 L. 443       644  LOAD_GLOBAL              os
              646  LOAD_ATTR                environ
              648  LOAD_STR                 'SCRATCH'
              650  BINARY_SUBSCR    
              652  STORE_FAST               'w_scratch'

 L. 444       654  LOAD_GLOBAL              os
              656  LOAD_ATTR                environ
              658  LOAD_STR                 'WIEN_GUTZ_ROOT'
              660  BINARY_SUBSCR    
              662  STORE_FAST               'g_root'

 L. 447       664  LOAD_GLOBAL              open
              666  LOAD_FAST                'w_case'
              668  LOAD_STR                 '.dayfile'
              670  BINARY_ADD       
              672  LOAD_STR                 'w'
              674  CALL_FUNCTION_2       2  '2 positional arguments'
              676  STORE_FAST               'fday'

 L. 448       678  LOAD_FAST                'fday'
              680  LOAD_METHOD              write
              682  LOAD_STR                 'Calculating {} in {} \non {} with PID {}\n'
              684  LOAD_METHOD              format

 L. 449       686  LOAD_FAST                'w_case'
              688  LOAD_GLOBAL              os
              690  LOAD_METHOD              getcwd
              692  CALL_METHOD_0         0  '0 positional arguments'
              694  LOAD_GLOBAL              socket
              696  LOAD_METHOD              gethostname
              698  CALL_METHOD_0         0  '0 positional arguments'
              700  LOAD_GLOBAL              os
              702  LOAD_METHOD              getpid
              704  CALL_METHOD_0         0  '0 positional arguments'
              706  CALL_METHOD_4         4  '4 positional arguments'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  POP_TOP          

 L. 451       712  LOAD_GLOBAL              os
              714  LOAD_ATTR                path
              716  LOAD_METHOD              isfile
              718  LOAD_FAST                'w_case'
              720  LOAD_STR                 '.inso'
              722  BINARY_ADD       
              724  CALL_METHOD_1         1  '1 positional argument'
          726_728  POP_JUMP_IF_FALSE   786  'to 786'

 L. 452       730  LOAD_GLOBAL              os
              732  LOAD_ATTR                path
              734  LOAD_METHOD              getsize
              736  LOAD_FAST                'w_case'
              738  LOAD_STR                 '.inso'
              740  BINARY_ADD       
              742  CALL_METHOD_1         1  '1 positional argument'
              744  LOAD_CONST               0
              746  COMPARE_OP               >
          748_750  POP_JUMP_IF_FALSE   786  'to 786'
              752  LOAD_FAST                'p_so'
          754_756  POP_JUMP_IF_TRUE    786  'to 786'

 L. 453       758  LOAD_STR                 'spin-orbit is off while {} file is present!'
              760  LOAD_METHOD              format

 L. 454       762  LOAD_FAST                'w_case'
              764  LOAD_STR                 '.inso'
              766  BINARY_ADD       
              768  CALL_METHOD_1         1  '1 positional argument'
              770  LOAD_STR                 '\nappending -so to turn it on.'
              772  BINARY_ADD       
              774  STORE_FAST               'msg'

 L. 455       776  LOAD_GLOBAL              warnings
              778  LOAD_METHOD              warn
              780  LOAD_FAST                'msg'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  POP_TOP          
            786_0  COME_FROM           754  '754'
            786_1  COME_FROM           748  '748'
            786_2  COME_FROM           726  '726'

 L. 457       786  LOAD_FAST                'p_so'
          788_790  POP_JUMP_IF_FALSE   802  'to 802'

 L. 458       792  LOAD_STR                 'so'
              794  STORE_FAST               'so'

 L. 459       796  LOAD_STR                 'c'
              798  STORE_FAST               'cmplx'
              800  JUMP_FORWARD        810  'to 810'
            802_0  COME_FROM           788  '788'

 L. 461       802  LOAD_STR                 ''
              804  STORE_FAST               'so'

 L. 462       806  LOAD_STR                 ''
              808  STORE_FAST               'cmplx'
            810_0  COME_FROM           800  '800'

 L. 465       810  LOAD_GLOBAL              file_exists
              812  LOAD_FAST                'w_case'
              814  LOAD_STR                 '.in1c'
              816  BINARY_ADD       
              818  CALL_FUNCTION_1       1  '1 positional argument'
          820_822  POP_JUMP_IF_FALSE   828  'to 828'

 L. 466       824  LOAD_STR                 'c'
              826  STORE_FAST               'cmplx'
            828_0  COME_FROM           820  '820'

 L. 468       828  LOAD_STR                 'mpi_prefix.dat'
              830  STORE_FAST               'f_mpi'

 L. 469       832  LOAD_GLOBAL              os
              834  LOAD_ATTR                path
              836  LOAD_METHOD              isfile
              838  LOAD_FAST                'f_mpi'
              840  CALL_METHOD_1         1  '1 positional argument'
          842_844  POP_JUMP_IF_FALSE   920  'to 920'

 L. 470       846  LOAD_GLOBAL              open
              848  LOAD_FAST                'f_mpi'
              850  LOAD_STR                 'r'
              852  CALL_FUNCTION_2       2  '2 positional arguments'
              854  SETUP_WITH          874  'to 874'
              856  STORE_FAST               'f'

 L. 471       858  LOAD_FAST                'f'
              860  LOAD_METHOD              readline
              862  CALL_METHOD_0         0  '0 positional arguments'
              864  LOAD_METHOD              split
              866  CALL_METHOD_0         0  '0 positional arguments'
              868  STORE_FAST               'mpi'
              870  POP_BLOCK        
              872  LOAD_CONST               None
            874_0  COME_FROM_WITH      854  '854'
              874  WITH_CLEANUP_START
              876  WITH_CLEANUP_FINISH
              878  END_FINALLY      

 L. 472       880  LOAD_GLOBAL              print
              882  LOAD_STR                 '{} exists -- running in parallel mode.'
              884  LOAD_METHOD              format
              886  LOAD_FAST                'f_mpi'
              888  CALL_METHOD_1         1  '1 positional argument'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  POP_TOP          

 L. 473       894  LOAD_GLOBAL              print
              896  LOAD_STR                 ' '
              898  LOAD_METHOD              join
              900  LOAD_GENEXPR             '<code_object <genexpr>>'
              902  LOAD_STR                 'run_gwien.<locals>.<genexpr>'
              904  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              906  LOAD_FAST                'mpi'
              908  GET_ITER         
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  CALL_METHOD_1         1  '1 positional argument'
              914  CALL_FUNCTION_1       1  '1 positional argument'
              916  POP_TOP          
              918  JUMP_FORWARD        956  'to 956'
            920_0  COME_FROM           842  '842'

 L. 475       920  LOAD_FAST                'para'
              922  LOAD_STR                 ''
              924  COMPARE_OP               !=
          926_928  POP_JUMP_IF_FALSE   938  'to 938'

 L. 476       930  LOAD_GLOBAL              ValueError
              932  LOAD_STR                 'missing mpi_prefix.dat with .machines present!'
              934  CALL_FUNCTION_1       1  '1 positional argument'
              936  RAISE_VARARGS_1       1  'exception instance'
            938_0  COME_FROM           926  '926'

 L. 477       938  LOAD_STR                 ''
              940  STORE_FAST               'mpi'

 L. 478       942  LOAD_GLOBAL              print
              944  LOAD_STR                 '{} not available -- running in serial mode.'
              946  LOAD_METHOD              format
              948  LOAD_FAST                'f_mpi'
              950  CALL_METHOD_1         1  '1 positional argument'
              952  CALL_FUNCTION_1       1  '1 positional argument'
              954  POP_TOP          
            956_0  COME_FROM           918  '918'

 L. 480       956  LOAD_FAST                'openmp'
          958_960  POP_JUMP_IF_FALSE   968  'to 968'

 L. 481       962  LOAD_STR                 ''
              964  STORE_FAST               '_mpi'
              966  JUMP_FORWARD        972  'to 972'
            968_0  COME_FROM           958  '958'

 L. 483       968  LOAD_FAST                'mpi'
              970  STORE_FAST               '_mpi'
            972_0  COME_FROM           966  '966'

 L. 485       972  LOAD_FAST                'gskip'
          974_976  POP_JUMP_IF_TRUE   1230  'to 1230'

 L. 486       978  LOAD_STR                 'gwien1'
              980  LOAD_STR                 'gwien2'
              982  BUILD_LIST_2          2 
              984  STORE_FAST               'p_list'

 L. 487       986  LOAD_FAST                'p_list'
              988  LOAD_METHOD              append
              990  LOAD_FAST                'cygutz'
              992  CALL_METHOD_1         1  '1 positional argument'
              994  POP_TOP          

 L. 488       996  SETUP_LOOP         1032  'to 1032'
              998  LOAD_FAST                'pa_list'
             1000  GET_ITER         
           1002_0  COME_FROM          1012  '1012'
             1002  FOR_ITER           1030  'to 1030'
             1004  STORE_FAST               'pa'

 L. 489      1006  LOAD_FAST                'pa'
             1008  LOAD_FAST                'p_list'
             1010  COMPARE_OP               not-in
         1012_1014  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 490      1016  LOAD_FAST                'p_list'
             1018  LOAD_METHOD              append
             1020  LOAD_FAST                'pa'
             1022  CALL_METHOD_1         1  '1 positional argument'
             1024  POP_TOP          
         1026_1028  JUMP_BACK          1002  'to 1002'
             1030  POP_BLOCK        
           1032_0  COME_FROM_LOOP      996  '996'

 L. 491      1032  SETUP_LOOP         1068  'to 1068'
             1034  LOAD_FAST                'p_list'
             1036  GET_ITER         
             1038  FOR_ITER           1066  'to 1066'
             1040  STORE_FAST               'p'

 L. 492      1042  LOAD_GLOBAL              shutil
             1044  LOAD_METHOD              copy2
             1046  LOAD_FAST                'g_root'
             1048  LOAD_STR                 '/'
             1050  BINARY_ADD       
             1052  LOAD_FAST                'p'
             1054  BINARY_ADD       
             1056  LOAD_STR                 '.'
             1058  CALL_METHOD_2         2  '2 positional arguments'
             1060  POP_TOP          
         1062_1064  JUMP_BACK          1038  'to 1038'
             1066  POP_BLOCK        
           1068_0  COME_FROM_LOOP     1032  '1032'

 L. 495      1068  LOAD_FAST                'spinpol'
         1070_1072  POP_JUMP_IF_FALSE  1186  'to 1186'

 L. 496      1074  LOAD_GLOBAL              fcreate_def_gwien
             1076  LOAD_FAST                'w_case'
             1078  LOAD_FAST                'w_scratch'

 L. 497      1080  LOAD_FAST                'so'
             1082  LOAD_FAST                '_para'

 L. 498      1084  LOAD_STR                 '1'
             1086  LOAD_FAST                'cmplx'
             1088  LOAD_FAST                '_band'

 L. 499      1090  LOAD_STR                 'up'
             1092  LOAD_STR                 'dn'
             1094  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band', 'updn', 'dnup')
             1096  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1098  POP_TOP          

 L. 500      1100  LOAD_FAST                'p_so'
         1102_1104  POP_JUMP_IF_TRUE   1132  'to 1132'

 L. 501      1106  LOAD_GLOBAL              fcreate_def_gwien
             1108  LOAD_FAST                'w_case'
             1110  LOAD_FAST                'w_scratch'

 L. 502      1112  LOAD_FAST                'so'
             1114  LOAD_FAST                '_para'

 L. 503      1116  LOAD_STR                 '1'
             1118  LOAD_FAST                'cmplx'
             1120  LOAD_FAST                '_band'

 L. 504      1122  LOAD_STR                 'dn'
             1124  LOAD_STR                 'up'
             1126  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band', 'updn', 'dnup')
             1128  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1130  POP_TOP          
           1132_0  COME_FROM          1102  '1102'

 L. 506      1132  LOAD_GLOBAL              fcreate_def_gwien
             1134  LOAD_FAST                'w_case'
             1136  LOAD_FAST                'w_scratch'

 L. 507      1138  LOAD_FAST                'so'
             1140  LOAD_FAST                '_para'

 L. 508      1142  LOAD_STR                 '2'
             1144  LOAD_FAST                'cmplx'
             1146  LOAD_FAST                '_band'

 L. 509      1148  LOAD_STR                 'up'
             1150  LOAD_STR                 'dn'
             1152  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band', 'updn', 'dnup')
             1154  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1156  POP_TOP          

 L. 510      1158  LOAD_GLOBAL              fcreate_def_gwien
             1160  LOAD_FAST                'w_case'
             1162  LOAD_FAST                'w_scratch'

 L. 511      1164  LOAD_FAST                'so'
             1166  LOAD_FAST                '_para'

 L. 512      1168  LOAD_STR                 '2'
             1170  LOAD_FAST                'cmplx'
             1172  LOAD_FAST                '_band'

 L. 513      1174  LOAD_STR                 'dn'
             1176  LOAD_STR                 'up'
             1178  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band', 'updn', 'dnup')
             1180  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
             1182  POP_TOP          
             1184  JUMP_FORWARD       1230  'to 1230'
           1186_0  COME_FROM          1070  '1070'

 L. 515      1186  LOAD_GLOBAL              fcreate_def_gwien
             1188  LOAD_FAST                'w_case'
             1190  LOAD_FAST                'w_scratch'

 L. 516      1192  LOAD_FAST                'so'
             1194  LOAD_FAST                '_para'

 L. 517      1196  LOAD_STR                 '1'
             1198  LOAD_FAST                'cmplx'
             1200  LOAD_FAST                '_band'
             1202  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band')
             1204  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1206  POP_TOP          

 L. 518      1208  LOAD_GLOBAL              fcreate_def_gwien
             1210  LOAD_FAST                'w_case'
             1212  LOAD_FAST                'w_scratch'

 L. 519      1214  LOAD_FAST                'so'
             1216  LOAD_FAST                '_para'

 L. 520      1218  LOAD_STR                 '2'
             1220  LOAD_FAST                'cmplx'
             1222  LOAD_FAST                '_band'
             1224  LOAD_CONST               ('scratch', 'so', 'para', 'idmf', 'cmplx', '_band')
             1226  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1228  POP_TOP          
           1230_0  COME_FROM          1184  '1184'
           1230_1  COME_FROM           974  '974'

 L. 523      1230  LOAD_GLOBAL              env
             1232  LOAD_ATTR                get_env_dict
             1234  LOAD_STR                 'SLURM_'
             1236  LOAD_CONST               ('key',)
             1238  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1240  STORE_FAST               'slurm_envs'

 L. 525      1242  LOAD_FAST                'nmaxiter'
             1244  LOAD_CONST               0
             1246  COMPARE_OP               >
         1248_1250  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 526      1252  LOAD_GLOBAL              os
             1254  LOAD_ATTR                path
             1256  LOAD_METHOD              isfile
             1258  LOAD_STR                 '{}.clmsum'
             1260  LOAD_METHOD              format
             1262  LOAD_FAST                'w_case'
             1264  CALL_METHOD_1         1  '1 positional argument'
             1266  CALL_METHOD_1         1  '1 positional argument'
         1268_1270  POP_JUMP_IF_TRUE   1314  'to 1314'

 L. 527      1272  LOAD_STR                 'no {}.clmsum file found--necessary for lapw0!'
             1274  LOAD_METHOD              format

 L. 528      1276  LOAD_FAST                'w_case'
             1278  CALL_METHOD_1         1  '1 positional argument'
             1280  STORE_FAST               'err_msg'

 L. 529      1282  LOAD_GLOBAL              print
             1284  LOAD_FAST                'err_msg'
             1286  CALL_FUNCTION_1       1  '1 positional argument'
             1288  POP_TOP          

 L. 530      1290  LOAD_FAST                'fday'
             1292  LOAD_METHOD              print
             1294  LOAD_FAST                'err_msg'
             1296  LOAD_STR                 '\n'
             1298  BINARY_ADD       
             1300  CALL_METHOD_1         1  '1 positional argument'
             1302  POP_TOP          

 L. 531      1304  LOAD_GLOBAL              sys
             1306  LOAD_METHOD              exit
             1308  LOAD_CONST               1
             1310  CALL_METHOD_1         1  '1 positional argument'
             1312  POP_TOP          
           1314_0  COME_FROM          1268  '1268'

 L. 532      1314  SETUP_LOOP         1346  'to 1346'
             1316  LOAD_GLOBAL              glob
             1318  LOAD_METHOD              glob
             1320  LOAD_STR                 '*.broyd*'
             1322  CALL_METHOD_1         1  '1 positional argument'
             1324  GET_ITER         
             1326  FOR_ITER           1344  'to 1344'
             1328  STORE_FAST               'f'

 L. 533      1330  LOAD_GLOBAL              os
             1332  LOAD_METHOD              remove
             1334  LOAD_FAST                'f'
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  POP_TOP          
         1340_1342  JUMP_BACK          1326  'to 1326'
             1344  POP_BLOCK        
           1346_0  COME_FROM_LOOP     1314  '1314'

 L. 535      1346  LOAD_FAST                'fday'
             1348  LOAD_METHOD              write
             1350  LOAD_STR                 '   start at {} with {} \n   1/{} to go.\n'
             1352  LOAD_METHOD              format

 L. 536      1354  LOAD_GLOBAL              time
             1356  LOAD_METHOD              asctime
             1358  CALL_METHOD_0         0  '0 positional arguments'
             1360  LOAD_FAST                'startp'
             1362  LOAD_FAST                'nmaxiter'
             1364  CALL_METHOD_3         3  '3 positional arguments'
             1366  CALL_METHOD_1         1  '1 positional argument'
             1368  POP_TOP          
           1370_0  COME_FROM          1248  '1248'

 L. 539  1370_1372  SETUP_LOOP         2342  'to 2342'
             1374  LOAD_GLOBAL              range
             1376  LOAD_FAST                'nmaxiter'
             1378  CALL_FUNCTION_1       1  '1 positional argument'
             1380  GET_ITER         
           1382_0  COME_FROM          2322  '2322'
           1382_1  COME_FROM          2312  '2312'
           1382_2  COME_FROM          2302  '2302'
         1382_1384  FOR_ITER           2340  'to 2340'
             1386  STORE_FAST               'icycle'

 L. 542      1388  LOAD_GLOBAL              env
             1390  LOAD_METHOD              unset_environ
             1392  LOAD_FAST                'slurm_envs'
             1394  CALL_METHOD_1         1  '1 positional argument'
             1396  POP_TOP          

 L. 544      1398  LOAD_FAST                'icycle'
             1400  LOAD_CONST               0
             1402  COMPARE_OP               >
         1404_1406  POP_JUMP_IF_TRUE   1418  'to 1418'
             1408  LOAD_FAST                'startp'
             1410  LOAD_STR                 'lapw0'
             1412  COMPARE_OP               in
         1414_1416  POP_JUMP_IF_FALSE  1436  'to 1436'
           1418_0  COME_FROM          1404  '1404'

 L. 545      1418  LOAD_GLOBAL              onestep
             1420  LOAD_FAST                'fday'
             1422  LOAD_FAST                'w_case'
             1424  LOAD_STR                 'lapw0'
             1426  LOAD_FAST                'w_root'
             1428  LOAD_FAST                'para'
             1430  LOAD_CONST               ('para',)
             1432  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1434  POP_TOP          
           1436_0  COME_FROM          1414  '1414'

 L. 546      1436  LOAD_FAST                'icycle'
             1438  LOAD_CONST               0
             1440  COMPARE_OP               >
         1442_1444  POP_JUMP_IF_TRUE   1456  'to 1456'
             1446  LOAD_FAST                'startp'
             1448  LOAD_STR                 'lapw0 lapw1'
             1450  COMPARE_OP               in
         1452_1454  POP_JUMP_IF_FALSE  1528  'to 1528'
           1456_0  COME_FROM          1442  '1442'

 L. 547      1456  LOAD_FAST                'spinpol'
         1458_1460  POP_JUMP_IF_FALSE  1508  'to 1508'

 L. 548      1462  LOAD_GLOBAL              onestep
             1464  LOAD_FAST                'fday'
             1466  LOAD_FAST                'w_case'
             1468  LOAD_STR                 'lapw1'
             1470  LOAD_FAST                'w_root'
             1472  LOAD_FAST                'para'
             1474  LOAD_FAST                'band'

 L. 549      1476  LOAD_STR                 '-up'
             1478  LOAD_CONST               ('para', 'band', 'updn')
             1480  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1482  POP_TOP          

 L. 550      1484  LOAD_GLOBAL              onestep
             1486  LOAD_FAST                'fday'
             1488  LOAD_FAST                'w_case'
             1490  LOAD_STR                 'lapw1'
             1492  LOAD_FAST                'w_root'
             1494  LOAD_FAST                'para'
             1496  LOAD_FAST                'band'

 L. 551      1498  LOAD_STR                 '-dn'
             1500  LOAD_CONST               ('para', 'band', 'updn')
             1502  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1504  POP_TOP          
             1506  JUMP_FORWARD       1528  'to 1528'
           1508_0  COME_FROM          1458  '1458'

 L. 553      1508  LOAD_GLOBAL              onestep
             1510  LOAD_FAST                'fday'
             1512  LOAD_FAST                'w_case'
             1514  LOAD_STR                 'lapw1'
             1516  LOAD_FAST                'w_root'
             1518  LOAD_FAST                'para'
             1520  LOAD_FAST                'band'
             1522  LOAD_CONST               ('para', 'band')
             1524  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1526  POP_TOP          
           1528_0  COME_FROM          1506  '1506'
           1528_1  COME_FROM          1452  '1452'

 L. 554      1528  LOAD_FAST                'icycle'
             1530  LOAD_CONST               0
             1532  COMPARE_OP               >
         1534_1536  POP_JUMP_IF_TRUE   1548  'to 1548'
             1538  LOAD_FAST                'startp'
             1540  LOAD_STR                 'lapw0 lapw1 lapwso'
             1542  COMPARE_OP               in
         1544_1546  POP_JUMP_IF_FALSE  1604  'to 1604'
           1548_0  COME_FROM          1534  '1534'
             1548  LOAD_FAST                'p_so'
         1550_1552  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 555      1554  LOAD_FAST                'spinpol'
         1556_1558  POP_JUMP_IF_FALSE  1584  'to 1584'

 L. 556      1560  LOAD_GLOBAL              onestep
             1562  LOAD_FAST                'fday'
             1564  LOAD_FAST                'w_case'
             1566  LOAD_STR                 'lapwso'
             1568  LOAD_FAST                'w_root'
             1570  LOAD_FAST                'para'

 L. 557      1572  LOAD_FAST                'band'
             1574  LOAD_STR                 '-up'
             1576  LOAD_CONST               ('para', 'band', 'updn')
             1578  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1580  POP_TOP          
             1582  JUMP_FORWARD       1604  'to 1604'
           1584_0  COME_FROM          1556  '1556'

 L. 559      1584  LOAD_GLOBAL              onestep
             1586  LOAD_FAST                'fday'
             1588  LOAD_FAST                'w_case'
             1590  LOAD_STR                 'lapwso'
             1592  LOAD_FAST                'w_root'
             1594  LOAD_FAST                'para'
             1596  LOAD_FAST                'band'
             1598  LOAD_CONST               ('para', 'band')
             1600  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1602  POP_TOP          
           1604_0  COME_FROM          1582  '1582'
           1604_1  COME_FROM          1550  '1550'
           1604_2  COME_FROM          1544  '1544'

 L. 561      1604  LOAD_FAST                'icycle'
             1606  LOAD_CONST               0
             1608  COMPARE_OP               ==
         1610_1612  POP_JUMP_IF_FALSE  1656  'to 1656'
             1614  LOAD_FAST                'para'
             1616  LOAD_STR                 ''
             1618  COMPARE_OP               !=
         1620_1622  POP_JUMP_IF_FALSE  1656  'to 1656'

 L. 562      1624  LOAD_FAST                'spinpol'
         1626_1628  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 563      1630  LOAD_GLOBAL              processes_convert
             1632  LOAD_FAST                'p_so'
             1634  LOAD_STR                 'up'
             1636  LOAD_CONST               ('updn',)
             1638  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1640  POP_TOP          
             1642  JUMP_FORWARD       1656  'to 1656'
           1644_0  COME_FROM          1626  '1626'

 L. 565      1644  LOAD_GLOBAL              processes_convert
             1646  LOAD_FAST                'p_so'
             1648  LOAD_STR                 ''
             1650  LOAD_CONST               ('updn',)
             1652  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1654  POP_TOP          
           1656_0  COME_FROM          1642  '1642'
           1656_1  COME_FROM          1620  '1620'
           1656_2  COME_FROM          1610  '1610'

 L. 568      1656  LOAD_GLOBAL              env
             1658  LOAD_METHOD              set_environ
             1660  LOAD_FAST                'slurm_envs'
             1662  CALL_METHOD_1         1  '1 positional argument'
             1664  POP_TOP          

 L. 570      1666  LOAD_FAST                'gskip'
         1668_1670  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 572      1672  LOAD_FAST                'icycle'
             1674  LOAD_CONST               0
             1676  COMPARE_OP               >
         1678_1680  POP_JUMP_IF_TRUE   1692  'to 1692'
             1682  LOAD_FAST                'startp'
             1684  LOAD_STR                 'lapw0 lapw1 lapwso lapw2'
             1686  COMPARE_OP               in
         1688_1690  POP_JUMP_IF_FALSE  2088  'to 2088'
           1692_0  COME_FROM          1678  '1678'

 L. 573      1692  LOAD_FAST                'spinpol'
         1694_1696  POP_JUMP_IF_FALSE  1744  'to 1744'

 L. 574      1698  LOAD_GLOBAL              onestep
             1700  LOAD_FAST                'fday'
             1702  LOAD_FAST                'w_case'
             1704  LOAD_STR                 'lapw2'
             1706  LOAD_FAST                'w_root'
             1708  LOAD_FAST                'para'

 L. 575      1710  LOAD_STR                 '-up'
             1712  LOAD_FAST                'so'
             1714  LOAD_CONST               ('para', 'updn', 'so')
             1716  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1718  POP_TOP          

 L. 576      1720  LOAD_GLOBAL              onestep
             1722  LOAD_FAST                'fday'
             1724  LOAD_FAST                'w_case'
             1726  LOAD_STR                 'lapw2'
             1728  LOAD_FAST                'w_root'
             1730  LOAD_FAST                'para'

 L. 577      1732  LOAD_STR                 '-dn'
             1734  LOAD_FAST                'so'
             1736  LOAD_CONST               ('para', 'updn', 'so')
             1738  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1740  POP_TOP          
             1742  JUMP_FORWARD       2088  'to 2088'
           1744_0  COME_FROM          1694  '1694'

 L. 579      1744  LOAD_GLOBAL              onestep
             1746  LOAD_FAST                'fday'
             1748  LOAD_FAST                'w_case'
             1750  LOAD_STR                 'lapw2'
             1752  LOAD_FAST                'w_root'
             1754  LOAD_FAST                'para'
             1756  LOAD_FAST                'so'
             1758  LOAD_CONST               ('para', 'so')
             1760  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1762  POP_TOP          
         1764_1766  JUMP_FORWARD       2088  'to 2088'
           1768_0  COME_FROM          1668  '1668'

 L. 581      1768  LOAD_FAST                'icycle'
             1770  LOAD_CONST               0
             1772  COMPARE_OP               >
         1774_1776  POP_JUMP_IF_TRUE   1788  'to 1788'
             1778  LOAD_FAST                'startp'
             1780  LOAD_STR                 'lapw0 lapw1 lapwso gwien1'
             1782  COMPARE_OP               in
         1784_1786  POP_JUMP_IF_FALSE  1884  'to 1884'
           1788_0  COME_FROM          1774  '1774'

 L. 582      1788  LOAD_FAST                'spinpol'
         1790_1792  POP_JUMP_IF_FALSE  1834  'to 1834'

 L. 583      1794  LOAD_GLOBAL              gonestep
             1796  LOAD_FAST                'fday'
             1798  LOAD_STR                 'gwien1'
             1800  LOAD_FAST                'mpi'
             1802  LOAD_STR                 'up'
             1804  LOAD_CONST               ('updn',)
             1806  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1808  POP_TOP          

 L. 584      1810  LOAD_FAST                'p_so'
         1812_1814  POP_JUMP_IF_TRUE   1846  'to 1846'

 L. 585      1816  LOAD_GLOBAL              gonestep
             1818  LOAD_FAST                'fday'
             1820  LOAD_STR                 'gwien1'
             1822  LOAD_FAST                'mpi'
             1824  LOAD_STR                 'dn'
             1826  LOAD_CONST               ('updn',)
             1828  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1830  POP_TOP          
             1832  JUMP_FORWARD       1846  'to 1846'
           1834_0  COME_FROM          1790  '1790'

 L. 587      1834  LOAD_GLOBAL              gonestep
             1836  LOAD_FAST                'fday'
             1838  LOAD_STR                 'gwien1'
             1840  LOAD_FAST                'mpi'
             1842  CALL_FUNCTION_3       3  '3 positional arguments'
             1844  POP_TOP          
           1846_0  COME_FROM          1832  '1832'
           1846_1  COME_FROM          1812  '1812'

 L. 588      1846  LOAD_FAST                'openmp'
         1848_1850  POP_JUMP_IF_FALSE  1860  'to 1860'

 L. 589      1852  LOAD_GLOBAL              create_gomp_file
             1854  CALL_FUNCTION_0       0  '0 positional arguments'
             1856  POP_TOP          
             1858  JUMP_FORWARD       1884  'to 1884'
           1860_0  COME_FROM          1848  '1848'

 L. 590      1860  LOAD_GLOBAL              os
             1862  LOAD_ATTR                path
             1864  LOAD_METHOD              isfile
             1866  LOAD_STR                 'GOMP.h5'
             1868  CALL_METHOD_1         1  '1 positional argument'
         1870_1872  POP_JUMP_IF_FALSE  1884  'to 1884'

 L. 591      1874  LOAD_GLOBAL              os
             1876  LOAD_METHOD              remove
             1878  LOAD_STR                 'GOMP.h5'
             1880  CALL_METHOD_1         1  '1 positional argument'
             1882  POP_TOP          
           1884_0  COME_FROM          1870  '1870'
           1884_1  COME_FROM          1858  '1858'
           1884_2  COME_FROM          1784  '1784'

 L. 592      1884  LOAD_FAST                'endp'
             1886  LOAD_STR                 'gwien1'
             1888  COMPARE_OP               ==
         1890_1892  POP_JUMP_IF_FALSE  1904  'to 1904'

 L. 593      1894  LOAD_GLOBAL              sys
             1896  LOAD_METHOD              exit
             1898  LOAD_CONST               0
             1900  CALL_METHOD_1         1  '1 positional argument'
             1902  POP_TOP          
           1904_0  COME_FROM          1890  '1890'

 L. 595      1904  LOAD_FAST                'icycle'
             1906  LOAD_CONST               0
             1908  COMPARE_OP               >
         1910_1912  POP_JUMP_IF_TRUE   1924  'to 1924'
             1914  LOAD_FAST                'startp'
             1916  LOAD_STR                 'lapw0 lapw1 lapwso gwien1 CyGutz'
             1918  COMPARE_OP               in
         1920_1922  POP_JUMP_IF_FALSE  1936  'to 1936'
           1924_0  COME_FROM          1910  '1910'

 L. 596      1924  LOAD_GLOBAL              gonestep
             1926  LOAD_FAST                'fday'
             1928  LOAD_FAST                'cygutz'
             1930  LOAD_FAST                '_mpi'
             1932  CALL_FUNCTION_3       3  '3 positional arguments'
             1934  POP_TOP          
           1936_0  COME_FROM          1920  '1920'

 L. 597      1936  LOAD_FAST                'band'
             1938  LOAD_STR                 '-band'
             1940  COMPARE_OP               ==
         1942_1944  POP_JUMP_IF_TRUE   1956  'to 1956'
             1946  LOAD_FAST                'dos'
             1948  LOAD_STR                 '-dos'
             1950  COMPARE_OP               ==
         1952_1954  POP_JUMP_IF_FALSE  1966  'to 1966'
           1956_0  COME_FROM          1942  '1942'

 L. 598      1956  LOAD_GLOBAL              sys
             1958  LOAD_METHOD              exit
             1960  LOAD_CONST               0
             1962  CALL_METHOD_1         1  '1 positional argument'
             1964  POP_TOP          
           1966_0  COME_FROM          1952  '1952'

 L. 599      1966  LOAD_GLOBAL              shutil
             1968  LOAD_METHOD              copy2
             1970  LOAD_STR                 'GUTZ.LOG'
             1972  LOAD_STR                 'SAVE_GUTZ.LOG'
             1974  CALL_METHOD_2         2  '2 positional arguments'
             1976  POP_TOP          

 L. 600      1978  LOAD_FAST                'endp'
             1980  LOAD_STR                 'CyGutz'
             1982  COMPARE_OP               ==
         1984_1986  POP_JUMP_IF_FALSE  1998  'to 1998'

 L. 601      1988  LOAD_GLOBAL              sys
             1990  LOAD_METHOD              exit
             1992  LOAD_CONST               0
             1994  CALL_METHOD_1         1  '1 positional argument'
             1996  POP_TOP          
           1998_0  COME_FROM          1984  '1984'

 L. 602      1998  LOAD_FAST                'recycle_rl'
         2000_2002  POP_JUMP_IF_FALSE  2016  'to 2016'

 L. 603      2004  LOAD_GLOBAL              shutil
             2006  LOAD_METHOD              copy2
             2008  LOAD_STR                 'WH_RL_OUT.h5'
             2010  LOAD_STR                 'WH_RL_INP.h5'
             2012  CALL_METHOD_2         2  '2 positional arguments'
             2014  POP_TOP          
           2016_0  COME_FROM          2000  '2000'

 L. 605      2016  LOAD_FAST                'spinpol'
         2018_2020  POP_JUMP_IF_FALSE  2056  'to 2056'

 L. 606      2022  LOAD_GLOBAL              gonestep
             2024  LOAD_FAST                'fday'
             2026  LOAD_STR                 'gwien2'
             2028  LOAD_FAST                'mpi'
             2030  LOAD_STR                 'up'
             2032  LOAD_CONST               ('updn',)
             2034  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2036  POP_TOP          

 L. 607      2038  LOAD_GLOBAL              gonestep
             2040  LOAD_FAST                'fday'
             2042  LOAD_STR                 'gwien2'
             2044  LOAD_FAST                'mpi'
             2046  LOAD_STR                 'dn'
             2048  LOAD_CONST               ('updn',)
             2050  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2052  POP_TOP          
             2054  JUMP_FORWARD       2068  'to 2068'
           2056_0  COME_FROM          2018  '2018'

 L. 609      2056  LOAD_GLOBAL              gonestep
             2058  LOAD_FAST                'fday'
             2060  LOAD_STR                 'gwien2'
             2062  LOAD_FAST                'mpi'
           2064_0  COME_FROM          1742  '1742'
             2064  CALL_FUNCTION_3       3  '3 positional arguments'
             2066  POP_TOP          
           2068_0  COME_FROM          2054  '2054'

 L. 611      2068  LOAD_FAST                'endp'
             2070  LOAD_STR                 'gwien2'
             2072  COMPARE_OP               ==
         2074_2076  POP_JUMP_IF_FALSE  2088  'to 2088'

 L. 612      2078  LOAD_GLOBAL              sys
             2080  LOAD_METHOD              exit
             2082  LOAD_CONST               0
             2084  CALL_METHOD_1         1  '1 positional argument'
             2086  POP_TOP          
           2088_0  COME_FROM          2074  '2074'
           2088_1  COME_FROM          1764  '1764'
           2088_2  COME_FROM          1688  '1688'

 L. 616      2088  LOAD_GLOBAL              env
             2090  LOAD_METHOD              unset_environ
             2092  LOAD_FAST                'slurm_envs'
             2094  CALL_METHOD_1         1  '1 positional argument'
             2096  POP_TOP          

 L. 618      2098  LOAD_FAST                'spinpol'
         2100_2102  POP_JUMP_IF_FALSE  2146  'to 2146'

 L. 619      2104  LOAD_GLOBAL              onestep
             2106  LOAD_FAST                'fday'
             2108  LOAD_FAST                'w_case'
             2110  LOAD_STR                 'lcore'
             2112  LOAD_FAST                'w_root'
             2114  LOAD_STR                 ''
             2116  LOAD_STR                 '-up'
             2118  LOAD_CONST               ('para', 'updn')
             2120  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2122  POP_TOP          

 L. 620      2124  LOAD_GLOBAL              onestep
             2126  LOAD_FAST                'fday'
             2128  LOAD_FAST                'w_case'
             2130  LOAD_STR                 'lcore'
             2132  LOAD_FAST                'w_root'
             2134  LOAD_STR                 ''
             2136  LOAD_STR                 '-dn'
             2138  LOAD_CONST               ('para', 'updn')
             2140  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2142  POP_TOP          
             2144  JUMP_FORWARD       2164  'to 2164'
           2146_0  COME_FROM          2100  '2100'

 L. 622      2146  LOAD_GLOBAL              onestep
             2148  LOAD_FAST                'fday'
             2150  LOAD_FAST                'w_case'
             2152  LOAD_STR                 'lcore'
             2154  LOAD_FAST                'w_root'
             2156  LOAD_STR                 ''
             2158  LOAD_CONST               ('para',)
             2160  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2162  POP_TOP          
           2164_0  COME_FROM          2144  '2144'

 L. 624      2164  LOAD_GLOBAL              scf
             2166  LOAD_FAST                'w_case'
             2168  LOAD_FAST                'spinpol'
             2170  CALL_FUNCTION_2       2  '2 positional arguments'
             2172  POP_TOP          

 L. 625      2174  LOAD_GLOBAL              onestep
             2176  LOAD_FAST                'fday'
             2178  LOAD_FAST                'w_case'
             2180  LOAD_STR                 'mixer'
             2182  LOAD_FAST                'w_root'
             2184  LOAD_STR                 ''
             2186  LOAD_CONST               ('para',)
             2188  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2190  POP_TOP          

 L. 626      2192  LOAD_GLOBAL              scfm
             2194  LOAD_FAST                'w_case'
             2196  CALL_FUNCTION_1       1  '1 positional argument'
             2198  POP_TOP          

 L. 627      2200  LOAD_GLOBAL              diff
             2202  LOAD_FAST                'fday'
             2204  LOAD_FAST                'w_case'
             2206  LOAD_FAST                'mix_dc'
             2208  LOAD_FAST                'avg_dc'
             2210  LOAD_FAST                'gskip'
             2212  CALL_FUNCTION_5       5  '5 positional arguments'
             2214  UNPACK_SEQUENCE_3     3 
             2216  STORE_FAST               'drho'
             2218  STORE_FAST               'dene'
             2220  STORE_FAST               'dvdc'

 L. 629      2222  LOAD_FAST                'gskip'
         2224_2226  POP_JUMP_IF_FALSE  2234  'to 2234'

 L. 630      2228  LOAD_CONST               0.0
             2230  STORE_FAST               'gerr'
             2232  JUMP_FORWARD       2270  'to 2270'
           2234_0  COME_FROM          2224  '2224'

 L. 632      2234  LOAD_GLOBAL              h5py
             2236  LOAD_METHOD              File
             2238  LOAD_STR                 'GLOG.h5'
             2240  LOAD_STR                 'r'
             2242  CALL_METHOD_2         2  '2 positional arguments'
             2244  SETUP_WITH         2264  'to 2264'
             2246  STORE_FAST               'f'

 L. 633      2248  LOAD_FAST                'f'
             2250  LOAD_STR                 '/rl_maxerr'
             2252  BINARY_SUBSCR    
             2254  LOAD_CONST               0
             2256  BINARY_SUBSCR    
             2258  STORE_FAST               'gerr'
             2260  POP_BLOCK        
             2262  LOAD_CONST               None
           2264_0  COME_FROM_WITH     2244  '2244'
             2264  WITH_CLEANUP_START
             2266  WITH_CLEANUP_FINISH
             2268  END_FINALLY      
           2270_0  COME_FROM          2232  '2232'

 L. 635      2270  LOAD_GLOBAL              print
             2272  LOAD_STR                 'dc={:.1e}, cc={:.1e} -> {:.0e}, ec={:.1e} -> {:.0e}, gc={:.1e} icycle={}'
             2274  LOAD_METHOD              format

 L. 637      2276  LOAD_FAST                'dvdc'
             2278  LOAD_FAST                'drho'
             2280  LOAD_FAST                'cc'
             2282  LOAD_FAST                'dene'
             2284  LOAD_FAST                'ec'
             2286  LOAD_FAST                'gerr'
             2288  LOAD_FAST                'icycle'
             2290  CALL_METHOD_7         7  '7 positional arguments'
             2292  CALL_FUNCTION_1       1  '1 positional argument'
             2294  POP_TOP          

 L. 638      2296  LOAD_FAST                'drho'
             2298  LOAD_FAST                'cc'
             2300  COMPARE_OP               <
         2302_2304  POP_JUMP_IF_FALSE  1382  'to 1382'
             2306  LOAD_FAST                'dene'
             2308  LOAD_FAST                'ec'
             2310  COMPARE_OP               <
         2312_2314  POP_JUMP_IF_FALSE  1382  'to 1382'
             2316  LOAD_FAST                'dvdc'
             2318  LOAD_FAST                'vc'
             2320  COMPARE_OP               <
         2322_2324  POP_JUMP_IF_FALSE  1382  'to 1382'

 L. 639      2326  LOAD_GLOBAL              sys
             2328  LOAD_METHOD              exit
             2330  LOAD_CONST               0
             2332  CALL_METHOD_1         1  '1 positional argument'
             2334  POP_TOP          
         2336_2338  JUMP_BACK          1382  'to 1382'
             2340  POP_BLOCK        
           2342_0  COME_FROM_LOOP     1370  '1370'

Parse error at or near `COME_FROM' instruction at offset 2064_0


def batch_init_ga(dir_template='./template'):
    """Loop over all the directories to initialize CyGutz calculations
     -- actually, since the CyGutz input files remain the same for different
    volumes, it simply copy the input files in template directory to
    each folder.
    """
    cwd = os.getcwd() + '/'
    for dname in glob.glob('V*'):
        os.chdir(dname + '/case')
        shutil.copy(cwd + '/' + dir_template + '/ginit.h5', './')
        shutil.copy(cwd + '/' + dir_template + '/GPARAM.h5', './')
        if os.path.isfile(cwd + '/' + dir_template + '/GESOLVER.h5'):
            shutil.copy(cwd + '/' + dir_template + '/GESOLVER.h5', './')
        shutil.copy(cwd + '/' + dir_template + '/case.indmfl', './')
        os.chdir(cwd)


def batch_init_mott(dir_template='./template'):
    """Loop over all the directories to initialize CyGutz-Mott calculations
     -- actually, since the CyGutz input files remain the same for different
    volumes, it simply copy the input files in template directory to
    each folder.
    """
    cwd = os.getcwd() + '/'
    for dname in glob.glob('V*'):
        os.chdir(dname + '/case')
        shutil.copy(cwd + '/' + dir_template + '/GMOTT.h5', './')
        os.chdir(cwd)


def batch_modify_ga_setup(args, nproc=1):
    """Loop over all the directories to modify CyGutz set up file.
    """
    cwd = os.getcwd() + '/'
    cmd = [os.environ['WIEN_GUTZ_ROOT'] + '/switch_gparam.py'] + args
    if '-p' in sys.argv:
        nproc = int(sys.argv[(sys.argv.index('-p') + 1)])
    for i, dname in enumerate(glob.glob('V*')):
        os.chdir(dname + '/case')
        proc = subprocess.Popen(cmd)
        os.chdir(cwd)
        if (i + 1) % nproc == 0:
            proc.communicate()


def batch_job_slurm(u, j, dir_template='./template', dir_work='./'):
    """copy template/job.slurm file to each working directory and submit jobs.
    """
    cwd = os.getcwd() + '/'
    jname = 'u{}j{}'.format(u, j)
    args = [
     '-unique_u_ev', u, '-unique_j_ev', j]
    cmd = [os.environ['WIEN_GUTZ_ROOT'] + '/switch_gparam.py'] + args
    if '-w' in sys.argv:
        dir_work = sys.argv[(sys.argv.index('-w') + 1)]
    cmd_s = [
     'qsub', './job.slurm']
    for dname in glob.glob('V*'):
        os.chdir(dname + '/case/' + dir_work)
        with open(cwd + '/' + dir_template + '/job.slurm', 'r') as (fin):
            with open('./job.slurm', 'w') as (fout):
                for line in fin:
                    fout.write(line.replace('VV', dname).replace('UJ', jname))

        proc = subprocess.Popen(cmd)
        proc.communicate()
        proc = subprocess.Popen(cmd_s)
        os.chdir(cwd)


def run_ga(nproc=1):
    """Loop over all the directories to run_ga using nproc processors.
    """
    cmd = [
     os.environ['WIEN_GUTZ_ROOT'] + '/run_ga.py']
    cwd = os.getcwd() + '/'
    if '-p' in sys.argv:
        nproc = int(sys.argv[(sys.argv.index('-p') + 1)])
    for i, dname in enumerate(glob.glob('V*')):
        os.chdir(dname + '/case')
        proc = subprocess.Popen(cmd)
        os.chdir(cwd)
        if (i + 1) % nproc == 0:
            proc.communicate()


def batch_gsave(sdir='ldag', args=['-f']):
    """Loop over all the directories to save_lapw.
    """
    cmd = [
     os.environ['WIEN_GUTZ_ROOT'] + '/save_ldag', '-d'] + [sdir] + args
    cwd = os.getcwd() + '/'
    for dname in glob.glob('V*'):
        os.chdir(dname + '/case')
        subprocess.call(cmd)
        os.chdir(cwd)


if __name__ == '__main__':
    fcreate_def_gwien('FeSb2', scratch='.', so='', para='', idmf='1',
      cmplx='',
      _band='',
      updn='',
      dnup='dn')