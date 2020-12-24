# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/data/vulnerability/infrastructure/outdated_platform.py
# Compiled at: 2014-02-05 05:50:56
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from .. import Vulnerability

class OutdatedPlatform(Vulnerability):
    """"""
    DEFAULTS = Vulnerability.DEFAULTS.copy()
    DEFAULTS['level'] = 'high'
    DEFAULTS['cvss_base'] = '9'
    DEFAULTS['description'] = 'An outdated, potentially vulnerable platform was found.'
    DEFAULTS['solution'] = 'If possible, apply all missing patches or upgrade to a newer version.\nIf not, consider adding firewall rules to restrict access to these hosts.'
    DEFAULTS['references'] = ('https://www.owasp.org/index.php/Top_10_2013-A5-Security_Misconfiguration', )


class OutdatedPlatformMandriva(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/mandriva'

    @property
    def display_name(self):
        return 'Outdated Platform: Mandriva'


class OutdatedPlatformWindows(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/windows'

    @property
    def display_name(self):
        return 'Outdated Platform: Windows'


class OutdatedPlatformDebian(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/debian'

    @property
    def display_name(self):
        return 'Outdated Platform: Debian'


class OutdatedPlatformMacOSX(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/mac_os_x'

    @property
    def display_name(self):
        return 'Outdated Platform: Mac OS X'


class OutdatedPlatformVMwareESX(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/vmware_esx'

    @property
    def display_name(self):
        return 'Outdated Platform: VMware ESX'


class OutdatedPlatformUbuntu(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/ubuntu'

    @property
    def display_name(self):
        return 'Outdated Platform: Ubuntu'


class OutdatedPlatformHPUX(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/hp_ux'

    @property
    def display_name(self):
        return 'Outdated Platform: HP-UX'


class OutdatedPlatformSuSE(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/suse'

    @property
    def display_name(self):
        return 'Outdated Platform: SuSE'


class OutdatedPlatformFreeBSD(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/freebsd'

    @property
    def display_name(self):
        return 'Outdated Platform: FreeBSD'


class OutdatedPlatformJunos(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/junos'

    @property
    def display_name(self):
        return 'Outdated Platform: JunOS'


class OutdatedPlatformScientificLinux(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/sci_linux'

    @property
    def display_name(self):
        return 'Outdated Platform: Scientific Linux'


class OutdatedPlatformSlackware(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/slackware'

    @property
    def display_name(self):
        return 'Outdated Platform: Slackware'


class OutdatedPlatformSolaris(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/solaris'

    @property
    def display_name(self):
        return 'Outdated Platform: Solaris'


class OutdatedPlatformRedHat(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/redhat'

    @property
    def display_name(self):
        return 'Outdated Platform: Red Hat'


class OutdatedPlatformAmazonLinux(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/amazon'

    @property
    def display_name(self):
        return 'Outdated Platform: Amazon Linux'


class OutdatedPlatformAIX(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/aix'

    @property
    def display_name(self):
        return 'Outdated Platform: AIX'


class OutdatedPlatformGentoo(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/gentoo'

    @property
    def display_name(self):
        return 'Outdated Platform: Gentoo'


class OutdatedPlatformCentOS(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/centos'

    @property
    def display_name(self):
        return 'Outdated Platform: CentOS'


class OutdatedPlatformOracleLinux(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/oracle'

    @property
    def display_name(self):
        return 'Outdated Platform: Oracle Linux'


class OutdatedPlatformFedora(OutdatedPlatform):
    vulnerability_type = OutdatedPlatform.vulnerability_type + '/fedora'

    @property
    def display_name(self):
        return 'Outdated Platform: Fedora'


__all__ = [ x for x in dir() if x.startswith('OutdatedPlatform') ]