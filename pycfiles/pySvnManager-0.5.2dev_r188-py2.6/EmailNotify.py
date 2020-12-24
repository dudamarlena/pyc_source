# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/EmailNotify.py
# Compiled at: 2010-09-03 11:31:17
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _
from webhelpers.util import html_escape

class EmailNotify(PluginBase):
    name = _('Send email notify for commit event')
    description = _('Send a notification email describing either a commit or a revprop-change action on a Subversion repository.')
    detail = _("\nYou must provide proper options to commit-email.pl using the\nconfiguration form for this plugin.\n\nYou can simply just provide the email_addr as the options.\n\n  [options] email_addr [email_addr ...]\n\nBut to be more versitile, you can setup a path-based email \nnotifier.\n\n  [-m regex1] [options] [email_addr ...]\n  [-m regex2] [options] [email_addr ...] \n  ...\n\nOptions:\n\n-m regex              Regular expression to match committed path\n--from email_address  Email address for 'From:' (overrides -h)\n-r email_address      Email address for 'Reply-To:\n-s subject_prefix     Subject line prefix\n--diff n              Do not include diff in message (default: y)\n")
    type = T_POST_COMMIT
    key_switch = 'email_notify_enable'
    key_config = 'email_notify_config'
    section = 'email'

    def enabled(self):
        """
        Return True, if this plugin has been installed.
        Simply call 'has_config()'.
        """
        return self.has_config(self.key_switch) and self.has_config(self.key_config)

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
                result += '- ' + _('Email notify enabled.')
            else:
                result += '- ' + _('Email notify disabled.')
            result += '\n'
            result += '- ' + _('Parameters: ') + '``' + self.get_config(self.key_config) + '``\n'
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
        result = ''
        result += '<p><strong>%s</strong></p>' % _('Fill this form')
        result += '<blockquote>'
        result += '<dl>'
        result += '\n<dt>'
        result += _('Enable email notify.')
        result += '\n<dd>'
        result += "<input type='radio' name='switch' value='yes' " + enable_checked + '>' + _('Enable') + '&nbsp;'
        result += "<input type='radio' name='switch' value='no' " + disable_checked + '>' + _('Disable') + '<br>'
        result += '\n<dt>'
        result += _('Input email notify configurations: ')
        result += '\n<dd>'
        result += "<textarea name='config' rows='5' cols='40'>"
        result += html_escape(self.get_config(self.key_config))
        result += '</textarea>'
        result += '\n</dl>'
        result += '</blockquote>'
        return result

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config(self.key_config)
        self.unset_config(self.key_switch)
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
        config = params.get('config')
        if not config:
            raise Exception, _('Wrong configuration.')
        self.set_config(self.key_switch, switch)
        self.set_config(self.key_config, config)
        self.save()


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return EmailNotify(repospath)