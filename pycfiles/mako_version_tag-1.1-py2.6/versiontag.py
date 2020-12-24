# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/versiontag.py
# Compiled at: 2009-09-12 14:21:56
"""A Mako-compatible module for writing out distribution versions from
``pkg_resources``.

.. highlight:: mako

To use the functions from this module in your Mako pages, import it into
a namespace ::

   <%namespace name="v" module="versiontag"/>
"""
import mako.runtime, pkg_resources
__all__ = [
 'distribution']

def distribution(context, distribution_spec, _get_distribution=pkg_resources.get_distribution):
    """Returns the distribution version of ``distribution_spec``.
    
    For example, to write the version of this library out to the page ::
    
        ${v.distribution('mako-version-tag')}
    
    Missing distributions are replaced with the Mako ``UNDEFINED`` constant.
    """
    try:
        dist = _get_distribution(distribution_spec)
        return dist.version
    except (ValueError, pkg_resources.DistributionNotFound):
        return mako.runtime.UNDEFINED