# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/checkin_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
checkin.conf - Files ``/etc/splice/checkin.conf``
=================================================

Parser for checkin.conf configuration file.

"""
from insights.specs import Specs
from .. import IniConfigFile, parser

@parser(Specs.checkin_conf)
class CheckinConf(IniConfigFile):
    """
    Class for parsing content of "/etc/splice/checkin.conf".

    Sample input::

        [logging]
        config = /etc/splice/logging/basic.cfg

        # this is used only for single-spacewalk deployments
        [spacewalk]
        # Spacewalk/Satellite server to use for syncing data.
        host=
        # Path to SSH private key used to connect to spacewalk host.
        ssh_key_path=
        login=swreport

        # these are used for multi-spacewalk deployments
        # [spacewalk_one]
        # type = ssh
        # # Spacewalk/Satellite server to use for syncing data.
        # host=
        # # Path to SSH private key used to connect to spacewalk host.
        # ssh_key_path=
        # login=swreport
        #
        # [spacewalk_two]
        # type = file
        # # Path to directory containing report output
        # path = /path/to/output

        [katello]
        hostname=localhost
        port=443
        proto=https
        api_url=/sam
        admin_user=admin
        admin_pass=admin
        #autoentitle_systems = False
        #flatten_orgs = False

    Examples:
        >>> list(checkin_conf.sections())
        [u'logging', u'spacewalk', u'katello']
        >>> checkin_conf.get('spacewalk', 'host')
        u''
    """
    pass