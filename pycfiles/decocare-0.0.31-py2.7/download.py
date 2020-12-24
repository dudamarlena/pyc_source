# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/download.py
# Compiled at: 2015-12-16 01:43:41
import time, logging
log = logging.getLogger().getChild(__name__)
import lib, commands

class Downloader(object):
    log_format = 'logs/'

    def __init__(self, stick=None, device=None, log_format=log_format):
        self.stick = stick
        stick.open()
        self.device = device
        self.log_format = log_format

    def download(self):
        """
    Download a single page, copy paste from elsewhere.
    """
        log.info('read HISTORY DATA')
        comm = commands.ReadHistoryData(serial=self.device.serial, page=0)
        self.device.execute(comm)
        log.info('comm:READ history data page!!!:\n%s' % comm.getData())
        comm.save(prefix=self.log_format)


class PageDownloader(Downloader):
    log_format = 'logs/'

    def __init__(self, stick=None, device=None, log_format=log_format):
        self.stick = stick
        stick.open()
        self.device = device
        self.log_format = log_format

    def read_current(self):
        log.info('read cur page number')
        comm = commands.ReadCurPageNumber()
        self.device.execute(comm)
        self.pages = comm.getData()
        log.info('attempting to read %s pages of history' % self.pages)
        return self.pages

    def download_page(self, x):
        log.info('comm:XXX:READ HISTORY DATA page number: %r' % x)
        comm = commands.ReadHistoryData(serial=self.device.serial, params=[x])
        self.device.execute(comm)
        page = comm.getData()
        comm.save(prefix=self.log_format)
        log.info('XXX: READ HISTORY DATA page number %r!!:\n%s' % (x, page))
        time.sleep(0.1)

    def download(self):
        self.read_current()
        for x in range(self.pages + 1):
            log.info('read page %s' % x)
            self.download_page(x)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import sys
    port = None
    port = sys.argv[1:] and sys.argv[1] or False
    serial_num = sys.argv[2:] and sys.argv[2] or False
    if not port or not serial_num:
        print 'usage:\n%s <port> <serial>, eg /dev/ttyUSB0 208850' % sys.argv[0]
        sys.exit(1)
    import link, stick, session
    from pprint import pformat
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.info("howdy! I'm going to take a look at your pump download something info.")
    stick = stick.Stick(link.Link(port, timeout=0.4))
    stick.open()
    session = session.Pump(stick, serial_num)
    log.info(pformat(stick.interface_stats()))
    downloader = Downloader(stick, session)
    downloader.download()
    downloader = PageDownloader(stick, session)
    downloader.download()
    log.info(pformat(stick.interface_stats()))
    log.info('howdy! we downloaded everything.')