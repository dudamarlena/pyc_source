# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_ansible_readme.py
# Compiled at: 2019-10-30 07:38:01
# Size of source mod 2**32: 6238 bytes
"""Unit tests against the AnsibleReadme module."""
import os, shutil, click, pytest
from ansible_readme import AnsibleReadme

def _inject_defaults(path, defaults):
    with open(path / 'defaults' / 'main.yml', 'a') as (handle):
        defaults[:] = [
         '\n'] + defaults
        handle.write('\n'.join(defaults))


def _inject_meta(path, defaults):
    with open(path / 'meta' / 'main.yml', 'a') as (handle):
        defaults[:] = [
         '\n'] + defaults
        handle.write('\n'.join(defaults))


def test_roles_path_single_role(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    assert ansible_readme.is_single_role
    assert not ansible_readme.is_multiple_role
    assert ansible_readme.role_paths == [single_role_path]


def test_roles_path_multiple_roles(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    assert not ansible_readme.is_single_role
    assert ansible_readme.is_multiple_role
    for role_path in ansible_readme.role_paths:
        assert role_path in [
         many_roles_path / 'role1',
         many_roles_path / 'role2',
         many_roles_path / 'role3']


def test_roles_path_no_roles(tmp_path):
    with pytest.raises(click.ClickException) as (exception):
        AnsibleReadme(tmp_path)
    assert 'does not contain' in str(exception.value)


def test_standard_role_paths_detection(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    assert ansible_readme.has_standard_role_paths(ansible_readme.path)


def test_gather_all_defaults_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_defaults(single_role_path, ['foobar: barfoo'])
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['defaults'] == {'foobar': 'barfoo'}


def test_gather_all_no_defaults_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_defaults(single_role_path, [])
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['defaults'] == {}


def test_gather_all_no_defaults_path_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_defaults(single_role_path, [])
    shutil.rmtree(single_role_path / 'defaults')
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['defaults'] == {}


def test_gather_all_defaults_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_defaults(role_path, ['foobar: barfoo'])
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['defaults'] == {'foobar': 'barfoo'}


def test_gather_all_no_defaults_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_defaults(role_path, [])
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['defaults'] == {}


def test_gather_all_no_defaults_path_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_defaults(role_path, [])
        shutil.rmtree(role_path / 'defaults')
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['defaults'] == {}


def test_gather_all_meta_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_meta(single_role_path, ['foobar: barfoo'])
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['meta'] == {'foobar':'barfoo', 
     'galaxy_info':{}}


def test_gather_all_no_meta_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_meta(single_role_path, [])
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['meta'] == {'galaxy_info': {}}


def test_gather_all_no_meta_path_single(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    name = os.path.basename(single_role_path)
    _inject_meta(single_role_path, [])
    shutil.rmtree(single_role_path / 'meta')
    ansible_readme.gather_all()
    assert ansible_readme.role_docs[name]['meta'] == {'galaxy_info': {}}


def test_gather_all_meta_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_meta(role_path, ['foobar: barfoo'])
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['meta'] == {'foobar':'barfoo', 
         'galaxy_info':{}}


def test_gather_all_no_meta_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_meta(role_path, [])
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['meta'] == {'galaxy_info': {}}


def test_gather_all_no_meta_path_multiple(many_roles_path):
    ansible_readme = AnsibleReadme(many_roles_path)
    for role_name in ('role1', 'role2', 'role3'):
        role_path = many_roles_path / role_name
        _inject_meta(role_path, [])
        shutil.rmtree(role_path / 'meta')
        ansible_readme.gather_all()
        assert ansible_readme.role_docs[role_name]['meta'] == {'galaxy_info': {}}


def test_render_readme(single_role_path):
    ansible_readme = AnsibleReadme(single_role_path)
    ansible_readme.gather_all()
    ansible_readme.render_readmes()
    assert 'role1' in ansible_readme.role_readmes['role1']