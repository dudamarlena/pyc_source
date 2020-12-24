# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/utils/fake_group.py
# Compiled at: 2017-04-17 00:51:41
from gerritclient.tests.utils import fake_account

def get_fake_group(name='fake-group', group_id=1, is_single_item=True):
    """Creates a fake group

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """
    fake_group = {'id': '6a1e70e1a88782771a91808c8af9bbb7a9871389', 
       'url': '#/admin/groups/uuid-6a1e70e1a88782771a91808c8af9bbb7a9871389', 
       'options': {'visible_to_all': True}, 
       'description': 'Fake group description', 
       'group_id': group_id, 
       'owner': 'Fake Owner', 
       'owner_id': '5057f3cbd3519d6ab69364429a89ffdffba50f73', 
       'members': fake_account.get_fake_accounts(5), 
       'includes': []}
    if is_single_item:
        fake_group['name'] = name
        return fake_group
    return {name: fake_group}


def get_fake_groups(groups_count):
    """Creates a random fake groups map."""
    fake_groups = {}
    for item in range(1, groups_count + 1):
        fake_groups.update(get_fake_group(name=('fake-group-{0}').format(item), group_id=item, is_single_item=False))

    return fake_groups