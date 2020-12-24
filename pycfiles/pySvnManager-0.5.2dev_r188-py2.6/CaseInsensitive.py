# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/plugins/CaseInsensitive.py
# Compiled at: 2010-06-08 22:36:02
from pysvnmanager.hooks.plugins import *
from pysvnmanager.hooks.plugins import _

class DetectCaseInsensitiveClash(PluginBase):
    name = _('Detect case-insensitive filename clashes')
    description = _('A pre-commit hook to detect case-insensitive filename clashes.')
    detail = _("Subversion services may host on a filename case-sensitive OS,\nwhile client **may not** (Windows is case-insensitive). This may cause 'clash'.\n\n- Detects new paths that 'clash' with existing, or other new, paths.\n- Ignores existings paths that already 'clash'\n- Exits with an error code, and a diagnostic on stderr, if 'clashes'\n  are detected.\n")
    type = T_PRE_COMMIT
    key = 'detect_case_insensitive_clash'
    value = 'yes'
    section = 'pre_commit'

    def enabled(self):
        """
        Return True, if this plugin has been installed.
        Simply call 'has_config()'.
        """
        return self.has_config()

    def install_info(self):
        """
        Show configurations if plugin is already installed.
        
        return reStructuredText.
        reST reference: http://docutils.sourceforge.net/docs/user/rst/quickref.html
        """
        return self.description

    def install_config_form(self):
        """
        This method will be called to build setup configuration form.
        If this plugin needs parameters, provides form fields here.
        Any html and javascript are welcome.
        """
        return ''

    def uninstall(self):
        """
        Uninstall hooks-plugin from repository.
        Simply call 'unset_config()' and 'save()'.
        """
        self.unset_config()
        self.save()

    def install(self, params=None):
        """
        Install hooks-plugin from repository.
        Simply call 'set_config()' and 'save()'.
        
        Form fields in setup_config() will pass as params.
        """
        self.set_config()
        self.save()


def execute(repospath=''):
    """
    Generate and return a hooks plugin object

    @param request: repos full path
    @rtype: Plugin
    @return: Plugin object
    """
    return DetectCaseInsensitiveClash(repospath)