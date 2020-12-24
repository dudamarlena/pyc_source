# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/hooks.py
# Compiled at: 2013-12-24 05:41:42
from collective.newrelic.utils import logger
from zope.browser.interfaces import IBrowserView
from zope.browserresource.interfaces import IResource
from zope.pagetemplate.interfaces import IPageTemplate
import newrelic.agent, newrelic.api

def newrelic_transaction(event):
    try:
        request = event.request
        published = request.get('PUBLISHED', None)
        trans = newrelic.agent.current_transaction()
        transname = published.__name__
        if trans:
            if (IBrowserView.providedBy(published) or IPageTemplate.providedBy(published)) and not IResource.providedBy(published):
                trans.name_transaction(transname, group='Zope2', priority=1)
                if hasattr(published, 'context'):
                    newrelic.agent.add_custom_parameter('id', published.context.id)
                    newrelic.agent.add_custom_parameter('absolute_url', published.context.absolute_url())
                elif hasattr(published, 'id') and hasattr(published, 'absolute_url'):
                    newrelic.agent.add_custom_parameter('id', published.id)
                    newrelic.agent.add_custom_parameter('absolute_url', published.absolute_url())
                else:
                    logger.debug('Published has no context nor an id/absolute_url. Skipping custom parameters')
                logger.debug(('Transaction: {0}').format(transname))
            else:
                logger.debug(('NO transaction? : {0}   Browser: {1}  Resource: {2} PageTemplate: {3}').format(transname, IBrowserView.providedBy(published), IResource.providedBy(published), IPageTemplate.providedBy(published)))
    except Exception, e:
        logger.exception(e)

    return