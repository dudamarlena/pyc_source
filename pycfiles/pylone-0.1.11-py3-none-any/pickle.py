# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pylon\io\pickle.py
# Compiled at: 2010-12-26 13:36:33
__doc__ = ' Defines a reader of pickled cases.\n'
import os.path, cPickle as pickle, logging
from pylon.io.common import _CaseReader, _CaseWriter
logger = logging.getLogger(__name__)

class PickleReader(_CaseReader):
    """ Defines a reader for pickled cases.
    """

    def read(self, file_or_filename):
        """ Loads a pickled case.
        """
        if isinstance(file_or_filename, basestring):
            fname = os.path.basename(file_or_filename)
            logger.info('Unpickling case file [%s].' % fname)
            file = None
            try:
                try:
                    file = open(file_or_filename, 'rb')
                except:
                    logger.error('Error opening %s.' % fname)
                    return

            finally:
                if file is not None:
                    case = pickle.load(file)
                    file.close()

        else:
            file = file_or_filename
            case = pickle.load(file)
        return case


class PickleWriter(_CaseWriter):
    """ Writes a case to file using pickle.
    """

    def write(self, file_or_filename):
        """ Writes the case to file using pickle.
        """
        if isinstance(file_or_filename, basestring):
            fname = os.path.basename(file_or_filename)
            logger.info('Pickling case [%s].' % fname)
            file = None
            try:
                try:
                    file = open(file_or_filename, 'wb')
                except:
                    logger.error("Error opening '%s'." % fname)
                    return False

            finally:
                if file is not None:
                    pickle.dump(self.case, file)
                    file.close()

        else:
            file = file_or_filename
            pickle.dump(file, self.case)
        return True