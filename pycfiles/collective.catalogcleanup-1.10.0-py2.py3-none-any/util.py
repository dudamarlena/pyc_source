# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/castle/util.py
# Compiled at: 2010-08-09 05:35:03
from Products.CMFCore.utils import getToolByName
from urllib import quote
from Products.statusmessages.interfaces import IStatusMessage
from collective.castle import CastleMessageFactory as _

def URL(context):
    return context.restrictedTraverse('@@plone').getCurrentUrl()


def get_cas_plugin(context):
    acl_users = getToolByName(context, 'acl_users')
    cas_auth_helpers = acl_users.objectValues(['CAS Auth Helper'])
    if cas_auth_helpers:
        return cas_auth_helpers[0]


def login_URL_base(context):
    p = get_cas_plugin(context)
    if p:
        return p.getLoginURL()


def login_query_string(context):
    quoted_here_url = mtool = quote(URL(context), '')
    querystring = '?came_from=%s' % quoted_here_url
    portal = getToolByName(context, 'portal_url')()
    if portal[-1:] == '/':
        portal = portal[:-1]
    service_URL = '%s/logged_in%s' % (portal, querystring)
    return '?service=%s' % quote(service_URL, '')


def login_URL(context):
    base = login_URL_base(context)
    if base is None:
        request = context.request
        IStatusMessage(request).addStatusMessage(_('CAS Login is not available. Please configure CAS'), type='warning')
        return
    return '%s%s' % (base, login_query_string(context))


def logout(context, request):
    mt = getToolByName(context, 'portal_membership')
    p = get_cas_plugin(context)
    mt.logoutUser(REQUEST=request)
    session = request.SESSION
    if session.has_key(p.session_var):
        session[p.session_var] = None
    portal = quote(getToolByName(context, 'portal_url').getPortalObject().absolute_url())
    IStatusMessage(request).addStatusMessage(_('You are now logged out.'), type='info')
    return request.RESPONSE.redirect('%s?url=%s' % (p.logout_url, portal))