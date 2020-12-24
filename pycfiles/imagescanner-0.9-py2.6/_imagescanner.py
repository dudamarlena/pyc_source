# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagescanner/core/_imagescanner.py
# Compiled at: 2011-05-14 11:23:48
"""Imagescanner main class. All embeded backends are loaded here.

$Id: _imagescanner.py,v b51df4bf61b9 2011/05/14 17:23:48 seocam $"""
import os, logging
from importlib import import_module
from imagescanner import settings
POSIX_BACKEND = 'imagescanner.backends.sane'
NT_BACKEND = 'imagescanner.backends.twain'
NETWORK_BACKEND = 'imagescanner.backends.net'
TEST_BACKEND = 'imagescanner.backends.test'
BACKENDS = getattr(settings, 'BACKENDS', None)

class ImageScanner(object):
    """Implements the interface from the backends with the lib."""

    def __init__(self, **kwargs):
        """Load the appropriate backends and its scanner managers.
    
        All keyword arguments are also passed to the constructor
        of each one of the ScannerManager.

        """
        self.managers = []
        backends = []
        if os.name == 'posix':
            logging.debug('Posix backend enabled (%s)', POSIX_BACKEND)
            backends.append(POSIX_BACKEND)
        elif os.name == 'nt':
            logging.debug('NT backend enabled (%s)', NT_BACKEND)
            backends.append(NT_BACKEND)
        if getattr(settings, 'ENABLE_TEST_BACKEND', False):
            logging.debug('Test backend enabled (%s)', TEST_BACKEND)
            backends.append(TEST_BACKEND)
        if getattr(settings, 'ENABLE_NET_BACKEND', False):
            logging.debug('Network backend enabled (%s)', NETWORK_BACKEND)
            backends.append(NETWORK_BACKEND)
        if BACKENDS is not None:
            logging.debug('Adding user backends (%s)', BACKENDS)
            backends.extend(BACKENDS)
        for backend in backends:
            try:
                logging.debug('Importing %s', backend)
                backend_module = import_module(backend)
            except Exception, exc:
                logging.warning('Error importing %s [skiping]', backend)
                logging.warning(exc)
                continue

            try:
                manager = backend_module.ScannerManager(**kwargs)
            except AttributeError:
                logging.error('Backend %s does not implement ScannerManager class [skiping]', backend)
                continue

            self.managers.append(manager)

        return

    def list_scanners(self):
        """List all devices for all the backends available"""
        logging.debug('Looking for all scanner devices')
        scanners = []
        for manager in self.managers:
            scanners.extend(manager.list_scanners())

        logging.debug('Found scanners: %s', scanners)
        return scanners

    def get_scanner(self, scanner_id):
        """Get the device with the given ID"""
        logging.debug('Looking for scanner with id: %s', scanner_id)
        scanner = None
        for manager in self.managers:
            scanner = manager.get_scanner(scanner_id)
            if scanner is not None:
                logging.debug('Scanner %s found', scanner_id)
                return scanner

        logging.debug('Scanner %s not found', scanner_id)
        return

    def scan(self, scanner_id, **kwargs):
        """Shortcut for scanning without get the device"""
        logging.debug('Trying to scan using: %s and %s', scanner_id, kwargs)
        scanner = self.get_scanner(scanner_id)
        if scanner is not None:
            return scanner.scan(**kwargs)
        else:
            logging.info('Scan failed. Scanner %s not found', scanner_id)
            return