# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\versions.py
# Compiled at: 2018-10-06 16:05:07
# Size of source mod 2**32: 14238 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six import iteritems
from io import BytesIO
from sc2gameLobby import dateFormat
from sc2gameLobby import gameConstants as c
import json, os, re, time

def addNew(label, version, baseVersion, dataHash='', fixedHash='', replayHash=''):
    """
    Add a new version record to the database to be tracked
    VERSION RECORD EXAMPLE:
        "base-version": 55505, 
        "data-hash": "60718A7CA50D0DF42987A30CF87BCB80", 
        "fixed-hash": "0189B2804E2F6BA4C4591222089E63B2", 
        "label": "3.16", 
        "replay-hash": "B11811B13F0C85C29C5D4597BD4BA5A4", 
        "version": 55505
        """
    baseVersion = int(baseVersion)
    version = int(version)
    minVersChecks = {'base-version':baseVersion,  'version':version}
    if label in handle.ALL_VERS_DATA:
        raise ValueError('given record label (%s) is already defined.  Consider performing update() for this record instead' % label)
    for vCheckK, vCheckV in iteritems(minVersChecks):
        maxVersion = min([vData[vCheckK] for vData in handle.ALL_VERS_DATA.values()])
        if vCheckV < c.MIN_VERSION_AI_API:
            raise ValueError('version %s / %s.%s does not support the Starcraft2 API' % (baseVersion, label, version))
        if vCheckV < maxVersion:
            raise ValueError('given %s (%d) cannot be smaller than newest known %s (%d)' % (vCheckK, vCheckV, vCheckK, maxVersion))

    uniqueValHeaders = list(c.JSON_HEADERS)
    uniqueValHeaders.remove('base-version')
    record = {'base-version': baseVersion}
    for k, v in zip(uniqueValHeaders, [label, version, dataHash, fixedHash, replayHash]):
        record[k] = v
        if not v:
            continue
        if v in [r[k] for r in Handler.ALL_VERS_DATA.values()]:
            raise ValueError("'%s' '%s' is in known values: %s" % (k, v, getattr(handle, k)))
            return

    handle.save(new=record)


class Handler(object):
    __doc__ = 'NOTE: the data-hash field is required to launch stand-alone versions of the game'
    ALL_VERS_DATA = None

    def __init__(self):
        self.load()

    def __len__(self):
        """the number of known version records"""
        return len(Handler.ALL_VERS_DATA)

    @property
    def mostRecent(self):
        records = iteritems(Handler.ALL_VERS_DATA)
        try:
            label, record = max(records)
            return record
        except ValueError:
            return

    def load(self):
        """load ALL_VERS_DATA from disk"""
        basepath = os.path.dirname(os.path.abspath(__file__))
        filename = os.sep.join([basepath, c.FOLDER_JSON, c.FILE_GAME_VERSIONS])
        Handler.ALL_VERS_DATA = {}
        with open(filename, 'r') as (f):
            data = json.loads(f.read())
        self.update(data)
        self._updated = False

    def save(self, new=None, timeout=2):
        """write ALL_VERS_DATA to disk in 'pretty' format"""
        if new:
            self.update(new)
        else:
            if not self._updated:
                return
            thisPkg = os.path.dirname(__file__)
            filename = os.path.join(thisPkg, c.FOLDER_JSON, c.FILE_GAME_VERSIONS)
            fParts = c.FILE_GAME_VERSIONS.split('.')
            newFile = os.path.join(thisPkg, c.FOLDER_JSON, '%s_%s.%s' % (fParts[0], dateFormat.now(), fParts[1]))
            if not os.path.isfile(newFile):
                os.rename(filename, newFile)
        recordKeys = [(record['version'], record) for record in Handler.ALL_VERS_DATA.values()]
        data = [r for k, r in sorted(recordKeys)]
        start = time.time()
        while time.time() - start < timeout:
            try:
                with open(filename, 'wb') as (f):
                    f.write(str.encode(json.dumps(data, indent=4, sort_keys=True)))
                self._updated = False
                return
            except IOError:
                pass

        raise

    def search(self, *args, **kwargs):
        """match all records that have any args in any key/field that also match
        key/value requirements specified in kwargs"""
        ret = []
        for record in Handler.ALL_VERS_DATA.values():
            matchArgs = list(kwargs.keys())
            for k, v in iteritems(kwargs):
                try:
                    if record[k] != v:
                        break
                except:
                    break

                matchArgs.remove(k)

            if matchArgs:
                pass
            else:
                matchArgs = list(args)
                for k, v in iteritems(record):
                    if k in matchArgs:
                        matchArgs.remove(k)
                    if v in matchArgs:
                        matchArgs.remove(v)

                if matchArgs:
                    pass
                else:
                    ret.append(record)

        return ret

    def update(self, data):
        """update known data with with newly provided data"""
        if not isinstance(data, list):
            data = [
             data]
        master = Handler.ALL_VERS_DATA
        for record in data:
            for k, v in iteritems(record):
                try:
                    record[k] = int(v)
                except ValueError:
                    record[k] = v

            try:
                label = record['label']
            except KeyError:
                raise ValueError('Must provide a valid label argument.  Given:%s%s' % (
                 os.linesep, ('%s  ' % os.linesep).join(['%15s:%s' % (k, v) for k, v in iteritems(kwargs)])))

            try:
                masterLabel = master[label]
            except KeyError:
                master[label] = record
                self._updated = True
                continue

            for k, v in iteritems(record):
                try:
                    if masterLabel[k] == v:
                        continue
                except KeyError:
                    pass

                self._updated = True
                try:
                    master[label].update(record)
                except KeyError:
                    break


handle = Handler()

class Version(object):
    __doc__ = 'Represent a single version of the game settings'

    def __init__(self, versionVal=None):
        if versionVal:
            if isinstance(versionVal, list):
                versionVal = max(versionVal)
            records = handle.search(versionVal)
            if len(records) > 1:
                raise ValueError('identified too many records (%d): %s' % (len(records), records))
            else:
                if len(records) < 1:
                    raise ValueError('first collect and update version information for version: %s' % versionVal)
            record = records.pop()
        else:
            record = handle.mostRecent
        for k in c.JSON_HEADERS:
            oldK = k
            wordBoundaries = re.search('(-\\w)', k)
            if wordBoundaries:
                for wb in wordBoundaries.groups():
                    newWb = wb.upper().strip('-')
                    k = re.sub(wb, newWb, k)

            setattr(self, k, record[oldK])

        while self.label.count('.') < 2:
            self.label += '.0'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s.%s' % (self.label, self.version)

    def __getitem__(self, key):
        return getattr(self, key)

    def toTuple(self, typeCast=int):
        return [typeCast(v) for v in self.label.split('.')]

    def toFilename(self):
        return re.sub('\\.', '_', str(self.label))