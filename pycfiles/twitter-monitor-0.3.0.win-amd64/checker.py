# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\twitter_monitor\checker.py
# Compiled at: 2015-01-30 16:40:32
import logging
logger = logging.getLogger(__name__)

class TermChecker(object):
    """
    Responsible for managing the current set of tracked terms
    and checking for updates.

    This is intended to be extended.
    """

    def __init__(self):
        self._tracking_terms_set = set()

    def update_tracking_terms(self):
        """
        Retrieve the current set of tracked terms from wherever it is stored.
        Subclasses may check in files, databases, etc...

        Should return a set of strings.
        """
        return set(['#afakehashtag'])

    def reset(self):
        """
        Clear the list of tracked terms.
        """
        self._tracking_terms_set = set()

    def check(self):
        """
        Checks if the list of tracked terms has changed.
        Returns True if changed, otherwise False.
        """
        new_tracking_terms = self.update_tracking_terms()
        terms_changed = False
        if self._tracking_terms_set > new_tracking_terms:
            logging.debug('Some tracking terms removed')
            terms_changed = True
        elif self._tracking_terms_set < new_tracking_terms:
            logging.debug('Some tracking terms added')
            terms_changed = True
        self._tracking_terms_set = new_tracking_terms
        return terms_changed

    def tracking_terms(self):
        """
        Get the current list of tracked terms.
        """
        return list(self._tracking_terms_set)


class FileTermChecker(TermChecker):
    """
    Checks for tracked terms in a file.
    """

    def __init__(self, filename):
        super(FileTermChecker, self).__init__()
        self.filename = filename

    def update_tracking_terms(self):
        """
        Terms must be one-per-line.
        Blank lines will be skipped.
        """
        import codecs
        with codecs.open(self.filename, 'r', encoding='utf8') as (input):
            lines = input.readlines()
            new_terms = set()
            for line in lines:
                line = line.strip()
                if len(line):
                    new_terms.add(line)

            return set(new_terms)