# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/utils/auto_delete.py
# Compiled at: 2008-03-10 06:37:07
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
import logging
from zope.interface import implements
from zope.component import queryUtility
from zope.app.component.hooks import getSite
from Acquisition import aq_parent
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from redomino.autodelete.config import PROJECTNAME
from redomino.autodelete.utils.interfaces import IAutoDelete
from redomino.autodelete.utils.interfaces import IAutoDeleteQuery

class AutoDeleteQuery(object):
    """ AutoDeleteQuery implementation """
    __module__ = __name__
    implements(IAutoDeleteQuery)
    _query = {'to_be_deleted': True}

    @property
    def query(self):
        return self._query


class AutoDelete(object):
    __module__ = __name__
    implements(IAutoDelete)

    def run_autodelete(self):
        """ Auto-deletes all objects expired (with autodelete actived and with delete_date < now) """
        site = getSite()
        portal_catalog = getToolByName(site, 'portal_catalog')
        logger = logging.getLogger(PROJECTNAME)
        query_utility = queryUtility(IAutoDeleteQuery)
        if query_utility:
            query = query_utility.query
        else:
            query = {'to_be_deleted': True}
        results = portal_catalog.searchResults(**query)
        results_paths = set([ item.getPath() for item in results ])
        no_paths = set()
        filtered_paths = set()
        for result1_path in results_paths:
            for result2_path in results_paths:
                query = result1_path + '/'
                if query in result2_path:
                    no_paths.add(result2_path)

        filtered_results_paths = results_paths - no_paths
        filtered_results_paths_list = [ item for item in filtered_results_paths ]
        filtered_results = filter(lambda x: x.getPath() in filtered_results_paths_list, results)
        if filtered_results:
            for result_brain in filtered_results:
                try:
                    current_title = result_brain.Title
                    current_path = result_brain.getPath()
                    current_delete_date = result_brain.delete_date
                    current_obj = result_brain.getObject()
                    parent = aq_parent(aq_inner(current_obj))
                    parent.manage_delObjects(ids=[current_obj.getId()])
                except Exception, e:
                    log_exc = '%s : %s [expired on %s] ERROR [%s]' % (current_path, current_title, current_delete_date, str(e))
                    logger.exception(log_exc)
                    yield log_exc
                else:
                    log_inf = '%s : %s [expired on %s] DELETED' % (current_path, current_title, current_delete_date)
                    logger.info(log_inf)
                    yield log_inf