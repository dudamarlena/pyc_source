# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codebuild/output/src613133936/src/github.com/awslabs/aws-service-catalog-puppet/servicecatalog_puppet/macros.py
# Compiled at: 2020-05-13 08:59:18
# Size of source mod 2**32: 278 bytes


def get_accounts_for_path(client, path):
    ou = client.convert_path_to_ou(path)
    response = client.list_children_nested(ParentId=ou, ChildType='ACCOUNT')
    return ','.join([r.get('Id') for r in response])


macros = {'get_accounts_for_path': get_accounts_for_path}