# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/SvnSyncMaster.py
# Compiled at: 2010-09-24 05:42:38
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _
from webhelpers.util import html_escape
from subprocess import Popen, PIPE, STDOUT
import re
SVNCMD = 'LC_ALL=C svn --non-interactive --no-auth-cache --trust-server-cert '
SVNSYNCCMD = 'LC_ALL=C svnsync --non-interactive --no-auth-cache --trust-server-cert '

class SvnSyncMaster(PluginBase):
    name = _('Sync with downstream svn mirrors')
    description = _('This subversion repository is a svnsync master server. Each new commit will propagate to downstream svn mirrors.')
    detail = _('This master svn repository maybe configured with one or several svn mirrors.You must give the url svn mirrors (one with each line), and give the username and password who initiates the mirror task.')
    type = T_POST_COMMIT
    key_switch = 'mirror_enabled'
    key_username = 'mirror_username'
    key_password = 'mirror_password'
    key_urls = 'mirror_urls'
    key_debug = 'mirror_debug'
    section = 'mirror'
    passwd_re = re.compile('(password|passwd)[\\s=]+\\S+')

    def strip_password(self, command):
        return self.passwd_re.sub('password=**********', command)

    def enabled(self):
        """
        Return True, if this plugin has been installed.
        Simply call 'has_config()'.
        """
        return self.has_config(self.key_switch)

    def install_info(self):
        """
        Show configurations if plugin is already installed.
        
        return reStructuredText.
        reST reference: http://docutils.sourceforge.net/docs/user/rst/quickref.html
        """
        result = self.description
        if self.enabled():
            result += '\n\n'
            result += '**' + _('Current configuration') + '**\n\n'
            if self.get_config(self.key_switch) == 'yes':
                result += '- ' + _('Mirror enabled.')
            else:
                result += '- ' + _('Mirror disabled.')
            result += '\n'
            username = self.get_config(self.key_username)
            if username:
                result += '- ' + _('Svnsync username:') + ' ``' + username + '``'
            result += '\n'
            urls = self.get_config(self.key_urls)
            if urls:
                result += '- ' + _('Url of downstream svn mirrors:') + '\n\n'
                for url in urls.split(';'):
                    result += '  * ``' + url + '``' + '\n'

            if self.get_config(self.key_debug) == 'yes':
                result += '- debug on\n'
        return result

    def install_config_form(self):
        """
        This method will be called to build setup configuration form.
        If this plugin needs parameters, provides form fields here.
        Any html and javascript are welcome.
        """
        if self.get_config(self.key_switch) == 'no':
            enable_checked = ''
            disable_checked = 'checked'
        else:
            enable_checked = 'checked'
            disable_checked = ''
        if self.get_config(self.key_debug) == 'yes':
            enable_debug = 'checked'
            disable_debug = ''
        else:
            enable_debug = ''
            disable_debug = 'checked'
        result = ''
        result += '<p><strong>%s</strong></p>' % _('Fill this form')
        result += '<blockquote>'
        result += '<dl>'
        result += '\n<dt>'
        result += _('Enable svn repo mirror: ')
        result += '\n<dd>'
        result += "<input type='radio' name='switch' value='yes' " + enable_checked + '>' + _('Enable') + '&nbsp;'
        result += "<input type='radio' name='switch' value='no' " + disable_checked + '>' + _('Disable') + '<br>'
        result += '\n<dt>'
        result += _('Svnsync username:')
        result += '\n<dd>'
        result += "<input type='text' name='username' size='18' value='%s'>" % self.get_config(self.key_username)
        result += '\n<dt>'
        result += _('Svnsync password:')
        result += '\n<dd>'
        result += "<input type='password' name='password' size='18' value='%s'>" % self.get_config(self.key_password)
        result += '\n<dt>'
        result += _('Url of downstream svn mirrors:')
        result += '\n<dd>'
        result += "<textarea name='urls' rows='3' cols='40'>"
        result += html_escape(('\n').join(self.get_config(self.key_urls).split(';')))
        result += '</textarea>'
        result += '\n<dt>'
        result += _('Debug: ')
        result += '\n<dd>'
        result += "<input type='radio' name='debug' value='yes' " + enable_debug + '>' + _('Enable') + '&nbsp;'
        result += "<input type='radio' name='debug' value='no' " + disable_debug + '>' + _('Disable') + '<br>'
        result += '\n</dl>'
        result += '</blockquote>'
        return result

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config(self.key_username)
        self.unset_config(self.key_password)
        self.unset_config(self.key_switch)
        self.unset_config(self.key_urls)
        self.unset_config(self.key_debug)
        self.save()

    def install(self, params=None):
        """
        Install hooks-plugin from repository.
        Simply call 'set_config()' and 'save()'.
        
        Form fields in setup_config() will pass as params.
        """
        switch = params.get('switch', 'yes')
        if switch != 'yes':
            switch = 'no'
        username = params.get('username')
        password = params.get('password')
        urls = params.get('urls')
        debug = params.get('debug')
        if urls:
            urls = (';').join(urls.splitlines())
        else:
            urls = ''
        if urls == '':
            switch = 'no'
        if switch != 'no':
            self.svnsync_init(urls, username, password)
        self.set_config(self.key_switch, switch)
        self.set_config(self.key_username, username)
        self.set_config(self.key_password, password)
        self.set_config(self.key_urls, urls)
        self.set_config(self.key_debug, debug)
        self.save()

    def svnsync_init(self, urls, username, password):

        def svn_info(url, username, password):
            if username and password:
                command = SVNCMD + 'info %(url)s --username %(username)s --password %(password)s' % locals()
            else:
                command = SVNCMD + 'info %(url)s' % locals()
            proc = Popen(command, stdout=PIPE, stderr=STDOUT, close_fds=True, shell=True)
            output = proc.communicate()[0]
            if proc.returncode != 0:
                log.error('Failed when execute: %s\n\tgenerate warnings with returncode %d.' % (self.strip_password(command), proc.returncode))
                if output:
                    log.error('Command output:\n' + output)
                raise Exception('Mirror %(url)s can not access. Detail: %(output)s.' % locals())
            else:
                log.debug('command: %s' % self.strip_password(command))
                if output:
                    log.debug('output:\n' + output)
            return SVN_INFO(output)

        def svn_revprop0(url, username, password):
            if username and password:
                command = SVNCMD + 'pl -v -r0 --revprop %(url)s --username %(username)s --password %(password)s' % locals()
            else:
                command = SVNCMD + 'pl -v -r0 --revprop %(url)s' % locals()
            proc = Popen(command, stdout=PIPE, stderr=STDOUT, close_fds=True, shell=True)
            output = proc.communicate()[0]
            if proc.returncode != 0:
                log.error('Failed when execute: %s\n\tgenerate warnings with returncode %d.' % (self.strip_password(command), proc.returncode))
                if output:
                    log.error('Command output:\n' + output)
                raise Exception('Revprop of mirror %(url)s can not access. Detail: %(output)s.' % locals())
            else:
                log.debug('command: %s' % self.strip_password(command))
                if output:
                    log.debug('output:\n' + output)
            return SVN_SYNC_INFO(output)

        sinfo = svn_info('file://' + self.repos, None, None)
        for url in urls.split(';'):
            cmdlist = []
            dinfo = svn_info(url, username, password)
            if sinfo.uuid != dinfo.uuid:
                raise Exception('UUID not matched, %s not like a mirror.' % url)
            uuid = sinfo.uuid
            sync_info = svn_revprop0(url, username, password)
            srcurl = 'file://' + self.repos
            if sync_info.sync_url is None:
                if dinfo.rev is None or int(dinfo.rev) == 0:
                    if username and password:
                        cmdlist.append(SVNSYNCCMD + 'init %(url)s %(srcurl)s --sync-username %(username)s --sync-password %(password)s' % locals())
                    else:
                        cmdlist.append(SVNSYNCCMD + 'init %(url)s %(srcurl)s' % locals())
                else:
                    newrev = dinfo.rev
                    if username and password:
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-last-merged-rev %(newrev)s %(url)s --username %(username)s --password %(password)s' % locals())
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-url %(srcurl)s %(url)s --username %(username)s --password %(password)s' % locals())
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-uuid %(uuid)s %(url)s --username %(username)s --password %(password)s' % locals())
                    else:
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-last-merged-rev %(newrev)s %(url)s' % locals())
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-url %(srcurl)s %(url)s' % locals())
                        cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-uuid %(uuid)s %(url)s' % locals())
            elif sync_info.sync_url and sync_info.sync_url != srcurl:
                if username and password:
                    cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-url %(srcurl)s %(url)s --username %(username)s --password %(password)s' % locals())
                else:
                    cmdlist.append(SVNCMD + 'ps --revprop -r0 svn:sync-from-url %(srcurl)s %(url)s' % locals())
            for command in cmdlist:
                proc = Popen(command, stdout=PIPE, stderr=STDOUT, close_fds=True, shell=True)
                output = proc.communicate()[0]
                if proc.returncode != 0:
                    log.error('Failed when execute: %s\n\tgenerate warnings with returncode %d.' % (self.strip_password(command), proc.returncode))
                    if output:
                        log.error('Command output:\n' + output)
                    raise Exception('Failed when execute: %(command)s\n   Detail: %(output)s.' % {'command': self.strip_password(command), 
                       'output': output})
                else:
                    log.debug('command: %s' % self.strip_password(command))
                    if output:
                        log.debug('output:\n' + output)

        return


class SVN_INFO(object):

    def __init__(self, output):
        self.url = None
        self.root = None
        self.uuid = None
        self.rev = None
        if output:
            self.parse(output)
        return

    def parse(self, output):
        if output:
            if isinstance(output, (str, unicode)):
                output = output.splitlines()
            for line in output:
                if line.startswith('URL:'):
                    self.url = line.split(':', 1)[1].strip()
                elif line.startswith('Repository Root:'):
                    self.root = line.split(':', 1)[1].strip()
                elif line.startswith('Repository UUID:'):
                    self.uuid = line.split(':', 1)[1].strip()
                elif line.startswith('Revision:'):
                    self.rev = line.split(':', 1)[1].strip()


class SVN_SYNC_INFO(object):

    def __init__(self, output):
        self.sync_url = None
        self.sync_uuid = None
        self.sync_rev = None
        if output:
            self.parse(output)
        return

    def parse(self, output):
        if output:
            if isinstance(output, (str, unicode)):
                output = output.splitlines()
            i = 0
            while True:
                if i >= len(output):
                    break
                if output[i].strip().startswith('svn:sync-from-uuid'):
                    i += 1
                    self.sync_uuid = output[i].strip()
                elif output[i].strip().startswith('sync-last-merged-rev'):
                    i += 1
                    self.sync_rev = output[i].strip()
                elif output[i].strip().startswith('svn:sync-from-url'):
                    i += 1
                    self.sync_url = output[i].strip()
                i += 1


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return SvnSyncMaster(repospath)