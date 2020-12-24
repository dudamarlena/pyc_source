# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/TracPostCommit.py
# Compiled at: 2010-09-03 11:31:17
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _
from webhelpers.util import html_escape

class TracPostCommit(PluginBase):
    name = _("Trac integration with subversion's post commit hook.")
    description = _('Integrate subversion with trac: Commit log of subversion appends to trac tickets if subversion commit log contains ticket id.')
    detail = ''
    type = T_POST_COMMIT
    key_switch = 'trac_post_commit_enabled'
    key_trac_env = 'trac_env'
    key_trac_repos_name = 'trac_repos_name'
    key_trac_fixed_status = 'trac_fixed_status'
    section = 'trac'

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
                result += '- ' + _('Trac post commit hook is enabled.')
            else:
                result += '- ' + _('Trac post commit hook is disabled.')
            result += '\n'
            result += '- ' + _('Trac environment location: ') + self.get_config(self.key_trac_env)
            result += '\n'
            result += '- ' + _('Repository name in trac: ') + self.get_config(self.key_trac_repos_name) or '*default*'
            result += '\n'
            result += '- ' + _("Fixed ticket's status: ") + self.get_config(self.key_trac_fixed_status) or '*default*'
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
        result += '\n<dl>'
        result += '\n<dt>'
        result += _('Enable trac post commit hook: ')
        result += '\n<dd>'
        result += "<input type='radio' name='switch' value='yes' " + enable_checked + '>' + _('Enable') + '&nbsp;'
        result += "<input type='radio' name='switch' value='no' " + disable_checked + '>' + _('Disable')
        result += '\n<dt>'
        result += _('Trac environment location: ')
        result += '\n<dd>'
        result += '<input type=\'text\' name=\'trac_env\' size=\'50\' value="%s">' % html_escape(self.get_config(self.key_trac_env))
        result += '\n<dt>'
        result += _('Repository name in trac (default is blank): ')
        result += '\n<dd>'
        result += '<input type=\'text\' name=\'trac_repos_name\' size=\'20\' value="%s">' % html_escape(self.get_config(self.key_trac_repos_name))
        result += '\n<dt>'
        result += _('Fixed ticket status (default is closed): ')
        result += '\n<dd>'
        result += '<input type=\'text\' name=\'trac_fixed_status\' size=\'10\' value="%s">' % html_escape(self.get_config(self.key_trac_fixed_status))
        result += '\n</dl>'
        result += '</blockquote>'
        return result

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config(self.key_switch)
        self.unset_config(self.key_trac_env)
        self.unset_config(self.key_trac_repos_name)
        self.unset_config(self.key_trac_fixed_status)
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
        trac_env = params.get('trac_env')
        trac_repos_name = params.get('trac_repos_name')
        trac_fixed_status = params.get('trac_fixed_status')
        log.debug('trac post commit setting: %s, %s' % (trac_env, trac_repos_name))
        if not trac_env:
            raise Exception('Trac environment not defined!')
        elif not trac_env.startswith('/'):
            raise Exception("Trac environment isn't a absolute path! It must begin with /.")
        self.set_config(self.key_switch, switch)
        self.set_config(self.key_trac_env, trac_env)
        self.set_config(self.key_trac_repos_name, trac_repos_name)
        self.set_config(self.key_trac_fixed_status, trac_fixed_status)
        self.save()


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return TracPostCommit(repospath)