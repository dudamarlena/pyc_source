# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/vault_aws_login/consul_template.py
# Compiled at: 2020-03-11 22:27:01
# Size of source mod 2**32: 373 bytes
import os

def consul_template_exec(login_data_json, consul_template_hcl, consul_template_flag, extra_ct_flags):
    os.environ['VAULTAWS_LOGINDATA_JSON'] = login_data_json
    (os.execlp)('consul-template', 'consul-template', '-config', consul_template_hcl, '-template', consul_template_flag, *extra_ct_flags)