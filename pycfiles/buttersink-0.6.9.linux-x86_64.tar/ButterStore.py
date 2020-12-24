# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/buttersink/ButterStore.py
# Compiled at: 2018-06-26 18:40:50
""" Manage read-only volumes in local btrfs file system.

Copyright (c) 2014 Ames Cornish.  All rights reserved.  Licensed under GPLv3.

"""
from __future__ import division
import btrfs, Butter, progress, Store, io, logging, math, os, os.path, time
logger = logging.getLogger(__name__)
theMinimumChangeRate = 1e-05

class ButterStore(Store.Store):
    """ A local btrfs synchronization source or sink. """

    def __init__(self, host, path, mode, dryrun):
        """ Initialize.

        host is ignored.
        path is the file system location of the read-only subvolumes.

        """
        path = os.path.abspath(path) + ('/' if path.endswith('/') else '')
        super(ButterStore, self).__init__(host, path, mode, dryrun)
        if not os.path.isdir(self.userPath):
            raise Exception("'%s' is not an existing directory" % self.userPath)
        self.butter = Butter.Butter(dryrun)
        self.btrfs = btrfs.FileSystem(self.userPath)
        self.butterVolumes = {}
        self.extraVolumes = {}

    def _btrfsVol2StoreVol(self, bvol):
        if bvol.received_uuid is not None:
            uuid = bvol.received_uuid
            gen = bvol.sent_gen
        else:
            uuid = bvol.uuid
            gen = bvol.current_gen
        if uuid is None:
            return
        else:
            return Store.Volume(uuid, gen, bvol.totalSize, bvol.exclusiveSize)

    def _fillVolumesAndPaths(self, paths):
        """ Fill in paths.

        :arg paths: = { Store.Volume: ["linux path",]}
        """
        with self.btrfs as (mount):
            for bv in mount.subvolumes:
                if not bv.readOnly:
                    continue
                vol = self._btrfsVol2StoreVol(bv)
                if vol is None:
                    continue
                path = bv.fullPath
                if path is None:
                    logger.info('Skipping deleted volume %s', bv.uuid)
                    continue
                relPath = None
                for path in bv.linuxPaths:
                    path = self._relativePath(path)
                    if path is None:
                        continue
                    paths[vol].append(path)
                    infoPath = self._fullPath(path + Store.theInfoExtension)
                    if os.path.exists(infoPath):
                        logger.debug('Reading %s', infoPath)
                        with open(infoPath) as (info):
                            Store.Volume.readInfo(info)
                    if not path.startswith('/'):
                        relPath = path

                if vol not in paths:
                    continue
                logger.debug('%s', vol.display(sink=self, detail='phrase'))
                if vol.uuid in self.butterVolumes:
                    logger.warn("Duplicate effective uuid %s in '%s' and '%s'", vol.uuid, path, self.butterVolumes[vol.uuid].fullPath)
                self.butterVolumes[vol.uuid] = bv
                if relPath is not None:
                    self.extraVolumes[vol] = relPath

        return

    def _fileSystemSync(self):
        with self.btrfs as (mount):
            mount.SYNC()
        time.sleep(2)

    def __unicode__(self):
        """ English description of self. """
        return 'btrfs %s' % self.userPath

    def __str__(self):
        """ English description of self. """
        return unicode(self).encode('utf-8')

    def getEdges(self, fromVol):
        """ Return the edges available from fromVol. """
        if fromVol is None:
            for toVol in self.paths:
                yield Store.Diff(self, toVol, fromVol, toVol.size)

            return
        if fromVol not in self.paths:
            return
        else:
            fromBVol = self.butterVolumes[fromVol.uuid]
            parentUUID = fromBVol.parent_uuid
            butterDir = os.path.dirname(fromBVol.fullPath)
            vols = [ vol for vol in self.butterVolumes.values() if vol.parent_uuid == parentUUID or os.path.dirname(vol.fullPath) == butterDir
                   ]
            changeRate = self._calcChangeRate(vols)
            for toBVol in vols:
                if toBVol == fromBVol:
                    continue
                estimatedSize = self._estimateSize(toBVol, fromBVol, changeRate)
                toVol = self._btrfsVol2StoreVol(toBVol)
                yield Store.Diff(self, toVol, fromVol, estimatedSize, sizeIsEstimated=True)

            return

    def hasEdge(self, diff):
        """ True if Store already contains this edge. """
        return diff.toUUID in self.butterVolumes

    def receive(self, diff, paths):
        """ Return Context Manager for a file-like (stream) object to store a diff. """
        if not self.dryrun:
            self._fileSystemSync()
        path = self.selectReceivePath(paths)
        if os.path.exists(path):
            raise Exception("Path %s exists, can't receive %s" % (path, diff.toUUID))
        return self.butter.receive(path, diff, self.showProgress is True)

    def receiveVolumeInfo(self, paths):
        """ Return Context Manager for a file-like (stream) object to store volume info. """
        path = self.selectReceivePath(paths)
        path = path + Store.theInfoExtension
        if Store.skipDryRun(logger, self.dryrun)('receive info to %s', path):
            return None
        else:
            return open(path, 'w')

    def _estimateSize(self, toBVol, fromBVol, changeRate):
        fromGen = fromBVol.current_gen
        genDiff = abs(toBVol.current_gen - fromGen)
        estimatedSize = max(0, toBVol.totalSize - fromBVol.totalSize)
        estimatedSize += toBVol.totalSize * (1 - math.exp(-changeRate * genDiff))
        estimatedSize = max(toBVol.exclusiveSize, estimatedSize)
        return estimatedSize

    def measureSize(self, diff, chunkSize):
        """ Spend some time to get an accurate size. """
        self._fileSystemSync()
        sendContext = self.butter.send(self.getSendPath(diff.toVol), self.getSendPath(diff.fromVol), diff, showProgress=self.showProgress is not False, allowDryRun=False)

        class _Measure(io.RawIOBase):

            def __init__(self, estimatedSize, showProgress):
                self.totalSize = None
                self.progress = progress.DisplayProgress(estimatedSize) if showProgress else None
                return

            def __enter__(self):
                self.totalSize = 0
                if self.progress:
                    self.progress.__enter__()
                return self

            def __exit__(self, exceptionType, exceptionValue, traceback):
                if self.progress:
                    self.progress.__exit__(exceptionType, exceptionValue, traceback)
                return False

            def writable(self):
                return True

            def write(self, bytes):
                self.totalSize += len(bytes)
                if self.progress:
                    self.progress.update(self.totalSize)

        logger.info('Measuring %s', diff)
        measure = _Measure(diff.size, self.showProgress is not False)
        Store.transfer(sendContext, measure, chunkSize)
        diff.setSize(measure.totalSize, False)
        for path in self.getPaths(diff.toVol):
            path = self._fullPath(path) + Store.theInfoExtension
            with open(path, 'a') as (infoFile):
                diff.toVol.writeInfoLine(infoFile, diff.fromUUID, measure.totalSize)

    def _calcChangeRate(self, bvols):
        total = 0
        diffs = 0
        minGen = bvols[0].current_gen
        maxGen = minGen
        minSize = bvols[0].totalSize
        maxSize = minSize
        for vol in bvols:
            total += vol.totalSize
            diffs += vol.exclusiveSize
            minGen = min(minGen, vol.current_gen)
            maxGen = max(maxGen, vol.current_gen)
            minSize = min(minSize, vol.totalSize)
            maxSize = max(maxSize, vol.totalSize)

        try:
            diffs = max(diffs, maxSize - minSize)
            rate = -math.log(1 - diffs / total) * (len(bvols) - 1) / (maxGen - minGen)
            rate /= 10
        except (ZeroDivisionError, ValueError):
            rate = theMinimumChangeRate

        return rate

    def send(self, diff):
        """ Write the diff (toVol from fromVol) to the stream context manager. """
        if not self.dryrun:
            self._fileSystemSync()
        return self.butter.send(self.getSendPath(diff.toVol), self.getSendPath(diff.fromVol), diff, self.showProgress is True)

    def keep(self, diff):
        """ Mark this diff (or volume) to be kept in path. """
        self._keepVol(diff.toVol)
        self._keepVol(diff.fromVol)

    def _keepVol(self, vol):
        """ Mark this volume to be kept in path. """
        if vol is None:
            return
        else:
            if vol in self.extraVolumes:
                del self.extraVolumes[vol]
                return
            if vol not in self.paths:
                raise Exception('%s not in %s' % (vol, self))
            paths = self.paths[vol]
            newPath = self.selectReceivePath(paths)
            if self._relativePath(newPath) in paths:
                return
            if self._skipDryRun(logger, 'INFO')('Copy %s to %s', vol, newPath):
                return
            self.butterVolumes[vol.uuid].copy(newPath)
            return

    def deleteUnused(self, dryrun=False):
        """ Delete any old snapshots in path, if not kept. """
        for vol, path in self.extraVolumes.items():
            if self._skipDryRun(logger, 'INFO', dryrun=dryrun)('Delete subvolume %s', path):
                continue
            self.butterVolumes[vol.uuid].destroy()

    def deletePartials(self, dryrun=False):
        """ Delete any old partial uploads/downloads in path. """
        for vol, path in self.extraVolumes.items():
            if not path.endswith('.part'):
                continue
            if self._skipDryRun(logger, 'INFO', dryrun=dryrun)('Delete subvolume %s', path):
                continue
            self.butterVolumes[vol.uuid].destroy()