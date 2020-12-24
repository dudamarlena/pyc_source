# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/dns_alias/get_dns_label.py
# Compiled at: 2015-09-04 04:29:27
from qingcloud.cli.iaas_client.actions.base import BaseAction

class GetDNSLabelAction(BaseAction):
    action = 'GetDNSLabel'
    command = 'get-dns-label'
    usage = '%(prog)s [-f <conf_file>]'

    @classmethod
    def build_directive(cls, options):
        return {}