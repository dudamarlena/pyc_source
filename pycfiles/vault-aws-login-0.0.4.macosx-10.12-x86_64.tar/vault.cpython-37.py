# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/vault_aws_login/vault.py
# Compiled at: 2020-03-11 22:26:57
# Size of source mod 2**32: 763 bytes
import os, subprocess

def vault_login_if_required(extra_vl_flags, vault_addr, vault_login_kwargs):
    if vault_addr:
        os.environ['VAULT_ADDR'] = vault_addr
    if not is_vault_logged_in():
        vault_login(extra_vl_flags=extra_vl_flags, **vault_login_kwargs)


def is_vault_logged_in():
    return_code = subprocess.call([
     'vault', 'token', 'lookup'],
      stdout=(subprocess.DEVNULL))
    return return_code == 0


def vault_login(method=None, extra_vl_flags=(), **kwargs):
    subprocess.check_call([
     'vault', 'login',
     f"-method={value}" for value in (method,) if value,
     *extra_vl_flags,
     f"{key}={value}" for key, value in kwargs.items()])