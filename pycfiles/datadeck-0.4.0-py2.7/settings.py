# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datadeck/settings.py
# Compiled at: 2011-11-23 15:36:55
import dpm.lib

class Settings(object):
    _ckan_section = 'index:ckan'
    _ckan_url_option = 'ckan.url'
    _ckan_api_key_option = 'ckan.api_key'
    _datadeck_section = 'datadeck'
    _datadeck_library_path_option = 'library_path'
    _licenses = [
     'Non-OKD Compliant::Creative Commons Non-Commercial (Any)',
     'Non-OKD Compliant::Crown Copyright',
     'Non-OKD Compliant::Non-Commercial Other',
     'Non-OKD Compliant::Other',
     'OKD Compliant::Creative Commons Attribution',
     'OKD Compliant::Creative Commons Attribution-ShareAlike',
     'OKD Compliant::Creative Commons CCZero',
     'OKD Compliant::GNU Free Documentation License (GFDL)',
     'OKD Compliant::Higher Education Statistics Agency Copyright with data.gov.uk rights',
     'OKD Compliant::Local Authority Copyright with data.gov.uk rights',
     'OKD Compliant::Open Data Commons Open Database License (ODbL)',
     'OKD Compliant::Open Data Commons Public Domain Dedication and License (PDDL)',
     'OKD Compliant::Other',
     'OKD Compliant::Other (Attribution)',
     'OKD Compliant::Other (Public Domain)',
     'OKD Compliant::Public Domain',
     'OKD Compliant::UK Click Use PSI',
     'OKD Compliant::UK Crown Copyright with data.gov.uk rights',
     'OSI Approved::Academic Free License',
     'OSI Approved::Adaptive Public License',
     'OSI Approved::Apache License, 2.0',
     'OSI Approved::Apache Software License',
     'OSI Approved::Apple Public Source License',
     'OSI Approved::Artistic license',
     'OSI Approved::Attribution Assurance Licenses',
     'OSI Approved::CUA Office Public License Version 1.0',
     'OSI Approved::Common Development and Distribution License',
     'OSI Approved::Common Public License 1.0',
     'OSI Approved::Computer Associates Trusted Open Source License 1.1',
     'OSI Approved::EU DataGrid Software License',
     'OSI Approved::Eclipse Public License',
     'OSI Approved::Educational Community License',
     'OSI Approved::Eiffel Forum License',
     'OSI Approved::Eiffel Forum License V2.0',
     'OSI Approved::Entessa Public License',
     'OSI Approved::Fair License',
     'OSI Approved::Frameworx License',
     'OSI Approved::GNU General Public License (GPL)',
     'OSI Approved::GNU General Public License v3 (GPLv3)',
     'OSI Approved::GNU Library or "Lesser" General Public License (LGPL)',
     'OSI Approved::IBM Public License',
     'OSI Approved::Intel Open Source License',
     'OSI Approved::Jabber Open Source License',
     'OSI Approved::Lucent Public License (Plan9)',
     'OSI Approved::Lucent Public License Version 1.02',
     'OSI Approved::MIT license',
     'OSI Approved::MITRE Collaborative Virtual Workspace License (CVW License)',
     'OSI Approved::Motosoto License',
     'OSI Approved::Mozilla Public License 1.0 (MPL)',
     'OSI Approved::Mozilla Public License 1.1 (MPL)',
     'OSI Approved::NASA Open Source Agreement 1.3',
     'OSI Approved::Naumen Public License',
     'OSI Approved::Nethack General Public License',
     'OSI Approved::New BSD license',
     'OSI Approved::Nokia Open Source License',
     'OSI Approved::OCLC Research Public License 2.0',
     'OSI Approved::Open Group Test Suite License',
     'OSI Approved::Open Software License',
     'OSI Approved::PHP License',
     'OSI Approved::Python Software Foundation License',
     'OSI Approved::Python license (CNRI Python License)',
     'OSI Approved::Qt Public License (QPL)',
     'OSI Approved::RealNetworks Public Source License V1.0',
     'OSI Approved::Reciprocal Public License',
     'OSI Approved::Ricoh Source Code Public License',
     'OSI Approved::Sleepycat License',
     'OSI Approved::Sun Industry Standards Source License (SISSL)',
     'OSI Approved::Sun Public License',
     'OSI Approved::Sybase Open Watcom Public License 1.0',
     'OSI Approved::University of Illinois/NCSA Open Source License',
     'OSI Approved::Vovida Software License v. 1.0',
     'OSI Approved::W3C License',
     'OSI Approved::X.Net License',
     'OSI Approved::Zope Public License',
     'OSI Approved::wxWindows Library License',
     'OSI Approved::zlib/libpng license',
     'Other::License Not Specified']

    @staticmethod
    def ckan_url(ckan_url=None):
        if not ckan_url:
            return dpm.lib.get_config(Settings._ckan_section, Settings._ckan_url_option)
        else:
            return dpm.lib.set_config(Settings._ckan_section, Settings._ckan_url_option, ckan_url)

    @staticmethod
    def ckan_api(ckan_api=None):
        if not ckan_api:
            return dpm.lib.get_config(Settings._ckan_section, Settings._ckan_api_key_option)
        else:
            return dpm.lib.set_config(Settings._ckan_section, Settings._ckan_api_key_option, ckan_api)

    @staticmethod
    def library_path(default_path=None):
        if not default_path:
            return dpm.lib.get_config(Settings._datadeck_section, Settings._datadeck_library_path_option)
        else:
            return dpm.lib.set_config(Settings._datadeck_section, Settings._datadeck_library_path_option, default_path)

    @staticmethod
    def licenses(key=None):
        if not key:
            return Settings._licenses
        if type(key) == int:
            try:
                return Settings._licenses[key]
            except IndexError:
                return 'Other::License Not Specified'

        if type(key) == str or type(key) == unicode:
            try:
                return Settings._licenses.index(key)
            except ValueError:
                return Settings._licenses.index('Other::License Not Specified')

        else:
            return 'Other::License Not Specified'