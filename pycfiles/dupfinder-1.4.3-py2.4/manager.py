# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dupfinder/manager.py
# Compiled at: 2010-01-12 03:33:41
"""Duplication manage utility.
Manage duplications files and directories in passed
inner file

%prog [options] <find_dir_1> inner_data_file
"""
import os, sys, csv
from optparse import OptionParser
import logging
DEFAULT_LOG = '/tmp/dupmanage.log'
FORMAT = '[%(asctime)s]: %(message)s'

def createHandler(hndlr_cls, level, *args, **kwargs):
    hndlr = hndlr_cls(*args, **kwargs)
    hndlr.setLevel(level)
    hndlr.setFormatter(logging.Formatter(FORMAT, datefmt='%H:%M:%S'))
    return hndlr


logger = logging.Logger('Manage Duplications', logging.NOTSET)
logger.addHandler(createHandler(logging.FileHandler, logging.DEBUG, DEFAULT_LOG))

class DupManage(object):
    """
    """
    __module__ = __name__

    def __init__(self, data_path):
        self.data = csv.DictReader(file(data_path, 'rb'))

    def manage(self):
        """ Manage items in data file
        """
        logger.info('Process items from data file')
        processed = 0
        for data in self.data:
            logger.debug(data.items())
            dirpath = os.path.abspath(data['directory'])
            path = os.path.join(dirpath, data['name'])
            oper = data['operation'].strip().upper()
            if oper == 'D':
                type_ = data['type'] == 'F' and 'file' or 'directory'
                logger.info('Remove %s %s' % (path, type_))
                try:
                    self.delItem(data['type'], path)
                except OSError, e:
                    logger.debug('%s error on deleting the item' % str(e))

            elif oper == 'L' and sys.platform.startswith('linux'):
                src_path = data['operation_data']
                try:
                    self.delItem(data['type'], path)
                except OSError, e:
                    logger.debug('%s error on deleting the item' % str(e))
                else:
                    logger.info('Symlink %s item to %s' % (src_path, path))
                    try:
                        os.symlink(src_path, path)
                    except OSError, e:
                        logger.debug('%s error on symlinking the item' % str(e))

            elif oper != '':
                logger.info("'%s' - unrecognized operation for %s" % (oper, path))
            processed += 1

        logger.info('Processed %d items' % processed)

    def delItem(self, itype, ipath):
        if itype == 'F':
            os.remove(ipath)
        else:
            for (dpath, dirs, files) in os.walk(ipath, topdown=False):
                [ os.remove(os.path.join(dpath, f)) for f in files ]
                [ os.rmdir(os.path.join(dpath, d)) for d in dirs ]

            os.rmdir(ipath)


def getConsoleParams():
    parser = OptionParser(__doc__)
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help="Show duplications manage process to console, default='%default'")
    (options, args) = parser.parse_args()
    logger.debug('Got options: %s\narguments: %s' % (str(options), str(args)))
    assert len(args) > 0, 'Path to data file is required argument'
    data_path = args[0]
    return (
     data_path, options.verbose)


def main(data_path='', verbose=False):
    if data_path == '':
        (data_path, verbose) = getConsoleParams()
    if verbose:
        logger.addHandler(createHandler(logging.StreamHandler, logging.INFO, sys.stdout))
    logger.info('Got options: %s\narguments: %s' % (verbose, data_path))
    manager = DupManage(data_path)
    manager.manage()


if __name__ == '__main__':
    main()