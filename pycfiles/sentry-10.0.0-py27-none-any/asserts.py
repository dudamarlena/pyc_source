# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/asserts.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from sentry.models import CommitFileChange

def assert_mock_called_once_with_partial(mock, *args, **kwargs):
    """
    Similar to ``mock.assert_called_once_with()``, but we dont require all
    args and kwargs to be specified.
    """
    assert len(mock.mock_calls) == 1
    m_args, m_kwargs = mock.call_args
    for i, arg in enumerate(args):
        assert m_args[i] == arg

    for kwarg in kwargs:
        assert m_kwargs[kwarg] == kwargs[kwarg]


commit_file_type_choices = {c[0] for c in CommitFileChange._meta.get_field('type').choices}

def assert_commit_shape(commit):
    assert commit['id']
    assert commit['repository']
    assert commit['author_email']
    assert commit['author_name']
    assert commit['message']
    assert commit['timestamp']
    assert commit['patch_set']
    patches = commit['patch_set']
    for patch in patches:
        assert patch['type'] in commit_file_type_choices
        assert patch['path']