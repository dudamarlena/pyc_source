# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nova_user_ids.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import nova_user_ids
from insights.parsers import ParseException, SkipException
from insights.tests import context_wrap
import doctest, pytest
NOVA_UID = ('\n162\n').strip()
NOVA_USER_NOT_FOUND = ('\nid: nova: no such user\n').strip()
NOVA_MIGRATION_UID = ('\n153\n').strip()
NOVA_MIGRATION_USER_NOT_FOUND = ('\nid: nova_migration: no such user\n').strip()
UNEXPECTED_OUTPUT = ('\nfoo\nbar\n9\n').strip()

def test_nova_uid():
    nova_uid = nova_user_ids.NovaUID(context_wrap(NOVA_UID))
    assert nova_uid.data == 162
    with pytest.raises(SkipException) as (ex):
        nova_user_ids.NovaUID(context_wrap(NOVA_USER_NOT_FOUND))
    assert '' in str(ex)
    with pytest.raises(SkipException) as (ex):
        nova_user_ids.NovaUID(context_wrap(''))
    assert '' in str(ex)
    with pytest.raises(ParseException) as (ex):
        nova_user_ids.NovaUID(context_wrap(UNEXPECTED_OUTPUT))
    assert 'Unable to parse user ID' in str(ex)


def test_nova_migration_uid():
    nova_migration_uid = nova_user_ids.NovaMigrationUID(context_wrap(NOVA_MIGRATION_UID))
    assert nova_migration_uid.data == 153
    with pytest.raises(SkipException) as (ex):
        nova_user_ids.NovaMigrationUID(context_wrap(NOVA_MIGRATION_USER_NOT_FOUND))
    assert '' in str(ex)
    with pytest.raises(SkipException) as (ex):
        nova_user_ids.NovaMigrationUID(context_wrap(''))
    assert '' in str(ex)
    with pytest.raises(ParseException) as (ex):
        nova_user_ids.NovaMigrationUID(context_wrap(UNEXPECTED_OUTPUT))
    assert 'Unable to parse user ID' in str(ex)


def test_doc_examples():
    failed, total = doctest.testmod(nova_user_ids, globs={'nova_uid': nova_user_ids.NovaUID(context_wrap(NOVA_UID)), 'nova_migration_uid': nova_user_ids.NovaMigrationUID(context_wrap(NOVA_MIGRATION_UID))})
    assert failed == 0