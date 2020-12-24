# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/sentry_tracpost/plugin.py
# Compiled at: 2012-08-17 05:02:37
from django import forms
import socket, sys, xmlrpclib, os
from array import array
from sentry.conf import settings
from sentry.plugins import Plugin
from sentry.models import Group
import pprint, sentry_tracpost

class TracPostOptionsForm(forms.Form):
    xmlrpc_url = forms.CharField(required=True, label='Trac XMLRPC URL', help_text='e.g. https://user:pass@hostname.com:91/trac/login/rpc')


class TracPost(Plugin):
    title = 'TracPost'
    author = 'Josh Harwood'
    conf_title = 'TracPost'
    conf_key = 'tracpost'
    project_conf_form = TracPostOptionsForm

    def is_configured(self, project):
        return all(self.get_option(k, project) for k in 'xmlrpc_url')

    def send_message(self, group_id, **kwargs):
        print 'i at least am called'
        group = Group.object.get(pk=group_id)
        if not self.is_configured(group.project):
            return
        else:
            rpc_srv = xmlrpclib.ServerProxy(self.get_option('xmlrpc_url', group.project), allow_none=True)
            socket.setdefaulttimeout(30)
            attrs = {'priority': 'minor'}
            if group.message != None:
                pp = pprint.PrettyPrinter(indent=4)
                ticket_id = rpc_srv.ticket.create(group.message, '{{{\n' + str(pp.pformat(group.data)) + '\n}}}\n\nSee Sentry Page @ http://sentry.joinerysoft-directory.co.uk/jms/group/' + str(event.group_id), {'priority': 'minor'}, False)
                print 'New Ticket - ' + str(ticket_id)
            else:
                print 'Something Went Wrong'
            return self.render('<html>Test</html>')

    def actions(self, request, group, action_list, **kwargs):
        action_list.append(('Send to Trac', 'http://google.com'))
        return action_list


def start(request, group_id):
    print 'Got to start - URL Works'
    tp = Tracpost()
    print 'Can Init Tracpost'
    response = tp.send_message(group_id)
    print 'Ticket Got Sent!'
    return response