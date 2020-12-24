# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\distortion\mutil.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
from stsci.tools import fileutil, wcsutil
import numpy as np, string, calendar, datetime
yes = True
no = False

def readIDCtab(tabname, chip=1, date=None, direction='forward', filter1=None, filter2=None, offtab=None, tddcorr=False):
    """
        Read IDCTAB, and optional OFFTAB if sepcified, and generate
        the two matrices with the geometric correction coefficients.

        If tabname == None, then return a default, undistorted solution.
        If offtab is specified, dateobs also needs to be given.

    """
    if tabname == None:
        print 'Warning: No IDCTAB specified! No distortion correction will be applied.'
        return defaultModel()
    else:
        if filter1 == None or filter1.find('CLEAR') == 0:
            filter1 = 'CLEAR'
        if filter2 == None or filter2.find('CLEAR') == 0:
            filter2 = 'CLEAR'
        try:
            ftab = fileutil.openImage(tabname)
        except:
            err_str = '------------------------------------------------------------------------ \n'
            err_str += 'WARNING: the IDCTAB geometric distortion file specified in the image     \n'
            err_str += 'header was not found on disk; namely, %s   \n' % tabname
            err_str += 'Please verify that your environment variable                             \n'
            err_str += "(one of 'jref'/'uref'/'oref'/'nref') has been correctly defined.         \n"
            err_str += 'If you do not have the IDCTAB file, you may obtain the latest version    \n'
            err_str += 'of it from the relevant instrument page on the STScI HST website:        \n'
            err_str += 'http://www.stsci.edu/hst/ For WFPC2, STIS and NICMOS data, the           \n'
            err_str += 'present run will continue using the old coefficients provided in         \n'
            err_str += 'the Dither Package (ca. 1995-1998).                                      \n'
            err_str += '------------------------------------------------------------------------ \n'
            raise IOError, err_str

        phdr = ftab['PRIMARY'].header
        skew_coeffs = None
        if 'TDD_DATE' in phdr:
            print 'Reading TDD coefficients from ', tabname
            skew_coeffs = read_tdd_coeffs(phdr)
        if 'DETECTOR' in phdr:
            detector = phdr['DETECTOR']
        else:
            if 'CAMERA' in phdr:
                detector = str(phdr['CAMERA'])
            else:
                detector = 1
            if detector == 'SBC':
                if filter1 == 'CLEAR':
                    filter1 = 'F115LP'
                    filter2 = 'N/A'
                if filter2 == 'CLEAR':
                    filter2 = 'N/A'
            norder = phdr['NORDER']
            if norder < 3:
                order = 3
            else:
                order = norder
            fx = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
            fy = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
            fshape = ftab[1].data.shape
            colnames = ftab[1].data.names
            row = -1
            for i in xrange(fshape[0]):
                try:
                    if 'FILTER1' in colnames and 'FILTER2' in colnames:
                        filt1 = ftab[1].data.field('FILTER1')[i]
                        if filt1.find('CLEAR') > -1:
                            filt1 = filt1[:5]
                        filt2 = ftab[1].data.field('FILTER2')[i]
                        if filt2.find('CLEAR') > -1:
                            filt2 = filt2[:5]
                    else:
                        if 'OPT_ELEM' in colnames:
                            filt1 = ftab[1].data.field('OPT_ELEM')
                            if filt1.find('CLEAR') > -1:
                                filt1 = filt1[:5]
                        else:
                            filt1 = filter1
                        if 'FILTER' in colnames:
                            _filt = ftab[1].data.field('FILTER')[i]
                            if _filt.find('CLEAR') > -1:
                                _filt = _filt[:5]
                            if 'OPT_ELEM' in colnames:
                                filt2 = _filt
                            else:
                                filt1 = _filt
                                filt2 = 'CLEAR'
                        else:
                            filt2 = filter2
                except:
                    filt1 = filter1
                    filt2 = filter2

                if 'DETCHIP' in colnames:
                    detchip = ftab[1].data.field('DETCHIP')[i]
                    if not str(detchip).isdigit():
                        detchip = 1
                else:
                    detchip = 1
                if 'DIRECTION' in colnames:
                    direct = string.strip(string.lower(ftab[1].data.field('DIRECTION')[i]))
                else:
                    direct = 'forward'
                if filt1 == filter1.strip() and filt2 == filter2.strip():
                    if direct == direction.strip():
                        if int(detchip) == int(chip) or int(detchip) == -999:
                            row = i
                            break

            if row < 0:
                err_str = '\nProblem finding row in IDCTAB! Could not find row matching:\n'
                err_str += '        CHIP: ' + str(detchip) + '\n'
                err_str += '     FILTERS: ' + filter1 + ',' + filter2 + '\n'
                ftab.close()
                del ftab
                raise LookupError, err_str
            else:
                print '- IDCTAB: Distortion model from row', str(row + 1), 'for chip', detchip, ':', filter1.strip(), 'and', filter2.strip()
            theta = None
            if 'V2REF' in colnames:
                v2ref = ftab[1].data.field('V2REF')[row]
                v3ref = ftab[1].data.field('V3REF')[row]
            elif offtab:
                v2ref, v3ref, theta = readOfftab(offtab, date, chip=detchip)
            else:
                v2ref = 0.0
                v3ref = 0.0
            if theta == None:
                if 'THETA' in colnames:
                    theta = ftab[1].data.field('THETA')[row]
                else:
                    theta = 0.0
            refpix = {}
            refpix['XREF'] = ftab[1].data.field('XREF')[row]
            refpix['YREF'] = ftab[1].data.field('YREF')[row]
            refpix['XSIZE'] = ftab[1].data.field('XSIZE')[row]
            refpix['YSIZE'] = ftab[1].data.field('YSIZE')[row]
            refpix['PSCALE'] = round(ftab[1].data.field('SCALE')[row], 8)
            refpix['V2REF'] = v2ref
            refpix['V3REF'] = v3ref
            refpix['THETA'] = theta
            refpix['XDELTA'] = 0.0
            refpix['YDELTA'] = 0.0
            refpix['DEFAULT_SCALE'] = yes
            refpix['centered'] = no
            if 'CX10' in ftab[1].data.names:
                cxstr = 'CX'
                cystr = 'CY'
            else:
                cxstr = 'A'
                cystr = 'B'
            for i in xrange(norder + 1):
                if i > 0:
                    for j in xrange(i + 1):
                        xcname = cxstr + str(i) + str(j)
                        ycname = cystr + str(i) + str(j)
                        fx[(i, j)] = ftab[1].data.field(xcname)[row]
                        fy[(i, j)] = ftab[1].data.field(ycname)[row]

        ftab.close()
        del ftab
        if fx[(1, 1)] == 1.0 and abs(fx[(1, 1)]) != refpix['PSCALE']:
            fx *= refpix['PSCALE']
            fy *= refpix['PSCALE']
        if tddcorr:
            print ' *** Computing ACS Time Dependent Distortion Coefficients *** '
            alpha, beta = compute_wfc_tdd_coeffs(date, skew_coeffs)
            fx, fy = apply_wfc_tdd_coeffs(fx, fy, alpha, beta)
            refpix['TDDALPHA'] = alpha
            refpix['TDDBETA'] = beta
        else:
            refpix['TDDALPHA'] = 0.0
            refpix['TDDBETA'] = 0.0
        return (
         fx, fy, refpix, order)


def readOfftab(offtab, date, chip=None):
    if offtab == None:
        return (0.0, 0.0)
    else:
        if chip:
            detchip = chip
        else:
            detchip = 1
        try:
            ftab = fileutil.openImage(offtab)
        except:
            raise IOError, "Offset table '%s' not valid as specified!" % offtab

        fshape = ftab[1].data.shape
        colnames = ftab[1].data.names
        row = -1
        row_start = None
        row_end = None
        v2end = None
        v3end = None
        date_end = None
        theta_end = None
        num_date = convertDate(date)
        for ri in xrange(fshape[0]):
            i = fshape[0] - ri - 1
            if 'DETCHIP' in colnames:
                detchip = ftab[1].data.field('DETCHIP')[i]
            else:
                detchip = 1
            obsdate = convertDate(ftab[1].data.field('OBSDATE')[i])
            if int(detchip) == int(chip) or int(detchip) == -999:
                if num_date <= obsdate:
                    date_end = obsdate
                    v2end = ftab[1].data.field('V2REF')[i]
                    v3end = ftab[1].data.field('V3REF')[i]
                    theta_end = ftab[1].data.field('THETA')[i]
                    row_end = i
                    continue
                if row_end == None and num_date > obsdate:
                    date_end = obsdate
                    v2end = ftab[1].data.field('V2REF')[i]
                    v3end = ftab[1].data.field('V3REF')[i]
                    theta_end = ftab[1].data.field('THETA')[i]
                    row_end = i
                    continue
                if num_date > obsdate:
                    date_start = obsdate
                    v2start = ftab[1].data.field('V2REF')[i]
                    v3start = ftab[1].data.field('V3REF')[i]
                    theta_start = ftab[1].data.field('THETA')[i]
                    row_start = i
                    break

        ftab.close()
        del ftab
        if row_start == None and row_end == None:
            print 'Row corresponding to DETCHIP of ', detchip, ' was not found!'
            raise LookupError
        elif row_start == None:
            print '- OFFTAB: Offset defined by row', str(row_end + 1)
        else:
            print '- OFFTAB: Offset interpolated from rows', str(row_start + 1), 'and', str(row_end + 1)
        if row_start == None or row_end == row_start:
            date_start = date_end
            v2start = v2end
            v3start = v3end
            _fraction = 0.0
            theta_start = theta_end
        else:
            _fraction = float(num_date - date_start) / float(date_end - date_start)
        v2ref = _fraction * (v2end - v2start) + v2start
        v3ref = _fraction * (v3end - v3start) + v3start
        theta = _fraction * (theta_end - theta_start) + theta_start
        return (
         v2ref, v3ref, theta)


def readWCSCoeffs(header):
    _xorder = header['a_order']
    _yorder = header['b_order']
    order = max(max(_xorder, _yorder), 3)
    fx = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
    fy = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
    refpix = {}
    refpix['XREF'] = header['crpix1']
    refpix['YREF'] = header['crpix2']
    refpix['XSIZE'] = header['naxis1']
    refpix['YSIZE'] = header['naxis2']
    refpix['PSCALE'] = header['IDCSCALE']
    if 'PAMSCALE' in header:
        refpix['PAMSCALE'] = header['PAMSCALE']
    else:
        refpix['PSCALE'] = header['IDCSCALE']
    refpix['V2REF'] = header['IDCV2REF']
    refpix['V3REF'] = header['IDCV3REF']
    refpix['THETA'] = header['IDCTHETA']
    refpix['XDELTA'] = 0.0
    refpix['YDELTA'] = 0.0
    refpix['DEFAULT_SCALE'] = yes
    refpix['centered'] = no
    cxstr = 'A_'
    cystr = 'B_'
    fx[0][0] = 0.0
    fy[0][0] = 0.0
    fx[1][0] = header['OCX10']
    fx[1][1] = header['OCX11']
    fy[1][0] = header['OCY10']
    fy[1][1] = header['OCY11']
    for i in xrange(_xorder + 1):
        for j in xrange(i + 1):
            xcname = cxstr + str(j) + '_' + str(i - j)
            ycname = cystr + str(j) + '_' + str(i - j)
            if xcname in header:
                fx[(i, j)] = fx[1][1] * header[xcname] + fx[1][0] * header[ycname]
                fy[(i, j)] = fy[1][1] * header[xcname] + fy[1][0] * header[ycname]

    return (fx, fy, refpix, order)


def readTraugerTable(idcfile, wavelength):
    if idcfile == None:
        return fileutil.defaultModel()
    else:
        order = 3
        numco = 10
        a_coeffs = [0] * numco
        b_coeffs = [0] * numco
        indx = _MgF2(wavelength)
        ifile = open(idcfile, 'r')
        _line = fileutil.rAsciiLine(ifile)
        while string.lower(_line[:7]) != 'trauger':
            _line = fileutil.rAsciiLine(ifile)

        j = 0
        while j < 20:
            _line = fileutil.rAsciiLine(ifile)
            if _line == '':
                continue
            _lc = string.split(_line)
            if j < 10:
                a_coeffs[j] = float(_lc[0]) + float(_lc[1]) * (indx - 1.5) + float(_lc[2]) * (indx - 1.5) ** 2
            else:
                b_coeffs[j - 10] = float(_lc[0]) + float(_lc[1]) * (indx - 1.5) + float(_lc[2]) * (indx - 1.5) ** 2
            j = j + 1

        ifile.close()
        del ifile
        fx = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
        fy = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
        fx[(0, 0)] = 0.0
        fx[1] = np.array([a_coeffs[2], a_coeffs[1], 0.0, 0.0], dtype=np.float64)
        fx[2] = np.array([a_coeffs[5], a_coeffs[4], a_coeffs[3], 0.0], dtype=np.float64)
        fx[3] = np.array([a_coeffs[9], a_coeffs[8], a_coeffs[7], a_coeffs[6]], dtype=np.float64)
        fy[(0, 0)] = 0.0
        fy[1] = np.array([b_coeffs[2], b_coeffs[1], 0.0, 0.0], dtype=np.float64)
        fy[2] = np.array([b_coeffs[5], b_coeffs[4], b_coeffs[3], 0.0], dtype=np.float64)
        fy[3] = np.array([b_coeffs[9], b_coeffs[8], b_coeffs[7], b_coeffs[6]], dtype=np.float64)
        refpix = {}
        refpix['XREF'] = None
        refpix['YREF'] = None
        refpix['V2REF'] = None
        refpix['V3REF'] = None
        refpix['XDELTA'] = 0.0
        refpix['YDELTA'] = 0.0
        refpix['PSCALE'] = None
        refpix['DEFAULT_SCALE'] = no
        refpix['centered'] = yes
        return (
         fx, fy, refpix, order)


def readCubicTable(idcfile):
    order = 3
    if idcfile == None:
        return fileutil.defaultModel()
    else:
        ifile = open(idcfile, 'r')
        _line = fileutil.rAsciiLine(ifile)
        _found = no
        while _found == no:
            if _line[:7] in ('cubic', 'quartic', 'quintic') or _line[:4] == 'poly':
                found = yes
                break
            _line = fileutil.rAsciiLine(ifile)

        _line = fileutil.rAsciiLine(ifile)
        a_coeffs = string.split(_line)
        x0 = float(a_coeffs[0])
        _line = fileutil.rAsciiLine(ifile)
        a_coeffs[(len(a_coeffs)):] = string.split(_line)
        for i in range(len(a_coeffs)):
            a_coeffs[i] = float(a_coeffs[i])

        _line = fileutil.rAsciiLine(ifile)
        b_coeffs = string.split(_line)
        y0 = float(b_coeffs[0])
        _line = fileutil.rAsciiLine(ifile)
        b_coeffs[(len(b_coeffs)):] = string.split(_line)
        for i in range(len(b_coeffs)):
            b_coeffs[i] = float(b_coeffs[i])

        ifile.close()
        del ifile
        fx = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
        fy = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
        fx[(0, 0)] = 0.0
        fx[1] = np.array([a_coeffs[2], a_coeffs[1], 0.0, 0.0], dtype=np.float64)
        fx[2] = np.array([a_coeffs[5], a_coeffs[4], a_coeffs[3], 0.0], dtype=np.float64)
        fx[3] = np.array([a_coeffs[9], a_coeffs[8], a_coeffs[7], a_coeffs[6]], dtype=np.float64)
        fy[(0, 0)] = 0.0
        fy[1] = np.array([b_coeffs[2], b_coeffs[1], 0.0, 0.0], dtype=np.float64)
        fy[2] = np.array([b_coeffs[5], b_coeffs[4], b_coeffs[3], 0.0], dtype=np.float64)
        fy[3] = np.array([b_coeffs[9], b_coeffs[8], b_coeffs[7], b_coeffs[6]], dtype=np.float64)
        refpix = {}
        refpix['XREF'] = None
        refpix['YREF'] = None
        refpix['V2REF'] = x0
        refpix['V3REF'] = y0
        refpix['XDELTA'] = 0.0
        refpix['YDELTA'] = 0.0
        refpix['PSCALE'] = None
        refpix['DEFAULT_SCALE'] = no
        refpix['centered'] = yes
        return (
         fx, fy, refpix, order)


def factorial(n):
    """ Compute a factorial for integer n. """
    m = 1
    for i in range(int(n)):
        m = m * (i + 1)

    return m


def combin(j, n):
    """ Return the combinatorial factor for j in n."""
    return factorial(j) / (factorial(n) * factorial(j - n))


def defaultModel():
    """ This function returns a default, non-distorting model
        that can be used with the data.
    """
    order = 3
    fx = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
    fy = np.zeros(shape=(order + 1, order + 1), dtype=np.float64)
    fx[(1, 1)] = 1.0
    fy[(1, 0)] = 1.0
    refpix = {}
    refpix['empty_model'] = yes
    refpix['XREF'] = None
    refpix['YREF'] = None
    refpix['V2REF'] = 0.0
    refpix['XSIZE'] = 0.0
    refpix['YSIZE'] = 0.0
    refpix['V3REF'] = 0.0
    refpix['XDELTA'] = 0.0
    refpix['YDELTA'] = 0.0
    refpix['PSCALE'] = None
    refpix['DEFAULT_SCALE'] = no
    refpix['THETA'] = 0.0
    refpix['centered'] = yes
    return (
     fx, fy, refpix, order)


def _MgF2(lam):
    _sig = pow(10000000.0 / lam, 2)
    return np.sqrt(1.0 + 25903550000.0 / (53129930000.0 - _sig) + 4454370800.0 / (11170830000.0 - _sig) + 408388.97 / (176636.1 - _sig))


def convertDate(date):
    """ Converts the DATE-OBS date string into an integer of the
        number of seconds since 1970.0 using calendar.timegm().

        INPUT: DATE-OBS in format of 'YYYY-MM-DD'.
        OUTPUT: Date (integer) in seconds.
    """
    _dates = date.split('-')
    _val = 0
    _date_tuple = (int(_dates[0]), int(_dates[1]), int(_dates[2]), 0, 0, 0, 0, 0, 0)
    return calendar.timegm(_date_tuple)


def read_tdd_coeffs(phdr):
    """ Read in the TDD related keywords from the PRIMARY header of the IDCTAB
    """
    skew_coeffs = {}
    skew_coeffs['TDD_DATE'] = phdr['TDD_DATE']
    skew_coeffs['TDDORDER'] = phdr['TDDORDER']
    skew_coeffs['TDD_A'] = []
    skew_coeffs['TDD_B'] = []
    for k in range(skew_coeffs['TDDORDER'] + 1):
        skew_coeffs['TDD_A'].append(phdr[('TDD_A' + str(k))])
        skew_coeffs['TDD_B'].append(phdr[('TDD_B' + str(k))])

    return skew_coeffs


def compute_wfc_tdd_coeffs(dateobs, skew_coeffs):
    """ Compute the alpha and beta terms for the ACS/WFC
        time-dependent skew correction as described in
        ACS ISR 07-08 by J. Anderson.
    """
    if not isinstance(dateobs, float):
        year, month, day = dateobs.split('-')
        rdate = datetime.datetime(int(year), int(month), int(day))
        rday = float(rdate.strftime('%j')) / 365.25 + rdate.year
    else:
        rday = dateobs
    if skew_coeffs is None:
        if rday > 2009.0:
            err_str = '------------------------------------------------------------------------  \n'
            err_str += 'WARNING: the IDCTAB geometric distortion file specified in the image      \n'
            err_str += '         header did not have the time-dependent distortion coefficients.  \n'
            err_str += '         The pre-SM4 time-dependent skew solution will be used by default.\n'
            err_str += '         Please update IDCTAB with new reference file from HST archive.   \n'
            err_str += '------------------------------------------------------------------------  \n'
            print err_str
        skew_coeffs = {'TDD_A': [0.095, 0.036], 'TDD_B': [
                   -0.029, -0.012], 
           'TDD_DATE': 2004.5, 
           'TDDORDER': 1}
    alpha = 0
    beta = 0
    for c in range(len(skew_coeffs['TDD_A'])):
        alpha += skew_coeffs['TDD_A'][c] * np.power(rday - skew_coeffs['TDD_DATE'], c)
        beta += skew_coeffs['TDD_B'][c] * np.power(rday - skew_coeffs['TDD_DATE'], c)

    return (
     alpha, beta)


def apply_wfc_tdd_coeffs(cx, cy, alpha, beta):
    """ Apply the WFC TDD coefficients directly to the distortion
        coefficients.
    """
    theta_v2v3 = 2.234529
    scale_idc = 0.05
    scale_jay = 0.04973324715
    idctheta = theta_v2v3
    idcrad = fileutil.DEGTORAD(idctheta)
    mrotp = fileutil.buildRotMatrix(idctheta)
    mrotn = fileutil.buildRotMatrix(-idctheta)
    abmat = np.array([[beta, alpha], [alpha, beta]])
    tdd_mat = np.array([[1 + beta / 2048.0, alpha / 2048.0], [alpha / 2048.0, 1 - beta / 2048.0]], np.float64)
    abmat1 = np.dot(tdd_mat, mrotn)
    abmat2 = np.dot(mrotp, abmat1)
    icxy = np.dot(abmat2, [cx.ravel(), cy.ravel()])
    icx = icxy[0]
    icy = icxy[1]
    icx.shape = cx.shape
    icy.shape = cy.shape
    return (
     icx, icy)


def rotate_coeffs(cx, cy, rot, scale=1.0):
    """ Rotate poly coeffs by 'rot' degrees.
    """
    mrot = fileutil.buildRotMatrix(rot) * scale
    rcxy = np.dot(mrot, [cx.ravel(), cy.ravel()])
    rcx = rcxy[0]
    rcy = rcxy[1]
    rcx.shape = cx.shape
    rcy.shape = cy.shape
    return (
     rcx, rcy)