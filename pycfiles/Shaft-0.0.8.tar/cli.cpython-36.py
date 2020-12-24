# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/cli.py
# Compiled at: 2017-01-26 21:50:02
# Size of source mod 2**32: 9960 bytes
r"""
________________________________________________________________________________

  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$$ /$$$$$$$$
 /$$__  $$| $$  | $$ /$$__  $$| $$_____/|__  $$__/
| $$  \__/| $$  | $$| $$  \ $$| $$         | $$
|  $$$$$$ | $$$$$$$$| $$$$$$$$| $$$$$      | $$
 \____  $$| $$__  $$| $$__  $$| $$__/      | $$
 /$$  \ $$| $$  | $$| $$  | $$| $$         | $$
|  $$$$$$/| $$  | $$| $$  | $$| $$         | $$
 \______/ |__/  |__/|__/  |__/|__/         |__/

https://github.com/mardix/shaft

________________________________________________________________________________
"""
import os, re, sys, traceback, logging, importlib, pkg_resources, click, yaml, functools, sh, json
from werkzeug import import_string
from .__about__ import *
from shaft import utils
CWD = os.getcwd()
SKELETON_DIR = 'skel'
APPLICATION_DIR = '%s/app' % CWD
APPLICATION_DATA_DIR = '%s/var' % APPLICATION_DIR
APPLICATION_BABEL_DIR = '%s/babel' % APPLICATION_DATA_DIR

class CLI(object):
    __doc__ = '\n    For command line classes in which __init__ contains all the functions to use\n\n    example\n\n    class MyCLI(ShaftCLI):\n        def __init__(self):\n\n            @cli.command()\n            def hello():\n                click.echo("Hello world")\n\n            @cli.command()\n            @click.argument("name")\n            def say_my_name(name):\n                click.echo("My name is %s" % name)\n    '


def get_project_dir_path(project_name):
    return '%s/%s' % (APPLICATION_DIR, project_name)


def copy_resource(src, dest):
    """
    To copy package data to destination
    """
    package_name = 'shaft'
    dest = (dest + '/' + os.path.basename(src)).rstrip('/')
    if pkg_resources.resource_isdir(package_name, src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        for res in pkg_resources.resource_listdir(__name__, src):
            copy_resource(src + '/' + res, dest)

    elif not os.path.isfile(dest):
        if os.path.splitext(src)[1] not in ('.pyc', ):
            with open(dest, 'wb') as (f):
                f.write(pkg_resources.resource_string(__name__, src))
    else:
        print('File exists: %s ' % dest)


application = None

def get_propel_config(cwd, key):
    with open('%s/%s' % (cwd, 'propel.yml')) as (f):
        config = yaml.load(f)
    return config.get(key)


def get_push_remotes_list(cwd, key=None):
    """
    Returns the remote hosts in propel
    :param cwd:
    :param key:
    :param file:
    :return: list
    """
    config = get_propel_config(cwd, 'deploy-remotes')
    if key:
        return config[key]
    else:
        return [v for k, l in config.items() for v in l]


def git_push_to_master(cwd, hosts, name='all', force=False):
    """
    To push to master
    :param cwd:
    :param hosts:
    :param force:
    :return:
    """

    def process_output(line):
        print(line)

    with sh.pushd(cwd):
        name = 'shaft_deploy_%s' % name
        if sh.git('status', '--porcelain').strip():
            raise Exception('Repository is UNCLEAN. Commit your changes')
        remote_list = sh.git('remote').strip().split()
        if name in remote_list:
            sh.git('remote', 'remove', name)
        sh.git('remote', 'add', name, hosts[0])
        if len(hosts) > 1:
            for h in hosts:
                sh.git('remote', 'set-url', name, '--push', '--add', h)

        _o = [
         'push', name, 'master']
        if force:
            _o.append('--force')
        (sh.git)(*_o, **{'_out': process_output})
        sh.git('remote', 'remove', name)


def catch_exception(func):

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            print('-' * 80)
            print('Exception Uncaught')
            print('-' * 80)
            print(ex)
            print('-' * 80)

    return decorated_view


def cwd_to_sys_path():
    sys.path.append(CWD)


def project_name(name):
    return re.compile('[^a-zA-Z0-9_]').sub('', name)


def header(title=None):
    print(__doc__)
    print('v. %s' % __version__)
    print('_' * 80)
    if title:
        print('** %s **' % title)


def build_assets(app):
    from webassets.script import CommandLineEnvironment
    assets_env = app.jinja_env.assets_environment
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()


@click.group()
def cli():
    """ Shaft (http://mardix.github.io/shaft) """
    pass


@click.group()
def cli_user():
    """ Shaft (http://mardix.github.io/shaft) """
    pass


@cli.command('init')
@catch_exception
def init():
    """  Setup Shaft in the current directory """
    shaftpyfile = os.path.join(os.path.join(CWD, 'shaftpy.py'))
    header('Setting up Shaft ...')
    if os.path.isfile(shaftpyfile):
        print('WARNING: It seems like Shaft is already setup!')
        print('*' * 80)
    else:
        copy_resource(SKELETON_DIR + '/', CWD)
        print('')
        print('----- That was so Shaft! ----')
        print('')
        print('- Shaft is now setup')
        print('')
        print("> What's next?")
        print('- Edit the config [ app/config.py ] ')
        print('- If necessary edit and run the command [ shaft :syncdb ]')
        print("- Launch app on development mode, run [ app='www' shaft :serve ]")
        print('')
        print('*' * 80)


@cli.command('serve')
@click.option('--port', '-p', default=5000)
@catch_exception
def server(port):
    """ Serve application in development mode """
    global application
    header('Serving application in development mode ... ')
    print('')
    print('- Port: %s' % port)
    print('')
    cwd_to_sys_path()
    application.app.run(debug=True, host='0.0.0.0', port=port)


@cli.command('syncdb')
def syncdb():
    """ Sync database Create new tables etc... """
    print('Syncing up database...')
    cwd_to_sys_path()
    application = import_string('application')
    if application.app.db:
        if application.app.db.Model:
            application.app.db.create_all()
            for m in application.app.db.Model.__subclasses__():
                if hasattr(m, '_syncdb'):
                    print('Sync up model: %s ...' % m.__name__)
                    getattr(m, '_syncdb')()

    print('Done')


@cli.command('assets2s3')
@catch_exception
def assets2s3():
    """ Upload assets files to S3 """
    import flask_s3
    header('Assets2S3...')
    print('')
    print('Building assets files...')
    print('')
    build_assets(application.app)
    print('')
    print('Uploading assets files to S3 ...')
    flask_s3.create_all(application.app)
    print('')


@cli.command('deploy')
@click.option('--site', '-s', default=None)
@click.option('--remote', '-r', default=None)
@click.option('--force', '-f', is_flag=True, default=False)
@catch_exception
def deploy(site, remote, force):
    """ To deploy application to a git repository """
    if site:
        pass
    else:
        remote_name = remote or 'ALL'
        print('Deploying application to remote: %s ' % remote_name)
        print('...')
        hosts = get_push_remotes_list(CWD, remote or None)
        git_push_to_master(cwd=CWD, hosts=hosts, name=remote_name, force=force)
        print('Done!')


@cli.command('version')
def version():
    print('-' * 80)
    print(__version__)
    print('-' * 80)


@cli.command('npm-install-static')
def npm_static():
    static_path = os.path.join(CWD, 'app/static')
    package_json = os.path.join(static_path, 'package.json')
    vendor_dir_ = os.path.join(static_path, 'vendor')
    node_modules_dir = os.path.join(static_path, 'node_modules')
    if os.path.isfile(package_json):
        shaft_copy = {}
        with open(package_json) as (f):
            package_data = json.load(f)
            if 'shaft' in package_data:
                if 'copy' in package_data['shaft']:
                    shaft_copy = package_data['shaft']['copy']
        with sh.pushd(static_path):
            print('npm install -f')
            sh.npm('install', '-f')
        if shaft_copy:
            print('copying files to vendor directories...')
            if not os.path.isdir(vendor_dir_):
                utils.make_dirs(vendor_dir_)
            for name, v in shaft_copy.items():
                vendor_dir = '%s/%s' % (vendor_dir_, name)
                if not os.path.exists(vendor_dir):
                    utils.make_dirs(vendor_dir)
                for f in v:
                    source = '%s/%s/%s' % (node_modules_dir, name, f)
                    f = f.rsplit('/', 1)[1] if '/' in f else f
                    dest = '%s/%s' % (vendor_dir, f)
                    if f.endswith(('.css', '.js')):
                        utils.copy_file(source, dest)
                    else:
                        utils.copy_dir(source, dest)


def cmd():
    """
    Help to run the command line
    :return:
    """
    global application
    shaftpyfile = os.path.join(os.path.join(CWD, 'shaft_init.py'))
    if os.path.isfile(shaftpyfile):
        cwd_to_sys_path()
        application = import_string('shaft_init')
    else:
        print('-' * 80)
        print("** Missing << 'shaft_init.py' >> @ %s" % CWD)
        print('-' * 80)
    if 'shaftcli' in sys.argv[0]:
        [cmd(cli_user.command, click) for cmd in CLI.__subclasses__()]
        cli_user()
    else:
        cli()