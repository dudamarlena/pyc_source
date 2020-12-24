# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\lib\hartfock.py
# Compiled at: 2013-12-12 06:06:51
from __future__ import print_function, division
from math import cos, pi, pow, exp, log, sinh, sqrt
from copy import deepcopy
import sys, os

def get_input(prompt):
    if sys.hexversion > 50331648:
        return input(prompt)
    else:
        return raw_input(prompt)


class hartfock(object):
    """
    hartfock class
    -------------------
    
    there are nr grid points, and distances are in bohr radii...
    
    r(i)=rmin*(rmax/rmin)**(float(i)/float(nr)) , i=1,2,3,...nr-1,nr
    
    
    
    The orbitals are store in phe(), first index goes 1...nr, the
    second index is the orbital index (i...nel)
    
    Look at the atomic files after printing this out to see everything...
    
    Suffice it to say, that the charge density at radius r(i)
    in units of electrons per cubic Bohr radius is given by 
    
    sum of j=1...nel, 
    occ[j]*phe(i,j)*phe(i,j)/(4.*3.14159265....*r(i)*r(i))... 
    
    Think of the phe functions as plotting the radial wave-functions
    as a function of radius...on our logarithmic mesh...
    
    Final note
    ----------  
    
    the Dirac equation is solved for the orbitals, whereas their density
    is treated by setting phe to the square root of Dirac's F*F+G*G
    times the sign of G...
    
    so we are doing Dirac-Fock, except that we are not treating exchange 
    exactly, in terms of working with major and minor components of the 
    orbitals, and the phe's give the CORRECT CHARGE DENSITY...
    
    the above approximation ought to be very small for valence states,
    so you need not worry about it...
    
    the Breit interaction has been neglected altogether...it should not 
    have a huge effect on the charge density you are concerned with...
    
    authors
    -------
    Eric Shirley - original implementation
    Liam Deacon - python translation
    
    """

    def __init__(self, iorbs=33, iside=600, lmax=4, ihmax=20, nrmax=4000, ntmax=10, npmax=60, input_stream='stdin'):
        """
        Description
        -----------
        Performs calculation of Hartfock subroutine
        
        Parameters
        ----------
        iorbs : int
            number of orbitals
        iside : int
            number of sides
        lmax : int
            maximum angular quantum number
        ihmax : int
            height?
        nrmax : int
            number of radii in grid
        ntmax : int
            ?
        npmax : int
            ?
        input_stream : str
            may be either 'stdin' for user input or else a path to input file
        """
        io2 = iorbs * (iorbs + 1) / 2.0
        ijive = io2 * (io2 + 1) / 2.0
        no = nl = nm = xnj = iss = ev = ek = occ = [None] * iorbs
        r = dr = r2 = v = rho = [None] * nrmax
        njrc = [None] * 4
        vi = [[None] * 7] * nrmax
        phe = orb = [[None] * iorbs] * nrmax
        rpower = [[None] * 16] * nrmax
        vctab = []
        nr = nel = rd = nst = iuflag = int
        e = etot = etot2 = zorig = xntot = rmin = rmax = dl = float
        if not input_stream != 'stdin' and not os.path.isfile(input_stream):
            raise IOError("'%s' is not a valid input file" % input_stream)
        else:
            if input_stream == 'stdin':
                pass
            elif os.path.isfile(input_stream):
                input_file = input_stream
                f = open(input_file, 'r')
            rel = 0
            iline = 0
            ichar = str
            while ichar != 'q':
                ichar = '!'
                while ichar == 'C' or ichar == '!':
                    if os.path.isfile(input_stream):
                        line = f.next()
                        ichar = line.strip()[0]
                        iline += 1
                    else:
                        ichar = get_input("Enter command character ('q' to quit): ")

                if ichar == 'd':
                    if os.path.isfile(input_stream):
                        rel = f.next().split('!')[0]
                    else:
                        rel = int(get_input('Please enter relativity flag: '))
                elif ichar == 'x':
                    if os.path.isfile(input_stream):
                        alfa = float(('').join([ ch for ch in f.next().split('!')[0] if ch is not 'd' and ch is not 'D'
                                               ]))
                    else:
                        alfa = float(get_input('Enter exchange correlation method (0=HARTREE-FOCK, >0=LDA, <0=XALPHA): '))
                elif ichar == 'a':
                    etot, nst, rel, alfa, nr, r, dr, r2, dl, e, njrc, vi, zorig, xntot, nel, no, nl, xnj, ev, occ, iss, ek, orb, iuflag, rpower, nm, phe, etot2 = abinitio(etot, nst, rel, alfa, nr, r, dr, r2, dl, e, njrc, vi, zorig, xntot, nel, no, nl, xnj, ev, occ, iss, ek, orb, iuflag, rpower, nm, phe, etot2, input_stream=f)
                elif ichar == 'i':
                    zorig, nr, rmin, rmax, r, dr, r2, dl, njrc, xntot, nel = initiali(zorig, nr, rmin, rmax, r, dr, r2, dl, njrc, xntot, nel, input_stream=f)
                else:
                    if ichar == 'q':
                        return
                    if ichar == 'w':
                        ixflag = 1
                        iu = -1
                        ir = 0
                        hfdisk(iu, ir, etot, nst, rel, nr, rmin, rmax, r, rho, zorig, xntot, ixflag, nel, no, nl, xnj, iss, ev, ek, occ, njrc, vi, phe, orb, input_stream=f)
                    elif ichar == 'r':
                        iu = -1
                        ir = 1
                        hfdisk(iu, ir, etot, nst, rel, nr, rmin, rmax, r, rho, zorig, xntot, ixflag, nel, no, nl, xnj, iss, ev, ek, occ, njrc, vi, phe, orb)
                        setgrid(nr, rmin, rmax, r, dr, r2, dl)
                    elif ichar == 'u':
                        if os.path.isfile(input_stream):
                            iuflag = int(f.next().split('!')[0])
                        else:
                            iuflag = int(get_input('Please enter IUFLAG (0=U, 1=SU, 2=R): '))
                    elif ichar == 'c':
                        if os.path.isfile(input_stream):
                            corpol, rs, rp, sd = f.next().split('!')[0].split()[:3]
                        else:
                            while True:
                                try:
                                    corpol, rs, rp, sd = get_input('enter ALPHA, RS, RP, RD: ').split()[:3]
                                    break
                                except:
                                    print('Invalid input - please retry...')

                            for k in range(0, nr):
                                fs = pow(1.0 - exp(-pow(r[k] / rs, 2.0)), 2.0)
                                fp = pow(1.0 - exp(-pow(r[k] / rp, 2.0)), 2.0)
                                fd = pow(1.0 - exp(-pow(r[k] / rd, 2.0)), 2.0)
                                vctab[k][0] = -corpol / 2.0 * fs * fs / pow(r[k], 4.0)
                                vctab[k][1] = -corpol / 2.0 * fp * fp / pow(r[k], 4.0)
                                vctab[k][2] = -corpol / 2.0 * fd * fd / pow(r[k], 4.0)

                    elif ichar == 'f':
                        if os.path.isfile(input_stream):
                            iunit, corpol = [ t(s) for t, s in zip((int, float), f.next().split('!')[0].split()[:1]) ]
                            ilev, inum, eold = [ t(s) for t, s in zip((
                             int, int, float), f.next().split('!')[0].split()[:2])
                                               ]
                        else:
                            while True:
                                try:
                                    iunit, corpol = [ t(s) for t, s in zip((
                                     int, float), get_input('Please enter IUNIT, CORPOL: ').split()[:2])
                                                    ]
                                    break
                                except:
                                    print('incorrect input - please retry...')

                            while True:
                                try:
                                    ilev, inum, eold = [ t(s) for t, s in zip((
                                     int, int, float), get_input('Please enter ILEV, INUM, EOLD: '))
                                                       ]
                                    break
                                except:
                                    print('incorrect input - please retry...')

                            xl = nl[ilev]
                            if inum == 1:
                                eav = f.next().split('!')[0]
                            else:
                                e1, e2 = f.next().split('!')[0].split()[:1]
                                eav = (e1 * xl + e2 * (xl + 1.0)) / (xl + xl + 1.0)
                            if eav < 0.0:
                                eav = eold + eav
                            if iunit == 2:
                                eav = eav / 2.0
                            elif iunit == 3:
                                eav = eav / 27.2116
                            elif iunit == 4:
                                eav = eav * 0.000123985 / 27.2116
                            sd = abs(abs(eav) - abs(ev[ilev]))
                            rl = sl = sh = 0.0
                            rh = 10.0
                            sc = abs(1 + sd * 1000000)
                            while abs(sc - sd) > 1e-06:
                                if sl * sh <= 1e-08:
                                    rc = rl + (rh - rl) / 2.0
                                if sl * sh > 1e-08:
                                    rc = rl + (rh - rl) * (sd - sl) / (sh - sl)
                                sc = 0.0
                                for i in range(1, nr + 1):
                                    f = pow(1.0 - exp(-pow(r[i] / rc, 2.0)), 2.0)
                                    vcpp = corpol / (2.0 * pow(r[i], 4.0)) * f * f
                                    sc += dr[i] * phe[i][ilev] * phe[i][ilev] * vcpp

                                if sc > sd:
                                    rl = rc
                                    sl = sc
                                elif sc < sd:
                                    rh = rc
                                    sh = sc
                                print(('{} {}').format(rc, sc))

                    elif ichar == 'p':
                        pseudo(etot, nst, rel, alfa, nr, rmin, rmax, r, dr, r2, dl, phe, orb, njrc, vi, zorig, xntot, nel, no, nl, xnj, ev, occ, iss, ek, iuflag, vctab)
                    elif ichar == 'g':
                        iu = f.next().split('!')[0]
                        jive = f.next().split('!')[0]
                        jive2 = f.next().split('!')[0]
                        jive3 = f.next().split('!')[0]
                        zizv = abs(r[(nr - 1)] * vi[(nr - 1)][1])
                        print(('{}').format(jive))
                        print(('{}').format(jive2))
                        print(('{}').format(jive3))
                        print(3, nr, zizv)
                        for i in range(1, nr + 1):
                            print(r[i])

                        for k in range(1, nr + 1):
                            print(0, vi[k][1])
                            print(1, vi[k][3])
                            print(2, vi[k][5])
                            print(0.0)

                        for j in range(1, nr + 1):
                            rh = 0.0
                            for k in range(1, nel + 1):
                                rh += phe[j][k] * phe[j][k] * occ[k]

                            print(('{}').format(rh))

                    elif ichar == 'v':
                        for k in range(1, nr + 1):
                            print(r[k], vi[k][1] * r[k])
                            print(r[k], vi[k][3] * r[k])
                            print(r[k], vi[k][5] * r[k])

                    elif ichar == 'V':
                        fourier(nr, r, dr, r2, vi)
                    else:
                        print("'%s' is not a valid command - valid characters are:\na: do abinitio\nc: corpol values\nd: relativistic switch\nf: \ng: write to iu file\ni: initialise\np: pseudo\nu: \nv: \nV: fourier\nq: quit\n" % ichar)

        return


def abinitio(etot, nst, rel, alfa, nr, r, dr, r2, dl, e, njrc, vi, zorig, xntot, nel, no, nl, xnj, ev, occ, iss, ek, orb, iuflag, rpower, nm, phe, etot2, input_stream='stdin'):
    """abinitio subroutine"""
    xntot = 0.0
    eerror = evi = float
    for i in range(8):
        xi = i
        for k in range(len(r)):
            rpower[k][i] = pow(r[k], xi)

    if input == 'stdin':
        nfc, nel, ratio, etol, xnum = [ t(s) for t, s in zip((int, int, float, float, float), get_input('Please enter NFC NEL RATIO ETOL XNUM: '))
                                      ]
    else:
        if isinstance(input_stream, file):
            f = input_stream
            nfc, nel, ratio, etol, xnum = [ t(s) for t, s in zip((
             int, int, float, float, float), f.next().split('!')[0].split()[:5])
                                          ]
        try:
            i = 0
            if input == 'stdin':
                for i in range(nfc, nel):
                    no[i], nl[i], nm[i], xnj[i], iss[i], occ[i] = [ t(s) for t, s in zip((int, int, int, float, float, float), get_input('Please enter [%i] N L M J S OCC: ' % i)) ]

                ev[i] = 0.0
                xntot += occ[i]
                for j in range(1, nr + 1):
                    phe[j][i] = 0.0
                    orb[j][i] = 0.0

            else:
                for i in range(nfc, nel):
                    no[i], nl[i], nm[i], xnj[i], iss[i], occ[i] = [ t(s) for t, s in zip((int, int, int, float, float, float), f.next().split('!')[0].split()[:6])
                                                                  ]
                    ev[i] = 0.0
                    xntot += occ[i]
                    for j in range(1, nr + 1):
                        phe[j][i] = 0.0
                        orb[j][i] = 0.0

        except TypeError:
            raise TypeError('Problem loading N L M J S OCC - entry %i')

        while True:
            atsolve(etot, nst, rel, alfa, eerror, nfc, nr, r, dr, r2, dl, phe, njrc, vi, zorig, xntot, nel, no, nl, nm, xnj, ev, occ, iss, ek, ratio, orb, rpower, xnum, etot2, iuflag, evi)
            eerror *= (1.0 - ratio) / ratio
            print(' %14.6f%14.6f' % (eerror, etot))
            if eerror <= etol:
                break

        for i in range(1, nel + 1):
            nj = xnj[i] * 2
            print('  %4i%2i%4i%10.4f%18.6f\n' % (no[i], nl[i], nm[i],
             nj, '/2', iss[i], occ[i], ev[i]))
            print('Total energy =  %14.6f  14.6f' % (etot, etot * 27.2116))

    return (
     etot, nst, rel, alfa, nr, r, dr, r2, dl,
     e, njrc, vi, zorig, xntot, nel, no, nl, xnj,
     ev, occ, iss, ek, orb, iuflag, rpower, nm, phe, etot2)


def atsolve(etot, nst, rel, alfa, eerror, nfc, nr, r, dr, r2, dl, phe, njrc, vi, zorig, xntot, nel, no, nl, nm, xnj, ev, occ, iss, ek, ratio, orb, rpower, xnum, etot2, iuflag, evi):
    """atsolve subroutine"""
    q0 = xm1 = xm2 = v = [
     None] * len(r)
    eerror = etot = zeff = 0.0
    for i in range(nel):
        if i > nfc:
            idoflag = 1
            i, orb, nl[i], iss[i], idoflag, v, zeff, zorig, rel, nr, r, r2, dl, q0, xm1, xm2, njrc, vi = setqmm(i, orb, nl[i], iss[i], idoflag, v, zeff, zorig, rel, nr, r, r2, dl, q0, xm1, xm2, njrc, vi)
        xkappa = -1.0
        if abs(xnj[i]) > nl[i] + 0.25:
            xkappa = -nl[i] - 1
        if abs(xnj[i]) < nl[i] - 0.25:
            xkappa = nl[i]
        print(i, occ[i], no[i], nl[i], xkappa, xnj[i], zorig, zeff, evi, phe[1][i], v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
        i, occ[i], no[i], nl[i], xkappa, xnj[i], zorig, zeff, evi, phe[1][i], v, q0, xm1, xm2, nr, r, dr, r2, dl, rel = elsolve(i, occ[i], no[i], nl[i], xkappa, xnj[i], zorig, zeff, evi, phe[1][i], v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
        if abs(ev[i] - evi) > eerror:
            eerror = abs(ev[i] - evi)
        ev[i] = evi
        ekk = 0.0
        ll = 2
        for j in range(nr, 0, -1):
            dq = phe[j][i] * phe[j][i]
            ekk = ekk + (evi - orb[j][i]) * dr[j] * dq * ll / 3.0
            ll = 6 - ll

        ek[i] = ekk
        etot += ek[i] * occ[i]
        getpot(etot, nst, rel, alfa, dl, nr, dr, r, r2, xntot, phe, ratio, orb, occ, iss, nel, nl, nm, no, xnj, rpower, xnum, etot2, iuflag)

    return (etot, nst, rel, alfa, eerror, nfc, nr, r, dr, r2, dl,
     phe, njrc, vi, zorig, xntot, nel, no, nl, nm, xnj, ev, occ, iss,
     ek, ratio, orb, rpower, xnum, etot2, iuflag, evi)


def getpot(etot, nst, rel, alfa, dl, nr, dr, r, r2, xntot, phe, ratio, orb, occ, iss, nel, nl, nm, no, xnj, rpower, xnum, etot2, iuflag):
    """getpot subroutine"""
    cg = [
     [
      [
       [
        [
         None] * 13] * 13] * 13] * 6] * 6
    pin = [[[None] * 17] * 9] * 9
    xq1 = xq2 = xq0 = xqi1 = xqi2 = xqi0 = xqj1 = xqj2 = xqj0 = [None] * nr
    clebschgordan(nel, nl, cg)
    getillls(pin)
    ratio1 = 1.0 - ratio
    for i in range(1, nel + 1):
        for k in range(1, nr + 1):
            orb[k][i] = ratio1 * orb[k][i]

    for i in range(1, nel + 1):
        li = nl[i]
        mi = nm[i]
        jstart = i + 1
        if xnj[i] < 0.0 or occ[i] > 1.0 or abs(alfa) > 0.001:
            jstart = i
        for j in range(jstart, nel + 1):
            if occ[i] == 0.0 and occ[j] == 0.0:
                continue
            lj = nl[j]
            mj = nm[j]
            lmx = 2 * li
            if li > lj:
                lmx = 2 * lj
            if occ[i] > 1.0 or occ[j] > 1.0 or xnj[i] < 0.0 or xnj[j] < 0.0:
                lmx = 0
            for la in range(lmx, -1, -2):
                lap = la + 1
                coeff = (li + li + 1) * (lj + lj + 1) / pow(la + la + 1, 2.0) * cg[li][li][la][mi][(-mi)] * cg[lj][lj][la][mj][(-mj)] * cg[li][li][la][0][0] * cg[lj][lj][la][0][0]

            if mi + mj != int(2 * ((mi + mj) / 2.0)):
                coeff = -coeff
            if i == j:
                coeff /= 2.0
            coeffi = occ[i] * coeff
            coeffj = occ[j] * coeff
            ri = ratio * coeffi
            rj = ratio * coeffj
            rc = coeff * occ[i] * occ[j]
            xouti = 0.0
            xoutj = 0.0
            for k in range(1, nr + 1):
                xqi0[k] = dr[k] * phe[k][i] * phe[k][i] / 2.0
                xqi1[k] = xqi0[k] * rpower[k][la]
                if rpower[k][lap] != 0.0:
                    xqi2[k] = xqi0[k] / rpower[k][lap]
                else:
                    xqi2[k] = 0.0
                xouti += xqi2[k]
                xqj0[k] = dr[k] * phe[k][j] * phe[k][j] / 2.0
                xqj1[k] = xqj0[k] * rpower[k][la]
                if rpower[k][lap] != 0.0:
                    xqj2[k] = xqj0[k] / rpower[k][lap]
                else:
                    xqj2[k] = 0.0
                xoutj += xqj2[k]

            xinti = xqi1[1]
            xintj = xqj1[1]
            xouti = 2.0 * xouti - xqi2[1]
            xoutj = 2.0 * xoutj - xqj2[1]
            for k in range(2, nr + 1):
                xinti += xqi1[k] + xqi1[(k - 1)]
                xouti -= xqi2[k] - xqi2[(k - 1)]
                vali = xouti * rpower[k][la]
                if rpower[k][lap] != 0.0:
                    vali += xinti / rpower[k][lap]
                orb[k][j] += ri * vali
                xintj = xintj + xqj1[k] + xqj1[(k - 1)]
                xoutj = xoutj - xqj2[k] - xqj2[(k - 1)]
                valj = xoutj * rpower[k][la]
                if rpower[k][lap] != 0.0:
                    valj += xintj / rpower[k][lap]
                orb[k][i] += rj * valj
                etot = etot + rc * (xqi0[k] * valj + xqj0[k] * vali)

            if iss[i] != iss[j] and occ[i] <= 1.0 and occ[j] <= 1.0 and xnj[i] >= 0.0 and xnj[j] >= 0.0:
                continue
            if abs(alfa) >= 0.001:
                continue
            lmx = li + lj
            lmin = abs(mi - mj)
            if occ[i] > 1.0 or occ[j] > 1.0 or xnj[i] < 0.0 or xnj[j] < 0.0:
                lmin = 0
            for la in range(lmx, lmin - 1, -2):
                lap = la + 1
                coeff = float((li + li + 1) * (lj + lj + 1)) / float(pow(la + la + 1, 2.0) * pow(cg[li][lj][la][(-mi)][mj] * cg[li][lj][la][0][0], 2.0))
                if occ[i] > 1.0 or occ[j] > 1.0 or xnj[i] < 0.0 or xnj[j] < 0.0:
                    coeff = pin[li][lj][la] / 4.0
                if i == j:
                    coeff /= 2.0
                coeffi = occ[i] * coeff
                coeffj = occ[j] * coeff
                ri = ratio * coeffi
                rj = ratio * coeffj
                rc = coeff * occ[i] * occ[j]
                xnum2 = xnum * xnum
                xout = 0.0
                for k in range(1, nr + 1):
                    xq0[k] = dr[k] * phe[k][i] * phe[k][j] / 2.0
                    xq1[k] = xq0[k] * rpower[k][la]
                    if rpower[k][lap] != 0.0:
                        xq2[k] = xq0[k] / rpower[k][lap]
                    else:
                        xq2[k] = 0.0
                    xout += xq2[k]

                xint = xq1[1]
                xout = 2.0 * xout - xq2[1]
                for k in range(2, nr + 1):
                    xint += xq1[k] + xq1[(k - 1)]
                    xout -= xq2[k] - xq2[(k - 1)]
                    if xq0[k] != 0.0:
                        val = xout * rpower[k][la]
                    if rpower[k][lap] != 0.0:
                        val += xint / rpower[k][lap]
                    etot -= 2.0 * xq0[k] * rc * val
                    xx = phe[k][j] / phe[k][i]
                    if abs(xx) / xnum > 1.0:
                        orb[k][i] -= rj * xnum2 / xx * val
                    else:
                        orb[k][i] -= rj * xx * val
                    xx = phe[k][i] / phe[k][j]
                    if abs(xx) / xnum > 1.0:
                        orb[k][j] -= ri * xnum2 / xx * val
                    else:
                        orb[k][j] -= ri * xx * val

    if abs(alfa) >= 0.001:
        if alfa > 0.0:
            fx = 1.0
            fc = 1.0
        else:
            fx = 1.5 * abs(alfa)
            fc = 0.0
    ex = ec = ux1 = ux2 = uc1 = uc2 = 0.0
    for i in range(1, nr + 1):
        xn = 0.0
        for j in range(1, nel + 1):
            xn += phe[i][j] * phe[i][j] * occ[j]

        xn1 = xn / 2.0
        xn2 = xn / 2.0
        nst = 2
        nst, rel, r2[i], xn1, xn2, ex, ec, ux1, ux2, uc1, uc2 = exchcorr(nst, rel, r2[i], xn1, xn2, ex, ec, ux1, ux2, uc1, uc2)
        exc = fx * ex + fc * ec
        uxc = fx * ux1 + fc * uc1
        etot = etot + dr[i] * xn * exc
        for j in range(1, nel + 1):
            orb[i][j] += uxc * ratio

    for i in range(1, nr + 1):
        if iuflag:
            jj = 1
        ii = jj
        icond = True
        while icond:
            if ii != nel:
                icond = False
                if no[jj] == no[(ii + 1)] and nl[jj] == nl[(ii + 1)] and iuflag == 2:
                    icond = True
                if no[jj] == no[(ii + 1)] and nl[jj] == nl[(ii + 1)] and iss[jj] == iss[(ii + 1)] and iuflag == 1:
                    icond = True
                if icond:
                    ii += 1

        orba = 0.0
        div = 0.0
        for k in range(jj, ii + 1):
            div += occ[k]
            orba += orb[i][k] * occ[k]

        if div != 0.0:
            orba /= div
            for k in range(jj, ii + 1):
                orb[i][k] = orba

        if ii != nel:
            jj = ii + 1
            continue

    return (
     etot, nst, rel, alfa, dl, nr, dr, r, r2,
     xntot, phe, ratio, orb, occ, iss,
     nel, nl, nm, no, xnj, rpower, xnum, etot2, iuflag)


def elsolve(i, occ, n, l, xkappa, xj, zorig, zeff, e, phi, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel):
    """elsolve subroutine"""
    el = -zorig * zorig / float(n * n)
    eh = 0.0
    etol = 1e-10
    ief = x0 = float
    nn = int
    while True:
        e = (el + eh) / 2.0
        istop = 0
        e, l, xkappa, n, nn, istop, ief, x0, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel = integ(e, l, xkappa, n, nn, istop, ief, x0, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
        if nn < n - l - 1:
            ief = -1
            if ief != 1:
                el = e
            if el > -0.001:
                print('Mixing too strong for level : %i' % i)
                return
            if ief != -1:
                eh = e
            if eh - el > etol:
                continue
            if abs(abs(xj) - abs(float(l))) > 0.25:
                augment(e, l, xj, phi, v, nr, r, dl)
            aa = 0.0
            for j in range(1, nr + 1):
                aa += phi[j] * phi[j] * dr[j]

            xnorm = sqrt(aa)
            for j in range(1, nr + 1):
                phi[j] /= xnorm

        break

    return (
     i, occ, n, l, xkappa, xj, zorig, zeff, e, phi, v,
     q0, xm1, xm2, nr, r, dr, r2, dl, rel)


def augment(e, l, xj, phi, v, nr, r, dl):
    """augment subroutine"""
    phi2 = [
     None] * len(phi)
    c = 137.038
    cc = c * c
    c2 = cc + cc
    xkappa = -1
    if abs(xj) > l + 0.25:
        xkappa = -l - 1
    if abs(xj) < l - 0.25:
        xkappa = l
    for j in range(4, nr - 3 + 1):
        if phi[j] != 0.0:
            g0 = phi[j]
            ga = phi[(j + 1)] - phi[(j - 1)]
            gb = (phi[(j + 2)] - phi[(j - 2)]) / 2.0
            gc = (phi[(j + 3)] - phi[(j - 3)]) / 3.0
            gg = ((1.5 * ga - 0.6 * gb + 0.1 * gc) / (2.0 * dl) + xkappa * g0) / r[j]
            f0 = c * gg / (e - v[j] + c2)
            phi2[j] = sqrt(g0 * g0 + f0 * f0)
            if g0 < 0.0:
                phi2[j] = -phi2[j]
            else:
                phi2[j] = phi[j]

    for j in range(1, 4):
        phi2[j] *= phi[4] / phi2[4]

    phi = phi2
    return


def setqmm(i, orb, l, ns, idoflag, v, zeff, zorig, rel, nr, r, r2, dl, q0, xm1, xm2, njrc, vi):
    """setqmm subroutine"""
    c = 137.038
    alpha = rel / c
    aa = alpha * alpha
    a2 = aa / 2.0
    lp = l + 1
    lpx = lp
    if lp > 4:
        lpx = 4
    lp2 = l + l + 1
    if lp2 > 7:
        lp2 = 7
    zeff = zorig
    if njrc[lpx] > 0:
        zeff = 0.0
    zaa = zeff * aa
    za2 = zeff * a2
    if idoflag:
        if not njrc[lpx]:
            if idoflag == 1:
                for j in range(1, nr + 1):
                    v[j] = -zeff / r[j] + orb[j][i]

            for j in range(2, nr - 1):
                dvdl = (orb[(j + 1)][i] - orb[(j - 1)][i]) / (2.0 * dl)
                ddvdrr = ((orb[(j + 1)][i] + orb[(j - 1)][i] - 2.0 * orb[j][i]) / (dl * dl) - dvdl) / r2[j]
                xm1[j] = -a2 * dvdl / r[j] - za2 / r2[j]
                xm2[j] = -a2 * ddvdrr + zaa / r2[j] / r[j]

            xm1[nr] = xm1[(nr - 1)]
            xm2[nr] = xm2[(nr - 1)]
            xm1[1] = xm1[2] + za2 / r2[2] - za2 / r2[1]
            xm2[1] = xm2[2] - zaa / r2[2] / r[2] + zaa / r2[1] / r[1]
    else:
        if idoflag == 1:
            for j in range(1, nr + 1):
                v[j] = vi[j][lp2] + orb[j][i]

        for j in range(2, nr - 1 + 1):
            dvdl = (v[(j + 1)] - v[(j - 1)]) / (2.0 * dl)
            ddvdrr = ((v[(j + 1)] + v[(j - 1)] - 2.0 * v[j]) / (dl * dl) - dvdl) / r2[j]
            xm1[j] = -a2 * dvdl / r[j]
            xm2[j] = -a2 * ddvdrr

        xm1[nr] = xm1[(nr - 1)]
        xm2[nr] = xm2[(nr - 1)]
        xm1[1] = xm1[2]
        xm2[1] = xm2[2]
    xlb = l + pow(0.5, 2.0) / 2.0
    for j in range(1, nr + 1):
        vj = v[j]
        q0[j] = vj * (1.0 - a2 * vj) + xlb / r2[j]

    return (i, orb, l, ns, idoflag, v, zeff, zorig, rel,
     nr, r, r2, dl, q0, xm1, xm2, njrc, vi)


def initiali(zorig, nr, rmin, rmax, r, dr, r2, dl, njrc=[
 None] * 4, xntot=0.0, nel=0, input_stream='stdin'):
    """
    Description
    -----------
    Initialise the radial charge grid
    
    Parameters
    ----------
    zorig : float
    
    nr : int
        Number of radial grid points
        
    rmin : float
        Minimum radius
        
    rmax : float
        Maximum radius
        
    r : list
        Dummy list of radii
        
    dr : list
        Dummy list to be populated
        
    r2 : list
        Dummy list to be populated
        
    dl : float
        Dummy float
        
    njrc : list
        Dummy list to be populated
    
    xntot :
    
    nel : int
    
    Returns
    -------
    tuple : (zorig, nr, rmin, rmax, r, dr, r2, dl, njrc, xntot, nel)
    
    """
    if input_stream == 'stdin':
        zorig, nr = [ t(s) for t, s in zip((float, int), get_input('Enter Z, NR: ').split()) ]
    elif isinstance(input_stream, file):
        zorig, nr = [ t(s) for t, s in zip((float, int), input_stream.next().split('!')[0].split()) ]
    else:
        raise IOError("input stream is not a file handle or 'stdin'")
    rmin = 0.0001 / zorig
    rmax = 800.0 / sqrt(zorig)
    nr, rmin, rmax, r, dr, r2, dl = setgrid(nr, rmin, rmax, r, dr, r2, dl)
    njrc[j] = [ 0 for j in range(len(njrc)) ]
    return (
     zorig, nr, rmin, rmax, r, dr, r2, dl, njrc, xntot, nel)


def setgrid(nr, rmin, rmax, r, dr, r2, dl):
    """Set the radial grid values"""
    ratio = rmax / rmin
    dl = log(ratio) / float(nr)
    xratio = exp(dl)
    xr1 = sqrt(xratio) - sqrt(1.0 / xratio)
    for i in range(len(r)):
        r[i] = pow(rmin * xratio, i)
        dr[i] = r[i] * xr1
        r2[i] = r[i] * r[i]

    return (nr, rmin, rmax, r, dr, r2, dl)


def integ(e, l, xkappa, n, nn, istop, ief, x0, phi, z, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel):
    """integrate out count nodes"""
    dl2 = dl * dl / 12.0
    dl5 = 10.0 * dl2
    c = 137.038
    alpha = rel / c
    za2 = z * z * alpha * alpha
    a2 = alpha * alpha / 2.0
    xl = l
    xlp = l + 1
    xl2 = 0.5 + xl
    xl4 = xl2 * xl2
    if rel == 0.0:
        ss = xlp
    else:
        rtest = 1.0 - za2
        if rtest < 0.0:
            print('Z>137 is too big.')
            sys.exit(1)
        ss = sqrt(rtest)
    ss2 = ss - 0.5
    ief = 0
    t = e - v(1)
    xm0 = 1.0 + a2 * t
    tm = xm0 + xm0
    xmx = xm1[1] / xm0
    xk0 = r2[1] * (tm * t - xmx * (xkappa / r[1] + 0.75 * xmx) + xm2[1] / tm) - xl4
    dk0 = 1.0 + dl2 * xk0
    p0 = dk0
    phi[1] = p0 * sqrt(xm0 * r[1]) / dk0
    t = e - v[2]
    xm = 1.0 + a2 * t
    tm = xm + xm
    xmx = xm1[2] / xm
    xk2 = r2[2] * (tm * t - xmx * (xkappa / r[2] + 0.75 * xmx) + xm2[2] / tm) - xl4
    dk2 = 1.0 + dl2 * xk2
    p1 = dk2 * pow((r[2] / r[1], ss2) - (r[2] - r[1]) * z / xlp) * sqrt(xm0 / xm)
    phi[2] = p1 * sqrt(xm * r[2]) / dk2
    is0 = istop
    if not istop:
        for j in range(nr - 1, 1, -1):
            if e > v[j]:
                break
            ief = -1
            return ief

        istop = j
    nn = 0
    nnideal = n - l - 1
    for i in range(3, istop + 2 + 1):
        t = e - v[i]
        xm = 1.0 + a2 * t
        tm = xm + xm
        xmx = xm1[i] / xm
        p2 = (2.0 - dl5 * xk2) * p1 / dk2 - p0
        xk2 = r2[i] * (tm * t - xmx * (xkappa / r[i] + 0.75 * xmx) + xm2[i] / tm) - xl4
        dk2 = 1.0 + dl2 * xk2
        phi[i] = p2 * sqrt(xm * r[i]) / dk2
        if abs(p2) > 10000000000.0:
            for j in range(1, i + 1):
                phi[j] /= p2

            p0 /= p2
            p1 /= p2
            p2 /= p2
        if p2 * p1 < 0.0:
            nn += 1
            if nn > nnideal:
                ief = 1
                return ief
        p0 = p1
        p1 = p2

    if istop > 0:
        psip2 = phi[(istop + 2)] - phi[(istop - 2)]
        psip1 = phi[(istop + 1)] - phi[(istop - 1)]
        psip = (8.0 * psip1 - psip2) / (12.0 * dl * r[istop])
        x0 = psip / phi[istop]
    if not is0:
        return
    for i in range(istop + 3, nr - 1 + 1):
        t = e - v[i]
        xm = 1.0 + a2 * t
        tm = xm + xm
        xmx = xm1[i] / xm
        p2 = (2.0 - dl5 * xk2) * p1 / dk2 - p0
        if p2 / p1 > 1.0:
            ief = -1
            return ief
        xk2 = r2[i] * (tm * t - xmx * (xkappa / r[i] + 0.75 * xmx) + xm2[i] / tm) - xl4
        dk2 = 1.0 + dl2 * xk2
        phi[i] = p2 * sqrt(xm * r[i]) / dk2
        if abs(p2) > 10000000000.0:
            for j in range(1, i + 1):
                phi[j] /= p2
                p0 = p2
                p1 /= p2
                p2 /= p2
                if p2 * p1 < 0.0:
                    nn += 1
                    if nn > nnideal:
                        ief = 1
                        return

            p0 = p1
            p1 = p2

    return ief


def clebschgordan(nel, nl, cg, si, fa):
    """
    routine to generate Clebsch-Gordan coefficients, in the form of 
    cg(l1,l2,L,m1,m2) = <l1,m1;l2,m2|L,m1+m2>, according to Rose's 
    'Elementary Theory of Angular Momentum', p. 39, Wigner's formula.
    those coefficients listed are only those for which l1.ge.l2.
    coefficients known to be zero because of either the L or M 
    selection rules are not computed, and should not be sought.
    """
    lmx = 0
    for i in range(len(nl)):
        if nl[i] > lmx:
            lmx = nl[i]

    si[0] = fa[0] = 1.0
    for i in range(1, len(si)):
        si[i] = -si[(i - 1)]
        fa[i] = i * fa[(i - 1)]

    for l1 in range(0, lmx + 1):
        for l2 in range(0, l1 + 1):
            for m1 in range(-l1, l1 + 1):
                for m2 in range(-l2, l2 + 1):
                    m3 = m1 + m2
                    lmin = abs(l1 - l2)
                    if lmin < abs(m3):
                        lmin = abs(m3)
                    for l3 in range(lmin, l1 + l2 + 1):
                        prefactor = float(2 * l3 + 1)
                        prefactor *= fa[(l3 + l1 - l2)] / fa[(l1 + l2 + l3 + 1)]
                        prefactor *= fa[(l3 - l1 + l2)] / fa[(l1 - m1)]
                        prefactor *= fa[(l1 + l2 - l3)] / fa[(l1 + m1)]
                        prefactor *= fa[(l3 + m3)] / fa[(l2 - m2)]
                        prefactor *= fa[(l3 - m3)] / fa[(l2 + m2)]
                        prefactor = sqrt(prefactor)
                        sum1 = 0.0
                        numax = l3 - l1 + l2
                        if l3 + m3 < numax:
                            numax = l3 + m3
                        numin = 0
                        if l1 - l2 - m3 < numin:
                            numin = -l1 - l2 - m3
                        for nu in range(numin, numax + 1):
                            sum1 += si[(nu + l2 + m2)] / fa[nu] * fa[(l2 + l3 + m1 - nu)] * fa[(l1 - m1 + nu)] / fa[(l3 - l1 + l2 - nu)] / fa[(l3 + m3 - nu)] / fa[(nu + l1 - l2 - m3)]

                        cg[l1][l2][l3][m1][m2] = prefactor * sum1
                        cg[l2][l1][l3][m2][m1] = si[(l1 + l2 + l3)] * prefactor * sum1


def pseudo--- This code section failed: ---

 L.1132         0  LOAD_CONST               0
                3  BUILD_LIST_1          1 
                6  LOAD_FAST            17  'nel'
                9  BINARY_MULTIPLY  
               10  STORE_FAST           27  'nm'

 L.1133        13  LOAD_GLOBAL           0  'deepcopy'
               16  LOAD_FAST            13  'njrc'
               19  CALL_FUNCTION_1       1  None
               22  STORE_FAST           29  'njrcdummy'

 L.1134        25  LOAD_CONST               None
               28  BUILD_LIST_1          1 
               31  LOAD_GLOBAL           2  'len'
               34  LOAD_FAST             7  'r'
               37  CALL_FUNCTION_1       1  None
               40  BINARY_MULTIPLY  
               41  DUP_TOP          
               42  STORE_FAST           30  'q0'
               45  DUP_TOP          
               46  STORE_FAST           31  'xm1'
               49  STORE_FAST           32  'xm2'

 L.1135        52  LOAD_CONST               None
               55  BUILD_LIST_1          1 
               58  LOAD_CONST               7
               61  BINARY_MULTIPLY  
               62  BUILD_LIST_1          1 
               65  LOAD_GLOBAL           2  'len'
               68  LOAD_FAST             7  'r'
               71  CALL_FUNCTION_1       1  None
               74  BINARY_MULTIPLY  
               75  STORE_FAST           33  'rpower'

 L.1136        78  LOAD_GLOBAL           3  'float'
               81  DUP_TOP          
               82  STORE_FAST           34  'zeff'
               85  STORE_FAST           35  'etot2'

 L.1139        88  LOAD_FAST            28  'input_stream'
               91  LOAD_CONST               'stdin'
               94  COMPARE_OP            2  ==
               97  POP_JUMP_IF_FALSE   179  'to 179'

 L.1140       100  BUILD_LIST_0          0 
              103  LOAD_GLOBAL           4  'zip'
              106  LOAD_GLOBAL           5  'int'
              109  LOAD_GLOBAL           3  'float'
              112  LOAD_GLOBAL           3  'float'
              115  BUILD_TUPLE_3         3 

 L.1141       118  LOAD_GLOBAL           6  'get_input'
              121  LOAD_CONST               'Please enter NP CORPOL RNORM: '
              124  CALL_FUNCTION_1       1  None
              127  LOAD_ATTR             7  'split'
              130  CALL_FUNCTION_0       0  None
              133  CALL_FUNCTION_2       2  None
              136  GET_ITER         
              137  FOR_ITER             24  'to 164'
              140  UNPACK_SEQUENCE_2     2 
              143  STORE_FAST           36  't'
              146  STORE_FAST           37  's'
              149  LOAD_FAST            36  't'
              152  LOAD_FAST            37  's'
              155  CALL_FUNCTION_1       1  None
              158  LIST_APPEND           2  None
              161  JUMP_BACK           137  'to 137'
              164  UNPACK_SEQUENCE_3     3 
              167  STORE_FAST           38  'np'
              170  STORE_FAST           39  'corpol'
              173  STORE_FAST           40  'rnorm'
              176  JUMP_FORWARD        119  'to 298'

 L.1143       179  LOAD_GLOBAL           8  'isinstance'
              182  LOAD_FAST            28  'input_stream'
              185  LOAD_GLOBAL           9  'file'
              188  CALL_FUNCTION_2       2  None
              191  POP_JUMP_IF_FALSE   286  'to 286'

 L.1144       194  BUILD_LIST_0          0 
              197  LOAD_GLOBAL           4  'zip'
              200  LOAD_GLOBAL           5  'int'
              203  LOAD_GLOBAL           3  'float'
              206  LOAD_GLOBAL           3  'float'
              209  BUILD_TUPLE_3         3 

 L.1145       212  LOAD_FAST            28  'input_stream'
              215  LOAD_ATTR            10  'readline'
              218  CALL_FUNCTION_0       0  None
              221  LOAD_ATTR             7  'split'
              224  LOAD_CONST               '!'
              227  CALL_FUNCTION_1       1  None
              230  LOAD_CONST               0
              233  BINARY_SUBSCR    
              234  LOAD_ATTR             7  'split'
              237  CALL_FUNCTION_0       0  None
              240  CALL_FUNCTION_2       2  None
              243  GET_ITER         
              244  FOR_ITER             24  'to 271'
              247  UNPACK_SEQUENCE_2     2 
              250  STORE_FAST           36  't'
              253  STORE_FAST           37  's'
              256  LOAD_FAST            36  't'
              259  LOAD_FAST            37  's'
              262  CALL_FUNCTION_1       1  None
              265  LIST_APPEND           2  None
              268  JUMP_BACK           244  'to 244'
              271  UNPACK_SEQUENCE_3     3 
              274  STORE_FAST           38  'np'
              277  STORE_FAST           39  'corpol'
              280  STORE_FAST           40  'rnorm'
              283  JUMP_FORWARD         12  'to 298'

 L.1147       286  LOAD_GLOBAL          11  'IOError'
              289  LOAD_CONST               'input_stream is not valid!'
              292  CALL_FUNCTION_1       1  None
              295  RAISE_VARARGS_1       1  None
            298_0  COME_FROM           283  '283'
            298_1  COME_FROM           176  '176'

 L.1149       298  LOAD_CONST               0.0
              301  STORE_FAST           16  'xntot'

 L.1151       304  SETUP_LOOP         1790  'to 2097'
              307  LOAD_GLOBAL          12  'True'
              310  POP_JUMP_IF_FALSE  2096  'to 2096'

 L.1152       313  SETUP_LOOP          610  'to 926'
              316  LOAD_GLOBAL          13  'range'
              319  LOAD_FAST            38  'np'
              322  LOAD_FAST            17  'nel'
              325  LOAD_CONST               1
              328  BINARY_ADD       
              329  CALL_FUNCTION_2       2  None
              332  GET_ITER         
              333  FOR_ITER            589  'to 925'
              336  STORE_FAST           41  'i'

 L.1153       339  LOAD_GLOBAL          14  'print'
              342  LOAD_CONST               'l={} ...'
              345  LOAD_ATTR            15  'format'
              348  LOAD_FAST            19  'nl'
              351  LOAD_FAST            41  'i'
              354  BINARY_SUBSCR    
              355  CALL_FUNCTION_1       1  None
              358  CALL_FUNCTION_1       1  None
              361  POP_TOP          

 L.1154       362  LOAD_FAST            19  'nl'
              365  LOAD_FAST            41  'i'
              368  BINARY_SUBSCR    
              369  LOAD_FAST            19  'nl'
              372  LOAD_FAST            41  'i'
              375  BINARY_SUBSCR    
              376  BINARY_ADD       
              377  LOAD_CONST               1
              380  BINARY_ADD       
              381  STORE_FAST           42  'lp2'

 L.1155       384  LOAD_FAST            21  'ev'
              387  LOAD_FAST            41  'i'
              390  BINARY_SUBSCR    
              391  STORE_FAST           43  'e'

 L.1156       394  SETUP_LOOP           59  'to 456'
              397  LOAD_GLOBAL          13  'range'
              400  LOAD_CONST               1
              403  LOAD_FAST             4  'nr'
              406  LOAD_CONST               1
              409  BINARY_ADD       
              410  CALL_FUNCTION_2       2  None
              413  GET_ITER         
              414  FOR_ITER             38  'to 455'
              417  STORE_FAST           44  'j'

 L.1157       420  LOAD_FAST            12  'orb'
              423  LOAD_FAST            44  'j'
              426  BINARY_SUBSCR    
              427  LOAD_FAST            41  'i'
              430  DUP_TOPX_2            2  None
              433  BINARY_SUBSCR    
              434  LOAD_FAST            26  'vctab'
              437  LOAD_FAST            44  'j'
              440  BINARY_SUBSCR    
              441  LOAD_FAST            19  'nl'
              444  LOAD_FAST            41  'i'
              447  BINARY_SUBSCR    
              448  BINARY_SUBSCR    
              449  INPLACE_ADD      
              450  ROT_THREE        
              451  STORE_SUBSCR     
              452  JUMP_BACK           414  'to 414'
              455  POP_BLOCK        
            456_0  COME_FROM           394  '394'

 L.1158       456  LOAD_CONST               1
              459  STORE_FAST           45  'idoflag'

 L.1159       462  LOAD_CONST               1
              465  STORE_FAST           46  'ns'

 L.1160       468  LOAD_GLOBAL          16  'setqmm'
              471  LOAD_FAST            41  'i'
              474  LOAD_FAST            12  'orb'
              477  LOAD_FAST            19  'nl'
              480  LOAD_FAST            41  'i'
              483  BINARY_SUBSCR    
              484  LOAD_FAST            46  'ns'
              487  LOAD_FAST            45  'idoflag'
              490  LOAD_FAST            14  'vi'
              493  LOAD_CONST               1
              496  BINARY_SUBSCR    
              497  LOAD_FAST            42  'lp2'
              500  BINARY_SUBSCR    
              501  LOAD_FAST            34  'zeff'
              504  LOAD_FAST            15  'zorig'
              507  LOAD_FAST             2  'rel'

 L.1161       510  LOAD_FAST             4  'nr'
              513  LOAD_FAST             7  'r'
              516  LOAD_FAST             9  'r2'
              519  LOAD_FAST            10  'dl'
              522  LOAD_FAST            30  'q0'
              525  LOAD_FAST            31  'xm1'
              528  LOAD_FAST            32  'xm2'
              531  LOAD_FAST            29  'njrcdummy'
              534  LOAD_FAST            14  'vi'
              537  CALL_FUNCTION_18     18  None
              540  POP_TOP          

 L.1162       541  SETUP_LOOP           41  'to 585'
              544  LOAD_GLOBAL          13  'range'
              547  LOAD_CONST               1
              550  LOAD_FAST             4  'nr'
              553  LOAD_CONST               1
              556  BINARY_ADD       
              557  CALL_FUNCTION_2       2  None
              560  GET_ITER         
              561  FOR_ITER             20  'to 584'
              564  STORE_FAST           44  'j'

 L.1163       567  LOAD_CONST               0.0
              570  LOAD_FAST            12  'orb'
              573  LOAD_FAST            44  'j'
              576  BINARY_SUBSCR    
              577  LOAD_FAST            41  'i'
              580  STORE_SUBSCR     
              581  JUMP_BACK           561  'to 561'
              584  POP_BLOCK        
            585_0  COME_FROM           541  '541'

 L.1168       585  LOAD_GLOBAL          17  'pseudize'
              588  LOAD_FAST            41  'i'
              591  LOAD_FAST            12  'orb'
              594  LOAD_FAST            43  'e'
              597  LOAD_FAST            19  'nl'
              600  LOAD_FAST            41  'i'
              603  BINARY_SUBSCR    
              604  LOAD_FAST            20  'xnj'
              607  LOAD_FAST            41  'i'
              610  BINARY_SUBSCR    
              611  LOAD_FAST            18  'no'
              614  LOAD_FAST            41  'i'
              617  BINARY_SUBSCR    
              618  LOAD_FAST            13  'njrc'
              621  LOAD_FAST            34  'zeff'

 L.1169       624  LOAD_FAST            14  'vi'
              627  LOAD_CONST               1
              630  BINARY_SUBSCR    
              631  LOAD_FAST            42  'lp2'
              634  BINARY_SUBSCR    
              635  LOAD_FAST            30  'q0'
              638  LOAD_FAST            31  'xm1'
              641  LOAD_FAST            32  'xm2'
              644  LOAD_FAST             4  'nr'
              647  LOAD_FAST             5  'rmin'
              650  LOAD_FAST             6  'rmax'
              653  LOAD_FAST             7  'r'
              656  LOAD_FAST             8  'dr'
              659  LOAD_FAST             9  'r2'

 L.1170       662  LOAD_FAST            10  'dl'
              665  LOAD_FAST             2  'rel'
              668  CALL_FUNCTION_20     20  None
              671  POP_TOP          

 L.1171       672  LOAD_GLOBAL          14  'print'
              675  LOAD_CONST               'Doing pseudo PP generation...'
              678  CALL_FUNCTION_1       1  None
              681  POP_TOP          

 L.1172       682  LOAD_FAST            19  'nl'
              685  LOAD_FAST            41  'i'
              688  BINARY_SUBSCR    
              689  LOAD_CONST               1
              692  BINARY_ADD       
              693  LOAD_FAST            18  'no'
              696  LOAD_FAST            41  'i'
              699  STORE_SUBSCR     

 L.1173       700  LOAD_CONST               0.0
              703  STORE_FAST           47  'ruse'

 L.1174       706  LOAD_CONST               -1.0
              709  STORE_FAST           48  'xkappa'

 L.1175       712  LOAD_GLOBAL          18  'elsolve'
              715  LOAD_FAST            41  'i'
              718  LOAD_FAST            22  'occ'
              721  LOAD_FAST            41  'i'
              724  BINARY_SUBSCR    
              725  LOAD_FAST            18  'no'
              728  LOAD_FAST            41  'i'
              731  BINARY_SUBSCR    
              732  LOAD_FAST            19  'nl'
              735  LOAD_FAST            41  'i'
              738  BINARY_SUBSCR    
              739  LOAD_FAST            48  'xkappa'
              742  LOAD_FAST            20  'xnj'
              745  LOAD_FAST            41  'i'
              748  BINARY_SUBSCR    

 L.1176       749  LOAD_FAST            15  'zorig'
              752  LOAD_FAST            34  'zeff'
              755  LOAD_FAST            21  'ev'
              758  LOAD_FAST            41  'i'
              761  BINARY_SUBSCR    
              762  LOAD_FAST            11  'phe'
              765  LOAD_CONST               1
              768  BINARY_SUBSCR    
              769  LOAD_FAST            41  'i'
              772  BINARY_SUBSCR    
              773  LOAD_FAST            14  'vi'
              776  LOAD_CONST               1
              779  BINARY_SUBSCR    
              780  LOAD_FAST            42  'lp2'
              783  BINARY_SUBSCR    

 L.1177       784  LOAD_FAST            30  'q0'
              787  LOAD_FAST            31  'xm1'
              790  LOAD_FAST            32  'xm2'
              793  LOAD_FAST             4  'nr'
              796  LOAD_FAST             7  'r'
              799  LOAD_FAST             8  'dr'
              802  LOAD_FAST             9  'r2'
              805  LOAD_FAST            10  'dl'
              808  LOAD_FAST            47  'ruse'
              811  CALL_FUNCTION_20     20  None
              814  POP_TOP          

 L.1178       815  LOAD_GLOBAL          14  'print'
              818  LOAD_FAST            19  'nl'
              821  LOAD_FAST            41  'i'
              824  BINARY_SUBSCR    
              825  LOAD_FAST            21  'ev'
              828  LOAD_FAST            41  'i'
              831  BINARY_SUBSCR    
              832  CALL_FUNCTION_2       2  None
              835  POP_TOP          

 L.1179       836  LOAD_FAST            16  'xntot'
              839  LOAD_FAST            22  'occ'
              842  LOAD_FAST            41  'i'
              845  BINARY_SUBSCR    
              846  INPLACE_ADD      
              847  STORE_FAST           16  'xntot'

 L.1180       850  LOAD_FAST            42  'lp2'
              853  LOAD_CONST               1
              856  COMPARE_OP            3  !=
              859  POP_JUMP_IF_FALSE   333  'to 333'

 L.1181       862  SETUP_LOOP           53  'to 918'
              865  LOAD_GLOBAL          13  'range'
              868  LOAD_CONST               1
              871  LOAD_FAST             4  'nr'
              874  LOAD_CONST               1
              877  BINARY_ADD       
              878  CALL_FUNCTION_2       2  None
              881  GET_ITER         
              882  FOR_ITER             32  'to 917'
              885  STORE_FAST           44  'j'

 L.1182       888  LOAD_FAST            14  'vi'
              891  LOAD_FAST            44  'j'
              894  BINARY_SUBSCR    
              895  LOAD_FAST            42  'lp2'
              898  BINARY_SUBSCR    
              899  LOAD_FAST            14  'vi'
              902  LOAD_FAST            44  'j'
              905  BINARY_SUBSCR    
              906  LOAD_FAST            42  'lp2'
              909  LOAD_CONST               1
              912  BINARY_SUBTRACT  
              913  STORE_SUBSCR     
              914  JUMP_BACK           882  'to 882'
              917  POP_BLOCK        
            918_0  COME_FROM           862  '862'

 L.1183       918  BREAK_LOOP       
              919  JUMP_BACK           333  'to 333'
              922  JUMP_BACK           333  'to 333'
              925  POP_BLOCK        
            926_0  COME_FROM           313  '313'

 L.1185       926  LOAD_GLOBAL          14  'print'
              929  LOAD_CONST               'everything is pseudized'
              932  CALL_FUNCTION_1       1  None
              935  POP_TOP          

 L.1186       936  SETUP_LOOP          187  'to 1126'
              939  LOAD_GLOBAL          13  'range'
              942  LOAD_FAST            38  'np'
              945  LOAD_FAST            17  'nel'
              948  LOAD_CONST               1
              951  BINARY_ADD       
              952  CALL_FUNCTION_2       2  None
              955  GET_ITER         
              956  FOR_ITER            166  'to 1125'
              959  STORE_FAST           41  'i'

 L.1187       962  LOAD_CONST               1
              965  LOAD_FAST            41  'i'
              968  BINARY_ADD       
              969  LOAD_FAST            38  'np'
              972  BINARY_SUBTRACT  
              973  STORE_FAST           49  'inew'

 L.1188       976  LOAD_FAST            18  'no'
              979  LOAD_FAST            41  'i'
              982  BINARY_SUBSCR    
              983  LOAD_FAST            18  'no'
              986  LOAD_FAST            49  'inew'
              989  STORE_SUBSCR     

 L.1189       990  LOAD_FAST            19  'nl'
              993  LOAD_FAST            41  'i'
              996  BINARY_SUBSCR    
              997  LOAD_FAST            19  'nl'
             1000  LOAD_FAST            49  'inew'
             1003  STORE_SUBSCR     

 L.1190      1004  LOAD_FAST            27  'nm'
             1007  LOAD_FAST            41  'i'
             1010  BINARY_SUBSCR    
             1011  LOAD_FAST            27  'nm'
             1014  LOAD_FAST            49  'inew'
             1017  STORE_SUBSCR     

 L.1191      1018  LOAD_FAST            20  'xnj'
             1021  LOAD_FAST            41  'i'
             1024  BINARY_SUBSCR    
             1025  LOAD_FAST            20  'xnj'
             1028  LOAD_FAST            49  'inew'
             1031  STORE_SUBSCR     

 L.1192      1032  LOAD_CONST               1
             1035  LOAD_FAST            23  'iss'
             1038  LOAD_FAST            49  'inew'
             1041  STORE_SUBSCR     

 L.1193      1042  LOAD_FAST            21  'ev'
             1045  LOAD_FAST            41  'i'
             1048  BINARY_SUBSCR    
             1049  LOAD_FAST            21  'ev'
             1052  LOAD_FAST            49  'inew'
             1055  STORE_SUBSCR     

 L.1194      1056  LOAD_FAST            22  'occ'
             1059  LOAD_FAST            41  'i'
             1062  BINARY_SUBSCR    
             1063  LOAD_FAST            22  'occ'
             1066  LOAD_FAST            49  'inew'
             1069  STORE_SUBSCR     

 L.1195      1070  SETUP_LOOP           49  'to 1122'
             1073  LOAD_GLOBAL          13  'range'
             1076  LOAD_CONST               1
             1079  LOAD_FAST             4  'nr'
             1082  LOAD_CONST               1
             1085  BINARY_ADD       
             1086  CALL_FUNCTION_2       2  None
             1089  GET_ITER         
             1090  FOR_ITER             28  'to 1121'
             1093  STORE_FAST           44  'j'

 L.1196      1096  LOAD_FAST            11  'phe'
             1099  LOAD_FAST            44  'j'
             1102  BINARY_SUBSCR    
             1103  LOAD_FAST            41  'i'
             1106  BINARY_SUBSCR    
             1107  LOAD_FAST            11  'phe'
             1110  LOAD_FAST            44  'j'
             1113  BINARY_SUBSCR    
             1114  LOAD_FAST            49  'inew'
             1117  STORE_SUBSCR     
             1118  JUMP_BACK          1090  'to 1090'
             1121  POP_BLOCK        
           1122_0  COME_FROM          1070  '1070'
             1122  JUMP_BACK           956  'to 956'
             1125  POP_BLOCK        
           1126_0  COME_FROM           936  '936'

 L.1198      1126  LOAD_FAST            17  'nel'
             1129  LOAD_CONST               1
             1132  LOAD_FAST            38  'np'
             1135  BINARY_SUBTRACT  
             1136  INPLACE_ADD      
             1137  STORE_FAST           17  'nel'

 L.1199      1140  SETUP_LOOP           86  'to 1229'
             1143  LOAD_GLOBAL          13  'range'
             1146  LOAD_CONST               0
             1149  LOAD_CONST               8
             1152  CALL_FUNCTION_2       2  None
             1155  GET_ITER         
             1156  FOR_ITER             69  'to 1228'
             1159  STORE_FAST           41  'i'

 L.1200      1162  LOAD_FAST            41  'i'
             1165  STORE_FAST           50  'xi'

 L.1201      1168  SETUP_LOOP           54  'to 1225'
             1171  LOAD_GLOBAL          13  'range'
             1174  LOAD_CONST               1
             1177  LOAD_FAST             4  'nr'
             1180  LOAD_CONST               1
             1183  BINARY_ADD       
             1184  CALL_FUNCTION_2       2  None
             1187  GET_ITER         
             1188  FOR_ITER             33  'to 1224'
             1191  STORE_FAST           51  'k'

 L.1202      1194  LOAD_GLOBAL          19  'pow'
             1197  LOAD_FAST             7  'r'
             1200  LOAD_FAST            51  'k'
             1203  BINARY_SUBSCR    
             1204  LOAD_FAST            50  'xi'
             1207  CALL_FUNCTION_2       2  None
             1210  LOAD_FAST            33  'rpower'
             1213  LOAD_FAST            51  'k'
             1216  BINARY_SUBSCR    
             1217  LOAD_FAST            41  'i'
             1220  STORE_SUBSCR     
             1221  JUMP_BACK          1188  'to 1188'
             1224  POP_BLOCK        
           1225_0  COME_FROM          1168  '1168'
             1225  JUMP_BACK          1156  'to 1156'
             1228  POP_BLOCK        
           1229_0  COME_FROM          1140  '1140'

 L.1204      1229  LOAD_GLOBAL          14  'print'
             1232  LOAD_CONST               'everything is scaled down...ready for unscreening'
             1235  CALL_FUNCTION_1       1  None
             1238  POP_TOP          

 L.1205      1239  LOAD_CONST               100.0
             1242  STORE_FAST           52  'xnum'

 L.1206      1245  LOAD_CONST               1.0
             1248  STORE_FAST           53  'ratio'

 L.1207      1251  LOAD_GLOBAL          20  'getpot'
             1254  LOAD_FAST             0  'etot'
             1257  LOAD_FAST             1  'nst'
             1260  LOAD_FAST             2  'rel'
             1263  LOAD_FAST             3  'alfa'
             1266  LOAD_FAST            10  'dl'
             1269  LOAD_FAST             4  'nr'
             1272  LOAD_FAST             8  'dr'
             1275  LOAD_FAST             7  'r'
             1278  LOAD_FAST             9  'r2'

 L.1208      1281  LOAD_FAST            16  'xntot'
             1284  LOAD_FAST            11  'phe'
             1287  LOAD_FAST            53  'ratio'
             1290  LOAD_FAST            12  'orb'
             1293  LOAD_FAST            22  'occ'
             1296  LOAD_FAST            23  'iss'

 L.1209      1299  LOAD_FAST            17  'nel'
             1302  LOAD_FAST            19  'nl'
             1305  LOAD_FAST            27  'nm'
             1308  LOAD_FAST            18  'no'
             1311  LOAD_FAST            20  'xnj'
             1314  LOAD_FAST            33  'rpower'
             1317  LOAD_FAST            52  'xnum'
             1320  LOAD_FAST            35  'etot2'
             1323  LOAD_FAST            25  'iuflag'
             1326  CALL_FUNCTION_24     24  None
             1329  POP_TOP          

 L.1210      1330  LOAD_GLOBAL          14  'print'
             1333  LOAD_CONST               'screening effects in pseudo atom computed...'
             1336  CALL_FUNCTION_1       1  None
             1339  POP_TOP          

 L.1211      1340  SETUP_LOOP          154  'to 1497'
             1343  LOAD_GLOBAL          13  'range'
             1346  LOAD_CONST               1
             1349  LOAD_FAST            17  'nel'
             1352  LOAD_CONST               1
             1355  BINARY_ADD       
             1356  CALL_FUNCTION_2       2  None
             1359  GET_ITER         
             1360  FOR_ITER            133  'to 1496'
             1363  STORE_FAST           51  'k'

 L.1212      1366  LOAD_FAST            19  'nl'
             1369  LOAD_FAST            51  'k'
             1372  BINARY_SUBSCR    
             1373  LOAD_FAST            19  'nl'
             1376  LOAD_FAST            51  'k'
             1379  BINARY_SUBSCR    
             1380  BINARY_ADD       
             1381  LOAD_CONST               1
             1384  BINARY_ADD       
             1385  STORE_FAST           42  'lp2'

 L.1213      1388  SETUP_LOOP          102  'to 1493'
             1391  LOAD_GLOBAL          13  'range'
             1394  LOAD_CONST               1
             1397  LOAD_FAST             4  'nr'
             1400  LOAD_CONST               1
             1403  BINARY_ADD       
             1404  CALL_FUNCTION_2       2  None
             1407  GET_ITER         
             1408  FOR_ITER             81  'to 1492'
             1411  STORE_FAST           44  'j'

 L.1214      1414  LOAD_FAST            14  'vi'
             1417  LOAD_FAST            44  'j'
             1420  BINARY_SUBSCR    
             1421  LOAD_FAST            42  'lp2'
             1424  DUP_TOPX_2            2  None
             1427  BINARY_SUBSCR    
             1428  LOAD_FAST            12  'orb'
             1431  LOAD_FAST            44  'j'
             1434  BINARY_SUBSCR    
             1435  LOAD_FAST            51  'k'
             1438  BINARY_SUBSCR    
             1439  INPLACE_SUBTRACT 
             1440  ROT_THREE        
             1441  STORE_SUBSCR     

 L.1215      1442  LOAD_FAST            42  'lp2'
             1445  LOAD_CONST               1
             1448  COMPARE_OP            4  >
             1451  POP_JUMP_IF_FALSE  1408  'to 1408'

 L.1216      1454  LOAD_FAST            14  'vi'
             1457  LOAD_FAST            44  'j'
             1460  BINARY_SUBSCR    
             1461  LOAD_FAST            42  'lp2'
             1464  LOAD_CONST               1
             1467  BINARY_SUBTRACT  
             1468  DUP_TOPX_2            2  None
             1471  BINARY_SUBSCR    
             1472  LOAD_FAST            12  'orb'
             1475  LOAD_FAST            44  'j'
             1478  BINARY_SUBSCR    
             1479  LOAD_FAST            51  'k'
             1482  BINARY_SUBSCR    
             1483  INPLACE_SUBTRACT 
             1484  ROT_THREE        
             1485  STORE_SUBSCR     
             1486  JUMP_BACK          1408  'to 1408'
             1489  JUMP_BACK          1408  'to 1408'
             1492  POP_BLOCK        
           1493_0  COME_FROM          1388  '1388'
             1493  JUMP_BACK          1360  'to 1360'
             1496  POP_BLOCK        
           1497_0  COME_FROM          1340  '1340'

 L.1218      1497  LOAD_GLOBAL          14  'print'
             1500  LOAD_CONST               'we got past the unscreening...'
             1503  CALL_FUNCTION_1       1  None
             1506  POP_TOP          

 L.1219      1507  SETUP_LOOP          323  'to 1833'
             1510  LOAD_GLOBAL          13  'range'
             1513  LOAD_CONST               1
             1516  LOAD_FAST             4  'nr'
             1519  LOAD_CONST               1
             1522  BINARY_ADD       
             1523  CALL_FUNCTION_2       2  None
             1526  GET_ITER         
             1527  FOR_ITER            302  'to 1832'
             1530  STORE_FAST           44  'j'

 L.1220      1533  LOAD_FAST            14  'vi'
             1536  LOAD_FAST            44  'j'
             1539  BINARY_SUBSCR    
             1540  LOAD_CONST               2
             1543  BINARY_SUBSCR    
             1544  LOAD_CONST               2.0
             1547  LOAD_FAST            14  'vi'
             1550  LOAD_FAST            44  'j'
             1553  BINARY_SUBSCR    
             1554  LOAD_CONST               3
             1557  BINARY_SUBSCR    
             1558  BINARY_MULTIPLY  
             1559  BINARY_ADD       
             1560  LOAD_CONST               3.0
             1563  BINARY_TRUE_DIVIDE
             1564  STORE_FAST           54  'vl'

 L.1221      1567  LOAD_CONST               2.0
             1570  LOAD_FAST            14  'vi'
             1573  LOAD_FAST            44  'j'
             1576  BINARY_SUBSCR    
             1577  LOAD_CONST               3
             1580  BINARY_SUBSCR    
             1581  LOAD_FAST            14  'vi'
             1584  LOAD_FAST            44  'j'
             1587  BINARY_SUBSCR    
             1588  LOAD_CONST               2
             1591  BINARY_SUBSCR    
             1592  BINARY_SUBTRACT  
             1593  BINARY_MULTIPLY  
             1594  LOAD_CONST               3.0
             1597  BINARY_TRUE_DIVIDE
             1598  STORE_FAST           55  'vso'

 L.1222      1601  LOAD_FAST            55  'vso'
             1604  LOAD_FAST            14  'vi'
             1607  LOAD_FAST            44  'j'
             1610  BINARY_SUBSCR    
             1611  LOAD_CONST               2
             1614  STORE_SUBSCR     

 L.1223      1615  LOAD_FAST            54  'vl'
             1618  LOAD_FAST            14  'vi'
             1621  LOAD_FAST            44  'j'
             1624  BINARY_SUBSCR    
             1625  LOAD_CONST               3
             1628  STORE_SUBSCR     

 L.1224      1629  LOAD_CONST               2.0
             1632  LOAD_FAST            14  'vi'
             1635  LOAD_FAST            44  'j'
             1638  BINARY_SUBSCR    
             1639  LOAD_CONST               4
             1642  BINARY_SUBSCR    
             1643  BINARY_MULTIPLY  
             1644  LOAD_CONST               3.0
             1647  LOAD_FAST            14  'vi'
             1650  LOAD_FAST            44  'j'
             1653  BINARY_SUBSCR    
             1654  LOAD_CONST               5
             1657  BINARY_SUBSCR    
             1658  BINARY_MULTIPLY  
             1659  BINARY_ADD       
             1660  LOAD_CONST               5.0
             1663  BINARY_TRUE_DIVIDE
             1664  STORE_FAST           54  'vl'

 L.1225      1667  LOAD_CONST               2.0
             1670  LOAD_FAST            14  'vi'
             1673  LOAD_FAST            44  'j'
             1676  BINARY_SUBSCR    
             1677  LOAD_CONST               5
             1680  BINARY_SUBSCR    
             1681  LOAD_FAST            14  'vi'
             1684  LOAD_FAST            44  'j'
             1687  BINARY_SUBSCR    
             1688  LOAD_CONST               4
             1691  BINARY_SUBSCR    
             1692  BINARY_SUBTRACT  
             1693  BINARY_MULTIPLY  
             1694  LOAD_CONST               5.0
             1697  BINARY_TRUE_DIVIDE
             1698  STORE_FAST           55  'vso'

 L.1226      1701  LOAD_FAST            55  'vso'
             1704  LOAD_FAST            14  'vi'
             1707  LOAD_FAST            44  'j'
             1710  BINARY_SUBSCR    
             1711  LOAD_CONST               4
             1714  STORE_SUBSCR     

 L.1227      1715  LOAD_FAST            54  'vl'
             1718  LOAD_FAST            14  'vi'
             1721  LOAD_FAST            44  'j'
             1724  BINARY_SUBSCR    
             1725  LOAD_CONST               5
             1728  STORE_SUBSCR     

 L.1229      1729  LOAD_CONST               3.0
             1732  LOAD_FAST            14  'vi'
             1735  LOAD_FAST            44  'j'
             1738  BINARY_SUBSCR    
             1739  LOAD_CONST               6
             1742  BINARY_SUBSCR    
             1743  BINARY_MULTIPLY  
             1744  LOAD_CONST               4.0
             1747  LOAD_FAST            14  'vi'
             1750  LOAD_FAST            44  'j'
             1753  BINARY_SUBSCR    
             1754  LOAD_CONST               7
             1757  BINARY_SUBSCR    
             1758  BINARY_MULTIPLY  
             1759  BINARY_ADD       
             1760  LOAD_CONST               7.0
             1763  BINARY_TRUE_DIVIDE
             1764  STORE_FAST           54  'vl'

 L.1230      1767  LOAD_CONST               2.0
             1770  LOAD_FAST            14  'vi'
             1773  LOAD_FAST            44  'j'
             1776  BINARY_SUBSCR    
             1777  LOAD_CONST               7
             1780  BINARY_SUBSCR    
             1781  LOAD_FAST            14  'vi'
             1784  LOAD_FAST            44  'j'
             1787  BINARY_SUBSCR    
             1788  LOAD_CONST               6
             1791  BINARY_SUBSCR    
             1792  BINARY_SUBTRACT  
             1793  BINARY_MULTIPLY  
             1794  LOAD_CONST               7.0
             1797  BINARY_TRUE_DIVIDE
             1798  STORE_FAST           55  'vso'

 L.1231      1801  LOAD_FAST            55  'vso'
             1804  LOAD_FAST            14  'vi'
             1807  LOAD_FAST            44  'j'
             1810  BINARY_SUBSCR    
             1811  LOAD_CONST               6
             1814  STORE_SUBSCR     

 L.1232      1815  LOAD_FAST            54  'vl'
             1818  LOAD_FAST            14  'vi'
             1821  LOAD_FAST            44  'j'
             1824  BINARY_SUBSCR    
             1825  LOAD_CONST               7
             1828  STORE_SUBSCR     
             1829  JUMP_BACK          1527  'to 1527'
             1832  POP_BLOCK        
           1833_0  COME_FROM          1507  '1507'

 L.1234      1833  LOAD_CONST               0.0
             1836  STORE_FAST            2  'rel'

 L.1235      1839  LOAD_GLOBAL          14  'print'
             1842  LOAD_CONST               'we got past the spin-orbit jazz'
             1845  CALL_FUNCTION_1       1  None
             1848  POP_TOP          

 L.1236      1849  LOAD_GLOBAL          21  'abs'
             1852  LOAD_FAST            14  'vi'
             1855  LOAD_FAST             4  'nr'
             1858  LOAD_CONST               2
             1861  BINARY_SUBTRACT  
             1862  BINARY_SUBSCR    
             1863  LOAD_CONST               1
             1866  BINARY_SUBSCR    
             1867  LOAD_FAST             7  'r'
             1870  LOAD_FAST             4  'nr'
             1873  LOAD_CONST               2
             1876  BINARY_SUBTRACT  
             1877  BINARY_SUBSCR    
             1878  BINARY_MULTIPLY  
             1879  CALL_FUNCTION_1       1  None
             1882  LOAD_CONST               0.5
             1885  BINARY_ADD       
             1886  STORE_FAST           56  'izuse'

 L.1237      1889  LOAD_FAST            56  'izuse'
             1892  STORE_FAST           57  'zuse'

 L.1240      1895  SETUP_LOOP          184  'to 2082'
             1898  LOAD_GLOBAL          13  'range'
             1901  LOAD_CONST               1
             1904  LOAD_FAST             4  'nr'
             1907  LOAD_CONST               1
             1910  BINARY_ADD       
             1911  CALL_FUNCTION_2       2  None
             1914  GET_ITER         
             1915  FOR_ITER            163  'to 2081'
             1918  STORE_FAST           51  'k'

 L.1241      1921  LOAD_FAST             7  'r'
             1924  LOAD_FAST            51  'k'
             1927  BINARY_SUBSCR    
             1928  LOAD_FAST            40  'rnorm'
             1931  COMPARE_OP            4  >
             1934  POP_JUMP_IF_FALSE  1915  'to 1915'

 L.1242      1937  LOAD_FAST            57  'zuse'
             1940  UNARY_NEGATIVE   
             1941  LOAD_FAST             7  'r'
             1944  LOAD_FAST            51  'k'
             1947  BINARY_SUBSCR    
             1948  BINARY_TRUE_DIVIDE
             1949  LOAD_FAST            39  'corpol'
             1952  LOAD_CONST               2.0
             1955  LOAD_GLOBAL          19  'pow'
             1958  LOAD_FAST             7  'r'
             1961  LOAD_FAST            51  'k'
             1964  BINARY_SUBSCR    
             1965  LOAD_CONST               4.0
             1968  CALL_FUNCTION_2       2  None
             1971  BINARY_MULTIPLY  
             1972  BINARY_TRUE_DIVIDE
             1973  BINARY_SUBTRACT  
             1974  STORE_FAST           58  'videal'

 L.1243      1977  LOAD_FAST            58  'videal'
             1980  LOAD_FAST            14  'vi'
             1983  LOAD_FAST            51  'k'
             1986  BINARY_SUBSCR    
             1987  LOAD_CONST               1
             1990  STORE_SUBSCR     

 L.1244      1991  LOAD_FAST            58  'videal'
             1994  LOAD_FAST            14  'vi'
             1997  LOAD_FAST            51  'k'
             2000  BINARY_SUBSCR    
             2001  LOAD_CONST               3
             2004  STORE_SUBSCR     

 L.1245      2005  LOAD_FAST            58  'videal'
             2008  LOAD_FAST            14  'vi'
             2011  LOAD_FAST            51  'k'
             2014  BINARY_SUBSCR    
             2015  LOAD_CONST               5
             2018  STORE_SUBSCR     

 L.1246      2019  LOAD_FAST            58  'videal'
             2022  LOAD_FAST            14  'vi'
             2025  LOAD_FAST            51  'k'
             2028  BINARY_SUBSCR    
             2029  LOAD_CONST               7
             2032  STORE_SUBSCR     

 L.1247      2033  LOAD_CONST               0.0
             2036  LOAD_FAST            14  'vi'
             2039  LOAD_FAST            51  'k'
             2042  BINARY_SUBSCR    
             2043  LOAD_CONST               2
             2046  STORE_SUBSCR     

 L.1248      2047  LOAD_CONST               0.0
             2050  LOAD_FAST            14  'vi'
             2053  LOAD_FAST            51  'k'
             2056  BINARY_SUBSCR    
             2057  LOAD_CONST               4
             2060  STORE_SUBSCR     

 L.1249      2061  LOAD_CONST               0.0
             2064  LOAD_FAST            14  'vi'
             2067  LOAD_FAST            51  'k'
             2070  BINARY_SUBSCR    
             2071  LOAD_CONST               6
             2074  STORE_SUBSCR     
             2075  JUMP_BACK          1915  'to 1915'
             2078  JUMP_BACK          1915  'to 1915'
             2081  POP_BLOCK        
           2082_0  COME_FROM          1895  '1895'

 L.1251      2082  LOAD_GLOBAL          14  'print'
             2085  LOAD_CONST               'we got to the end'
             2088  CALL_FUNCTION_1       1  None
             2091  POP_TOP          

 L.1252      2092  LOAD_CONST               None
             2095  RETURN_END_IF    
           2096_0  COME_FROM           310  '310'
             2096  POP_BLOCK        
           2097_0  COME_FROM           304  '304'
             2097  LOAD_CONST               None
             2100  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 2096


def parabreg(f, fp, fpp, rf, vf):
    f = vf[2]
    r21 = rf[2] - rf[1]
    r32 = rf[3] - rf[2]
    v21 = vf[2] - vf[1]
    v32 = vf[3] - vf[2]
    fp = (v21 + v32) / (r21 + r32)
    fpp = (v32 / r32 - v21 / r21) / ((r21 + r32) / 2.0)
    return (f, fp, fpp, rf, vf)


def hb(x, factor):
    if x > 3.0:
        hb = 0
    if x <= 3.0:
        hb = pow(0.01, pow(sinh(x / factor) / 1.1752, 2.0))
    return hb


def fitx0(i, orb, rcut, njrc, e, l, xj, n, jrt, xideal, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel, factor):
    """fitx0 subroutine"""
    vl = -1000000.0
    vh = 1000000.0
    dummy = nn = ief = xactual = None
    while True:
        idoflag = 2
        ns = 1
        xkappa = -1.0
        i, orb, l, ns, idoflag, v, zeff, dummy, rel, nr, r, r2, dl, q0, xm1, xm2, njrc = setqmm(i, orb, l, ns, idoflag, v, zeff, dummy, rel, nr, r, r2, dl, q0, xm1, xm2, njrc)
        e, l, xkappa, n, nn, jrt, ief, xactual, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel = integ(e, l, xkappa, n, nn, jrt, ief, xactual, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
        if int(nn):
            vl = v[1]
            xla = 1.0
        else:
            if xactual > xideal:
                vh = v[1]
            else:
                vl = v[1]
            xerror = xideal - xactual
            if abs(xerror) < 1e-09:
                return
            dxdla = 0.0
            for ii in range(1, jrt + 1):
                dxdla += dr[ii] * phi[ii] * phi[ii] * hb(r[ii] / rcut, factor)

            dxdla = 2.0 * dxdla / (phi[jrt] * phi[jrt])
            xla = xerror / dxdla
            vmaybe = v[1] + xla
            if vmaybe > vh or vmaybe < vl:
                xla = (vl + vh) / (2.0 - v[1])
            for ii in range(1, jrt - 1 + 1):
                v[ii] += xla * hb(r[ii] / rcut, factor)

    return


def pseudize(i, orb, ev, l, xj, n, njrc, zeff, v, q0, xm1, xm2, nr, rmin, rmax, r, dr, r2, dl, rel, phi, rcut=None, factor=None):
    """pseudize subroutine"""
    nn = ief = x0 = x00 = xm = xp = fp = fpp = psi = psip = psipp = None
    xdummy = [None] * len(phi)
    rf = vf = [None] * len(njrc) - 1
    lp = l + 1
    xkappa = -1.0
    istop = nr
    while ev > q0[istop]:
        istop -= 1

    ev, l, xkappa, n, nn, istop, ief, xdummy, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel = integ(ev, l, xkappa, n, nn, istop, ief, xdummy, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
    if rcut is None or factor is None:
        rcut, factor = get_input('Please enter the cutoff radius, and factor: ').split()
    if rcut < 0.0:
        xnodefrac = -rcut
        j = istop
        while phi[(j - 1)] / phi[j] <= 1.0:
            j -= 1

        if n > l + 1:
            k = j
        while phi[(k - 1)] / phi[k] <= 1.0:
            k -= 1

    else:
        k = 1
    rcut = r[k] + xnodefrac * (r[j] - r[k])
    jrc = 1.0 + float(nr - 1) * log(rcut / rmin) / log(rmax / rmin)
    rcut = r[jrc]
    rtest = 2.0 * rcut
    jrt = 1.0 + float(nr - 1) * log(rtest / rmin) / log(rmax / rmin)
    njrc[lp] = jrt
    rtest = r[jrt]
    print('RCUTOFF = %8.4f  JRC = %5i' % (rcut, jrc))
    print('RTEST   = %8.4f  JRT = %5i' % (rtest, jrt))
    integ(ev, l, xkappa, n, nn, jrt, ief, x00, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
    for ii in range(len(phi)):
        phi[ii] /= phi[jrt]

    xn00 = 0.0
    for ii in range(1, jrt - 1 + 1):
        xn00 += dr[ii] * phi[ii] * phi[ii]

    xn00 += dr[jrt] * phi[jrt] * phi[jrt] / 2.0
    de = 0.0001
    ee = ev + de / 2.0
    integ(ee, l, xkappa, n, nn, jrt, ief, xp, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
    ee = ev - de / 2.0
    integ(ee, l, xkappa, n, nn, jrt, ief, xm, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, rel)
    c00 = (xm - xp) / (2.0 * de)
    print(c00, x00)
    print(xn00)
    ruse = 0.0
    v0 = v[jrc]
    dvdl = (8.0 * (v[(jrc + 1)] - v[(jrc - 1)]) - (v[(jrc + 2)] - v[(jrc - 2)])) / (12.0 * dl)
    ddvdll = (16.0 * (v[(jrc + 1)] + v[(jrc - 1)]) - 30.0 * v[jrc] - v[(jrc + 2)] - v[(jrc - 2)]) / (12.0 * dl * dl)
    dldr = 1.0 / r[jrc]
    ddldrr = -1.0 / r2[jrc]
    v1 = dvdl * dldr
    v2 = dvdl * ddldrr + ddvdll * dldr * dldr
    b4 = (v2 * rcut - v1) / (8.0 * pow(rcut, 3.0))
    b2 = (v1 - 4.0 * b4 * pow(rcut, 3.0)) / (2.0 * rcut)
    b0 = v0 - b4 * pow(rcut, 4.0) - b2 * pow(rcut, 2.0)
    for ii in range(1, jrc + 1):
        rr = r[ii]
        v[ii] = b0 + b2 * pow(rr, 2.0) + b4 * pow(rr, 4.0)
        fitx0(i, orb, rcut, njrc, ev, l, xj, lp, jrt, x00, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, ruse, factor)

    phi0 = deepcopy(phi)
    vraw = deepcopy(v)
    xi0 = 0.0
    xi1 = 0.0
    xi2 = 0.0
    for ii in range(1, jrt + 1):
        f = hb(r[ii] / rcut, factor)
        ph2 = dr[ii] * phi0[ii] * phi0[ii]
        xi0 = xi0 + ph2
        if ii <= jrt:
            xi1 += ph2 * f
            xi2 += ph2 * f * f

    ph2 = phi0[jrt] * phi0[jrt]
    xi0 /= ph2
    xi1 /= ph2
    xi2 /= ph2
    quant = xi1 * xi1 + xi2 * (c00 - xi0)
    if quant > 0.0:
        deltal = (sqrt(xi1 * xi1 + xi2 * (c00 - xi0)) - xi1) / xi2
    else:
        deltal = (c00 - xi0) / (2.0 * xi1)
    print('DELTAL = %11.8f' % deltal)
    yl = [
     None] * len(phi0)
    while True:
        for ii in range(1, jrt):
            yl[ii] = phi0[ii] * hb(r[ii] / rcut, factor)
            phi[ii] = phi0[ii] + deltal * yl[ii]
            if phi[ii] < 0.0:
                print('Big trouble# # #  cross axis# # # ')
                sys.exit(1)

        for ii in range(1, jrt - 1 + 1):
            if phi[ii] == 0.0 or yl[ii] == 0.0:
                break
            jj = ii
            if ii == 1:
                jj = 2
            for j in range(jj - 1, jj + 1 + 1):
                rf[2 + j - jj] = r[j]
                vf[2 + j - jj] = hb(r[j] / rcut, factor)

            f, fp, fpp, rf, vf = parabreg(f, fp, fpp, rf, vf)
            for j in range(jj - 1, jj + 1):
                vf[2 + j - jj] = phi0[j]

            psi, psip, psipp, rf, vf = parabreg(psi, psip, psipp, rf, vf)
            v[ii] = vraw[ii] + (1.0 - phi0[ii] / phi[ii]) * (2.0 * psip / psi * fp / f + fpp / f) / 2.0
            fitx0(i, orb, rcut, njrc, ev, l, xj, lp, jrt, x00, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, ruse, factor)
            integ(ev, l, xkappa, n, nn, jrt, ief, x0, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, ruse)

        for ii in range(1, jrt + 1):
            phi[ii] = phi[ii] / phi[jrt]

        xn0 = 0.0
        for ii in range(1, jrt - 1 + 1):
            xn0 = xn0 + dr[ii] * phi[ii] * phi[ii]

        xn0 = xn0 + dr[jrt] * phi[jrt] * phi[jrt] / 2.0
        de = 0.0001
        ee = ev + de / 2.0
        integ(ee, l, xkappa, n, nn, jrt, ief, xp, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, ruse)
        ee = ev - de / 2.0
        integ(ee, l, xkappa, n, nn, jrt, ief, xm, phi, zeff, v, q0, xm1, xm2, nr, r, dr, r2, dl, ruse)
        c0 = (xm - xp) / (2.0 * de)
        print(c0, x0)
        print(xn0)
        if abs(c0 - c00) > 1e-09:
            dqddel = 2.0 * (xi1 + deltal * xi2)
            deltal = deltal + (c00 - c0) / dqddel
        else:
            break

    print(c0, x0)
    print('NCPP achieved # # # ')
    return


def fourier(nr, r, dr, r2, vi, output='stdout'):
    """fourier subroutine"""
    a = [
     None] * len(r)
    v1 = [None] * len(r)
    for l in range(0, 4):
        lp2 = l + l + 1
        dl = log(r[2] / r[1])
        dl1 = 12.0 * dl
        for i in range(1, nr + 1):
            a[i] = r[i] * vi[i][lp2]

        for i in range(3, nr - 2 + 1):
            al = (-(a[(i + 2)] - a[(i - 2)]) + 8.0 * (a[(i + 1)] - a[(i - 1)])) / dl1
            ar = al / r[i]
            v1[i] = ar

        if output == 'stdout':
            for ii in range(1, 201):
                q = ii / 10.0
                vq = 0.0
                for i in range(3, nr - 2 + 1):
                    vq = vq + dr[i] * cos(q * r[i]) * v1[i]

                print(('{} {}').format(q, vq))

        else:
            try:
                if not os.path.exists(os.path.dirname(output)):
                    os.makedirs(os.path.dirname(output))
                with open(output, 'rw') as (fl):
                    for ii in range(1, 201):
                        q = ii / 10.0
                        vq = 0.0
                        for i in range(3, nr - 2 + 1):
                            vq = vq + dr[i] * cos(q * r[i]) * v1[i]

                        fl.write(('{} {}\n').format(q, vq))

            except IOError:
                assert IOError("Could not write file '%s'\n" % output)

    return


def getillls(pin):
    """getills subroutine"""
    si = fa = [None] * 33
    fa[0] = 1.0
    si[0] = 1.0
    for i in range(1, 32):
        fa[i] = float[i] * fa[(i - 1)]
        si[i] = -si[(i - 1)]

    for l in range(8):
        for m in range(8):
            for n in range(m + l, 0, -2):
                xi = 0.0
                xf = 2.0 / pow(2.0, n + l + m)
                nn = (n + 1) / 2.0
                mm = (m + 1) / 2.0
                ll = (l + 1) / 2.0
                for ia in range(nn, n):
                    af = si[ia] * fa[(ia + ia)] / fa[ia] / fa[(n - ia)] / fa[(ia + ia - n)]
                    for ib in range(ll, l):
                        bf = si[ib] * fa[(ib + ib)] / fa[ib] / fa[(l - ib)] / fa[(ib + ib - l)]
                        for ic in range(mm, m):
                            xcf = si[ic] * fa[(ic + ic)] / fa[ic] / fa[(m - ic)] / fa[(ic + ic - m)]
                            xi = xi + xf * af * bf * xcf / (ia * 2 + ib * 2 + ic * 2 - n - l - m + 1)

                pin[l][m][n] = xi

    return (
     fa, si)


def hfdisk(iu, ir, etot, nst, rel, nr, rmin, rmax, r, rho, zorig, xntot, ixflag, nel, no, nl, xnj, iss, ev, ek, occ, njrc, vi, phe, orb, input_stream='stdin'):
    """    """
    if input_stream == 'stdin':
        while True:
            filename = get_input('Please enter full filename: ')
            if os.path.isfile(filename):
                break

    else:
        filename = input_stream.next().strip().split('!')[0]
    try:
        with open(filename, 'rw') as (f):
            for i in range(0, nr):
                r[i] = pow(rmin * (rmax / rmin), i / float(nr))

            for i in range(0, nr):
                rho[i] = 0.0
                for ii in range(0, nel):
                    rho[i] = rho[i] + occ[ii] * pow(phe[i][ii], 2)

            iprint = 0
            f.write('RELA\nRELAT. ATOMIC CHARGE DENSITY\n%i\n' % iprint)
            f.write('%15.8d%15.8d%5i%5.2f\n' % (rmin, rmax, nr, zorig))
            for j in range(0, nr + 1):
                file.write('%15.11f\n' % rho[j])

    except IOError:
        assert IOError

    return (iu, ir, etot, nst, rel, nr, rmin, rmax, r, rho, zorig)


def exchcorr(nst, rel, rr, rh1, rh2, ex=0.0, ec=0.0, ux1=0.0, ux2=0.0, uc1=0.0, uc2=0.0):
    """
    Description
    -----------
    Exchange correlation routine, via Ceperley-Alder, as parametrized by
    Perdew and Zunger, Phys. Rev. B 23, 5048.  we use their interpolation
    between the unpolarized and polarized gas for the correlation part.
    
    Parameters
    ----------
    nst : float, int or bool
        Will cause spin averaging if polarisation is equal to 1
        
    rel : int
        Flag to signify whether to account for relativistic effects.
        
    rr : 
    
    rh1 : 
    
    rh2 :
    
    ex : 
    
    ec :
    
    ux1 :
    
    ux2 :
    
    uc1 :
    
    uc2 :
    
        
    """
    trd = 0.3333333333333333
    ft = 1.3333333333333333
    rh = rh1 + rh2
    if float(nst) == 1.0:
        rh1 = rh / 2.0
        rh2 = rh / 2.0
    fp = 4.0 * pi
    xn1 = rh1 / (rr * fp)
    xn2 = rh2 / (rr * fp)
    xn = xn1 + xn2
    if nst == 3 or xn < 1e-08:
        ex = ec = ux1 = ux2 = uc1 = uc2 = 0.0
    else:
        rs = pow(3.0 / (fp * xn), trd)
        zeta = (xn1 - xn2) / xn
    exchfactor = -0.930525546
    if xn1 == 0.0:
        fe1 = 1.0
        fu1 = 1.0
        ex1 = 0.0
        ux1 = 0.0
    else:
        beta = 0.028433756 * pow(xn1, trd)
        b2 = beta * beta
        eta = sqrt(1.0 + b2)
        xl = log(beta + eta)
        fe1 = 1.0 - 1.5 * (pow(beta * eta - xl) / b2, 2.0)
        fu1 = -0.5 + 1.5 * xl / beta / eta
        ex1 = exchfactor * pow(xn1, trd)
        ux1 = 4.0 * ex1 / 3.0
    if xn2 == 0.0:
        fe2 = 1.0
        fu2 = 1.0
        ex2 = 0.0
        ux2 = 0.0
    else:
        beta = 0.028433756 * pow(xn2, trd)
        b2 = beta * beta
        eta = sqrt(1.0 + b2)
        xl = log(beta + eta)
        fe2 = 1.0 - 1.5 * pow((beta * eta - xl) / b2, 2.0)
        fu2 = -0.5 + 1.5 * xl / beta / eta
        ex2 = exchfactor * pow(xn2, trd)
        ux2 = 4.0 * ex2 / 3.0
    if rs > 1.0:
        rootr = sqrt(rs)
        gamma = -0.1423
        beta1 = 1.0529
        beta2 = 0.3334
        denom = 1.0 + beta1 * rootr + beta2 * rs
        ecu = gamma / denom
        ucu = ecu * (1.0 + 1.1666666666666667 * beta1 * rootr + ft * beta2 * rs) / denom
        gamma = -0.0843
        beta1 = 1.3981
        beta2 = 0.2611
        denom = 1.0 + beta1 * rootr + beta2 * rs
        ecp = gamma / denom
        ucp = ecp * (1.0 + 1.1666666666666667 * beta1 * rootr + ft * beta2 * rs) / denom
    else:
        xlr = log(rs)
        rlr = rs * xlr
        au = 0.0311
        bu = -0.048
        cu = 0.002
        du = -0.0116
        ecu = au * xlr + bu + cu * rlr + du * rs
        ucu = au * xlr + (bu - au / 3.0) + 0.6666666666666666 * cu * rlr + (2.0 * du - cu) * rs / 3.0
        ap = 0.01555
        bp = -0.0269
        cp = 0.0007
        dp = -0.0048
        ecp = ap * xlr + bp + cp * rlr + dp * rs
        ucp = ap * xlr + (bp - ap / 3.0) + 0.6666666666666666 * cp * rlr + (2.0 * dp - cp) * rs / 3.0
    if not rel:
        fe1 = fu1 = fe2 = fu2 = 1.0
    denom = pow(2.0, ft) - 2.0
    f = (pow(1.0 + zeta), ft + pow(1.0 - zeta, ft) - 2.0) / denom
    dfdz = ft / denom * (pow(1.0 + zeta), trd) - pow(1.0 - zeta, trd)
    ec = ecu + f * (ecp - ecu)
    uc1 = ucu + f * (ucp - ucu) + (ecp - ecu) * (1.0 - zeta) * dfdz
    uc2 = ucu + f * (ucp - ucu) + (ecp - ecu) * -(1.0 + zeta) * dfdz
    ex = (xn1 * fe1 * ex1 + xn2 * fe2 * ex2) / xn
    ux1 = fu1 * ux1
    ux2 = fu2 * ux2
    uc1 = uc1
    uc2 = uc2
    return (
     nst, rel, rr, rh1, rh2, ex, ec, ux1, ux2, uc1, uc2)


def test():
    """for testing"""
    filename = os.path.join(os.path.expanduser('~'), 'Desktop', 'atorb_Re')
    hartfock(input_stream=filename)


if __name__ == '__main__':
    test()