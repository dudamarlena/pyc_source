# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_anger/check_migration_tests.py
# Compiled at: 2013-05-16 15:00:26
import nose
from django_anger.check_migration import check_duplicate_fields
from django_anger.check_migration import check_duplicate_models
from django_anger.check_migration import check_gratuitous_frozen_models
from django_anger.check_migration import check_missing_related_models
from django_anger.check_migration import check_model_names
from django_anger.check_migration import validate_migration_file
from django_anger.check_migration import ValidationError

def check_model_names_test():
    check_model_names(open('testdata/good_migration.py'))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open('testdata/bad_migration_bad_model_name_1.py'))
    with nose.tools.assert_raises(ValidationError):
        check_model_names(open('testdata/bad_migration_bad_model_name_2.py'))


def check_duplicate_models_test():
    check_duplicate_models(open('testdata/good_migration.py'))
    with nose.tools.assert_raises(ValidationError):
        check_duplicate_models(open('testdata/bad_migration_model_frozen_twice.py'))


def check_duplicate_fields_test():
    check_duplicate_fields(open('testdata/good_migration.py'))
    with nose.tools.assert_raises(ValidationError):
        check_duplicate_fields(open('testdata/bad_migration_field_frozen_twice.py'))


def check_missing_foreign_keys_test():
    check_missing_related_models(open('testdata/good_migration.py'))
    with nose.tools.assert_raises(ValidationError):
        check_missing_related_models(open('testdata/bad_migration_missing_foreign_key.py'))


def check_gratuitous_frozen_models_test():
    check_gratuitous_frozen_models(open('testdata/good_migration.py'))
    with nose.tools.assert_raises(ValidationError):
        check_gratuitous_frozen_models(open('testdata/bad_migration_gratuitous_frozen_model.py'))


def data_migration_test():
    validate_migration_file(open('testdata/good_data_migration.py'))