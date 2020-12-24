# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/src/nozama-cloudsearch/nozama-cloudsearch-service/nozama/cloudsearch/service/views.py
# Compiled at: 2013-12-03 06:00:21
"""
nozama-cloudsearch-service

"""
import pkg_resources
from pyramid.view import view_config

@view_config(route_name='home', request_method='GET', renderer='json')
@view_config(route_name='ping', request_method='GET', renderer='json')
def status(request):
    """This is used to 'ping' the web service to check if its running.

    :returns: a status dict which the configured view will return as JSON.

    The dict has the form::

        dict(
            status="ok",
            name="<project name>",
            version="<egg version of nozama.cloudsearch.service>"
        )

    """
    pkg = pkg_resources.get_distribution('nozama-cloudsearch-service')
    return dict(status='ok', name='nozama-cloudsearch-service', version=pkg.version)