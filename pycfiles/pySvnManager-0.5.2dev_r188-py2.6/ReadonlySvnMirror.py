# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/ReadonlySvnMirror.py
# Compiled at: 2010-06-08 22:36:02
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _

class ReadonlySvnMirror(PluginBase):
    name = _('Subversion readonly mirror')
    description = _('This subversion repository is a svnsync readonly mirror. Nobody can checkin, except the svnsync admin user.')
    detail = _("Commit to the remote svn server, this repository is a readonly svn mirror.It is the svnsync admin's duty to synchronize svnsync server and mirror.")
    type = T_START_COMMIT
    key_switch = 'mirror_readonly'
    key_admin = 'mirror_admin'
    section = 'start_commit'

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
                result += '- ' + _('Readonly mirror enabled.')
            else:
                result += '- ' + _('Readonly mirror disabled.')
            result += '\n'
            admin = self.get_config(self.key_admin)
            if admin:
                result += '- ' + _('Admin user: ') + '``' + self.get_config(self.key_admin) + '``'
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
        result += _('Enable readonly mirror: ')
        result += '\n<dd>'
        result += "<input type='radio' name='switch' value='yes' " + enable_checked + '>' + _('Enable') + '&nbsp;'
        result += "<input type='radio' name='switch' value='no' " + disable_checked + '>' + _('Disable') + '<br>'
        result += '\n<dt>'
        result += _('Svnsync administrator: ')
        result += '\n<dd>'
        result += "<input type='text' name='admin' size='18' value='%s'>" % self.get_config(self.key_admin)
        result += '\n</dl>'
        result += '</blockquote>'
        return result

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config(self.key_admin)
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
        admin = params.get('admin')
        if not admin:
            switch = 'no'
        self.set_config(self.key_switch, switch)
        self.set_config(self.key_admin, admin)
        self.save()


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return ReadonlySvnMirror(repospath)