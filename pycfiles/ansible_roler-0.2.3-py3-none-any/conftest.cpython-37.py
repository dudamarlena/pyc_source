# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/conftest.py
# Compiled at: 2019-10-28 09:42:37
# Size of source mod 2**32: 907 bytes
__doc__ = 'Pytest fixtures.'
import pathlib, typing, pytest

def __generate_roles(role_names: typing.List[str], tmp_path: pathlib.Path) -> None:
    """Generate dummy roles for testing."""
    STANDARD_ROLE_PATHS = [
     'defaults',
     'files',
     'meta',
     'tasks',
     'templates',
     'vars']
    for role in role_names:
        role_root = tmp_path / role
        role_root.mkdir()
        for path in STANDARD_ROLE_PATHS:
            role_path = role_root / path
            role_path.mkdir()
            main_yml = role_path / 'main.yml'
            main_yml.write_text('---')


@pytest.fixture()
def single_role_path(tmp_path):
    __generate_roles(['role1'], tmp_path)
    return tmp_path / 'role1'


@pytest.fixture()
def many_roles_path(tmp_path):
    __generate_roles(['role1', 'role2', 'role3'], tmp_path)
    return tmp_path