# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/BrukerNMR.py
# Compiled at: 2020-01-29 14:45:26
# Size of source mod 2**32: 34202 bytes
"""
    Utility to Handle NMR Bruker files

partly based on NPK v1 code
"""
from __future__ import print_function
__author__ = "Marc Andre' Delsuc"
__date__ = 'november 2014'
import os
import os.path as op
import glob, re, struct, unittest, shutil, numpy as np
from ..NPKData import LaplaceAxis
from ..NMR import NMRData
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

debug = False
VERBOSE = False

def find_acqu_proc_gene(dir, acqulist):
    """
    find a Bruker acqu or proc file associated to the directory dir and return its name
    """
    found = 0
    for a in acqulist:
        filename = op.join(dir, a)
        if op.exists(filename):
            break
    else:
        raise Exception('no parameter file found in ' + dir)

    return filename


def find_acqu(dir='.'):
    """
    find a Bruker acqu file associated to the directory dir and return its name
    
    """
    return find_acqu_proc_gene(dir, ('acqus', 'acqu', 'ACQUS', 'ACQU'))


def find_acqu2(dir='.'):
    """
    find a Bruker acqu2 file associated to the directory dir and return its name
    
    """
    return find_acqu_proc_gene(dir, ('acqu2s', 'acqu2', 'ACQU2S', 'ACQU2'))


def find_acqu3(dir='.'):
    """
    find a Bruker acqu3 file associated to the directory dir and return its name
    
    """
    return find_acqu_proc_gene(dir, ('acqu3s', 'acqu3', 'ACQU3S', 'ACQU3'))


def find_proc_down(dire, proclist):
    """
    find a Bruker proc file associated to the directory dir and return its name
    
    search in pdada/PROCNO and returns the first one
    """
    for pdata in glob.glob(op.join(dire, 'pdata', '*')):
        for f in proclist:
            fname = op.join(pdata, f)
            if debug:
                print('SEARCH', fname)
            if op.exists(fname):
                if debug:
                    print('FOUND', f)
                break

        break
    else:
        raise Exception('No proc file found in ' + dire)

    return fname


def find_proc(dir='.', down=True):
    """
    find a Bruker proc file associated to the directory dir and return its name
    if  down is True - search in dir/pdata/* other searches here
    """
    if down:
        return find_proc_down(dir, ('procs', 'proc', 'PROCS', 'PROC'))
    return find_acqu_proc_gene(dir, ('procs', 'proc', 'PROCS', 'PROC'))


def find_proc2(dir='.', down=True):
    """
    find a Bruker proc file associated to the directory dir and return its name
    
    """
    if down:
        return find_proc_down(dir, ('proc2s', 'proc2', 'PROC2S', 'PROC2'))
    return find_acqu_proc_gene(dir, ('proc2s', 'proc2', 'PROC2S', 'PROC2'))


def find_proc3(dir='.', down=True):
    """
    find a Bruker proc file associated to the directory dir and return its name
    
    """
    if down:
        return find_proc_down(dir, ('proc3s', 'proc3', 'PROC3S', 'PROC3'))
    return find_acqu_proc_gene(dir, ('proc3s', 'proc3', 'PROC3S', 'PROC3'))


def read_param(filename='acqus'):
    """ 
    load a Bruker acqu or proc file as a dictionnary
    
    arrayed values are stored in python array
    
    comments (lines starting with $$) are stored in the special entry [comments]
    
    M-A Delsuc jan 2006
    oct 2006 : added support for array
    """
    debug = 0
    with open(filename) as (fin):
        dico = {}
        dico['comments'] = ''
        f = fin.read()
        fin.close()
        ls = f.split('\n')
        while ls:
            v = ls.pop(0)
            v = v.strip()
            if debug:
                print('-', v, '-')
            if re.search('^\\$\\$', v):
                dico['comments'] = dico['comments'] + '\n' + v
            else:
                m = re.match('##(.*)= *\\(0\\.\\.([0-9]*)\\)(.*)$', v)
                if m is not None:
                    if debug:
                        print('ARRAY', v, m.group(1, 2, 3))
                    key, numb, line = m.group(1, 2, 3)
                    v = ls.pop(0)
                    v = v.lstrip()
                    while not re.match('##', v):
                        line = line + ' ' + v
                        v = ls.pop(0)
                        if debug:
                            v = v.lstrip()

                    ls.insert(0, v)
                    array = line.split()
                    if debug:
                        print(key, numb, len(array), array)
                    if int(numb) + 1 != len(array):
                        raise 'size mismatch in array'
                    dico[key] = array
                    continue
                m = re.match('##(.*)= *<(.*)>', v)
                if m is not None:
                    if debug:
                        print('STRING', v)
                    key, val = m.group(1, 2)
                    dico[key] = '<' + val + '>'
                    continue
                m = re.match('##(.*)= *(.*)$', v)
                if m is not None:
                    if debug:
                        print('VAL', v)
                    key, val = m.group(1, 2)
                    dico[key] = val
                    continue

    dico['title'] = read_title(filename)
    version = 'unknown'
    try:
        version = dico['TITLE']
    except:
        pass

    if '2.' in version:
        dico['ORIGIN'] = 'TOPSPIN2'
    else:
        if '3.' in version:
            dico['ORIGIN'] = 'TOPSPIN3'
        else:
            if '4.' in version:
                dico['ORIGIN'] = 'TOPSPIN4'
            if debug:
                for i in dico.keys():
                    print(i + ' = ' + str(dico[i]))

            return dico


def read_title(filename):
    """
    infer and load title of imported experiment
    """
    proc = find_proc(dir=(op.dirname(filename)), down=('acqu' in filename))
    ftitle = op.join(op.dirname(proc), 'title')
    try:
        title = open(ftitle, 'r').read()
    except FileNotFoundError:
        title = '-'

    return title


def write_param(param, filename):
    """
    writes back a acqu/proc param file
    """

    def out(k):
        if isinstance(param[k], list):
            F.write('##%s= (0..%d)\n' % (k, len(param[k]) - 1))
            line = ''
            for l in param[k]:
                line += l + ' '
                if len(line) >= 72:
                    F.write(line.strip() + '\n')
                    line = ''

            if line != '':
                F.write(line.strip() + '\n')
        else:
            F.write('##%s= %s\n' % (k, param[k]))

    klist = sorted(param.keys())
    with open(filename, 'w') as (F):
        out('TITLE')
        out('JCAMPDX')
        for k in klist:
            if k.startswith('$') or k not in ('TITLE', 'JCAMPDX', 'comments', 'END'):
                out(k)

        F.write(param['comments'].lstrip() + '\n')
        for k in klist:
            if k.startswith('$'):
                out(k)

        out('END')


def read_1D(size, filename='fid', bytorda=1, dtypa=0, uses='struct'):
    """
    Reads in a Bruker 1D fid as a numpy float array
    
    size is the number of data-points in the fid
    uses struct or numpy / numpy is non-standard but ~2x faster
    dtypa   = 0 => int4
            = 2 => float8
    does not check endianess
    """
    if dtypa == 2:
        fmt = 'd'
        nfmt = 'f8'
        mlt = 8
    else:
        fmt = 'i'
        nfmt = 'i4'
        mlt = 4
    if bytorda == 0:
        fmt = '<%d' + fmt
    else:
        fmt = '>%d' + fmt
    if uses == 'struct':
        with open(filename, 'rb') as (F):
            buf = F.read(mlt * size)
            ibuf = struct.unpack(fmt % size, buf)
        npkbuf = np.empty(size, dtype=(np.float))
        npkbuf[:] = ibuf[:]
    else:
        if uses == 'numpy':
            npkbuf = np.fromfile(filename, nfmt).astype(float)
    return npkbuf


def read_2D(sizeF1, sizeF2, filename='ser', bytorda=1, dtypa=0, uses='struct'):
    """
    Reads in a Bruker 2D fid as a numpy float array

    sizeF1 is the number of fid
    sizeF2 is the number of data-points in the fid
    """
    if uses != 'struct':
        raise Exception('Only mode "struct" is implemented')
    else:
        npkbuf = np.empty((sizeF1, sizeF2), dtype=(np.float))
        if dtypa == 0:
            fmt = '256i'
        else:
            fmt = '256i'
        if bytorda == 0:
            fmt = '<256i'
        else:
            fmt = '>256i'
    with open(filename, 'rb') as (F):
        for i1 in range(sizeF1):
            for i2 in range(0, sizeF2, 256):
                buf = F.read(1024)
                data = struct.unpack(fmt, buf)
                bufsz = min(256, sizeF2 - i2)
                npkbuf[i1, i2:i2 + bufsz] = data[:bufsz]

    return npkbuf


def zerotime(acqu):
    """get digital filter parameters, if any
    
  The zerotime function computes the correction for the Bruker figital filter.
  the phase correction to apply is computed given the 3 parameters :
  DSPFIRM DSPFVS DECIM
  as found in the acqus parameter file in XwinNMR

  correction is then -360*zerotime in firstorder correction

  dspfvs is not used so far
  oct 2006
  """
    tabdelay = [
     [
      179, 201, 533, 709, 1097, 1449, 2225, 2929, 4481, 5889, 8993, 11809, 18017, 23649, 36065, 47329, 72161, 94689, 144353, 189409, 288737],
     [
      184, 219, 384, 602, 852, 1668, 2312, 3368, 4656, 6768, 9344, 13568, 18560, 27392, 36992, 50040, 73856, 110336, 147584, 220928, 295040],
     [
      184, 219, 384, 602, 852, 1668, 2292, 3369, 4616, 6768, 9264, 13568, 18560, 27392, 36992, 50040, 73856, 110336, 147584, 220928, 295040],
     [
      11, 17, 23, 35, 47, 71, 95, 143, 191, 287, 383, 575, -1, -1, -1, -1, -1, -1, -1, -1, -1],
     [
      60, 90, 118, 179, 244, 360, 492, 724, 980, 1444, 1958, 2886, 3912, 5768, 7820, 11532, -1, -1, -1, -1, -1],
     [
      -1, -1, 58, 152, 202, 318, 418, 642, 842, 1290, 1690, 2586, 3386, -1, -1, -1, -1, -1, -1, -1, -1]]
    decim_offset = [
     2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048]
    try:
        decim = int(float(acqu['$DECIM']))
    except:
        decim = 1

    if decim != 1:
        dspfvs = int(acqu['$DSPFVS'])
        dspfirm = int(acqu['$DSPFIRM'])
        if dspfvs >= 20:
            if dspfvs <= 23:
                zerotimeposition = float(acqu['$GRPDLY'])
                return zerotimeposition
        if dspfvs == 15:
            if decim == 3:
                if float(acqu['$SW_h']) >= 104000:
                    z = -110.0 / decim
                    zerotimeposition = z / 2
                    return zerotimeposition
        if dspfvs == 0 or decim == 1:
            return 0.0
        try:
            j = decim_offset.index(decim)
        except:
            raise '*** wrong value for DECIM'

        try:
            d = tabdelay[(dspfvs - 10)][j]
        except:
            raise '*** wrong value for DSPFVS ' + dspfirm

        if d == -1:
            raise '*** wrong DECIM/DSPFVS parameter combination'
        z = float(d) / float(decim)
        zerotimeposition = z / 2
        return zerotimeposition
    zerotimeposition = 0.0
    return zerotimeposition
    return zerotimeposition


def offset(acqu, proc):
    """
    computes the offset from Bruker to spike
    """
    try:
        ppmPointUn = float(proc['$OFFSET'])
        ppmWidth = float(acqu['$SW_h']) / float(acqu['$SFO1'])
        calibrationOffset = float(ppmPointUn - ppmWidth) * float(acqu['$SFO1'])
    except:
        calibrationOffset = 0.0

    return calibrationOffset


def revoffset(loffset, acqu, proc):
    """
    computes the Bruker OFFSET (ppm of left most point) from spike axis offset value (Hz of rightmost point)
    """
    try:
        SW_h = float(acqu['$SW_h'])
        SFO1 = float(acqu['$SFO1'])
        OFF = (loffset + SW_h) / SFO1
    except:
        OFF = 0.0

    return OFF


def Import_1D(filename='fid', outfile=None, verbose=VERBOSE):
    """
    Imports a 1D Bruker fid as a NMRData
    
    """
    if not op.exists(filename):
        raise Exception(filename + ' : file not found')
    else:
        dire = op.dirname(filename)
        acqu = read_param(find_acqu(dire))
        size = int(acqu['$TD'])
        if verbose:
            print('imported 1D FID, size =%d\n%s' % (size, acqu['title']))
        data = read_1D(size, filename, bytorda=(int(acqu['$BYTORDA'])), dtypa=(int(acqu['$DTYPA'])))
        NC = int(acqu['$NC'])
        if NC != 0:
            data *= 2 ** NC
        d = NMRData(buffer=data)
        d.axis1.specwidth = float(acqu['$SW_h'])
        d.axis1.frequency = float(acqu['$SFO1'])
        d.frequency = d.axis1.frequency
        if acqu['$AQ_mod'] == '0':
            d.axis1.itype = 0
        else:
            d.axis1.itype = 1
    proc = read_param(find_proc(dire))
    d.axis1.offset = offset(acqu, proc)
    d.axis1.zerotime = zerotime(acqu)
    if outfile is not None:
        raise Exception('Not implemented yet')
    pardic = {'acqu':acqu, 
     'proc':proc}
    d.params = pardic
    if verbose:
        print('imported 1D FID, size =%d\n%s' % (size, acqu['title']))
    return d


def Import_1D_proc(filename='1r', verbose=VERBOSE):
    """
    Imports a 1D Bruker 1r processed file as a NMRData
    if 1i exists imports the complex spectrum

    """
    if not op.exists(filename):
        raise Exception(filename + ' : file not found')
    dire = op.dirname(filename)
    proc = read_param(find_proc(dire, down=False))
    diracq = op.dirname(op.dirname(op.dirname(filename)))
    acqu = read_param(find_acqu(diracq))
    data = np.fromfile(filename, 'i4').astype(float)
    if op.exists(op.join(dire, '1i')):
        data = data + complex(0.0, 1.0) * np.fromfile(filename, 'i4')
    d = NMRData(buffer=data)
    d.axis1.specwidth = float(acqu['$SW_h'])
    d.axis1.frequency = float(acqu['$SFO1'])
    d.frequency = d.axis1.frequency
    d.axis1.offset = offset(acqu, proc)
    d.axis1.zerotime = zerotime(acqu)
    pardic = {'acqu':acqu,  'proc':proc}
    d.params = pardic
    if verbose:
        print('1D spectrum imported\n%s' % proc['title'])
    return d


def write_file(bytordp, data, filename):
    """
    data written as integers.
    """
    if bytordp == '0':
        fmt = '<i4'
    else:
        fmt = '>i4'
    with open(filename, 'wb') as (f):
        f.write(data.astype(fmt).tostring())


def Export_proc(d, filename, template=None, verbose=VERBOSE):
    """
    Exports a 1D or a 2D NMRData to a  Bruker 1r / 2rr file, using templname as a template
    
    filename and template are procno : datadir/my_experiment/expno/pdata/procno/
    and the files are created in the filename directory
    a pdata/procno should already exists in template for templating
    
    if d contains metadata parameters from Bruker, there will be used,
    however all files common to fname and templname expno will not be updated
    
    if fname and templname are exactly the same, (or templname is None)
        only 1r / 2rr proc and procs files will be overwriten
    """
    from .BrukerSMX import BrukerSMXHandler
    if d.dim > 2:
        raise Exception('Not implemented yet')
    if template is None:
        template = filename
    template = op.normpath(template)
    filename = op.normpath(filename)
    if not op.exists(template):
        raise Exception(template + ' : file not found')
    if verbose:
        print('Export %dD spectrum to %s using %s' % (d.dim, filename, template))
    fexpno = op.dirname(op.dirname(filename))
    texpno = op.dirname(op.dirname(template))
    if debug:
        print('texpno', texpno)
        print('fexpno', fexpno)
    escratch = False
    pscratch = False
    if not op.exists(fexpno):
        os.makedirs(fexpno)
        escratch = True
        for f in glob.glob(op.join(texpno, '*')):
            if op.isfile(f):
                if op.basename(f) not in ('ser', 'fid'):
                    if debug:
                        print('**CP**', f, fexpno)
                shutil.copy(f, op.join(fexpno, op.basename(f)))

    else:
        if not op.exists(filename):
            os.makedirs(filename)
            fscratch = True
            for f in glob.glob(op.join(template, '*')):
                if op.isfile(f):
                    if op.basename(f) not in ('1r', '1i', '2rr', '2ri', '2ir', '2ii'):
                        if debug:
                            print('**CP**', f, filename)
                    shutil.copy(f, op.join(filename, op.basename(f)))

        if escratch:
            warn = False
            if d.dim == 1:
                pnamelist = ('acqu', )
            else:
                if d.dim == 2:
                    pnamelist = ('acqu', 'acqu2')
                for pname in pnamelist:
                    try:
                        par = d.params[pname]
                    except (AttributeError, KeyError):
                        warn = True
                    else:
                        write_param(par, op.join(fexpno, pname))
                        write_param(par, op.join(fexpno, pname + 's'))

                if warn:
                    print('Warning, acqu/acqus files have not been updated')
            if pscratch:
                warn = False
                if d.dim == 1:
                    pnamelist = ('proc', )
        elif d.dim == 2:
            pnamelist = ('proc', 'proc2')
    for pname in pnamelist:
        try:
            par = d.params[pname]
        except (AttributeError, KeyError):
            warn = True
        else:
            write_param(par, op.join(filename, pname))
            write_param(par, op.join(filename, pname + 's'))

    if warn:
        print('Warning, proc/procs files have not been updated')
    else:
        proc = read_param(find_proc(template, down=False))
        acqu = read_param(find_acqu(texpno))
        if d.dim == 2:
            proc2 = read_param(find_proc2(template, down=False))
            acqu2 = read_param(find_acqu2(texpno))
        bufabs = abs(d.buffer)
        bmax = bufabs.max()
        NC_proc = 0
        while bmax < 268435456:
            bmax *= 2
            NC_proc -= 1

        while bmax > 536870912:
            bmax /= 2
            NC_proc += 1

        if debug:
            print('NC_proc :', NC_proc)
        buffinal = d.buffer * 2 ** (-NC_proc)
        if d.dim == 1:
            proc['$SI'] = str(d.axis1.cpxsize)
            proc['$SF'] = str(d.axis1.frequency)
            proc['$SW_p'] = str(d.axis1.specwidth)
            proc['$OFFSET'] = str(revoffset(d.axis1.offset, acqu, proc))
            proc['$YMAX_p'] = str(buffinal.max())
            proc['$YMIN_p'] = str(buffinal.min())
            write_param(proc, op.join(filename, 'proc'))
            write_param(proc, op.join(filename, 'procs'))
        if d.dim == 2:
            proc['$SI'] = str(d.axis2.cpxsize)
            proc['$SF'] = str(d.axis2.frequency)
            proc['$SW_p'] = str(d.axis2.specwidth)
            proc['$OFFSET'] = str(revoffset(d.axis2.offset, acqu, proc))
            proc2['$SI'] = str(d.axis1.cpxsize)
            if isinstance(d.axis1, LaplaceAxis):
                print('Warning, storing DOSY parameters to Topspin dataset still not fully tested !')
            else:
                proc2['$SF'] = str(d.axis1.frequency)
                proc2['$SW_p'] = str(d.axis1.specwidth)
                proc2['$OFFSET'] = str(revoffset(d.axis1.offset, acqu2, proc2))
            proc['$YMAX_p'] = str(buffinal.max())
            proc['$YMIN_p'] = str(buffinal.min())
            write_param(proc, op.join(filename, 'proc'))
            write_param(proc, op.join(filename, 'procs'))
            write_param(proc2, op.join(filename, 'proc2'))
            write_param(proc2, op.join(filename, 'proc2s'))
        if d.dim == 1:
            if d.axis1.itype == 0:
                write_file(proc['$BYTORDP'], op.join(filename, '1r'), buffinal)
            else:
                write_file(proc['$BYTORDP'], op.join(filename, '1r'), buffinal[::2])
                write_file(proc['$BYTORDP'], op.join(filename, '1r'), buffinal[1::2])
    if d.dim == 2:
        SMX = BrukerSMXHandler(filename)
        if d.axis2.itype == 0:
            if d.axis1.itype == 0:
                SMX.data_2d_2rr = buffinal
            else:
                SMX.data_2d_2rr = buffinal[::2, :]
                SMX.data_2d_2ir = buffinal[1::2, :]
        if d.axis2.itype == 1:
            if d.axis1.itype == 0:
                SMX.data_2d_2rr = buffinal[:, ::2]
                SMX.data_2d_2ri = buffinal[:, 1::2]
            else:
                SMX.data_2d_2rr = buffinal[::2, ::2]
                SMX.data_2d_2ir = buffinal[1::2, ::2]
                SMX.data_2d_2ri = buffinal[::2, 1::2]
                SMX.data_2d_2ii = buffinal[1::2, 1::2]
        SMX.write_smx()
    if debug:
        print(filename, 'file written')
    return d


def FnMODE(acqu, proc):
    """
    complex type along F1 for a 2D or 3D
    search FnMODE in acqu
    and if absent, search MC2 in proc
    None    0
    QF      1
    QSEQ    2
    TPPI    3
    States  4
    States-TPPI 5
    Echo-AntiEcho   6
    
    returns either 0 (real) or 1 (complex)
    """
    try:
        mode = acqu['$FnMODE']
    except KeyError:
        try:
            mode = proc['$MC2']
        except KeyError:
            mode = '0'

    if mode in ('4', '5'):
        r = 1
    else:
        r = 0
    return r


def Import_2D(filename='ser', outfile=None, verbose=VERBOSE):
    """
    Imports a 2D Bruker ser
    
    """
    if not op.exists(filename):
        raise Exception(filename + ' : file not found')
    else:
        dire = op.dirname(filename)
        acqu = read_param(find_acqu(dire))
        acqu2 = read_param(find_acqu2(dire))
        proc = read_param(find_proc(dire))
        proc2 = read_param(find_proc2(dire))
        sizeF1 = int(acqu2['$TD'])
        sizeF2 = int(acqu['$TD'])
        data = read_2D(sizeF1, sizeF2, filename, bytorda=(int(acqu['$BYTORDA'])))
        d = NMRData(buffer=data)
        d.axis1.frequency = float(acqu2['$SFO1'])
        try:
            d.axis1.specwidth = float(acqu2['$SW_h'])
        except KeyError:
            d.axis1.specwidth = float(acqu2['$SW']) * d.axis1.frequency

        d.axis2.specwidth = float(acqu['$SW_h'])
        d.axis2.frequency = float(acqu['$SFO1'])
        d.frequency = d.axis2.frequency
        if acqu['$AQ_mod'] == '0':
            d.axis2.itype = 0
        else:
            d.axis2.itype = 1
        if d.axis2.itype == 1:
            if d.axis2.size % 2 == 1:
                d.axis2.size = d.axis2.size - 1
                d.buffer = d.buffer[:, :-1]
                print('axis2 was truncated to match size and type')
        d.axis1.itype = FnMODE(acqu2, proc2)
        if d.axis1.itype == 1 and d.axis1.size % 2 == 1:
            d.axis1.size = d.axis1.size - 1
            d.buffer = d.buffer[:-1, :]
            print('axis1 was truncated to match size and type')
    d.axis1.offset = offset(acqu2, proc2)
    d.axis2.offset = offset(acqu, proc)
    d.axis2.zerotime = zerotime(acqu)
    if outfile is not None:
        raise Exception('Not implemented yet')
    pardic = {'acqu':acqu,  'acqu2':acqu2, 
     'proc':proc, 
     'proc2':proc2}
    d.params = pardic
    if verbose:
        print('imported 2D FID, size = %d x %d\n%s' % (sizeF1, sizeF2, acqu['title']))
    return d


def Import_2D_proc(filename='2rr', outfile=None, verbose=VERBOSE):
    """
    Imports a 2D Bruker 2rr files
    if 2ri 2ir 2ii files exist, will imports the (hyper)complex spectrum

    """
    from .BrukerSMX import BrukerSMXHandler
    if not op.exists(filename):
        raise Exception(filename + ' : file not found')
    else:
        if verbose:
            print('importing 2D spectrum')
        SMX = BrukerSMXHandler(op.dirname(filename))
        SMX.read_smx()
        datar = SMX.data_2d_2rr.astype('float')
        if SMX.data_2d_2ir is not None:
            datar = datar + complex(0.0, 1.0) * SMX.data_2d_2ir.astype('float')
        if SMX.data_2d_2ri is not None:
            datai = SMX.data_2d_2ri.astype('float')
            if SMX.data_2d_2ii is not None:
                datai = datai + complex(0.0, 1.0) * SMX.data_2d_2ii.astype('float')
            data = np.concatenate((datar, datai))
        else:
            data = datar
    d = NMRData(buffer=data)
    if SMX.data_2d_2ri is not None:
        d.swap(axis='F1')
    d.axis1.frequency = float(SMX.acqu2['$SFO1'])
    try:
        d.axis1.specwidth = float(SMX.acqu2['$SW_h'])
    except KeyError:
        d.axis1.specwidth = float(SMX.acqu2['$SW']) * d.axis1.frequency

    d.axis2.specwidth = float(SMX.acqu['$SW_h'])
    d.axis2.frequency = float(SMX.acqu['$SFO1'])
    d.frequency = d.axis2.frequency
    d.axis1.offset = offset(SMX.acqu2, SMX.proc2)
    d.axis2.offset = offset(SMX.acqu, SMX.proc)
    d.axis2.zerotime = zerotime(SMX.acqu)
    if outfile is not None:
        raise Exception('Not implemented yet')
    pardic = {'acqu':SMX.acqu,  'acqu2':SMX.acqu2, 
     'proc':SMX.proc, 
     'proc2':SMX.proc2}
    d.params = pardic
    if verbose:
        print('imported 2D spectrum, size = %d x %d\n%s' % (data.shape(0), data.shape(1), SMX.acqu['title']))
    return d


def calibdosy(file='acqus'):
    """
    get the parameters from the acqus file and compute the calibration (dfactor)

    returns : (BigDelta, litteldelta, recovery, sequence, nucleus)

    assumes that you are using the standard Bruker set-up, and have started the dosy acquisition ith the dosy macro.

    from calibdosy.g in Gifa 5.2006
    """
    param = read_param(file)
    nuc1 = param['$NUC1']
    p30 = float(param['$P'][30]) * 1e-06
    p1 = float(param['$P'][1]) * 1e-06
    p19 = float(param['$P'][19]) * 1e-06
    d16 = float(param['$D'][16])
    d17 = float(param['$D'][17])
    d20 = float(param['$D'][20])
    pulprog = param['$PULPROG']
    if re.search('dstebp', pulprog):
        sequence = 'bpp_ste_2echoes'
        if nuc1 in ('1H', '15N', '13C', '31P', '19F', '17O'):
            nucleus = nuc1
        delta = 2 * p30
        bdelta = d20 - 10 * p1 - 8 * p30 - 8 * d16 - 8 * d17 - 2 * p19
        tau = d16
    else:
        if re.search('dstegp', pulprog):
            sequence = 'ste_2echoes'
            if nuc1 in ('1H', '15N', '13C', '31P', '19F', '17O'):
                nucleus = nuc1
            delta = p30
            bdelta = 2 * (d20 - 2 * p1 - p30 - 2 * d16 - p19)
            tau = d16
        else:
            if re.search('stegpbp|ledbp', pulprog):
                sequence = 'bpp_ste'
                if nuc1 in ('1H', '15N', '13C', '31P', '19F', '17O'):
                    nucleus = nuc1
                delta = 2 * p30
                bdelta = d20 - 4 * p1 - 2 * p30 - 3 * d16 - p19
                tau = 2 * d16
            else:
                if re.search('stegp|led', pulprog):
                    sequence = 'ste'
                    if nuc1 in ('1H', '15N', '13C', '31P', '19F', '17O'):
                        nucleus = nuc1
                    delta = p30
                    bdelta = d20 - 2 * p1 - p30 - 2 * d16 - p19
                    tau = d16
                else:
                    print('Unsupported pulse program.')
    return (
     bdelta, delta, tau, sequence, nucleus)


class Bruker_Tests(unittest.TestCase):
    __doc__ = ' A FAIRE'

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_import(self):
        from ..Tests import filename
        name = filename('Lasalocid-Tocsy/dataset/ser')
        d = Import_2D(name)
        self.assertEqual(d.axis1.itype, 1)
        self.assertEqual(d.axis2.itype, 1)
        self.assertAlmostEqual(d[(234, 567)], 8729.0)
        self.assertAlmostEqual(d.axis2.frequency, 400.131880611)
        self.assertAlmostEqual(d.axis1.specwidth, 5201.56046814)
        self.assertAlmostEqual(d.axis2.zerotime, 70.1875)
        d.apod_sin(axis=2, maxi=0.5).revf().fft(axis=2).apod_sin(axis=1, maxi=0.5).fft(axis=1).modulus()
        self.assertAlmostEqual(d[(65, 43)], 4469.468735277225)


if __name__ == '__main__':
    unittest.main()