# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pippkgapi\packages.py
# Compiled at: 2019-01-08 00:21:17
# Size of source mod 2**32: 1387 bytes
import requests as r, json

def package(pkgname):
    url = 'https://pypi.org/pypi/'
    resptype = '/json'
    request = r.get(url + pkgname + resptype).text
    pkginfo = json.loads(request)
    return pkginfo


def getName(pkginfo):
    name = pkginfo['info']['name']
    return name


def getAuthor(pkginfo):
    author = pkginfo['info']['author']
    return author


def getLongDesc(pkginfo):
    longDesc = pkginfo['info']['description']
    return longDesc


def getLicense(pkginfo):
    licenseType = pkginfo['info']['license']
    return licenseType


def getSummary(pkginfo):
    summary = pkginfo['info']['summary']
    return summary


def getReqs(pkginfo):
    requirements = pkginfo['info']['requires_dist']
    return requirements


def getHomePage(pkginfo):
    homePage = pkginfo['info']['home_page']
    return homePage


def getClassifiers(pkginfo):
    classifiers = pkginfo['info']['classifiers']
    return classifiers


def getProjectURLS(pkginfo):
    projURLs = pkginfo['info']['project_urls']
    return projURLs


def getURL(pkginfo):
    projURL = pkginfo['info']['project_url']
    return projURL


def getVersion(pkginfo):
    version = pkginfo['info']['version']
    return version


def getReleases(pkginfo):
    releases = []
    for i in pkginfo['releases']:
        releases.append(i)

    return releases