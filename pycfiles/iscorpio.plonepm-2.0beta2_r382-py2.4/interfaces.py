# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/portlets/interfaces.py
# Compiled at: 2009-11-12 02:06:02
"""
defines the marker interfaces for portlets.  All portlet should implement
interface IPortletDataProvider.
"""
from plone.portlets.interfaces import IPortletDataProvider
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class IProjectOverviewPortlet(IPortletDataProvider):
    """
    The marker interface for project overview portlet.
    """
    __module__ = __name__


class IProjectSimpleNavPortlet(IPortletDataProvider):
    """
    The marker interface for project simple navigation portlet.
    """
    __module__ = __name__


class IRecentArtifactsPortlet(IPortletDataProvider):
    """
    the marker interface for a portlet to list recent changed artifacts.
    """
    __module__ = __name__


class IStoryFactsPortlet(IPortletDataProvider):
    """
    The marker interface for the story facts portlet.
    """
    __module__ = __name__