# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/evla_mcast/controller.py
# Compiled at: 2018-02-26 13:33:11
# Size of source mod 2**32: 5606 bytes
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input, str
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import logging, asyncore
from . import mcast_clients
from .scan_config import ScanConfig

class Dataset(object):

    def __init__(self, datasetId):
        self.datasetId = datasetId
        self.queued = []
        self.handled = []
        self.ant = None
        self.stopTime = None


class Controller(object):

    def __init__(self):
        self.obs_client = mcast_clients.ObsClient(self)
        self.ant_client = mcast_clients.AntClient(self)
        self._datasets = {}
        self.vci = {}
        self.scans_require = [
         'obs', 'vci', 'ant', 'stop']

    def run(self):
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            logging.info('Exiting controller...')

    def dataset(self, dsid):
        if dsid not in list(self._datasets.keys()):
            self._datasets[dsid] = Dataset(dsid)
        return self._datasets[dsid]

    def add_obs(self, obs):
        dsid = obs.attrib['datasetId']
        cfgid = obs.attrib['configId']
        ds = self.dataset(dsid)
        config = ScanConfig(obs=obs, vci=(self.vci[cfgid]), requires=(self.scans_require))
        if ds.ant is not None:
            config.set_ant(ds.ant)
        for scan in ds.queued:
            if scan.startTime < config.startTime and (scan.stopTime is None or scan.stopTime > config.startTime):
                scan.stopTime = config.startTime

        is_finish = config.source == 'FINISH'
        if not is_finish:
            ds.queued.append(config)
            logging.debug('Queued scan {0}, scan {1}.'.format(config.scan_intent, config.scanId))
        self.clean_queue(ds)
        if is_finish:
            logging.debug('Finishing dataset {0}'.format(ds.datasetId))
            ds.stopTime = config.startTime
            self.handle_finish(ds)
            self._datasets.pop(ds.datasetId)

    def add_vci(self, vci):
        self.vci[vci.attrib['configId']] = vci

    def add_ant(self, ant):
        dsid = ant.attrib['datasetId']
        ds = self.dataset(dsid)
        ds.ant = ant
        for scan in ds.queued:
            if not scan.has_ant:
                scan.set_ant(ant)

        self.clean_queue(ds)

    def clean_queue(self, ds):
        complete = [s for s in ds.queued if s.is_complete()]
        for scan in complete:
            logging.debug('Handling complete scan {0}'.format(scan.scanId))
            self.handle_config(scan)
            ds.handled.append(scan)
            ds.queued.remove(scan)

        for s in ds.queued:
            logging.debug('Queued %s start=%.6f stop=%.6f' % (
             s.scanId, s.startTime,
             s.stopTime if s.stopTime is not None else 0.0))

        for s in ds.handled:
            logging.debug('handled %s start=%.6f stop=%.6f' % (
             s.scanId, s.startTime,
             s.stopTime if s.stopTime is not None else 0.0))

    def handle_config(self, config):
        pass

    def handle_finish(self, dataset):
        pass