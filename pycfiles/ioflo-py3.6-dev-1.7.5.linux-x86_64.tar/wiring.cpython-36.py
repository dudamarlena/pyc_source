# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/wiring.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 5545 bytes
"""
wiring.py  wire logging module

"""
from __future__ import absolute_import, division, print_function
import sys, os, time, io
from ..aid.sixing import *
from ..aid.consoling import getConsole
console = getConsole()

class WireLog(object):
    __doc__ = "\n    Provides log files for logging 'over the wire' network tx and rx\n    for non blocking transports for debugging purposes\n    in addition to the standard console logging capability\n    "

    def __init__(self, path='', prefix='', midfix='', rx=True, tx=True, same=False, buffify=False):
        """
        Initialization method for instance.
        path = directory for log files
        prefix = prefix to include in log name if provided
        midfix = another more prefix for log name if provided
        rx = Boolean create rx log file if True
        tx = Boolean create tx log file if True
        same = Boolean use same log file for both rx and tx
        buffify = Boolean use BytesIO in memory buffer instead of File object
        """
        self.path = path
        self.prefix = prefix
        self.midfix = midfix
        self.rx = True if rx else False
        self.tx = True if tx else False
        self.same = True if same else False
        self.rxLog = None
        self.txLog = None
        self.buffify = True if buffify else False

    def reopen(self, path='', prefix='', midfix=''):
        """
        Close and then open log files on path if given otherwise self.path
        Use ha in log file name if given
        """
        self.close()
        if path:
            self.path = path
        if prefix:
            self.prefix = prefix
        elif midfix:
            self.midfix = midfix
        else:
            prefix = '{0}_'.format(self.prefix) if self.prefix else ''
            midfix = '{0}_'.format(self.midfix) if self.midfix else ''
            date = time.strftime('%Y%m%d_%H%M%S', time.gmtime(time.time()))
            if self.same and (self.rx or self.tx):
                if not self.buffify:
                    name = '{0}{1}{2}.txt'.format(prefix, midfix, date)
                    path = os.path.join(self.path, name)
                    try:
                        log = io.open(path, mode='wb+')
                        if self.rx:
                            self.rxLog = log
                        if self.tx:
                            self.txLog = log
                    except IOError:
                        self.rxLog = self.txLog = None
                        return False

                else:
                    try:
                        log = io.BytesIO()
                        if self.rx:
                            self.rxLog = log
                        if self.tx:
                            self.txLog = log
                    except IOError:
                        self.rxLog = self.txLog = None
                        return False

            else:
                if self.rx:
                    name = self.buffify or '{0}{1}{2}_rx.txt'.format(prefix, midfix, date)
                    path = os.path.join(self.path, name)
                    try:
                        self.rxLog = io.open(path, mode='wb+')
                    except IOError:
                        self.rxLog = None
                        return False

                else:
                    try:
                        self.rxLog = io.BytesIO()
                    except IOError:
                        self.rxLog = None
                        return False

        if self.tx:
            name = self.buffify or '{0}{1}{2}_tx.txt'.format(prefix, midfix, date)
            path = os.path.join(self.path, name)
            try:
                self.txLog = io.open(path, mode='wb+')
            except IOError:
                self.txLog = None
                return False

        else:
            try:
                self.txLog = io.BytesIO()
            except IOError:
                self.txLog = None
                return False

            return True

    def close(self):
        """
        Close log files
        """
        if self.txLog:
            if not self.txLog.closed:
                self.txLog.close()
        if self.rxLog:
            if not self.rxLog.closed:
                self.rxLog.close()

    def getRx(self):
        """
        Returns rx string buffer value if .buffify else None
        """
        if self.buffify:
            if self.rxLog:
                if not self.rxLog.closed:
                    return self.rxLog.getvalue()

    def getTx(self):
        """
        Returns tx string buffer value if .buffify else None
        """
        if self.buffify:
            if self.txLog:
                if not self.txLog.closed:
                    return self.txLog.getvalue()

    def writeRx(self, sa, data):
        """
        Write bytes data received from source address sa,
        """
        if self.rx:
            if self.rxLog:
                self.rxLog.write(ns2b('RX {0}\n'.format(sa)))
                self.rxLog.write(data)
                self.rxLog.write(b'\n')

    def writeTx(self, da, data):
        """
        Write bytes data transmitted to destination address da,
        """
        if self.tx:
            if self.txLog:
                self.txLog.write(ns2b('TX {0}\n'.format(da)))
                self.txLog.write(data)
                self.txLog.write(b'\n')