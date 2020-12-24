# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hgmonitor/__init__.py
# Compiled at: 2012-07-25 21:23:47
"""batch handling of all repositories under a directory"""
from mercurial import cmdutil, commands, hg, mail, patch, extensions
from mercurial.i18n import _
from hgmonlib import monitor_cmd, mlist_cmd, mbackup_cmd, mpull_cmd, mpush_cmd
commands.norepo += ' monitor mlist mbackup mpull mpush'
emailopts = [
 (
  '', 'bcc', [], _('email addresses of blind carbon copy recipients')),
 (
  'c', 'cc', [], _('email addresses of copy recipients')),
 (
  's', 'subject', 'Repository crumbs:  {basename}',
  _('subject of e-mail message (sent sent)')),
 (
  '', 'email', '', _('email address to notify'))]
base_mon_commands = [
 (
  'd', 'dir', [], _('directory which contains repositories to traverse'))]
mqopts = [
 (
  '', 'mq', False, _('include patch queue sub-repositories (if existing)'))]
cmdtable = {'monitor': [
             monitor_cmd,
             [
              (
               'u', 'unknown', False, _('include unknown files as crumbs'))] + base_mon_commands + emailopts,
             _('hg monitor [--dir <directory>]')], 
   'mlist': [
           mlist_cmd,
           base_mon_commands[:],
           _('hg mlist [--dir <directory>]')], 
   'mpull': [
           mpull_cmd,
           [
            (
             '', 'update', False, _('update after pull in all repositories'))] + base_mon_commands,
           _('hg mpull  [--dir <directory>]')], 
   'mbackup': [
             mbackup_cmd,
             [
              (
               'u', 'unknown', False, _('include unknown files as crumbs')),
              (
               '', 'dest', '{sysname}-{clone}-{datetime}.zip',
               _('backup file-name in .hg/mbackup')),
              (
               'r', 'remote', '', _('remote destination for offsite'))] + base_mon_commands,
             _('hg mbackup [--dir <directory>]')], 
   'mpush': [
           mpush_cmd,
           base_mon_commands[:],
           _('hg mpush [--dir <directory>]')]}

def extsetup():
    """
    Add mq support on all commands if mq available.
    
    Add fetch and rebase on mpull if available.
    """
    fetch_ext = rebase_ext = mq_ext = None
    try:
        fetch_ext = extensions.find('fetch')
    except KeyError as e:
        pass

    try:
        rebase_ext = extensions.find('rebase')
    except KeyError as e:
        pass

    try:
        mq_ext = extensions.find('mq')
    except KeyError as e:
        pass

    if fetch_ext is not None:
        cmdtable['mpull'][1] += [('', 'fetch', False, _('fetch after pull in all repositories'))]
    if rebase_ext is not None:
        cmdtable['mpull'][1] += [('', 'rebase', False, _('rebase after pull in all repositories'))]
    if mq_ext is not None:
        cmdtable['monitor'][1] += mqopts
        cmdtable['mlist'][1] += mqopts
        cmdtable['mpull'][1] += mqopts
        cmdtable['mpush'][1] += mqopts
    return


__version_info__ = ['0', '5']
__version__ = ('.').join(__version_info__)