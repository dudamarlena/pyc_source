# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pippkgapi\releases.py
# Compiled at: 2019-01-08 00:21:22
# Size of source mod 2**32: 2220 bytes


def getReleases(pkginfo):
    releases = []
    for i in pkginfo['releases']:
        releases.append(i)

    return releases


def getReleaseMD5Hashes(pkginfo, release):
    rnum = release
    try:
        releaseMD5 = pkginfo['releases'][rnum][0]['digests']['md5']
        releaseMD52 = pkginfo['releases'][rnum][1]['digests']['md5']
        releaseMD5Hashes = releaseMD5 + '\n' + releaseMD52
    except:
        releaseMD5Hashes = pkginfo['releases'][rnum][0]['digests']['md5']

    return releaseMD5Hashes


def getReleaseSHA256Hashes(pkginfo, release):
    rnum = release
    try:
        releaseSHA = pkginfo['releases'][rnum][0]['digests']['sha256']
        releaseSHA1 = pkginfo['releases'][rnum][1]['digests']['sha256']
        releaseSHA256Hashes = releaseSHA + '\n' + releaseSHA1
    except:
        releaseSHA256Hashes = pkginfo['releases'][rnum][0]['digests']['sha256']

    return releaseSHA256Hashes


def getReleaseFilenames(pkginfo, release):
    rnum = release
    releaseFilenames = []
    try:
        for i in range(0, 2):
            releaseFilenames.append([pkginfo['releases'][rnum][i]['packagetype'], rnum, pkginfo['releases'][rnum][i]['filename']])

    except:
        releaseFilenames.append([pkginfo['releases'][rnum][0]['packagetype'], rnum, pkginfo['releases'][rnum][0]['filename']])

    return releaseFilenames


def getReleaseFileURLs(pkginfo, release):
    rnum = release
    releaseFileURLs = []
    try:
        for i in range(0, 2):
            releaseFileURLs.append([pkginfo['releases'][rnum][i]['packagetype'], pkginfo['releases'][rnum][i]['url']])

    except:
        releaseFileURLs.append([pkginfo['releases'][rnum][i]['packagetype'], pkginfo['releases'][rnum][i]['url']])

    return releaseFileURLs


def getReleaseSize(pkginfo, release):
    rnum = release
    releaseFileSizes = []
    try:
        for i in range(0, 2):
            releaseFileSizes.append([pkginfo['releases'][rnum][i]['packagetype'], str(pkginfo['releases'][rnum][i]['size']) + ' bytes'])

    except:
        releaseFileSizes.append([pkginfo['releases'][rnum][0]['packagetype'], str(pkginfo['releases'][rnum][0]['size']) + ' bytes'])

    return releaseFileSizes