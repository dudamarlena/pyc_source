# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dave/Dropbox/github_projects/dryxPython/dryxPython/logs.py
# Compiled at: 2013-08-19 06:26:15
"""
logs.py

Initially created by David Young on October 10, 2012
If you have any questions requiring this script please email me: d.r.young@qub.ac.uk

dryx syntax:
p<Var> = variable formated in the way I want it output to file or screen
xxx = come back here and do some more work

"""
import os, sys, logging
from logging import handlers

def main():
    pass


if __name__ == '__main__':
    main()

def setup_dryx_logging(yaml_file):
    """setup dryx style python logging

    """
    import logging, logging.config, yaml
    handlers.GroupWriteRotatingFileHandler = GroupWriteRotatingFileHandler
    logging.config.dictConfig(yaml.load(open(yaml_file, 'r')))
    logger = logging.getLogger(__name__)
    return logger


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    """
    rotating file handler for logging
    """

    def doRollover(self):
        """
        Override base class method to make the new log file group writable.
        """
        handlers.RotatingFileHandler.doRollover(self)
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, currMode | stat.S_IWGRP | stat.S_IRGRP | stat.S_IWOTH | stat.S_IROTH)


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    """
    rotating file handler for logging
    """

    def _open(self):
        prevumask = os.umask(0)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv