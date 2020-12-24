# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/config/routing.py
# Compiled at: 2007-10-26 04:41:08
"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.connect('error/:action/:id', controller='error')
    map.connect('/robots.txt', controller='robots', action='index')
    map.connect('/', controller='wiki', action='index')
    map.connect('/about', controller='wiki', action='about')
    map.connect('/contact', controller='home', action='contact')
    map.connect('/recent_changes', controller='wiki', action='recent_changes')
    map.connect('/recent_changes_atom', controller='wiki', action='site_atom')
    map.connect('/random_page', controller='wiki', action='random_page')
    map.connect('/search', controller='search', action='results')
    map.connect('/adm/boycott_form/:addr', controller='admin', action='boycott_form')
    map.connect('/adm/:action', controller='admin')
    map.connect('/login', controller='visitor', action='login')
    map.connect('/login_email', controller='visitor', action='login_email_action')
    map.connect('/login_openid', controller='visitor', action='login_openid_action')
    map.connect('/login_openid_conf', controller='visitor', action='login_openid_conf')
    map.connect('/logout', controller='visitor', action='logout')
    map.connect('/register', controller='visitor', action='register')
    map.connect('/confirm_openid/:username/:key', controller='visitor', action='confirm_openid')
    map.connect('/confirm/:username/:key', controller='visitor', action='confirm_email')
    map.connect('/confirm_action/:username/:key', controller='visitor', action='confirm_email_action')
    map.connect('/u/:username', controller='visitor', action='user_profile')
    map.connect('/u/:username/edit', controller='visitor', action='user_profile_edit_form')
    map.connect('/u/:username/edit_action', controller='visitor', action='user_profile_edit_action')
    map.connect('/msg', controller='gazmail', action='inbox')
    map.connect('/msg/compose', controller='gazmail', action='compose_form')
    map.connect('/msg/compose_form_action', controller='gazmail', action='compose_form_action')
    map.connect('/msg/read/:msg_id', controller='gazmail', action='message_read', requirements=dict(msg_id='\\d+'))
    map.connect('/msg/reply/:msg_id', controller='gazmail', action='message_reply_form', requirements=dict(msg_id='\\d+'))
    map.connect('/msg/reply_action/:msg_id', controller='gazmail', action='message_reply_action', requirements=dict(msg_id='\\d+'))
    map.connect('/msg/read/:msg_id/important', controller='gazmail', action='message_make_important', requirements=dict(msg_id='\\d+'))
    map.connect('/msg/read/:msg_id/unimportant', controller='gazmail', action='message_make_unimportant', requirements=dict(msg_id='\\d+'))
    map.connect('/msg/read/:msg_id/delete', controller='gazmail', action='message_delete', requirements=dict(msg_id='\\d+'))
    map.connect('/wiki/*slug/rev/:rev_id', controller='wiki', action='past_revision', requirements=dict(rev_id='\\d+'))
    map.connect('/wiki/*slug/abuse_report/:rev_id', controller='wiki', action='abuse_report_form', requirements=dict(rev_id='\\d+'))
    map.connect('/wiki/*slug/abuse_report_action/:rev_id', controller='wiki', action='abuse_report_action', requirements=dict(rev_id='\\d+'))
    map.connect('/wiki/*slug/undo/:rev_id', controller='wiki', action='undo_revision', requirements=dict(rev_id='\\d+'))
    map.connect('/wiki/*slug/diff/:to_id/:from_id', controller='wiki', action='revision_diff', from_id=None, requirements=dict(from_id='\\d+', to_id='\\d+'))
    map.connect('/wiki/*slug/hist', controller='wiki', action='diff_form')
    map.connect('/wiki/*slug/atom', controller='wiki', action='page_atom')
    map.connect('/wiki/*slug/edit', controller='wiki', action='edit_form')
    map.connect('/wiki/*slug/edit_action', controller='wiki', action='edit_action')
    map.connect('/wiki/*slug', controller='wiki', action='view')
    map.connect('/wiki', controller='wiki', action='index')
    map.connect('/dagimg/arc/:top/:bottom/:mid', controller='dagimage', action='arc', top='0', mid='0', bottom='0', requirements=dict(top='\\d+', mid='\\d+', bottom='\\d+'))
    map.connect('/dagimg/node/:top/:bottom', controller='dagimage', action='node', top='0', bottom='0', requirements=dict(top='\\d+', bottom='\\d+'))
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')
    return map