# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/PackageManager.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 29063 bytes
__doc__ = '\nSeparated on Jul 28, 2013 from DialogOpenArchive.py\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import sys, os, io, re, time, json, logging
from collections import defaultdict
from fnmatch import fnmatch
from lxml import etree
if sys.version[0] >= '3':
    from urllib.parse import urljoin
else:
    from urlparse import urljoin
openFileSource = None
from arelle import Locale, XmlUtil
from arelle.UrlUtil import isAbsolute
ArchiveFileIOError = None
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

EMPTYDICT = {}

def baseForElement(element):
    base = ''
    baseElt = element
    while baseElt is not None:
        baseAttr = baseElt.get('{http://www.w3.org/XML/1998/namespace}base')
        if baseAttr:
            if baseAttr.startswith('/'):
                base = baseAttr
            else:
                base = baseAttr + base
            baseElt = baseElt.getparent()

    return base


def xmlLang(element):
    return (element.xpath('@xml:lang') + element.xpath('ancestor::*/@xml:lang') + [''])[0]


def langCloseness(l1, l2):
    _len = min(len(l1), len(l2))
    for i in range(0, _len):
        if l1[i] != l2[i]:
            return i

    return _len


def parsePackage(cntlr, filesource, metadataFile, fileBase, errors=[]):
    global ArchiveFileIOError
    if ArchiveFileIOError is None:
        from arelle.FileSource import ArchiveFileIOError
    unNamedCounter = 1
    txmyPkgNSes = ('http://www.corefiling.com/xbrl/taxonomypackage/v1', 'http://xbrl.org/PWD/2014-01-15/taxonomy-package',
                   'http://xbrl.org/PWD/2015-01-14/taxonomy-package', 'http://xbrl.org/PR/2015-12-09/taxonomy-package',
                   'http://xbrl.org/2016/taxonomy-package', 'http://xbrl.org/WGWD/YYYY-MM-DD/taxonomy-package')
    catalogNSes = ('urn:oasis:names:tc:entity:xmlns:xml:catalog', )
    pkg = {}
    currentLang = Locale.getLanguageCode()
    _file = filesource.file(metadataFile)[0]
    try:
        tree = etree.parse(_file)
    except etree.XMLSyntaxError as err:
        cntlr.addToLog(_('Package catalog syntax error %(error)s'), messageArgs={'error': str(err)}, messageCode='tpe:invalidMetaDataFile', file=os.path.basename(metadataFile), level=logging.ERROR)
        errors.append('tpe:invalidMetaDataFile')
        raise

    root = tree.getroot()
    ns = root.tag.partition('}')[0][1:]
    nsPrefix = '{{{}}}'.format(ns)
    if ns in txmyPkgNSes:
        for eltName in ('identifier', 'version', 'license', 'publisher', 'publisherURL',
                        'publisherCountry', 'publicationDate'):
            pkg[eltName] = ''
            for m in root.iterchildren(tag=nsPrefix + eltName):
                if eltName == 'license':
                    pkg[eltName] = m.get('name')
                else:
                    pkg[eltName] = (m.text or '').strip()
                break

        for eltName in ('name', 'description'):
            closest = ''
            closestLen = 0
            for m in root.iterchildren(tag=nsPrefix + eltName):
                s = (m.text or '').strip()
                eltLang = xmlLang(m)
                l = langCloseness(eltLang, currentLang)
                if l > closestLen:
                    closestLen = l
                    closest = s
                elif closestLen == 0 and eltLang.startswith('en'):
                    closest = s

            if not closest and eltName == 'name':
                closest = os.path.splitext(os.path.basename(filesource.baseurl))[0]
            pkg[eltName] = closest

        for eltName in ('supersededTaxonomyPackages', 'versioningReports'):
            pkg[eltName] = []

        for m in root.iterchildren(tag=nsPrefix + 'supersededTaxonomyPackages'):
            pkg['supersededTaxonomyPackages'] = [r.text.strip() for r in m.iterchildren(tag=nsPrefix + 'taxonomyPackageRef')]

        for m in root.iterchildren(tag=nsPrefix + 'versioningReports'):
            pkg['versioningReports'] = [r.get('href') for r in m.iterchildren(tag=nsPrefix + 'versioningReport')]

        langElts = defaultdict(list)
        for n in root.iter(tag=nsPrefix + '*'):
            for eltName in ('name', 'description', 'publisher'):
                langElts.clear()
                for m in n.iterchildren(tag=nsPrefix + eltName):
                    langElts[xmlLang(m)].append(m)

                for lang, elts in langElts.items():
                    if not lang:
                        cntlr.addToLog(_('Multi-lingual element %(element)s has no in-scope xml:lang attribute'), messageArgs={'element': eltName}, messageCode='tpe:missingLanguageAttribute', refs=[{'href': os.path.basename(metadataFile), 'sourceLine': m.sourceline} for m in elts], level=logging.ERROR)
                        errors.append('tpe:missingLanguageAttribute')
                    elif len(elts) > 1:
                        cntlr.addToLog(_('Multi-lingual element %(element)s has multiple (%(count)s) in-scope xml:lang %(lang)s elements'), messageArgs={'element': eltName, 'lang': lang, 'count': len(elts)}, messageCode='tpe:duplicateLanguagesForElement', refs=[{'href': os.path.basename(metadataFile), 'sourceLine': m.sourceline} for m in elts], level=logging.ERROR)
                        errors.append('tpe:duplicateLanguagesForElement')

        del langElts
    else:
        fileName = getattr(metadataFile, 'fileName', getattr(metadataFile, 'name', metadataFile))
        pkg['name'] = os.path.basename(os.path.dirname(fileName))
        pkg['description'] = 'oasis catalog'
        pkg['version'] = '(none)'
    remappings = {}
    rewriteTree = tree
    catalogFile = metadataFile
    if ns in ('http://xbrl.org/PWD/2015-01-14/taxonomy-package', 'http://xbrl.org/PR/2015-12-09/taxonomy-package',
              'http://xbrl.org/WGWD/YYYY-MM-DD/taxonomy-package', 'http://xbrl.org/2016/taxonomy-package',
              'http://xbrl.org/REC/2016-04-19/taxonomy-package'):
        catalogFile = metadataFile.replace('taxonomyPackage.xml', 'catalog.xml')
        try:
            rewriteTree = etree.parse(filesource.file(catalogFile)[0])
        except ArchiveFileIOError:
            pass

    for tag, prefixAttr, replaceAttr in ((nsPrefix + 'remapping', 'prefix', 'replaceWith'),
     ('{urn:oasis:names:tc:entity:xmlns:xml:catalog}rewriteSystem', 'systemIdStartString',
 'rewritePrefix'),
     ('{urn:oasis:names:tc:entity:xmlns:xml:catalog}rewriteURI', 'uriStartString', 'rewritePrefix')):
        for m in rewriteTree.iter(tag=tag):
            prefixValue = m.get(prefixAttr)
            replaceValue = m.get(replaceAttr)
            if prefixValue and replaceValue is not None:
                if prefixValue not in remappings:
                    base = baseForElement(m)
                    if base:
                        replaceValue = os.path.join(base, replaceValue)
                    if replaceValue:
                        if not isAbsolute(replaceValue):
                            if not os.path.isabs(replaceValue):
                                replaceValue = fileBase + replaceValue
                            replaceValue = replaceValue.replace('/', os.sep)
                        _normedValue = os.path.normpath(replaceValue)
                        if replaceValue.endswith(os.sep) and not _normedValue.endswith(os.sep):
                            _normedValue += os.sep
                        remappings[prefixValue] = _normedValue
                    else:
                        cntlr.addToLog(_('Package catalog duplicate rewrite start string %(rewriteStartString)s'), messageArgs={'rewriteStartString': prefixValue}, messageCode='tpe:multipleRewriteURIsForStartString', file=os.path.basename(catalogFile), level=logging.ERROR)
                        errors.append('tpe:multipleRewriteURIsForStartString')

    pkg['remappings'] = remappings
    entryPoints = defaultdict(list)
    pkg['entryPoints'] = entryPoints
    for entryPointSpec in tree.iter(tag=nsPrefix + 'entryPoint'):
        name = None
        closestLen = 0
        for nameNode in entryPointSpec.iter(tag=nsPrefix + 'name'):
            s = (nameNode.text or '').strip()
            nameLang = xmlLang(nameNode)
            l = langCloseness(nameLang, currentLang)
            if l > closestLen:
                closestLen = l
                name = s
            elif closestLen == 0 and nameLang.startswith('en'):
                name = s

        if not name:
            name = _('<unnamed {0}>').format(unNamedCounter)
            unNamedCounter += 1
        epDocCount = 0
        for epDoc in entryPointSpec.iterchildren(nsPrefix + 'entryPointDocument'):
            epUrl = epDoc.get('href')
            base = epDoc.get('{http://www.w3.org/XML/1998/namespace}base')
            if base:
                resolvedUrl = urljoin(base, epUrl)
            else:
                resolvedUrl = epUrl
            epDocCount += 1
            remappedUrl = resolvedUrl
            longestPrefix = 0
            for mapFrom, mapTo in remappings.items():
                if remappedUrl.startswith(mapFrom):
                    prefixLength = len(mapFrom)
                    if prefixLength > longestPrefix:
                        _remappedUrl = remappedUrl[prefixLength:]
                        if not (_remappedUrl[0] in (os.sep, '/') or mapTo[(-1)] in (os.sep, '/')):
                            _remappedUrl = mapTo + os.sep + _remappedUrl
                        else:
                            _remappedUrl = mapTo + _remappedUrl
                        longestPrefix = prefixLength

            if longestPrefix:
                remappedUrl = _remappedUrl.replace(os.sep, '/')
            closest = ''
            closestLen = 0
            for m in entryPointSpec.iterchildren(tag=nsPrefix + 'description'):
                s = (m.text or '').strip()
                eltLang = xmlLang(m)
                l = langCloseness(eltLang, currentLang)
                if l > closestLen:
                    closestLen = l
                    closest = s
                elif closestLen == 0 and eltLang.startswith('en'):
                    closest = s

            if not closest and name:
                closest = name
            entryPoints[name].append((remappedUrl, resolvedUrl, closest))

    return pkg


packagesJsonFile = None
packagesConfig = None
packagesConfigChanged = False
packagesMappings = {}
_cntlr = None

def init(cntlr, loadPackagesConfig=True):
    global _cntlr
    global packagesConfig
    global packagesJsonFile
    if loadPackagesConfig:
        try:
            packagesJsonFile = cntlr.userAppDir + os.sep + 'taxonomyPackages.json'
            with io.open(packagesJsonFile, 'rt', encoding='utf-8') as (f):
                packagesConfig = json.load(f)
            packagesConfigChanged = False
        except Exception:
            pass

        if packagesConfig is None:
            packagesConfig = {'packages': [], 
             'remappings': {}}
            packagesConfigChanged = False
        pluginMethodsForClasses = {}
        _cntlr = cntlr


def reset():
    global packagesMappings
    packagesConfig.clear()
    packagesMappings.clear()


def orderedPackagesConfig():
    return OrderedDict((
     (
      'packages',
      [OrderedDict(sorted(_packageInfo.items(), key=lambda k: {'name': '01', 
       'status': '02', 
       'version': '03', 
       'fileDate': '04', 
       'license': '05', 
       'URL': '06', 
       'description': '07', 
       'publisher': '08', 
       'publisherURL': '09', 
       'publisherCountry': '10', 
       'publicationDate': '11', 
       'supersededTaxonomyPackages': '12', 
       'versioningReports': '13', 
       'remappings': '14'}.get(k[0], k[0]))) for _packageInfo in packagesConfig['packages']]),
     (
      'remappings', OrderedDict(sorted(packagesConfig['remappings'].items())))))


def save(cntlr):
    global packagesConfigChanged
    if packagesConfigChanged and cntlr.hasFileSystem:
        with io.open(packagesJsonFile, 'wt', encoding='utf-8') as (f):
            jsonStr = _STR_UNICODE(json.dumps(orderedPackagesConfig(), ensure_ascii=False, indent=2))
            f.write(jsonStr)
        packagesConfigChanged = False


def close():
    global webCache
    packagesConfig.clear()
    packagesMappings.clear()
    webCache = None


def packageNamesWithNewerFileDates():
    names = set()
    for package in packagesConfig['packages']:
        freshenedFilename = _cntlr.webCache.getfilename(package['URL'], checkModifiedTime=True, normalize=True)
        try:
            if package['fileDate'] < time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(os.path.getmtime(freshenedFilename))):
                names.add(package['name'])
        except Exception:
            pass

    return names


def packageInfo(cntlr, URL, reload=False, packageManifestName=None, errors=[]):
    global openFileSource
    packageFilename = _cntlr.webCache.getfilename(URL, reload=reload, normalize=True)
    if packageFilename:
        from arelle.FileSource import TAXONOMY_PACKAGE_FILE_NAMES
        filesource = None
        try:
            if openFileSource is None:
                from arelle.FileSource import openFileSource
            filesource = openFileSource(packageFilename, _cntlr)
            packages = []
            packageFiles = []
            if filesource.isZip:
                _dir = filesource.dir
                if not _dir:
                    raise IOError(_('Unable to open taxonomy package: {0}.').format(packageFilename))
                topLevelDirectories = set(f.partition('/')[0] for f in _dir)
                if len(topLevelDirectories) != 1:
                    cntlr.addToLog(_('Taxonomy package contains %(count)s top level directories:  %(topLevelDirectories)s'), messageArgs={'count': len(topLevelDirectories), 
                     'topLevelDirectories': ', '.join(sorted(topLevelDirectories))}, messageCode='tpe:invalidDirectoryStructure', file=os.path.basename(packageFilename), level=logging.ERROR)
                    errors.append('tpe:invalidDirectoryStructure')
                else:
                    if not any('/META-INF/' in f for f in _dir):
                        cntlr.addToLog(_('Taxonomy package does not contain a subdirectory META-INF'), messageCode='tpe:metadataDirectoryNotFound', file=os.path.basename(packageFilename), level=logging.ERROR)
                        errors.append('tpe:metadataDirectoryNotFound')
                    else:
                        if any(f.endswith('/META-INF/taxonomyPackage.xml') for f in _dir):
                            packageFiles = [f for f in _dir if f.endswith('/META-INF/taxonomyPackage.xml')]
                        else:
                            cntlr.addToLog(_('Taxonomy package does not contain a metadata file */META-INF/taxonomyPackage.xml'), messageCode='tpe:metadataFileNotFound', file=os.path.basename(packageFilename), level=logging.ERROR)
                            errors.append('tpe:metadataFileNotFound')
                        if not packageFiles:
                            _metaInf = '{}/META-INF/'.format(os.path.splitext(os.path.basename(packageFilename))[0])
                            if packageManifestName:
                                packageFiles = [fileName for fileName in _dir if fnmatch(fileName, packageManifestName)]
                            else:
                                if _metaInf + 'taxonomyPackage.xml' in _dir:
                                    packageFiles = [_metaInf + 'taxonomyPackage.xml']
                                else:
                                    if 'META-INF/taxonomyPackage.xml' in _dir:
                                        packageFiles = ['META-INF/taxonomyPackage.xml']
                                    else:
                                        packageFiles = filesource.taxonomyPackageMetadataFiles
                                if len(packageFiles) < 1:
                                    raise IOError(_('Taxonomy package contained no metadata file: {0}.').format(', '.join(packageFiles)))
                            if any(pf.startswith('_metaInf') for pf in packageFiles) and any(not pf.startswith(_metaInf) for pf in packageFiles):
                                packageFiles = [pf for pf in packageFiles if pf.startswith(_metaInf)]
                            elif any(pf.startswith('META-INF/') for pf in packageFiles) and any(not pf.startswith('META-INF/') for pf in packageFiles):
                                packageFiles = [pf for pf in packageFiles if pf.startswith('META-INF/')]
                            for packageFile in packageFiles:
                                packageFileUrl = filesource.url + os.sep + packageFile
                                packageFilePrefix = os.sep.join(os.path.split(packageFile)[:-1])
                                if packageFilePrefix:
                                    packageFilePrefix += os.sep
                                packageFilePrefix = filesource.baseurl + os.sep + packageFilePrefix
                                packages.append([packageFileUrl, packageFilePrefix, packageFile])

                        else:
                            cntlr.addToLog(_('Taxonomy package is not a zip file.'), messageCode='tpe:invalidArchiveFormat', file=os.path.basename(packageFilename), level=logging.ERROR)
                            errors.append('tpe:invalidArchiveFormat')
                            if os.path.basename(filesource.url) in TAXONOMY_PACKAGE_FILE_NAMES or os.path.basename(filesource.url) == 'taxonomyPackage.xml' and os.path.basename(os.path.dirname(filesource.url)) == 'META-INF':
                                packageFile = packageFileUrl = filesource.url
                                packageFilePrefix = os.path.dirname(packageFile)
                                if packageFilePrefix:
                                    packageFilePrefix += os.sep
                                packages.append([packageFileUrl, packageFilePrefix, ''])
                            else:
                                raise IOError(_('File must be a taxonomy package (zip file), catalog file, or manifest (): {0}.').format(packageFilename, ', '.join(TAXONOMY_PACKAGE_FILE_NAMES)))
                remappings = {}
                packageNames = []
                descriptions = []
                for packageFileUrl, packageFilePrefix, packageFile in packages:
                    parsedPackage = parsePackage(_cntlr, filesource, packageFileUrl, packageFilePrefix, errors)
                    packageNames.append(parsedPackage['name'])
                    if parsedPackage.get('description'):
                        descriptions.append(parsedPackage['description'])
                    for prefix, remapping in parsedPackage['remappings'].items():
                        if prefix not in remappings:
                            remappings[prefix] = remapping
                        else:
                            cntlr.addToLog('Package mapping duplicate rewrite start string %(rewriteStartString)s', messageArgs={'rewriteStartString': prefix}, messageCode='arelle.packageDuplicateMapping', file=os.path.basename(URL), level=logging.ERROR)
                            errors.append('arelle.packageDuplicateMapping')

                return parsedPackage or None
            else:
                package = {'name': ', '.join(packageNames), 
                 'status': 'enabled', 
                 'version': parsedPackage.get('version'), 
                 'license': parsedPackage.get('license'), 
                 'fileDate': time.strftime('%Y-%m-%dT%H:%M:%S UTC', time.gmtime(os.path.getmtime(packageFilename))), 
                 'URL': URL, 
                 'manifestName': packageManifestName, 
                 'description': '; '.join(descriptions), 
                 'publisher': parsedPackage.get('publisher'), 
                 'publisherURL': parsedPackage.get('publisherURL'), 
                 'publisherCountry': parsedPackage.get('publisherCountry'), 
                 'publicationDate': parsedPackage.get('publicationDate'), 
                 'supersededTaxonomyPackages': parsedPackage.get('supersededTaxonomyPackages'), 
                 'versioningReports': parsedPackage.get('versioningReports'), 
                 'remappings': remappings}
                filesource.close()
                return package
        except (EnvironmentError, etree.XMLSyntaxError):
            pass

        if filesource:
            filesource.close()


def rebuildRemappings(cntlr):
    remappings = packagesConfig['remappings']
    remappings.clear()
    remapOverlapUrls = []
    for _packageInfo in packagesConfig['packages']:
        _packageInfoURL = _packageInfo['URL']
        if _packageInfo['status'] == 'enabled':
            for prefix, remapping in _packageInfo['remappings'].items():
                remappings[prefix] = remapping
                remapOverlapUrls.append((prefix, _packageInfoURL, remapping))

    remapOverlapUrls.sort()
    for i, _remap in enumerate(remapOverlapUrls):
        _prefix, _packageURL, _rewrite = _remap
        for j in range(i - 1, -1, -1):
            _prefix2, _packageURL2, _rewrite2 = remapOverlapUrls[j]
            if _packageURL != _packageURL2 and _prefix and _prefix2 and (_prefix.startswith(_prefix2) or _prefix2.startswith(_prefix)):
                _url1 = os.path.basename(_packageURL)
                _url2 = os.path.basename(_packageURL2)
                if _url1 == _url2:
                    _url1 = _packageURL
                    _url2 = _packageURL2
                cntlr.addToLog(_('Packages overlap the same rewrite start string %(rewriteStartString)s') if _prefix == _prefix2 else _('Packages overlap rewrite start strings %(rewriteStartString)s and %(rewriteStartString2)s'), messageArgs={'rewriteStartString': _prefix, 'rewriteStartString2': _prefix2}, messageCode='arelle.packageRewriteOverlap', file=(
                 _url1, _url2), level=logging.WARNING)


def isMappedUrl(url):
    return packagesConfig is not None and any(url.startswith(mapFrom) for mapFrom in packagesConfig.get('remappings', EMPTYDICT).keys())


def mappedUrl(url):
    if packagesConfig is not None:
        longestPrefix = 0
        for mapFrom, mapTo in packagesConfig.get('remappings', EMPTYDICT).items():
            if url.startswith(mapFrom):
                prefixLength = len(mapFrom)
                if prefixLength > longestPrefix:
                    mappedUrl = mapTo + url[prefixLength:]
                    longestPrefix = prefixLength

        if longestPrefix:
            pass
        return mappedUrl
    return url


def addPackage(cntlr, url, packageManifestName=None):
    global packagesConfigChanged
    newPackageInfo = packageInfo(cntlr, url, packageManifestName=packageManifestName)
    if newPackageInfo and newPackageInfo.get('name'):
        name = newPackageInfo.get('name')
        version = newPackageInfo.get('version')
        j = -1
        packagesList = packagesConfig['packages']
        for i, _packageInfo in enumerate(packagesList):
            if _packageInfo['name'] == name and _packageInfo['version'] == version:
                j = i
                break

        if 0 <= j < len(packagesList):
            packagesList[j] = newPackageInfo
        else:
            packagesList.append(newPackageInfo)
        packagesConfigChanged = True
        return newPackageInfo


def reloadPackageModule(cntlr, name):
    packageUrls = []
    packagesList = packagesConfig['packages']
    for _packageInfo in packagesList:
        if _packageInfo['name'] == name:
            packageUrls.append(_packageInfo['URL'])

    result = False
    for url in packageUrls:
        addPackage(cntlr, url)
        result = True

    return result


def removePackageModule(cntlr, name):
    global packagesConfigChanged
    packageIndices = []
    packagesList = packagesConfig['packages']
    for i, _packageInfo in enumerate(packagesList):
        if _packageInfo['name'] == name:
            packageIndices.insert(0, i)

    result = False
    for i in packageIndices:
        del packagesList[i]
        result = True

    if result:
        packagesConfigChanged = True
    return result