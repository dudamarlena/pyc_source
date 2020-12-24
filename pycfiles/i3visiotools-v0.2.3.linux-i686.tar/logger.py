# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/logger.py
# Compiled at: 2014-12-25 06:48:18
import logging, os

def setupLogger(loggerName='i3visiotools', logFolder='./logs', verbosity=1):
    """ 
                Returns the logger to be used for the whole app. This method may be invoked if required by the launcher to update the verbosity syntax.
        
                :param loggerName:      Name of the package or app that is going to use this logger.
                :param logFolder:       Path to the folder where the information will be logged.
                :param verbosity:       Level of verbosity to be used: 
                        - 0:    Only errors.
                        - 1:    Standard output.
                        - 2:    Verbose level with rich outputs.
                        
                :return:        The logger already created.
        """
    logger = logging.getLogger(loggerName)
    loginFormat = '%(asctime)s - %(filename)s - %(levelname)s:\n\t %(message)s\n'
    formatter = logging.Formatter(loginFormat)
    if verbosity == 0:
        logging.basicConfig(level=logging.ERROR, format=loginFormat)
    else:
        if verbosity == 1:
            logging.basicConfig(level=logging.INFO, format=loginFormat)
        elif verbosity == 2:
            logging.basicConfig(level=logging.DEBUG, format=loginFormat)
        try:
            logFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), logFolder)
            if not os.path.exists(logFolder):
                os.makedirs(logFolder)
            logFile = os.path.join(logFolder, loggerName + '.log')
            handler = logging.FileHandler(logFile)
            handler.setLevel(logging.DEBUG)
            formatterLogFile = logging.Formatter(loginFormat)
            handler.setFormatter(formatterLogFile)
            logger.addHandler(handler)
        except:
            logger.warning('The log file could not be created. No log will be stored for this session.')

    logger.debug(loggerName + ' successfully imported.')
    return logger