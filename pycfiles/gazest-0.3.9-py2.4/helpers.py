# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/helpers.py
# Compiled at: 2007-10-25 16:57:52
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
from pylons.controllers.util import log
from pylons.i18n import get_lang, set_lang
from pylons import request, c, session, config
from pylons.templating import render
import smtplib
from request_util import *
from difflib import Differ, HtmlDiff
import difflib
from gazest import model
import os

def set_auth_cookie(username):
    request.environ['paste.auth_tkt.set_user'](username.encode('utf-8'))


def render_email(template):
    """Send a mako rendered mail.
    
    All params must be plugged in to c by the caller.  The important one is
    
    c.to_addr

    Optional ones are

    c.from_addr 
    c.subject"""
    conf = config['global_conf']
    if not c.from_addr:
        c.from_addr = conf['system_email_from']
    msg = render(template)
    server = smtplib.SMTP(conf['smtp_server'])
    server.sendmail(c.from_addr, c.to_addr, msg)
    server.quit()


def get_remote_user():
    try:
        username = request.environ['REMOTE_USER']
    except KeyError:
        return

    return model.User.query.selectfirst_by(username=username, status='active')


def pretty_date(dt):
    """Return a nice date time representation.  
    
    dt sould be a date or a datetime"""
    return '%s %s' % (dt.date(), dt.strftime('%X'))


def pretty_bool(val):
    """Return a representation of booleans suitable for the Web."""
    if not val:
        return 'no'
    if val:
        alt = 'yes'
        img = 'cr22-action-button_ok.png'
    else:
        alt = 'no'
        img = 'cr22-action-button_cancel.png'
    return '<img src="/img/%s" alt="%s" width="22" height="22" />' % (img, alt)


def fq_url_for(*args, **kwargs):
    return site_base() + url_for(*args, **kwargs)


def q_info(msg):
    """Schedule a message for flashing on the next visited page."""
    session['m_info'] = session.get('m_info', []) + [msg]
    session.save()


def q_warn(msg):
    """Schedule a warning for flashing on the next visited page."""
    session['m_warn'] = session.get('m_warn', []) + [msg]
    session.save()


def m_info(msg):
    """Add a message for flashing on visited page."""
    c.m_info.append(msg)


def m_warn(msg):
    """Add a warning for flashing on visited page."""
    c.m_warn.append(msg)


def diff_highlight(from_rev, to_rev):

    def revdesc(rev, label):
        cmt = rev.comment or 'No comment'
        if rev.id:
            url = url_for(action='past_revision', rev_id=rev.id)
            desc = '<a href="%s">%s</a> (%s)' % (url, cmt, label)
        else:
            desc = '%s (%s)' % (cmt, label)
        desc += '<br/>on %s' % pretty_date(rev.creat_date)
        desc += '<br/>by %s' % (rev.user or rev.creat_ip)
        return desc.encode('utf-8')

    differ = HtmlDiff(wrapcolumn=46)
    diff = differ.make_table(from_rev.body.encode('utf-8').split('\n'), to_rev.body.encode('utf-8').split('\n'), context=True, numlines=2, fromdesc=revdesc(from_rev, 'old'), todesc=revdesc(to_rev, 'new'))
    return unicode(diff, 'utf-8')


def diff_stats(from_rev, to_rev):
    differ = Differ()
    f_lines = from_rev.body.split('\n')
    t_lines = to_rev.body.split('\n')
    diff = differ.compare(f_lines, t_lines)
    gain = 0
    lost = 0
    for l in diff:
        if l.startswith('+'):
            gain += 1
        elif l.startswith('-'):
            lost += 1

    ratio = 1.0 * max(gain, lost) / max(min(len(f_lines), len(t_lines)), 1)
    return (gain, lost, ratio)


def diff_unified(from_rev, to_rev, context=3):
    """ Return a list of lines like the ones yuo get with 'diff -u' """
    from_user = from_rev.user and from_rev.user.username or from_rev.creat_ip
    to_user = to_rev.user and to_rev.user.username or to_rev.creat_ip
    diff = difflib.unified_diff(from_rev.body.split('\n'), to_rev.body.split('\n'), fromfile='old verion by %s' % from_user, tofile='new verion by %s' % to_user, fromfiledate=from_rev.creat_date, tofiledate=to_rev.creat_date, n=context, lineterm='')
    return diff


def diff_html_unified(from_rev, to_rev):
    """ A fully escaped HTML fragment that looks like a <pre>
    of 'diff -u' """
    lines = [ escape_once(l.rstrip()) for l in diff_unified(from_rev, to_rev) ]

    def highlight(line):
        if line.startswith('+') or line.startswith('-'):
            return '<strong>%s</strong>' % line
        elif line.startswith(' '):
            return '&#xa0;' + line[1:]
        return line

    lines = lines[:2] + map(highlight, lines[2:])
    return '<pre>%s</pre>' % ('<br/>').join(lines)


def rev_actions(rev):
    """ HTML fragment of links to actions that one can do with a
    revison"""
    actions = []
    if c.routes_dict['action'] != 'diff_form':
        actions.append((url_for(action='diff_form', slug=rev.slug), 'hist'))
    if rev.parents():
        actions += [(url_for(action='revision_diff', to_id=rev.id, slug=rev.slug), 'diff'), (url_for(action='undo_revision', rev_id=rev.id, slug=rev.slug), 'undo')]
    actions.append((url_for(action='abuse_report_form', rev_id=rev.id, slug=rev.slug), 'report abuse'))
    if has_rank('thaumaturge'):
        actions.append((url_for(action='boycott_form', controller='/admin', addr=rev.creat_ip), 'ban'))
    if actions:
        return '(%s)' % (' | ').join([ '<a href="%s">%s</a>' % (u, l) for (u, l) in actions ])
    else:
        return ''


def rank_lvl(rank):
    """ Return a rank numeric id.  Rank can be a rank number or a rank
    name. """
    try:
        lvl = int(rank)
    except ValueError:
        lvl = model.RANK_LVLS[rank]

    return lvl


def lvl_rank(lvl):
    """ Return a rank name. """
    if lvl in model.USER_RANKS:
        return lvl
    return model.USER_RANKS[lvl]


def has_rank(rank):
    """ Return true if the user is logged has at least the given rank."""
    user = get_remote_user()
    if not user:
        return False
    if user.rank >= rank_lvl(rank):
        return True
    return False