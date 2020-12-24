# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/niteoweb.plr/src/niteoweb.aweber/src/niteoweb/aweber/aweberapi.py
# Compiled at: 2013-02-08 05:15:09
"""Integration with Aweber API."""
from aweber_api import AWeberAPI
from plone import api

def subscribe_to_aweber_mailinglist(email, fullname):
    """Subscribe a member to Aweber mailinglist.

    :param email: email address of user to subscribe
    :type email: string
    :param fullname: full name of the user related to previous argument
    :type fullname: string
    """
    consumer_key = api.portal.get_registry_record('niteoweb.aweber.interfaces.IAweberSettings.consumer_key')
    consumer_secret = api.portal.get_registry_record('niteoweb.aweber.interfaces.IAweberSettings.consumer_secret')
    access_token = api.portal.get_registry_record('niteoweb.aweber.interfaces.IAweberSettings.access_token')
    access_secret = api.portal.get_registry_record('niteoweb.aweber.interfaces.IAweberSettings.access_secret')
    list_name = api.portal.get_registry_record('niteoweb.aweber.interfaces.IAweberSettings.list_name')
    aweber = AWeberAPI(consumer_key, consumer_secret)
    account = aweber.get_account(access_token, access_secret)
    list_ = account.lists.find(name=list_name)[0]
    list_url = '/accounts/%s/lists/%s' % (account.id, list_.id)
    list_ = account.load_from_url(list_url)
    params = {'email': email, 
       'name': fullname}
    list_.subscribers.create(**params)