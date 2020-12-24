# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/max/Workspaces/gsfc/photometry_pipeline/code/reduction/astrom/astrometrydist.py
# Compiled at: 2016-11-15 15:22:29
import numpy, astrometrystats

def distance(obj1, obj2):
    ddec = obj2.dec_rad - obj1.dec_rad
    dra = obj2.ra_rad - obj1.ra_rad
    dist_rad = 2 * numpy.arcsin(numpy.sqrt(numpy.sin(ddec / 2.0) ** 2 + numpy.cos(obj1.dec_rad) * numpy.cos(obj2.dec_rad) * numpy.sin(dra / 2.0) ** 2))
    dist_deg = dist_rad * 180.0 / numpy.pi
    dist_sec = dist_deg * 3600.0
    return dist_sec


def tooclose(glist, minsep=3, quiet=False):
    deleteset = set()
    for i in range(len(glist)):
        for j in range(i + 1, len(glist)):
            if i == j:
                continue
            dist = distance(glist[i], glist[j])
            if dist < minsep:
                if glist[i].mag > glist[j].mag:
                    deleteset.add(i)
                else:
                    deleteset.add(j)

    deletelist = list(deleteset)
    for d in sorted(deletelist, reverse=True):
        del glist[d]
        if quiet == False:
            print 'deleted index ' + str(d)

    return glist


def quickdistance(obj1, obj2, cosdec):
    ddec = obj2.dec - obj1.dec
    dra = obj2.ra - obj1.ra
    if dra > 180:
        dra = 360 - dra
    return 3600 * numpy.sqrt(ddec ** 2 + (cosdec * dra) ** 2)


def posangle(obj1, obj2):
    dra = obj2.ra_rad - obj1.ra_rad
    pa_rad = numpy.arctan2(numpy.cos(obj1.dec_rad) * numpy.tan(obj2.dec_rad) - numpy.sin(obj1.dec_rad) * numpy.cos(dra), numpy.sin(dra))
    pa_deg = pa_rad * 180.0 / numpy.pi
    pa_deg = 90.0 - pa_deg
    while pa_deg > 200:
        pa_deg -= 360.0

    while pa_deg < -160:
        pa_deg += 360.0

    return pa_deg


def imdistance(obj1, obj2):
    return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5


def calcdist(slist, maxrad, minrad, rascale):
    dists = []
    matchids = []
    for i in range(len(slist)):
        d = []
        dj = []
        for j in range(len(slist)):
            if i == j:
                continue
            if abs(slist[i].dec - slist[j].dec) > maxrad:
                continue
            if rascale * abs(slist[i].ra - slist[j].ra) > maxrad:
                continue
            dist = quickdistance(slist[i], slist[j], rascale)
            if dist > minrad and dist < maxrad:
                d.append(dist)
                dj.append(j)

        dists.append(d)
        matchids.append(dj)

    return (dists, matchids)


def distmatch(sexlist, catlist, maxrad=180, minrad=10, reqmatch=3, patolerance=1.2, uncpa=-1, showmatches=0, fastmatch=1, quiet=False):
    if reqmatch < 2:
        print 'Warning: reqmatch >=3 suggested'
    if patolerance <= 0:
        print 'PA tolerance cannot be negative!!!'
        patolerance = abs(patolerance)
    if uncpa < 0:
        uncpa = 720
    declist = []
    for s in sexlist:
        declist.append(s.dec_rad)

    avdec_rad = astrometrystats.median(declist)
    rascale = numpy.cos(avdec_rad)
    sexdists, sexmatchids = calcdist(sexlist, maxrad, minrad, rascale)
    catdists, catmatchids = calcdist(catlist, maxrad, minrad, rascale)
    countgreatmatches = 0
    smatch = []
    cmatch = []
    mpa = []
    offset = []
    offpa = []
    nmatch = []
    primarymatchs = []
    primarymatchc = []
    for si in range(len(sexdists)):
        sexdistarr = sexdists[si]
        sexidarr = sexmatchids[si]
        if len(sexdistarr) < 2:
            continue
        for ci in range(len(catdists)):
            catdistarr = catdists[ci]
            catidarr = catmatchids[ci]
            if len(catdistarr) < 2:
                continue
            match = 0
            smatchin = []
            cmatchin = []
            for sj in range(len(sexdistarr)):
                sexdist = sexdistarr[sj]
                newmatch = 1
                for cj in range(len(catdistarr)):
                    catdist = catdistarr[cj]
                    if abs(sexdist / catdist - 1.0) < 0.05:
                        match += newmatch
                        newmatch = 0
                        smatchin.append(sexmatchids[si][sj])
                        cmatchin.append(catmatchids[ci][cj])

            if match >= reqmatch:
                dpa = []
                for i in range(len(smatchin)):
                    ddpa = posangle(sexlist[si], sexlist[smatchin[i]]) - posangle(catlist[ci], catlist[cmatchin[i]])
                    while ddpa > 200:
                        ddpa -= 360.0

                    while ddpa < -160:
                        ddpa += 360.0

                    dpa.append(ddpa)

                for i in range(len(smatchin) - 1, -1, -1):
                    if abs(dpa[i]) > uncpa:
                        del smatchin[i]
                        del cmatchin[i]
                        del dpa[i]

                if len(smatchin) < 2:
                    continue
                dpamode = astrometrystats.most(dpa, vmin=patolerance * 3, vmax=patolerance * 3)
                for i in range(len(smatchin) - 1, -1, -1):
                    if abs(dpa[i] - dpamode) > patolerance:
                        del smatchin[i]
                        del cmatchin[i]
                        del dpa[i]

                if len(smatchin) < 2:
                    continue
                ndegeneracies = len(smatchin) - len(astrometrystats.unique(smatchin)) + len(cmatchin) - len(astrometrystats.unique(cmatchin))
                mpa.append(dpamode)
                primarymatchs.append(si)
                primarymatchc.append(ci)
                smatch.append(smatchin)
                cmatch.append(cmatchin)
                nmatch.append(len(smatchin) - ndegeneracies)
                if len(smatchin) - ndegeneracies > 6:
                    countgreatmatches += 1

        if countgreatmatches > 16 and fastmatch == 1:
            break

    nmatches = len(smatch)
    if nmatches == 0:
        print 'Found no potential matches of any sort (including pairs).'
        print 'The algorithm is probably not finding enough real stars to solve the field.  Check seeing.'
        return ([], [], [])
    for i in range(len(primarymatchs) - 1, -1, -1):
        if nmatch[i] < reqmatch:
            del mpa[i]
            del primarymatchs[i]
            del primarymatchc[i]
            del smatch[i]
            del cmatch[i]
            del nmatch[i]

    if len(smatch) < 1:
        print 'Found no matching clusters of reqmatch =', reqmatch
        return ([], [], [])
    minmatch = min(nmatch)
    countnotmin = 0
    for n in nmatch:
        if n > minmatch:
            countnotmin += 1

    if len(nmatch) > 16 and countnotmin > 3:
        print 'Too many matches: increasing reqmatch to', reqmatch + 1
        for i in range(len(primarymatchs) - 1, -1, -1):
            if nmatch[i] == minmatch:
                del mpa[i]
                del primarymatchs[i]
                del primarymatchc[i]
                del smatch[i]
                del cmatch[i]
                del nmatch[i]

    nmatches = len(smatch)
    if quiet == False:
        print 'Found', nmatches, 'candidate matches.'
    rejects = 0
    offpa = astrometrystats.most(mpa, vmin=3 * patolerance, vmax=3 * patolerance)
    if len(smatch) > 2:
        for i in range(len(primarymatchs) - 1, -1, -1):
            if abs(mpa[i] - offpa) > patolerance:
                del mpa[i]
                del primarymatchs[i]
                del primarymatchc[i]
                del smatch[i]
                del cmatch[i]
                del nmatch[i]
                rejects += 1

        medpa = astrometrystats.median(mpa)
        stdevpa = astrometrystats.stdev(mpa)
        refinedtolerance = 2.0 * stdevpa
        for i in range(len(primarymatchs) - 1, -1, -1):
            if abs(mpa[i] - offpa) > refinedtolerance:
                del mpa[i]
                del primarymatchs[i]
                del primarymatchc[i]
                del smatch[i]
                del cmatch[i]
                del nmatch[i]
                rejects += 1

    ndistflags = [
     0] * len(primarymatchs)
    for v in range(2):
        if len(primarymatchs) == 0:
            break
        for i in range(len(primarymatchs)):
            for j in range(len(primarymatchs)):
                if i == j:
                    continue
                si = primarymatchs[i]
                ci = primarymatchc[i]
                sj = primarymatchs[j]
                cj = primarymatchc[j]
                sexdistij = distance(sexlist[si], sexlist[sj])
                catdistij = distance(catlist[ci], catlist[cj])
                try:
                    if abs(sexdistij / catdistij - 1.0) > 0.05:
                        ndistflags[i] += 1
                except:
                    pass

        ntestmatches = len(primarymatchs)
        for i in range(ntestmatches - 1, -1, -1):
            if ndistflags[i] == ntestmatches - 1:
                del mpa[i]
                del primarymatchs[i]
                del primarymatchc[i]
                del smatch[i]
                del cmatch[i]
                del nmatch[i]
                rejects += 1

    nmatches = len(primarymatchs)
    if quiet == False:
        print 'Rejected', rejects, 'bad matches.'
        print 'Found', nmatches, 'good matches.'
    if nmatches == 0:
        return ([], [], [])
    pixscalelist = []
    if len(primarymatchs) >= 2:
        for i in range(len(primarymatchs) - 1):
            for j in range(i + 1, len(primarymatchs)):
                si = primarymatchs[i]
                ci = primarymatchc[i]
                sj = primarymatchs[j]
                cj = primarymatchc[j]
                try:
                    pixscalelist.append(distance(catlist[ci], catlist[cj]) / imdistance(sexlist[si], sexlist[sj]))
                except:
                    pass

        pixelscale = astrometrystats.median(pixscalelist)
        pixelscalestd = astrometrystats.stdev(pixscalelist)
        if quiet == False:
            if len(primarymatchs) >= 3:
                print 'Refined pixel scale measurement: %.4f"/pix (+/- %.4f)' % (pixelscale, pixelscalestd)
            else:
                print 'Refined pixel scale measurement: %.4f"/pix' % pixelscale
    for i in range(len(primarymatchs)):
        si = primarymatchs[i]
        ci = primarymatchc[i]
        if quiet == False:
            print '%3i' % si, 'matches', '%3i' % ci, ' (dPA =%7.3f)' % mpa[i],
        if showmatches:
            print
            if len(smatch[i]) < 16:
                print '  ', si, '-->', smatch[i],
                if len(smatch[i]) >= 7:
                    print
                print '  ', ci, '-->', cmatch[i]
            else:
                print '  ', si, '-->', smatch[i][0:10], '+', len(smatch[i]) - 10, 'more'
                print '  ', ci, '-->', cmatch[i][0:10], '+'
            if i + 1 >= 10 and len(primarymatchs) - 10 > 0:
                print len(primarymatchs) - 10, 'additional matches not shown.'
                break
        elif quiet == False:
            print ':', str(len(smatch[i])).strip(), 'rays'

    out = open('matchlines.im.reg', 'w')
    i = -1
    color = 'red'
    out.write('# Region file format: DS9 version 4.0\nglobal color=' + color + ' font="helvetica 10 normal" select=1 highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source\n')
    out.write('image\n')
    for i in range(len(primarymatchs)):
        si = primarymatchs[i]
        for j in range(len(smatch[i])):
            sj = smatch[i][j]
            out.write('line(%.3f,%.3f,%.3f,%.3f) # line=0 0\n' % (sexlist[si].x, sexlist[si].y, sexlist[sj].x, sexlist[sj].y))

    out.close()
    out = open('matchlines.wcs.reg', 'w')
    i = -1
    color = 'green'
    out.write('# Region file format: DS9 version 4.0\nglobal color=' + color + ' font="helvetica 10 normal" select=1 highlite=1 edit=1 move=1 delete=1 include=1 fixed=0 source\n')
    out.write('fk5\n')
    for i in range(len(primarymatchs)):
        ci = primarymatchc[i]
        for j in range(len(smatch[i])):
            cj = cmatch[i][j]
            out.write('line(%.5f,%.5f,%.5f,%.5f) # line=0 0\n' % (catlist[ci].ra, catlist[ci].dec, catlist[cj].ra, catlist[cj].dec))

    out.close()
    return (
     primarymatchs, primarymatchc, mpa)