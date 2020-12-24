# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/vault_aws_login/context.py
# Compiled at: 2020-03-11 22:21:09
# Size of source mod 2**32: 2631 bytes
from collections import ChainMap
from configparser import ConfigParser, SectionProxy
from pathlib import Path

def gen_config(cli_profile_section, cli_config, cli_login, login_template_section='login_template'):
    config = ConfigParser(dict(credentials_file=(Path('~/.aws/credentials').expanduser().absolute()),
      consul_template_hcl=(Path('~/.vault-aws/credentials.hcl').expanduser().absolute()),
      template_source=(Path('~/.vault-aws/credentials.tpl').expanduser().absolute()),
      template_dest=(Path('~/.aws/vaultprovided-credentials').expanduser().absolute()),
      template_cmd='%(aws_credentials_merge_path)s -o %(credentials_file)s -i %(credentials_file)s %(template_dest)s',
      aws_credentials_merge_path='aws_credentials_merge'))
    config.read(cli_config)
    if login_template_section not in config:
        config.add_section(login_template_section)
    if cli_profile_section not in config:
        config.add_section(cli_profile_section)
    if cli_login:
        config.set(cli_profile_section, 'login_ids', value=cli_login)
    return config


def gen_login_data(profile, config, login_template_section='login_template', login_override_section='login_override {}'):
    login_template = config[login_template_section]
    login_ids = profile['login_ids'].split(',')
    for login_id in login_ids:
        curr_vars = dict(login_id=login_id)
        curr_sect = login_override_section.format(login_id)
        override_vars = ChainMap(curr_vars, config[curr_sect]) if curr_sect in config else curr_vars
        aws_profile_name = login_template.get('aws_profile_name', vars=override_vars,
          fallback=login_id)
        vault_secret_path = login_template.get('vault_secret_path', vars=override_vars)
        yield {'aws_profile_name':aws_profile_name, 
         'vault_secret_path':vault_secret_path}


def gen_vault_login_kwargs(profile, key_prefix='vault_login_'):
    offset = len(key_prefix)
    return {key[offset:]:value for key, value in profile.items() if key.startswith(key_prefix)}


def gen_consul_template_flag(profile: SectionProxy):
    template_flag = ':'.join(filter(None, (
     profile['template_source'],
     profile['template_dest'],
     profile.get('template_cmd', fallback=None))))
    return template_flag