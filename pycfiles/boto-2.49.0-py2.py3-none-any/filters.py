# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/filters.py
# Compiled at: 2012-08-16 08:17:27
__doc__ = '\nFilter class: \nInterfaces to doc_store and/or doc_manager_store to peform filtering on mongodb\nFilters file should be in JSON format\n'
import json, logging, dateutil
from botnee.doc_store import DocStore
from botnee import debug, errors

class Filters(object):
    """
    Loads filters from a json object
    """

    def __init__(self, json_object, doc_store, verbose=False):
        if type(doc_store) is not DocStore:
            raise TypeError('Expected DocStore, got ' + str(type(doc_store)))
        self.logger = logging.getLogger(__name__)
        with debug.Timer(None, None, verbose, self.logger):
            self.doc_store = doc_store
            self.load_filters(json_object, verbose)
            self.guids = self.execute(verbose)
        return

    def load_filters(self, json_object, verbose=False):
        """
        Loads the filters from a json object
        Searches for 'date' in keys, and converts to datetime object if found
        """
        with debug.Timer(None, None, verbose, self.logger):
            try:
                self.filters = json.loads(json_object)
            except ValueError, e:
                errors.FiltersWarning('Failed to parse JSON\n' + str(e), self.logger)
                self.filters = None
                return
            except TypeError, e:
                msg = 'Failed to parse JSON\n%s got %s' % (
                 str(e), str(type(json_object)))
                errors.FiltersWarning(msg, self.logger)
                self.filters = None
                return
            except Exception, e:
                errors.FiltersWarning('Failed to parse JSON\n' + str(e), self.logger)
                self.filters = None
                return
            else:
                for (key, value) in self.filters.items():
                    if key == 'publication-date':
                        for (k, v) in value.items():
                            try:
                                self.filters[key][k] = dateutil.parser.parse(v)
                                msg = 'Date parsed ok'
                                debug.print_verbose(msg, verbose, self.logger)
                            except ValueError, e:
                                msg = (
                                 'Invalid date format\n' + str(e),)
                                debug.print_verbose(msg, verbose, self.logger, logging.WARNING)
                                self.filters = None
                                return
                            except AttributeError, e:
                                msg = (
                                 'Invalid date format\n' + str(e),)
                                debug.print_verbose(msg, verbose, self.logger, logging.WARNING)
                                self.filters = None
                                return

        return

    def execute(self, verbose=False):
        """
        Performs the filter query and stores the guids
        """

        def evaluate_cursor(cursor):
            with debug.Timer(None, None, verbose, self.logger):
                return [ c['_id'] for c in cursor ]
            return

        with debug.Timer(None, None, verbose, self.logger):
            if not self.filters:
                errors.FiltersWarning('Filters not set', self.logger)
                return []
            else:
                db = self.doc_store._database
                cursor = db.docs.find(self.filters, {'_id': 1})
                msg = 'Filter resulted in %d hits' % cursor.count()
                debug.print_verbose(msg, verbose)
                guids = evaluate_cursor(cursor)
                return guids
        return

    def get_summary_as_list(self):
        """
        Gets a summary of the filters as a list of strings
        """
        msg_list = []
        if not self.filters:
            return []
        for (key, value) in self.filters.items():
            msg_list.append('%20s: %s' % (key, str(value)))

        return msg_list

    def print_summary(self, verbose=False):
        """
        Prints the summary to screen (and log)
        """
        msg_list = self.get_summary_as_list()
        for msg in msg_list:
            debug.print_verbose(msg, verbose, self.logger)