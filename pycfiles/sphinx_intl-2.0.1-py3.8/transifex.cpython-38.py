# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build/bdist.macosx-10.15-x86_64/egg/sphinx_intl/transifex.py
# Compiled at: 2020-04-19 02:09:17
# Size of source mod 2**32: 4937 bytes
import os, re, textwrap, click
from .pycompat import relpath
from .catalog import load_po
IGNORED_RESOURCE_NAMES = ('glossary', 'settings')
TRANSIFEXRC_TEMPLATE = '[https://www.transifex.com]\nhostname = https://www.transifex.com\npassword = %(transifex_password)s\nusername = %(transifex_username)s\ntoken =\n'
TXCONFIG_TEMPLATE = '[main]\nhost = https://www.transifex.com\n'

def get_tx_root():
    import txclib.utils
    tx_root = txclib.utils.find_dot_tx()
    if tx_root is None:
        msg = "'.tx/config' not found. You need 'create-txconfig' first."
        raise click.BadParameter(msg)
    return tx_root


def normalize_resource_name(name):
    name = re.sub('[\\\\/]', '--', name)
    name = re.sub('[^\\-\\w]', '_', name)
    while name in IGNORED_RESOURCE_NAMES:
        name += '_'

    return name


def create_transifexrc(transifex_username, transifex_password):
    """
    Create `$HOME/.transifexrc`
    """
    target = os.path.normpath(os.path.expanduser('~/.transifexrc'))
    if os.path.exists(target):
        click.echo('{0} already exists, skipped.'.format(target))
        return None
    if not transifex_username or False:
        msg = textwrap.dedent('        You need transifex username/password by command option or environment.\n        command option: --transifex-username, --transifex-password\n        ')
        raise click.BadParameter(msg, param_hint='transifex_username,transifex_password')
    with open(target, 'wt') as (rc):
        rc.write(TRANSIFEXRC_TEMPLATE % locals())
    click.echo('Create: {0}'.format(target))


def create_txconfig():
    """
    Create `./.tx/config`
    """
    target = os.path.normpath('.tx/config')
    if os.path.exists(target):
        click.echo('{0} already exists, skipped.'.format(target))
        return None
    if not os.path.exists('.tx'):
        os.mkdir('.tx')
    with open(target, 'wt') as (f):
        f.write(TXCONFIG_TEMPLATE)
    click.echo('Create: {0}'.format(target))


def update_txconfig_resources(transifex_project_name, locale_dir, pot_dir):
    """
    Update resource sections of `./.tx/config`.
    """
    try:
        import txclib, txclib.utils
    except ImportError:
        msg = textwrap.dedent("            Could not import 'txclib.utils'.\n            You need install transifex_client external library.\n            Please install below command if you want to this action:\n\n                $ pip install sphinx-intl[transifex]\n            ")
        raise click.BadParameter(msg)
    else:
        tx_root = get_tx_root()
        tx_version = getattr(txclib, '__version__', '0.0')
        if tx_version < '0.13':
            args_tmpl = ('--auto-local', '-r', '%(transifex_project_name)s.%(resource_name)s',
                         '%(locale_dir)s/<lang>/LC_MESSAGES/%(resource_path)s.po',
                         '--source-lang', 'en', '--source-file', '%(pot_dir)s/%(resource_path)s.pot',
                         '--execute')
        else:
            args_tmpl = ('mapping', '-r', '%(transifex_project_name)s.%(resource_name)s',
                         '-t', 'PO', '-s', 'en', '-f', '%(pot_dir)s/%(resource_path)s.pot',
                         '--execute', '%(locale_dir)s/<lang>/LC_MESSAGES/%(resource_path)s.po')
        transifex_project_name = transifex_project_name.replace(' ', '-')
        transifex_project_name = re.sub('[^\\-_\\w]', '', transifex_project_name)
        for dirpath, dirnames, filenames in os.walk(pot_dir):
            dirnames.sort()
            for filename in sorted(filenames):
                pot_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(pot_file)
                if ext != '.pot':
                    pass
                else:
                    resource_path = relpath(base, pot_dir)
                    pot = load_po(pot_file)
                    if len(pot):
                        resource_name = normalize_resource_name(resource_path)
                        lv = locals()
                        args = [arg % lv for arg in args_tmpl]
                        txclib.utils.exec_command('set', args, tx_root)
                    else:
                        click.echo('{0} is empty, skipped'.format(pot_file))