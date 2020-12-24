# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/comicvine_ui.py
# Compiled at: 2010-09-01 16:36:47
__doc__ = 'Contains included user interfaces for Comicvine series selection.\nModified from http://github.com/dbr/tvdb_api\n\nA UI is a callback. A class, it\'s __init__ function takes two arguments:\n\n- config, which is the Comicvine config dict, setup in comicvine_api.py\n- log, which is Comicvine\'s logger instance (which uses the logging module). You can\ncall log.info() log.warning() etc\n\nIt must have a method "selectSeries", this is passed a list of dicts, each dict\ncontains the the keys "name" (human readable series name), and "sid" (the series\nID as on comicvine.com). For example:\n\n[{\'name\': u\'Lost\', \'sid\': u\'73739\'},\n {\'name\': u\'Lost Universe\', \'sid\': u\'73181\'}]\n\nThe "selectSeries" method must return the appropriate dict, or it can raise\ncomicvine_userabort (if the selection is aborted), comicvine_seriesnotfound (if the series\ncannot be found).\n\nA simple example callback, which returns a random series:\n\n>>> import random\n>>> from comicvine_ui import BaseUI\n>>> class RandomUI(BaseUI):\n...    def selectSeries(self, allSeries):\n...            import random\n...            return random.choice(allSeries)\n\nThen to use it..\n\n>>> from comicvine_api import Comicvine\n>>> c = Comicvine(custom_ui = RandomUI)\n>>> random_matching_series = c[\'Fables\']\n>>> type(random_matching_series)\n<class \'comicvine_api.Series\'>\n'
__author__ = 'swc/Steve'
__version__ = '1.01'
import logging, warnings
from comicvine_exceptions import comicvine_userabort

def log():
    return logging.getLogger(__name__)


class BaseUI:
    """Default non-interactive UI, which auto-selects first results
    """

    def __init__(self, config, log=None):
        self.config = config
        if log is not None:
            warnings.warn("the UI's log parameter is deprecated, instead use\nuse import logging; logging.getLogger('ui').info('blah')\nThe self.log attribute will be removed in the next version")
            self.log = logging.getLogger(__name__)
        return

    def selectSeries(self, allSeries):
        return allSeries[0]


class ConsoleUI(BaseUI):
    """Interactively allows the user to select a series from a console based UI
    """

    def _displaySeries(self, allSeries):
        """Helper function, lists series with corresponding ID
        """
        print 'ComicVine Search Results:'
        for (i, cseries) in enumerate(allSeries[:6]):
            i_series = i + 1
            log().debug('Showing allSeries[%s], series %s)' % (i_series, allSeries[i]['seriesname']))
            print '%s -> %s # http://api.comicvine.com/series/%s/' % (
             i_series,
             cseries['seriesname'].encode('UTF-8', 'ignore'),
             str(cseries['id']))

    def selectSeries(self, allSeries):
        self._displaySeries(allSeries)
        if len(allSeries) == 1:
            print 'Automatically selecting only result'
            return allSeries[0]
        if self.config['select_first'] is True:
            print 'Automatically returning first search result'
            return allSeries[0]
        while True:
            try:
                print 'Enter choice (first number, ? for help):'
                ans = raw_input()
            except KeyboardInterrupt:
                raise comicvine_userabort('User aborted (^c keyboard interupt)')
            except EOFError:
                raise comicvine_userabort('User aborted (EOF received)')

            log().debug('Got choice of: %s' % ans)
            try:
                selected_id = int(ans) - 1
            except ValueError:
                if ans == 'q':
                    log().debug('Got quit command (q)')
                    raise comicvine_userabort("User aborted ('q' quit command)")
                elif ans == '?':
                    print '## Help'
                    print '# Enter the number that corresponds to the correct series.'
                    print '# ? - this help'
                    print '# q - abort comicnamer'
                else:
                    log().debug('Unknown keypress %s' % ans)
            else:
                log().debug('Trying to return ID: %d' % selected_id)
                try:
                    return allSeries[selected_id]
                except IndexError:
                    log().debug('Invalid series number entered!')
                    print 'Invalid number (%s) selected!'
                    self._displaySeries(allSeries)