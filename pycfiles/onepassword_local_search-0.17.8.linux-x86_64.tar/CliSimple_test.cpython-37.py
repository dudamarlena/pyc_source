# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/CliSimple_test.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 11277 bytes
import pytest
import onepassword_local_search.CliSimple as CliSimple
import onepassword_local_search.__version__ as __version__
from onepassword_local_search.tests.fixtures_common import common_data, no_op_session, op_session, op_personal_session, op_dual_session
nl = common_data('nl')

@pytest.fixture
def cli_version():
    return CliSimple('script', 'version')


@pytest.mark.usefixtures('no_op_session')
def test_usage(capsys):
    CliSimple('script').run()
    std = capsys.readouterr()
    assert 'Version: ' + __version__ in std.out
    assert 'usage: ' in std.out


@pytest.mark.usefixtures('no_op_session')
def test_version(cli_version, capsys):
    cli_version.run()
    std = capsys.readouterr()
    assert std.out == 'Version: ' + __version__ + nl


@pytest.mark.usefixtures('op_dual_session')
def test_check_cache():
    import os, glob
    for file in glob.glob(os.path.join(os.path.dirname(__file__), 'tests', '.*_cache')):
        os.unlink(file)

    CliSimple('script', 'list').run()
    assert os.path.isfile(os.path.join(os.path.dirname(__file__), 'tests', '.bWUmfqAZUUOJMWoYaBQN4wC5JbM_cached'))
    assert os.path.isfile(os.path.join(os.path.dirname(__file__), 'tests', '.XPgC-AnuKJcmG3-Lj4UG2iKBxcQ_cached'))


@pytest.mark.usefixtures('op_dual_session')
def test_check_cache_removal():
    import os, glob
    for file in glob.glob(os.path.join(os.path.dirname(__file__), 'tests', '.*_cache')):
        os.unlink(file)

    CliSimple('script', 'get', common_data('item_uuid'), 'title').run()
    CliSimple('script', '--disable-session-caching').run()
    assert glob.glob(os.path.join(os.path.dirname(__file__), 'tests', '.*_cache')) == []


@pytest.fixture
def cli_get_uuid():
    return CliSimple('script', 'get', common_data('item_uuid'), 'password')


@pytest.mark.usefixtures('no_op_session')
def test_get_uuid_without_session(cli_get_uuid, capsys):
    with pytest.raises(SystemExit) as (exit_code):
        cli_get_uuid.run()
    std = capsys.readouterr()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert std.err.find('You are not connected to the required account to decrypt item') != -1


@pytest.mark.usefixtures('op_session')
def test_get_title(capsys):
    CliSimple('script', 'get', common_data('item_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Software licence'


@pytest.mark.usefixtures('op_session')
def test_get_login_title(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Connexion'


@pytest.mark.usefixtures('op_session')
def test_get_login_title_auto_custom_uuid(capsys):
    CliSimple('script', 'get', common_data('login_custom_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Connexion'


@pytest.mark.usefixtures('op_session')
def test_get_login_title_auto_lastpass_uuid(capsys):
    CliSimple('script', 'get', common_data('login_lastpass_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Connexion'


@pytest.mark.usefixtures('op_session')
def test_get_no_totp(capsys):
    with pytest.raises(SystemExit) as (exit_code):
        CliSimple('script', 'get', common_data('item_uuid'), 'totp').run()
    std = capsys.readouterr()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1
    assert std.err == 'Item e25haqmocd5ifiymorfzwxnzry doesn\'t seem to have a field untitled "One-time password"\n'


@pytest.mark.usefixtures('op_session')
def test_get_login_totp(capsys):
    import pyotp
    totp = pyotp.TOTP('EGUUASD55RTXQAL4CAI43HGGM673NUUU')
    CliSimple('script', 'get', common_data('login_uuid'), 'totp').run()
    std = capsys.readouterr()
    assert std.out == totp.now()


@pytest.mark.usefixtures('op_session')
def test_get_login_uuid(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'uuid').run()
    std = capsys.readouterr()
    assert std.out == 'zzfmhu2j7ajq55mmpm3ihs3oqy'


@pytest.mark.usefixtures('op_session')
def test_get_login_url(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'url').run()
    std = capsys.readouterr()
    assert std.out == 'https://site1.com'


@pytest.mark.usefixtures('op_session')
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'username').run()
    std = capsys.readouterr()
    assert std.out == 'username'


@pytest.mark.usefixtures('op_session')
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'password').run()
    std = capsys.readouterr()
    assert std.out == 'password'


@pytest.mark.usefixtures('op_session')
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'Section1;;Section1Field1').run()
    std = capsys.readouterr()
    assert std.out == 'Section1Field1Value'


@pytest.mark.usefixtures('op_session')
def test_get_login_username(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'Section2;;Section2Field2').run()
    std = capsys.readouterr()
    assert std.out == 'Section2Field2Value'


@pytest.mark.usefixtures('op_session')
def test_list(capsys):
    CliSimple('script', 'list').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '\n5pwta5jhf5fhj5wzfek4sb22ve Mickaël\na53bppwuhi65b2e34g45fjyfwu Email account\nakvb4bbdequd3z6tuorl44btqm Bienvenue dans 1Password\xa0!\nc6mqeodzuvazris6v6toq5trja Test JSON encoding: &é"\'è;?\ne25haqmocd5ifiymorfzwxnzry Software licence\nhujxh3pryngc7du3owbkwwuh3i test\nmvkzp2v2myljdqzxcv5736optu Secure Note\nn3iopimevz3pddels3dgfwyp2a Simple Password\nngkzmk54qoltpdoseqspma4tba File certificate\nsmeg46sk3agiee4cfinvpf7z4u Database\nw2euij3m4zhqa5opftnthe5d4q Server\nzzfmhu2j7ajq55mmpm3ihs3oqy Connexion'


@pytest.mark.usefixtures('op_session')
def test_list_custom_field(capsys):
    CliSimple('script', 'list', '--format={uuid} {username} {password}').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '\n5pwta5jhf5fhj5wzfek4sb22ve\na53bppwuhi65b2e34g45fjyfwu\nakvb4bbdequd3z6tuorl44btqm\nc6mqeodzuvazris6v6toq5trja\ne25haqmocd5ifiymorfzwxnzry\nhujxh3pryngc7du3owbkwwuh3i\nmvkzp2v2myljdqzxcv5736optu\nn3iopimevz3pddels3dgfwyp2a  password\nngkzmk54qoltpdoseqspma4tba\nsmeg46sk3agiee4cfinvpf7z4u username password\nw2euij3m4zhqa5opftnthe5d4q username password\nzzfmhu2j7ajq55mmpm3ihs3oqy username password'


@pytest.mark.usefixtures('op_session')
def test_list_custom_uuid(capsys):
    CliSimple('script', 'list', '--format={uuid} {UUID}').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '\n5pwta5jhf5fhj5wzfek4sb22ve\na53bppwuhi65b2e34g45fjyfwu c08335ad-5f93-471f-8605-2500ae4b9ce1\nakvb4bbdequd3z6tuorl44btqm\nc6mqeodzuvazris6v6toq5trja\ne25haqmocd5ifiymorfzwxnzry 84103613-2483-430d-8e74-bc72036f378c\nhujxh3pryngc7du3owbkwwuh3i\nmvkzp2v2myljdqzxcv5736optu b325bc32-7c2d-4107-bc2c-73777cb3e33a\nn3iopimevz3pddels3dgfwyp2a 41495d3a-9b1a-4ce6-9bbd-82fbc4e538a9\nngkzmk54qoltpdoseqspma4tba 4dc2d37a-bc4e-47a8-a96b-206048b7d7d5\nsmeg46sk3agiee4cfinvpf7z4u 6bf1b272-f35d-4087-808f-253909fb0c91\nw2euij3m4zhqa5opftnthe5d4q f544c30d-612f-4c70-9686-cf95b9d9f096\nzzfmhu2j7ajq55mmpm3ihs3oqy c3264cef-1e5e-4c96-a192-26729539f3f5'


@pytest.mark.usefixtures('op_session')
def test_get_by_custom_uuid(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'title').run()
    std = capsys.readouterr()
    out_op_uuid = std.out
    CliSimple('script', 'get', common_data('login_custom_uuid'), 'title', '--use-custom-uuid').run()
    std2 = capsys.readouterr()
    out_custom_uuid = std2.out
    assert out_custom_uuid == out_op_uuid


@pytest.mark.usefixtures('op_session')
def test_get_by_lastpass_uuid(capsys):
    CliSimple('script', 'get', common_data('login_uuid'), 'title').run()
    std = capsys.readouterr()
    out_op_uuid = std.out
    CliSimple('script', 'get', common_data('login_lastpass_uuid'), 'title', '--use-lastpass-uuid').run()
    std2 = capsys.readouterr()
    out_custom_uuid = std2.out
    assert out_custom_uuid == out_op_uuid


@pytest.mark.usefixtures('op_session')
def test_mapping_list(capsys):
    CliSimple('script', 'mapping', 'update').run()
    CliSimple('script', 'mapping', 'list').run()
    std = capsys.readouterr()
    assert std.out == 'smeg46sk3agiee4cfinvpf7z4u <-> 6bf1b272-f35d-4087-808f-253909fb0c91\na53bppwuhi65b2e34g45fjyfwu <-> c08335ad-5f93-471f-8605-2500ae4b9ce1\nngkzmk54qoltpdoseqspma4tba <-> 4dc2d37a-bc4e-47a8-a96b-206048b7d7d5\nmvkzp2v2myljdqzxcv5736optu <-> b325bc32-7c2d-4107-bc2c-73777cb3e33a\nw2euij3m4zhqa5opftnthe5d4q <-> f544c30d-612f-4c70-9686-cf95b9d9f096\nn3iopimevz3pddels3dgfwyp2a <-> 41495d3a-9b1a-4ce6-9bbd-82fbc4e538a9\ne25haqmocd5ifiymorfzwxnzry <-> 84103613-2483-430d-8e74-bc72036f378c\nzzfmhu2j7ajq55mmpm3ihs3oqy <-> c3264cef-1e5e-4c96-a192-26729539f3f5\n'


@pytest.mark.usefixtures('op_session')
def test_mapping_list_lastpass(capsys):
    CliSimple('script', 'mapping', 'update').run()
    CliSimple('script', 'mapping', 'list', '--use-lastpass-uuid').run()
    std = capsys.readouterr()
    assert std.out == 'smeg46sk3agiee4cfinvpf7z4u <-> \na53bppwuhi65b2e34g45fjyfwu <-> \nngkzmk54qoltpdoseqspma4tba <-> \nmvkzp2v2myljdqzxcv5736optu <-> \nw2euij3m4zhqa5opftnthe5d4q <-> \nn3iopimevz3pddels3dgfwyp2a <-> \ne25haqmocd5ifiymorfzwxnzry <-> \nzzfmhu2j7ajq55mmpm3ihs3oqy <-> 1234567890\n'


@pytest.mark.usefixtures('no_op_session')
def test_not_authenticated(capsys):
    with pytest.raises(SystemExit) as (exit_code):
        CliSimple('script', 'is-authenticated').run()
    std = capsys.readouterr()
    assert exit_code.type == SystemExit
    assert exit_code.value.code == 1


@pytest.mark.usefixtures('op_session')
def test_not_authenticated(capsys):
    CliSimple('script', 'is-authenticated').run()
    std = capsys.readouterr()
    assert std.out == ''


@pytest.mark.usefixtures('op_dual_session')
def test_get_personal_login_title(capsys):
    CliSimple('script', 'get', common_data('personal_login_uuid'), 'title').run()
    std = capsys.readouterr()
    assert std.out == 'Personal login'


@pytest.mark.usefixtures('op_session')
def test_list_json_encoding(capsys):
    CliSimple('script', 'list', '--format={{"uuid": "{uuid}", "title": "{title}"}},\n', '--output-encoding=json').run()
    std = capsys.readouterr()
    assert '\n'.join(sorted(std.out.split('\n'))) == '\n{"uuid": "5pwta5jhf5fhj5wzfek4sb22ve", "title": "Micka\\u00ebl"},\n{"uuid": "a53bppwuhi65b2e34g45fjyfwu", "title": "Email account"},\n{"uuid": "akvb4bbdequd3z6tuorl44btqm", "title": "Bienvenue dans 1Password\\u00a0!"},\n{"uuid": "c6mqeodzuvazris6v6toq5trja", "title": "Test JSON encoding: &\\u00e9\\"\'\\u00e8;?"},\n{"uuid": "e25haqmocd5ifiymorfzwxnzry", "title": "Software licence"},\n{"uuid": "hujxh3pryngc7du3owbkwwuh3i", "title": "test"},\n{"uuid": "mvkzp2v2myljdqzxcv5736optu", "title": "Secure Note"},\n{"uuid": "n3iopimevz3pddels3dgfwyp2a", "title": "Simple Password"},\n{"uuid": "ngkzmk54qoltpdoseqspma4tba", "title": "File certificate"},\n{"uuid": "smeg46sk3agiee4cfinvpf7z4u", "title": "Database"},\n{"uuid": "w2euij3m4zhqa5opftnthe5d4q", "title": "Server"},\n{"uuid": "zzfmhu2j7ajq55mmpm3ihs3oqy", "title": "Connexion"},'