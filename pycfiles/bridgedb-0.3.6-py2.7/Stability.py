# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/Stability.py
# Compiled at: 2015-11-05 10:40:17
"""This module provides functionality for tracking bridge stability metrics.

Bridge stability metrics are calculated using the model introduced in
`"An Analysis of Tor Bridge Stability"`_ and
`implemented in the Tor Metrics library`_.

.. An Analysis of Tor Bridge Stability:
    https://metrics.torproject.org/papers/bridge-stability-2011-10-31.pdf
    Karsten Loesing, An Analysis of Tor Bridge Stability. Technical Report.
    The Tor Project, October 2011.

.. implemented in the Tor Metrics library:
    https://gitweb.torproject.org/metrics-tasks/task-4255/SimulateBridgeStability.java
"""
import logging, bridgedb.Storage
from bridgedb.schedule import toUnixSeconds
weighting_factor = float(19) / float(20)
discountIntervalMillis = long(43200000)

class BridgeHistory(object):
    """ Record Class that tracks a single Bridge
    The fields stored are:

    fingerprint, ip, port, weightedUptime, weightedTime, weightedRunLength,
    totalRunWeights, lastSeenWithDifferentAddressAndPort,
    lastSeenWithThisAddressAndPort, lastDiscountedHistoryValues.

    fingerprint         The Bridge Fingerprint (unicode)
    ip                  The Bridge IP (unicode)
    port                The Bridge orport (integer)

    weightedUptime      Weighted uptime in seconds (long int)
    weightedTime        Weighted time in seconds (long int)
    weightedRunLength   Weighted run length of previous addresses or ports in
                        seconds. (long int)
    totalRunWeights     Total run weights of previously used addresses or
                        ports. (float)

    lastSeenWithDifferentAddressAndPort
        Timestamp in milliseconds when this
        bridge was last seen with a different address or port. (long int)

    lastSeenWithThisAddressAndPort
        Timestamp in milliseconds when this bridge was last seen
        with this address and port. (long int)

    lastDiscountedHistoryValues:
        Timestamp in milliseconds when this bridge was last discounted. (long int)

    lastUpdatedWeightedTime:
        Timestamp in milliseconds when the weighted time was updated. (long int)
    """

    def __init__(self, fingerprint, ip, port, weightedUptime, weightedTime, weightedRunLength, totalRunWeights, lastSeenWithDifferentAddressAndPort, lastSeenWithThisAddressAndPort, lastDiscountedHistoryValues, lastUpdatedWeightedTime):
        self.fingerprint = fingerprint
        self.ip = ip
        self.port = port
        self.weightedUptime = long(weightedUptime)
        self.weightedTime = long(weightedTime)
        self.weightedRunLength = long(weightedRunLength)
        self.totalRunWeights = float(totalRunWeights)
        self.lastSeenWithDifferentAddressAndPort = long(lastSeenWithDifferentAddressAndPort)
        self.lastSeenWithThisAddressAndPort = long(lastSeenWithThisAddressAndPort)
        self.lastDiscountedHistoryValues = long(lastDiscountedHistoryValues)
        self.lastUpdatedWeightedTime = long(lastUpdatedWeightedTime)

    def discountWeightedFractionalUptimeAndWeightedTime(self, discountUntilMillis):
        """ discount weighted times """
        if self.lastDiscountedHistoryValues == 0:
            self.lastDiscountedHistoryValues = discountUntilMillis
        rounds = self.numDiscountRounds(discountUntilMillis)
        if rounds > 0:
            discount = lambda x: weighting_factor ** rounds * x
            self.weightedUptime = discount(self.weightedUptime)
            self.weightedTime = discount(self.weightedTime)
            self.weightedRunLength = discount(self.weightedRunLength)
            self.totalRunWeights = discount(self.totalRunWeights)
            self.lastDiscountedHistoryValues += discountIntervalMillis * rounds
        return rounds

    def numDiscountRounds(self, discountUntilMillis):
        """ return the number of rounds of discounting needed to bring this
        history element current """
        result = discountUntilMillis - self.lastDiscountedHistoryValues
        result = int(result / discountIntervalMillis)
        return max(result, 0)

    @property
    def weightedFractionalUptime(self):
        """Weighted Fractional Uptime"""
        if self.weightedTime < 0.0001:
            return long(0)
        return long(10000) * self.weightedUptime / self.weightedTime

    @property
    def tosa(self):
        """the Time On Same Address (TOSA)"""
        return (self.lastSeenWithThisAddressAndPort - self.lastSeenWithDifferentAddressAndPort) / 1000

    @property
    def familiar(self):
        """
        A bridge is 'familiar' if 1/8 of all active bridges have appeared
        more recently than it, or if it has been around for a Weighted Time of 8 days.
        """
        if self.weightedTime >= long(691200):
            return True
        with bridgedb.Storage.getDB() as (db):
            allWeightedTimes = [ bh.weightedTime for bh in db.getAllBridgeHistory() ]
            numBridges = len(allWeightedTimes)
            logging.debug('Got %d weightedTimes', numBridges)
            allWeightedTimes.sort()
            if self.weightedTime >= allWeightedTimes[(numBridges / 8)]:
                return True
            return False

    @property
    def wmtbac(self):
        """Weighted Mean Time Between Address Change"""
        totalRunLength = self.weightedRunLength + (self.lastSeenWithThisAddressAndPort - self.lastSeenWithDifferentAddressAndPort) / long(1000)
        totalWeights = self.totalRunWeights + 1.0
        if totalWeights < 0.0001:
            return long(0)
        assert isinstance(long, totalRunLength)
        assert isinstance(long, totalWeights)
        return totalRunlength / totalWeights


def addOrUpdateBridgeHistory(bridge, timestamp):
    with bridgedb.Storage.getDB() as (db):
        bhe = db.getBridgeHistory(bridge.fingerprint)
        if not bhe:
            secondsSinceLastStatusPublication = long(3600)
            lastSeenWithDifferentAddressAndPort = timestamp * long(1000)
            lastSeenWithThisAddressAndPort = timestamp * long(1000)
            bhe = BridgeHistory(bridge.fingerprint, bridge.address, bridge.orPort, 0, 0, 0, 0, lastSeenWithDifferentAddressAndPort, lastSeenWithThisAddressAndPort, 0, 0)
            db.updateIntoBridgeHistory(bhe)
        statusPublicationMillis = long(timestamp * 1000)
        if statusPublicationMillis - bhe.lastSeenWithThisAddressAndPort > 3600000:
            secondsSinceLastStatusPublication = long(3600)
            logging.debug('Capping secondsSinceLastStatusPublication to 1 hour')
        else:
            secondsSinceLastStatusPublication = (statusPublicationMillis - bhe.lastSeenWithThisAddressAndPort) / 1000
        if secondsSinceLastStatusPublication <= 0 and bhe.weightedTime > 0:
            logging.warn('Received old descriptor for bridge %s with timestamp %d', bhe.fingerprint, statusPublicationMillis / 1000)
            return bhe
        discountAndPruneBridgeHistories(statusPublicationMillis)
        updateWeightedTime(statusPublicationMillis)
        bhe = db.getBridgeHistory(bridge.fingerprint)
        if not bridge.running:
            logging.info('%s is not running' % bridge.fingerprint)
            return bhe
        if bridge.orport != bhe.port or bridge.ip != bhe.ip:
            bhe.totalRunWeights += 1.0
            bhe.weightedRunLength += bhe.tosa
            bhe.lastSeenWithDifferentAddressAndPort = bhe.lastSeenWithThisAddressAndPort
        bhe.weightedUptime += secondsSinceLastStatusPublication
        bhe.lastSeenWithThisAddressAndPort = statusPublicationMillis
        bhe.ip = str(bridge.ip)
        bhe.port = bridge.orport
        return db.updateIntoBridgeHistory(bhe)


def discountAndPruneBridgeHistories(discountUntilMillis):
    with bridgedb.Storage.getDB() as (db):
        bhToRemove = []
        bhToUpdate = []
        for bh in db.getAllBridgeHistory():
            bh.discountWeightedFractionalUptimeAndWeightedTime(discountUntilMillis)
            if bh.weightedFractionalUptime < 1 and bh.weightedTime > 86400:
                logging.debug('Removing bridge from history: %s' % bh.fingerprint)
                bhToRemove.append(bh.fingerprint)
            else:
                bhToUpdate.append(bh)

        for k in bhToUpdate:
            db.updateIntoBridgeHistory(k)

        for k in bhToRemove:
            db.delBridgeHistory(k)


def updateWeightedTime(statusPublicationMillis):
    bhToUpdate = []
    with bridgedb.Storage.getDB() as (db):
        for bh in db.getBridgesLastUpdatedBefore(statusPublicationMillis):
            interval = (statusPublicationMillis - bh.lastUpdatedWeightedTime) / 1000
            if interval > 0:
                bh.weightedTime += min(3600, interval)
                bh.lastUpdatedWeightedTime = statusPublicationMillis
                bhToUpdate.append(bh)

        for bh in bhToUpdate:
            db.updateIntoBridgeHistory(bh)


def updateBridgeHistory(bridges, timestamps):
    """Process all the timestamps and update the bridge stability statistics in
    the database.

    .. warning: This function is extremely expensive, and will keep getting
        more and more expensive, on a linearithmic scale, every time it is
        called. Blame the :mod:`bridgedb.Stability` module.

    :param dict bridges: All bridges from the descriptors, parsed into
        :class:`bridgedb.bridges.Bridge`s.
    :param dict timestamps: A dictionary whose keys are bridge fingerprints,
        and whose values are lists of integers, each integer being a timestamp
        (in seconds since Unix Epoch) for when a descriptor for that bridge
        was published.
    :rtype: dict
    :returns: The original **timestamps**, but which each list of integers
        (re)sorted.
    """
    logging.debug('Beginning bridge stability calculations')
    sortedTimestamps = {}
    for fingerprint, stamps in timestamps.items()[:]:
        stamps.sort()
        bridge = bridges[fingerprint]
        for timestamp in stamps:
            logging.debug('Adding/updating timestamps in BridgeHistory for %s in database: %s' % (
             fingerprint, timestamp))
            timestamp = toUnixSeconds(timestamp.timetuple())
            addOrUpdateBridgeHistory(bridge, timestamp)

        sortedTimestamps[fingerprint] = stamps

    logging.debug('Stability calculations complete')
    return sortedTimestamps