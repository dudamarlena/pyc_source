# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/utils/fake_weblinkifno.py
# Compiled at: 2017-04-19 03:22:39


def get_fake_weblinkinfo(name='gitweb', project_id='fake-project'):
    """Creates a fake WebLinkInfo entity

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review WebLinkInfo entity.
    """
    return [
     {'name': name, 
        'url': ('gitweb?p\\u003d{}.git;a\\u003dsummary').format(project_id), 
        'image_url': None}]