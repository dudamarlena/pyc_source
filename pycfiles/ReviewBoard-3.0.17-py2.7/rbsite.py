# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/cmdline/rbsite.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import print_function, unicode_literals
import getpass, imp, logging, os, pkg_resources, platform, re, shutil, sys, textwrap, subprocess, warnings
from importlib import import_module
from optparse import OptionGroup, OptionParser
from random import choice as random_choice
from django.db.utils import OperationalError
from django.utils import six
from django.utils.encoding import force_str
from django.utils.six.moves import input
from django.utils.six.moves.urllib.request import urlopen
import reviewboard
from reviewboard import get_manual_url, get_version_string
from reviewboard.rb_platform import SITELIST_FILE_UNIX, DEFAULT_FS_CACHE_PATH, INSTALLED_SITE_PATH
warnings.filterwarnings(b'ignore', category=PendingDeprecationWarning)
VERSION = get_version_string()
DEBUG = False
options = None
args = None
site = None
ui = None

class Dependencies(object):
    """An object which queries and caches dependency information."""
    memcached_modules = [
     b'memcache']
    sqlite_modules = [b'pysqlite2', b'sqlite3']
    mysql_modules = [b'MySQLdb']
    postgresql_modules = [b'psycopg2']
    cache_dependency_info = {b'required': False, 
       b'title': b'Server Cache', 
       b'dependencies': [
                       (
                        b'memcached', memcached_modules)]}
    db_dependency_info = {b'required': True, 
       b'title': b'Databases', 
       b'dependencies': [
                       (
                        b'sqlite3', sqlite_modules),
                       (
                        b'MySQL', mysql_modules),
                       (
                        b'PostgreSQL', postgresql_modules)]}

    @classmethod
    def get_support_memcached(cls):
        """Return whether memcached is supported."""
        return cls.has_modules(cls.memcached_modules)

    @classmethod
    def get_support_mysql(cls):
        """Return whether mysql is supported."""
        return cls.has_modules(cls.mysql_modules)

    @classmethod
    def get_support_postgresql(cls):
        """Return whether postgresql is supported."""
        return cls.has_modules(cls.postgresql_modules)

    @classmethod
    def get_support_sqlite(cls):
        """Return whether sqlite is supported."""
        return cls.has_modules(cls.sqlite_modules)

    @classmethod
    def get_missing(cls):
        """Return any missing dependencies.

        This will return a two-tuple, where the first item is a boolean
        indicating if any missing dependencies are fatal, and the second is a
        list of missing dependency groups.
        """
        fatal = False
        missing_groups = []
        for dep_info in [cls.cache_dependency_info,
         cls.db_dependency_info]:
            missing_deps = []
            for desc, modules in dep_info[b'dependencies']:
                if not cls.has_modules(modules):
                    missing_deps.append(b'%s (%s)' % (desc, (b', ').join(modules)))

            if missing_deps:
                if dep_info[b'required'] and len(missing_deps) == len(dep_info[b'dependencies']):
                    fatal = True
                    text = b'%s (required)' % dep_info[b'title']
                else:
                    text = b'%s (optional)' % dep_info[b'title']
                missing_groups.append({b'title': text, 
                   b'dependencies': missing_deps})

        return (fatal, missing_groups)

    @classmethod
    def has_modules(cls, names):
        """Return True if one of the specified modules is installed."""
        for name in names:
            try:
                __import__(name)
                return True
            except ImportError:
                continue

        return False


class Site(object):
    """An object which contains the configuration for a Review Board site."""
    CACHE_BACKENDS = {b'memcached': b'django.core.cache.backends.memcached.MemcachedCache', 
       b'file': b'django.core.cache.backends.filebased.FileBasedCache'}

    def __init__(self, install_dir, options):
        """Initialize the site."""
        self.install_dir = self.get_default_site_path(install_dir)
        self.abs_install_dir = os.path.abspath(self.install_dir)
        self.site_id = os.path.basename(install_dir).replace(b' ', b'_').replace(b'.', b'_')
        self.options = options
        self.company = None
        self.domain_name = None
        self.web_server_port = None
        self.site_root = None
        self.static_url = None
        self.media_url = None
        self.db_type = None
        self.db_name = None
        self.db_host = None
        self.db_port = None
        self.db_user = None
        self.db_pass = None
        self.reenter_db_pass = None
        self.cache_type = None
        self.cache_info = None
        self.web_server_type = None
        self.python_loader = None
        self.admin_user = None
        self.admin_password = None
        self.reenter_admin_password = None
        self.send_support_usage_stats = True
        return

    def get_default_site_path(self, install_dir):
        """Return the default site path."""
        if os.path.isabs(install_dir) or os.sep in install_dir:
            return install_dir
        return os.path.join(INSTALLED_SITE_PATH, install_dir)

    def rebuild_site_directory(self):
        """Rebuild the site hierarchy."""
        htdocs_dir = os.path.join(self.install_dir, b'htdocs')
        errordocs_dir = os.path.join(htdocs_dir, b'errordocs')
        media_dir = os.path.join(htdocs_dir, b'media')
        static_dir = os.path.join(htdocs_dir, b'static')
        self.mkdir(self.install_dir)
        self.mkdir(os.path.join(self.install_dir, b'logs'))
        self.mkdir(os.path.join(self.install_dir, b'conf'))
        self.mkdir(os.path.join(self.install_dir, b'tmp'))
        os.chmod(os.path.join(self.install_dir, b'tmp'), 511)
        self.mkdir(os.path.join(self.install_dir, b'data'))
        self.mkdir(htdocs_dir)
        self.mkdir(media_dir)
        self.mkdir(static_dir)
        uploaded_dir = os.path.join(media_dir, b'uploaded')
        self.mkdir(uploaded_dir)
        writable_st = os.stat(uploaded_dir)
        writable_dirs = [
         os.path.join(uploaded_dir, b'images'),
         os.path.join(uploaded_dir, b'files'),
         os.path.join(media_dir, b'ext'),
         os.path.join(static_dir, b'ext')]
        for writable_dir in writable_dirs:
            self.mkdir(writable_dir)
            try:
                if hasattr(os, b'chown'):
                    os.chown(writable_dir, writable_st.st_uid, writable_st.st_gid)
            except OSError:
                pass

        if os.path.exists(errordocs_dir) and os.path.islink(errordocs_dir):
            os.unlink(errordocs_dir)
        self.mkdir(errordocs_dir)
        self.process_template(b'cmdline/conf/errordocs/500.html.in', os.path.join(errordocs_dir, b'500.html'))
        self.link_pkg_dir(b'reviewboard', b'htdocs/static/lib', os.path.join(static_dir, b'lib'))
        self.link_pkg_dir(b'reviewboard', b'htdocs/static/rb', os.path.join(static_dir, b'rb'))
        self.link_pkg_dir(b'reviewboard', b'htdocs/static/admin', os.path.join(static_dir, b'admin'))
        self.link_pkg_dir(b'djblets', b'htdocs/static/djblets', os.path.join(static_dir, b'djblets'))
        self.unlink_media_dir(os.path.join(media_dir, b'admin'))
        self.unlink_media_dir(os.path.join(media_dir, b'djblets'))
        self.unlink_media_dir(os.path.join(media_dir, b'rb'))
        common_htaccess = [
         b'<IfModule mod_expires.c>', b'  <FilesMatch "\\.(jpg|gif|png|css|js|htc)">', b'    ExpiresActive on', b'    ExpiresDefault "access plus 1 year"', b'  </FilesMatch>', b'</IfModule>', b'', b'<IfModule mod_deflate.c>'] + [ b'  AddOutputFilterByType DEFLATE %s' % mimetype for mimetype in [b'text/html', b'text/plain', b'text/xml', b'text/css', b'text/javascript', b'application/javascript', b'application/x-javascript'] ] + [
         b'</IfModule>']
        static_htaccess = common_htaccess
        media_htaccess = common_htaccess + [
         b'<IfModule mod_headers.c>',
         b'  Header set Content-Disposition "attachment"',
         b'</IfModule>']
        with open(os.path.join(static_dir, b'.htaccess'), b'w') as (fp):
            fp.write((b'\n').join(static_htaccess))
            fp.write(b'\n')
        with open(os.path.join(media_dir, b'.htaccess'), b'w') as (fp):
            fp.write((b'\n').join(media_htaccess))
            fp.write(b'\n')

    def setup_settings(self):
        """Set up the environment for running django management commands."""
        sys.path.insert(0, os.path.join(self.abs_install_dir, b'conf'))
        os.environ[b'DJANGO_SETTINGS_MODULE'] = b'reviewboard.settings'

    def get_apache_version(self):
        """Return the version of the installed apache."""
        try:
            apache_version = subprocess.check_output([b'httpd', b'-v'])
            m = re.search(b'Apache\\/(\\d+).(\\d+)', apache_version)
            if m:
                return m.group(1, 2)
            raise re.error
        except:
            return (2, 2)

    def generate_cron_files(self):
        """Generate sample crontab for this site."""
        self.process_template(b'cmdline/conf/cron.conf.in', os.path.join(self.install_dir, b'conf', b'cron.conf'))

    def generate_config_files(self):
        """Generate the configuration files for this site."""
        web_conf_filename = b''
        enable_fastcgi = False
        enable_wsgi = False
        if self.web_server_type == b'apache':
            if self.python_loader == b'fastcgi':
                web_conf_filename = b'apache-fastcgi.conf'
                enable_fastcgi = True
            elif self.python_loader == b'wsgi':
                web_conf_filename = b'apache-wsgi.conf'
                enable_wsgi = True
            else:
                assert False
            apache_version = self.get_apache_version()
            if apache_version[0] >= 2 and apache_version[1] >= 4:
                self.apache_auth = b'Require all granted'
            else:
                self.apache_auth = b'Allow from all'
        elif self.web_server_type == b'lighttpd':
            web_conf_filename = b'lighttpd.conf'
            enable_fastcgi = True
        else:
            assert False
        conf_dir = os.path.join(self.install_dir, b'conf')
        htdocs_dir = os.path.join(self.install_dir, b'htdocs')
        self.process_template(b'cmdline/conf/%s.in' % web_conf_filename, os.path.join(conf_dir, web_conf_filename))
        self.generate_cron_files()
        if enable_fastcgi:
            fcgi_filename = os.path.join(htdocs_dir, b'reviewboard.fcgi')
            self.process_template(b'cmdline/conf/reviewboard.fcgi.in', fcgi_filename)
            os.chmod(fcgi_filename, 493)
        elif enable_wsgi:
            wsgi_filename = os.path.join(htdocs_dir, b'reviewboard.wsgi')
            self.process_template(b'cmdline/conf/reviewboard.wsgi.in', wsgi_filename)
            os.chmod(wsgi_filename, 493)
        secret_key = (b'').join([ random_choice(b'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)
                                ])
        fp = open(os.path.join(conf_dir, b'settings_local.py'), b'w')
        fp.write(b'# Site-specific configuration settings for Review Board\n')
        fp.write(b'# Definitions of these settings can be found at\n')
        fp.write(b'# http://docs.djangoproject.com/en/dev/ref/settings/\n')
        fp.write(b'\n')
        fp.write(b'# Database configuration\n')
        db_engine = self.db_type
        if db_engine == b'postgresql':
            db_engine = b'postgresql_psycopg2'
        fp.write(b'DATABASES = {\n')
        fp.write(b"    'default': {\n")
        fp.write(b"        'ENGINE': 'django.db.backends.%s',\n" % db_engine)
        fp.write(b"        'NAME': '%s',\n" % self.db_name.replace(b'\\', b'\\\\'))
        if self.db_type != b'sqlite3':
            if b':' in self.db_host:
                self.db_host, self.db_port = self.db_host.split(b':', 1)
            fp.write(b"        'USER': '%s',\n" % (self.db_user or b''))
            fp.write(b"        'PASSWORD': '%s',\n" % (self.db_pass or b''))
            fp.write(b"        'HOST': '%s',\n" % (self.db_host or b''))
            fp.write(b"        'PORT': '%s',\n" % (self.db_port or b''))
        fp.write(b'    },\n')
        fp.write(b'}\n')
        fp.write(b'\n')
        fp.write(b"# Unique secret key. Don't share this with anybody.\n")
        fp.write(b"SECRET_KEY = '%s'\n" % secret_key)
        fp.write(b'\n')
        fp.write(b'# Cache backend settings.\n')
        fp.write(b'CACHES = {\n')
        fp.write(b"    'default': {\n")
        fp.write(b"        'BACKEND': '%s',\n" % self.CACHE_BACKENDS[self.cache_type])
        fp.write(b"        'LOCATION': '%s',\n" % self.cache_info)
        fp.write(b'    },\n')
        fp.write(b'}\n')
        fp.write(b'\n')
        fp.write(b'# Extra site information.\n')
        fp.write(b'SITE_ID = 1\n')
        fp.write(b"SITE_ROOT = '%s'\n" % self.site_root)
        fp.write(b"FORCE_SCRIPT_NAME = ''\n")
        fp.write(b'DEBUG = False\n')
        fp.write(b"ALLOWED_HOSTS = ['%s']\n" % (self.domain_name or b'*'))
        fp.close()
        self.setup_settings()

    def sync_database(self, allow_input=False):
        """Synchronize the database."""
        global ui
        params = []
        if not allow_input:
            params.append(b'--noinput')
        while True:
            try:
                self.run_manage_command(b'syncdb', params)
                break
            except OperationalError as e:
                ui.error(b'There was an error synchronizing the database. Make sure the database is created and has the appropriate permissions, and then continue.\nDetails: %s' % e, force_wait=True)
            except Exception:
                raise

        self.run_manage_command(b'registerscmtools')

    def migrate_database(self):
        """Perform a database migration."""
        self.run_manage_command(b'evolve', [b'--noinput', b'--execute'])

    def harden_passwords(self):
        """Harden any password storage.

        Any legacy plain-text passwords will be encrypted, and any
        repositories with stored credentials that are also associated with
        a hosting service will have those credentials removed.
        """
        from reviewboard.scmtools.models import Repository
        repositories = Repository.objects.filter(hosting_account__isnull=False).exclude(username=b'', encrypted_password=b'')
        repositories.update(username=b'', encrypted_password=b'')
        Repository.objects.encrypt_plain_text_passwords()

    def get_static_media_upgrade_needed(self):
        """Determine if a static media config upgrade is needed."""
        from djblets.siteconfig.models import SiteConfiguration
        siteconfig = SiteConfiguration.objects.get_current()
        manual_updates = siteconfig.settings.get(b'manual-updates', {})
        resolved_update = manual_updates.get(b'static-media', False)
        return not resolved_update and pkg_resources.parse_version(siteconfig.version) < pkg_resources.parse_version(b'1.7')

    def get_diff_dedup_needed(self):
        """Determine if there's likely duplicate diff data stored."""
        from reviewboard.diffviewer.models import FileDiff
        try:
            return FileDiff.objects.unmigrated().exists()
        except:
            return True

    def get_settings_upgrade_needed(self):
        """Determine if a settings upgrade is needed."""
        try:
            import settings_local
            if hasattr(settings_local, b'DATABASE_ENGINE') or hasattr(settings_local, b'CACHE_BACKEND'):
                return True
            if hasattr(settings_local, b'DATABASES'):
                engine = settings_local.DATABASES[b'default'][b'ENGINE']
                if not engine.startswith(b'django.db.backends'):
                    return True
        except ImportError:
            sys.stderr.write(b'Unable to import settings_local. Cannot determine if upgrade is needed.\n')

        return False

    def upgrade_settings(self):
        """Perform a settings upgrade."""
        settings_file = os.path.join(self.abs_install_dir, b'conf', b'settings_local.py')
        perform_upgrade = False
        buf = []
        database_info = {}
        database_keys = ('ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT')
        backend_info = {}
        from django.core.cache import parse_backend_uri, InvalidCacheBackendError
        try:
            import settings_local
            if hasattr(settings_local, b'DATABASE_ENGINE'):
                engine = settings_local.DATABASE_ENGINE
                if engine in ('sqlite3', 'mysql', 'postgresql', 'postgresql_psycopg2'):
                    engine = b'django.db.backends.' + engine
                database_info[b'ENGINE'] = engine
                for key in database_keys:
                    if key != b'ENGINE':
                        database_info[key] = getattr(settings_local, b'DATABASE_%s' % key, b'')

                perform_upgrade = True
            if hasattr(settings_local, b'DATABASES'):
                engine = settings_local.DATABASES[b'default'][b'ENGINE']
                if engine == b'postgresql_psycopg2':
                    perform_upgrade = True
            if hasattr(settings_local, b'CACHE_BACKEND'):
                try:
                    backend_info = parse_backend_uri(settings_local.CACHE_BACKEND)
                    perform_upgrade = True
                except InvalidCacheBackendError:
                    pass

        except ImportError:
            sys.stderr.write(b'Unable to import settings_local for upgrade.\n')
            return

        if not perform_upgrade:
            return
        fp = open(settings_file, b'r')
        found_database = False
        found_cache = False
        for line in fp.readlines():
            if line.startswith(b'DATABASE_'):
                if not found_database:
                    found_database = True
                    buf.append(b'DATABASES = {\n')
                    buf.append(b"    'default': {\n")
                    for key in database_keys:
                        if database_info[key]:
                            buf.append(b"        '%s': '%s',\n" % (
                             key, database_info[key]))

                    buf.append(b'    },\n')
                    buf.append(b'}\n')
            elif line.startswith(b'CACHE_BACKEND') and backend_info:
                if not found_cache:
                    found_cache = True
                    buf.append(b'CACHES = {\n')
                    buf.append(b"    'default': {\n")
                    buf.append(b"        'BACKEND': '%s',\n" % self.CACHE_BACKENDS[backend_info[0]])
                    buf.append(b"        'LOCATION': '%s',\n" % backend_info[1])
                    buf.append(b'    },\n')
                    buf.append(b'}\n')
            elif line.strip().startswith(b"'ENGINE': 'postgresql_psycopg2'"):
                buf.append(b"        'ENGINE': 'django.db.backends.postgresql_psycopg2',\n")
            else:
                buf.append(line)

        fp.close()
        fp = open(settings_file, b'w')
        fp.writelines(buf)
        fp.close()
        del sys.modules[b'settings_local']
        del sys.modules[b'reviewboard.settings']
        import django.conf
        django.conf.settings = django.conf.LazySettings()

    def create_admin_user(self):
        """Create an administrator user account."""
        from django.contrib.auth.models import User
        if not User.objects.filter(username=self.admin_user).exists():
            cwd = os.getcwd()
            os.chdir(self.abs_install_dir)
            User.objects.create_superuser(self.admin_user, self.admin_email, self.admin_password)
            os.chdir(cwd)

    def register_support_page(self):
        """Register this installation with the support data tracker."""
        from reviewboard.admin.support import get_register_support_url
        url = get_register_support_url(force_is_admin=True)
        try:
            urlopen(url, timeout=5).read()
        except:
            pass

    def run_manage_command(self, cmd, params=None):
        """Run a given django management command."""
        cwd = os.getcwd()
        os.chdir(self.abs_install_dir)
        try:
            from django.core.management import execute_from_command_line, get_commands
            os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', b'reviewboard.settings')
            if not params:
                params = []
            if DEBUG:
                params.append(b'--verbosity=0')
            commands_dir = os.path.join(self.abs_install_dir, b'commands')
            if os.path.exists(commands_dir):
                get_commands()
                from django.core.management import _commands
                for command in os.listdir(commands_dir):
                    module_globals = {}
                    filename = os.path.join(commands_dir, command)
                    with open(filename) as (f):
                        code = compile(f.read(), filename, b'exec')
                        exec code in module_globals
                    if b'Command' in module_globals:
                        name = os.path.splitext(f)[0]
                        _commands[name] = module_globals[b'Command']()

            execute_from_command_line([__file__, cmd] + params)
        except ImportError as e:
            ui.error(b'Unable to execute the manager command %s: %s' % (
             cmd, e))

        os.chdir(cwd)

    def mkdir(self, dirname):
        """Create a directory, but only if it doesn't already exist."""
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def link_pkg_dir(self, pkgname, src_path, dest_dir, replace=True):
        """Create the package directory."""
        src_dir = pkg_resources.resource_filename(pkgname, src_path)
        if os.path.islink(dest_dir) and not os.path.exists(dest_dir):
            os.unlink(dest_dir)
        if os.path.exists(dest_dir):
            if not replace:
                return
            self.unlink_media_dir(dest_dir)
        if self.options.copy_media:
            shutil.copytree(src_dir, dest_dir)
        else:
            os.symlink(src_dir, dest_dir)

    def unlink_media_dir(self, path):
        """Delete the given media directory and all contents."""
        if os.path.exists(path):
            if os.path.islink(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)

    def process_template(self, template_path, dest_filename):
        """Generate a file from a template."""
        domain_name = self.domain_name or b''
        domain_name_escaped = domain_name.replace(b'.', b'\\.')
        template = pkg_resources.resource_string(b'reviewboard', template_path)
        sitedir = os.path.abspath(self.install_dir).replace(b'\\', b'/')
        if self.site_root:
            site_root = self.site_root
            site_root_noslash = site_root[1:-1]
        else:
            site_root = b'/'
            site_root_noslash = b''
        if hasattr(sys, b'frozen') or hasattr(sys, b'importers') or imp.is_frozen(b'__main__'):
            rbsite_path = sys.executable
        else:
            rbsite_path = b'"%s" "%s"' % (sys.executable, sys.argv[0])
        data = {b'rbsite': rbsite_path, 
           b'port': self.web_server_port, 
           b'sitedir': sitedir, 
           b'sitedomain': domain_name, 
           b'sitedomain_escaped': domain_name_escaped, 
           b'siteid': self.site_id, 
           b'siteroot': site_root, 
           b'siteroot_noslash': site_root_noslash}
        if hasattr(self, b'apache_auth'):
            data[b'apache_auth'] = self.apache_auth
        template = re.sub(b'@([a-z_]+)@', lambda m: data.get(m.group(1)), template)
        fp = open(dest_filename, b'w')
        fp.write(template)
        fp.close()


class SiteList(object):
    """Maintains the list of sites installed on the system."""

    def __init__(self, path):
        """Initialize the site list."""
        self.path = path
        self.sites = set()
        if os.path.exists(self.path):
            f = open(self.path, b'r')
            for line in f:
                site = line.strip()
                if os.path.exists(site):
                    self.sites.add(site)

            f.close()

    def add_site(self, site_path):
        """Add a site to the site list."""
        self.sites.add(site_path)
        ordered_sites = list(self.sites)
        ordered_sites.sort()
        if not os.path.exists(os.path.dirname(self.path)):
            try:
                os.makedirs(os.path.dirname(self.path), 493)
            except:
                print(b'WARNING: Could not save site to sitelist %s' % self.path)
                return

        with open(self.path, b'w') as (f):
            for site in ordered_sites:
                f.write(b'%s\n' % site)


class UIToolkit(object):
    """An abstract class that forms the basis for all UI interaction.

    Subclasses can override this to provide new ways of representing the UI
    to the user.
    """

    def run(self):
        """Run the UI."""
        pass

    def page(self, text, allow_back=True, is_visible_func=None, on_show_func=None):
        """Add a new "page" to display to the user.

        Input and text are associated with this page and may be displayed
        immediately or later, depending on the toolkit.

        If is_visible_func is specified and returns False, this page will
        be skipped.
        """
        return

    def prompt_input(self, page, prompt, default=None, password=False, normalize_func=None, save_obj=None, save_var=None):
        """Prompt the user for some text. This may contain a default value."""
        raise NotImplementedError

    def prompt_choice(self, page, prompt, choices, save_obj=None, save_var=None):
        """Prompt the user for an item amongst a list of choices."""
        raise NotImplementedError

    def text(self, page, text):
        """Display a block of text to the user."""
        raise NotImplementedError

    def disclaimer(self, page, text):
        """Display a block of disclaimer text to the user."""
        raise NotImplementedError

    def urllink(self, page, url):
        """Display a URL to the user."""
        raise NotImplementedError

    def itemized_list(self, page, title, items):
        """Display an itemized list."""
        raise NotImplementedError

    def step(self, page, text, func):
        """Add a step of a multi-step operation.

        This will indicate when it's starting and when it's complete.
        """
        raise NotImplementedError

    def error(self, text, force_wait=False, done_func=None):
        """Display a block of error text to the user."""
        raise NotImplementedError


class ConsoleUI(UIToolkit):
    """A UI toolkit that simply prints to the console."""

    def __init__(self):
        """Initialize the UI toolkit."""
        super(UIToolkit, self).__init__()
        self.header_wrapper = textwrap.TextWrapper(initial_indent=b'* ', subsequent_indent=b'  ')
        indent_str = b'    '
        self.text_wrapper = textwrap.TextWrapper(initial_indent=indent_str, subsequent_indent=indent_str, break_long_words=False)
        self.error_wrapper = textwrap.TextWrapper(initial_indent=b'[!] ', subsequent_indent=b'    ', break_long_words=False)

    def page(self, text, allow_back=True, is_visible_func=None, on_show_func=None):
        """Add a new "page" to display to the user.

        In the console UI, we only care if we need to display or ask questions
        for this page. Our representation of a page in this case is simply
        a boolean value. If False, nothing associated with this page will
        be displayed to the user.
        """
        visible = not is_visible_func or is_visible_func()
        if not visible:
            return False
        if on_show_func:
            on_show_func()
        print()
        print()
        print(self.header_wrapper.fill(text))
        return True

    def prompt_input(self, page, prompt, default=None, password=False, yes_no=False, optional=False, normalize_func=None, save_obj=None, save_var=None):
        """Prompt the user for some text. This may contain a default value."""
        if not save_obj:
            raise AssertionError
            assert save_var
            return page or None
        else:
            if yes_no:
                if default:
                    prompt = b'%s [Y/n]' % prompt
                else:
                    prompt = b'%s [y/N]' % prompt
                    default = False
            else:
                if default:
                    self.text(page, b'The default is %s' % default)
                    prompt = b'%s [%s]' % (prompt, default)
                elif optional:
                    prompt = b'%s (optional)' % prompt
                print()
                prompt += b': '
                value = None
                while not value:
                    if password:
                        temp_value = getpass.getpass(force_str(prompt))
                        if save_var.startswith(b'reenter'):
                            if not self.confirm_reentry(save_obj, save_var, temp_value):
                                self.error(b'Passwords must match.')
                                continue
                        value = temp_value
                    else:
                        value = input(prompt)
                    if not value:
                        if default:
                            value = default
                        elif optional:
                            break
                    if yes_no:
                        if isinstance(value, bool):
                            norm_value = value
                        else:
                            assert isinstance(value, six.string_types)
                            norm_value = value.lower()
                        if norm_value not in (True, False, b'y', b'n', b'yes', b'no'):
                            self.error(b'Must specify one of Y/y/yes or N/n/no.')
                            value = None
                            continue
                        else:
                            value = norm_value in (True, b'y', b'yes')
                            break
                    elif not value:
                        self.error(b'You must answer this question.')

            if normalize_func:
                value = normalize_func(value)
            setattr(save_obj, save_var, value)
            return

    def confirm_reentry(self, obj, reenter_var, value):
        """Confirm whether a re-entered piece of data matches.

        This is used to ensure that secrets and passwords are what the user
        intended to type.
        """
        global site
        first_var = reenter_var.replace(b'reenter_', b'')
        first_entry = getattr(site, first_var)
        return first_entry == value

    def prompt_choice(self, page, prompt, choices, save_obj=None, save_var=None):
        """Prompt the user for an item amongst a list of choices."""
        if not save_obj:
            raise AssertionError
            assert save_var
            return page or None
        else:
            self.text(page, b'You can type either the name or the number from the list below.')
            valid_choices = []
            i = 0
            for choice in choices:
                description = b''
                enabled = True
                if isinstance(choice, six.string_types):
                    text = choice
                elif len(choice) == 2:
                    text, enabled = choice
                else:
                    text, description, enabled = choice
                if enabled:
                    self.text(page, b'(%d) %s %s\n' % (i + 1, text, description), leading_newline=i == 0)
                    valid_choices.append(text)
                    i += 1

            print()
            prompt += b': '
            choice = None
            while not choice:
                choice = input(prompt)
                if choice not in valid_choices:
                    try:
                        i = int(choice) - 1
                        if 0 <= i < len(valid_choices):
                            choice = valid_choices[i]
                            break
                    except ValueError:
                        pass

                    self.error(b"'%s' is not a valid option." % choice)
                    choice = None

            setattr(save_obj, save_var, choice)
            return

    def text(self, page, text, leading_newline=True, wrap=True):
        """Display a block of text to the user.

        This will wrap the block to fit on the user's screen.
        """
        if not page:
            return
        if leading_newline:
            print()
        if wrap:
            print(self.text_wrapper.fill(text))
        else:
            print(b'    %s' % text)

    def disclaimer(self, page, text):
        """Display a disclaimer to the user."""
        self.text(page, b'NOTE: %s' % text)

    def urllink(self, page, url):
        """Display a URL to the user."""
        self.text(page, url, wrap=False)

    def itemized_list(self, page, title, items):
        """Display an itemized list."""
        if title:
            self.text(page, b'%s:' % title)
        for item in items:
            self.text(page, b'    * %s' % item, False)

    def step(self, page, text, func):
        """Add a step of a multi-step operation.

        This will indicate when it's starting and when it's complete.
        """
        sys.stdout.write(b'%s ... ' % text)
        func()
        print(b'OK')

    def error(self, text, force_wait=False, done_func=None):
        """Display a block of error text to the user."""
        print()
        for text_block in text.split(b'\n'):
            print(self.error_wrapper.fill(text_block))

        if force_wait:
            print()
            input(b'Press Enter to continue')
        if done_func:
            done_func()


class Command(object):
    """An abstract command."""
    needs_ui = False

    def add_options(self, parser):
        """Add any command-specific options to the parser."""
        pass

    def run(self):
        """Run the command."""
        pass


class InstallCommand(Command):
    """Installer command.

    This command installs a new Review Board site tree and generates web server
    configuration files. This will ask several questions about the site before
    performing the installation.
    """
    needs_ui = True

    def add_options(self, parser):
        """Add any command-specific options to the parser."""
        is_windows = platform.system() == b'Windows'
        group = OptionGroup(parser, b"'install' command", self.__doc__.strip())
        group.add_option(b'--advanced', action=b'store_true', dest=b'advanced', default=False, help=b'provide more advanced configuration options')
        group.add_option(b'--copy-media', action=b'store_true', dest=b'copy_media', default=is_windows, help=b'copy media files instead of symlinking')
        group.add_option(b'--noinput', action=b'store_true', default=False, help=b'run non-interactively using configuration provided in command-line options')
        group.add_option(b'--opt-out-support-data', action=b'store_false', default=True, dest=b'send_support_usage_stats', help=b'opt out of sending data and stats for improved user and admin support')
        group.add_option(b'--company', help=b'the name of the company or organization that owns the server')
        group.add_option(b'--domain-name', help=b'fully-qualified host name of the site, excluding the http://, port or path')
        group.add_option(b'--site-root', default=b'/', help=b'path to the site relative to the domain name')
        group.add_option(b'--static-url', default=b'static/', help=b'the URL containing the static (shipped) media files')
        group.add_option(b'--media-url', default=b'media/', help=b'the URL containing the uploaded media files')
        group.add_option(b'--db-type', help=b'database type (mysql, postgresql or sqlite3)')
        group.add_option(b'--db-name', default=b'reviewboard', help=b'database name (not for sqlite3)')
        group.add_option(b'--db-host', default=b'localhost', help=b'database host (not for sqlite3)')
        group.add_option(b'--db-user', help=b'database user (not for sqlite3)')
        group.add_option(b'--db-pass', help=b'password for the database user (not for sqlite3)')
        group.add_option(b'--cache-type', default=b'memcached', help=b'cache server type (memcached or file)')
        group.add_option(b'--cache-info', default=b'localhost:11211', help=b'cache identifier (memcached connection string or file cache directory)')
        group.add_option(b'--web-server-type', default=b'apache', help=b'web server (apache or lighttpd)')
        group.add_option(b'--web-server-port', help=b'port that the web server should listen on', default=b'80')
        group.add_option(b'--python-loader', default=b'wsgi', help=b'python loader for apache (fastcgi or wsgi)')
        group.add_option(b'--admin-user', default=b'admin', help=b"the site administrator's username")
        group.add_option(b'--admin-password', help=b"the site administrator's password")
        group.add_option(b'--admin-email', help=b"the site administrator's e-mail address")
        if not is_windows:
            group.add_option(b'--sitelist', default=SITELIST_FILE_UNIX, help=b'the path to a file storing a list of installed sites')
        parser.add_option_group(group)

    def run(self):
        """Run the command."""
        global options
        if not self.check_permissions():
            return
        site.__dict__.update(options.__dict__)
        self.print_introduction()
        if self.print_missing_dependencies():
            return
        if not options.noinput:
            self.ask_domain()
            self.ask_site_root()
            if options.advanced:
                self.ask_shipped_media_url()
                self.ask_uploaded_media_url()
            self.ask_database_type()
            self.ask_database_name()
            self.ask_database_host()
            self.ask_database_login()
            if options.advanced:
                self.ask_cache_type()
            self.ask_cache_info()
            if options.advanced:
                self.ask_web_server_type()
                self.ask_python_loader()
            self.ask_admin_user()
            self.ask_support_data()
        self.show_install_status()
        self.show_finished()
        self.show_get_more()

    def normalize_root_url_path(self, path):
        """Convert user-specified root URL paths to a normal format."""
        if not path.endswith(b'/'):
            path += b'/'
        if not path.startswith(b'/'):
            path = b'/' + path
        return path

    def normalize_media_url_path(self, path):
        """Convert user-specified media URLs to a normal format."""
        if not path.endswith(b'/'):
            path += b'/'
        if path.startswith(b'/'):
            path = path[1:]
        return path

    def check_permissions(self):
        """Check that permissions are usable.

        If not, this will show an error to the user.
        """
        try:
            if os.path.exists(site.install_dir):
                os.rmdir(site.install_dir)
            os.mkdir(site.install_dir)
            os.rmdir(site.install_dir)
            return True
        except OSError:
            ui.error(b"Unable to create the %s directory. Make sure you're running as an administrator and that the directory does not contain any files." % site.install_dir, done_func=lambda : sys.exit(1))
            return False

    def print_introduction(self):
        """Print an introduction to the site installer."""
        page = ui.page(b'Welcome to the Review Board site installation wizard')
        ui.text(page, b'This will prepare a Review Board site installation in:')
        ui.text(page, site.abs_install_dir)
        ui.text(page, b'We need to know a few things before we can prepare your site for installation. This will only take a few minutes.')

    def print_missing_dependencies(self):
        """Print information on any missing dependencies."""
        fatal, missing_dep_groups = Dependencies.get_missing()
        if missing_dep_groups:
            if fatal:
                page = ui.page(b'Required modules are missing')
                ui.text(page, b'You are missing Python modules that are needed before the installation process. You will need to install the necessary modules and restart the install.')
            else:
                page = ui.page(b'Make sure you have the modules you need')
                ui.text(page, b'Depending on your installation, you may need certain Python modules and servers that are missing.')
                ui.text(page, b'If you need support for any of the following, you will need to install the necessary modules and restart the install.')
            for group in missing_dep_groups:
                ui.itemized_list(page, group[b'title'], group[b'dependencies'])

        return fatal

    def ask_domain(self):
        """Ask the user what domain Review Board will be served from."""
        page = ui.page(b"What's the host name for this site?")
        ui.text(page, b'This should be the fully-qualified host name without the http://, port or path.')
        ui.prompt_input(page, b'Domain Name', site.domain_name, save_obj=site, save_var=b'domain_name')

    def ask_site_root(self):
        """Ask the user what site root they'd like."""
        page = ui.page(b'What URL path points to Review Board?')
        ui.text(page, b'Typically, Review Board exists at the root of a URL. For example, http://reviews.example.com/. In this case, you would specify "/".')
        ui.text(page, b'However, if you want to listen to, say, http://example.com/reviews/, you can specify "/reviews/".')
        ui.text(page, b'Note that this is the path relative to the domain and should not include the domain name.')
        ui.prompt_input(page, b'Root Path', site.site_root, normalize_func=self.normalize_root_url_path, save_obj=site, save_var=b'site_root')

    def ask_shipped_media_url(self):
        """Ask the user the URL where shipped media files are served."""
        page = ui.page(b'What URL will point to the shipped media files?')
        ui.text(page, b'While most installations distribute media files on the same server as the rest of Review Board, some custom installs may instead have a separate server for this purpose.')
        ui.text(page, b"If unsure, don't change the default.")
        ui.prompt_input(page, b'Shipped Media URL', site.static_url, normalize_func=self.normalize_media_url_path, save_obj=site, save_var=b'static_url')

    def ask_uploaded_media_url(self):
        """Ask the user the URL where uploaded media files are served."""
        page = ui.page(b'What URL will point to the uploaded media files?')
        ui.text(page, b'Note that this is different from shipped media. This is where all uploaded screenshots, file attachments, and extension media will go. It must be a different location from the shipped media.')
        ui.text(page, b"If unsure, don't change the default.")
        ui.prompt_input(page, b'Uploaded Media URL', site.media_url, normalize_func=self.normalize_media_url_path, save_obj=site, save_var=b'media_url')

    def ask_database_type(self):
        """Ask the user for the database type."""
        page = ui.page(b'What database type will you be using?')
        ui.prompt_choice(page, b'Database Type', [
         (
          b'mysql', Dependencies.get_support_mysql()),
         (
          b'postgresql', Dependencies.get_support_postgresql()),
         (
          b'sqlite3', b'(not supported for production use)',
          Dependencies.get_support_sqlite())], save_obj=site, save_var=b'db_type')

    def ask_database_name(self):
        """Ask the user for the database name."""

        def determine_sqlite_path():
            site.db_name = sqlite_db_name

        sqlite_db_name = os.path.join(site.abs_install_dir, b'data', b'reviewboard.db')
        page = ui.page(b'Determining database file path', is_visible_func=lambda : site.db_type == b'sqlite3', on_show_func=determine_sqlite_path)
        ui.text(page, b'The sqlite database file will be stored in %s' % sqlite_db_name)
        ui.text(page, b'If you are migrating from an existing installation, you can move your existing database there, or edit settings_local.py to point to your old location.')
        page = ui.page(b'What database name should Review Board use?', is_visible_func=lambda : site.db_type != b'sqlite3')
        ui.disclaimer(page, b'You need to create this database and grant user modification rights before continuing. See your database documentation for more information.')
        ui.prompt_input(page, b'Database Name', site.db_name, save_obj=site, save_var=b'db_name')

    def ask_database_host(self):
        """Ask the user for the database host."""
        page = ui.page(b"What is the database server's address?", is_visible_func=lambda : site.db_type != b'sqlite3')
        ui.text(page, b"This should be specified in hostname:port form. The port is optional if you're using a standard port for the database type.")
        ui.prompt_input(page, b'Database Server', site.db_host, save_obj=site, save_var=b'db_host')

    def ask_database_login(self):
        """Ask the user for database login credentials."""
        page = ui.page(b'What is the login and password for this database?', is_visible_func=lambda : site.db_type != b'sqlite3')
        ui.text(page, b'This must be a user that has table creation and modification rights on the database you already specified.')
        ui.prompt_input(page, b'Database Username', site.db_user, save_obj=site, save_var=b'db_user')
        ui.prompt_input(page, b'Database Password', site.db_pass, password=True, save_obj=site, save_var=b'db_pass')
        ui.prompt_input(page, b'Confirm Database Password', password=True, save_obj=site, save_var=b'reenter_db_pass')

    def ask_cache_type(self):
        """Ask the user what type of caching they'd like to use."""
        page = ui.page(b'What cache mechanism should be used?')
        ui.text(page, b'memcached is strongly recommended. Use it unless you have a good reason not to.')
        ui.prompt_choice(page, b'Cache Type', [
         (
          b'memcached', b'(recommended)',
          Dependencies.get_support_memcached()),
         b'file'], save_obj=site, save_var=b'cache_type')

    def ask_cache_info(self):
        """Ask the user for caching configuration."""
        page = ui.page(b'What memcached host should be used?', is_visible_func=lambda : site.cache_type == b'memcached')
        ui.text(page, b'This is in the format of hostname:port')
        ui.prompt_input(page, b'Memcache Server', site.cache_info, save_obj=site, save_var=b'cache_info')
        page = ui.page(b'Where should the temporary cache files be stored?', is_visible_func=lambda : site.cache_type == b'file')
        ui.prompt_input(page, b'Cache Directory', site.cache_info or DEFAULT_FS_CACHE_PATH, save_obj=site, save_var=b'cache_info')

    def ask_web_server_type(self):
        """Ask the user which web server they're using."""
        page = ui.page(b'What web server will you be using?')
        ui.prompt_choice(page, b'Web Server', [b'apache', b'lighttpd'], save_obj=site, save_var=b'web_server_type')

    def ask_python_loader(self):
        """Ask the user which Python loader they're using."""
        page = ui.page(b'What Python loader module will you be using?', is_visible_func=lambda : site.web_server_type == b'apache')
        ui.text(page, b'Based on our experiences, we recommend using wsgi with Review Board.')
        ui.prompt_choice(page, b'Python Loader', [
         (
          b'wsgi', b'(recommended)', True),
         b'fastcgi'], save_obj=site, save_var=b'python_loader')

    def ask_admin_user(self):
        """Ask the user to create an admin account."""
        page = ui.page(b'Create an administrator account')
        ui.text(page, b"To configure Review Board, you'll need an administrator account. It is advised to have one administrator and then use that account to grant administrator permissions to your personal user account.")
        ui.text(page, b'If you plan to use NIS or LDAP, use an account name other than your NIS/LDAP account so as to prevent conflicts.')
        ui.prompt_input(page, b'Username', site.admin_user, save_obj=site, save_var=b'admin_user')
        ui.prompt_input(page, b'Password', site.admin_password, password=True, save_obj=site, save_var=b'admin_password')
        ui.prompt_input(page, b'Confirm Password', password=True, save_obj=site, save_var=b'reenter_admin_password')
        ui.prompt_input(page, b'E-Mail Address', site.admin_email, save_obj=site, save_var=b'admin_email')
        ui.prompt_input(page, b'Company/Organization Name', site.company, save_obj=site, save_var=b'company', optional=True)

    def ask_support_data(self):
        """Ask the user if they'd like to enable support data collection."""
        page = ui.page(b'Enable collection of data for better support')
        ui.text(page, b'We would like to periodically collect data and statistics about your installation to provide a better support experience for you and your users.')
        ui.text(page, b'The data collected includes basic information such as your company name, the version of Review Board, and the size of your install. It does NOT include confidential data such as source code. Data collected never leaves our server and is never given to any third parties for any purposes.')
        ui.text(page, b"We use this to provide a user support page that's more specific to your server. We also use it to determine which versions to continue to support, and to help track how upgrades affect our number of bug reports and support incidents.")
        ui.text(page, b'You can choose to turn this off at any time in Support Settings in Review Board.')
        ui.prompt_input(page, b'Allow us to collect support data?', site.send_support_usage_stats, yes_no=True, save_obj=site, save_var=b'send_support_usage_stats')

    def show_install_status(self):
        """Show the install status page."""
        page = ui.page(b'Installing the site...', allow_back=False)
        ui.step(page, b'Building site directories', site.rebuild_site_directory)
        ui.step(page, b'Building site configuration files', site.generate_config_files)
        ui.step(page, b'Creating database', site.sync_database)
        ui.step(page, b'Performing migrations', site.migrate_database)
        ui.step(page, b'Creating administrator account', site.create_admin_user)
        ui.step(page, b'Saving site settings', self.save_settings)
        ui.step(page, b'Setting up support', self.setup_support)

    def show_finished(self):
        """Show the finished page."""
        page = ui.page(b'The site has been installed', allow_back=False)
        ui.text(page, b'The site has been installed in %s' % site.abs_install_dir)
        ui.text(page, b'Sample configuration files for web servers and cron are available in the conf/ directory.')
        ui.text(page, b'You need to modify the ownership of the following directories and their contents to be owned by the web server:')
        ui.itemized_list(page, None, [
         os.path.join(site.abs_install_dir, b'htdocs', b'media', b'uploaded'),
         os.path.join(site.abs_install_dir, b'htdocs', b'media', b'ext'),
         os.path.join(site.abs_install_dir, b'htdocs', b'static', b'ext'),
         os.path.join(site.abs_install_dir, b'data')])
        ui.text(page, b'For more information, visit:')
        ui.urllink(page, b'%sadmin/installation/creating-sites/' % get_manual_url())
        return

    def show_get_more(self):
        """Show the "Get More out of Review Board" page."""
        from reviewboard.admin.support import get_install_key
        page = ui.page(b'Get more out of Review Board', allow_back=False)
        ui.text(page, b'To enable PDF document review, enhanced scalability, GitHub Enterprise support, and more, download Power Pack at:')
        ui.urllink(page, b'https://www.reviewboard.org/powerpack/')
        ui.text(page, b'Your install key for Power Pack is: %s' % get_install_key())
        ui.text(page, b'Support contracts for Review Board are also available:')
        ui.urllink(page, b'https://www.beanbaginc.com/support/contracts/')

    def save_settings(self):
        """Save some settings in the database."""
        from django.contrib.sites.models import Site
        from djblets.siteconfig.models import SiteConfiguration
        cur_site = Site.objects.get_current()
        cur_site.domain = site.domain_name
        cur_site.save()
        if site.static_url.startswith(b'http'):
            site_static_url = site.static_url
        else:
            site_static_url = site.site_root + site.static_url
        if site.media_url.startswith(b'http'):
            site_media_url = site.media_url
        else:
            site_media_url = site.site_root + site.media_url
        htdocs_path = os.path.join(site.abs_install_dir, b'htdocs')
        site_media_root = os.path.join(htdocs_path, b'media')
        site_static_root = os.path.join(htdocs_path, b'static')
        siteconfig = SiteConfiguration.objects.get_current()
        siteconfig.set(b'company', site.company)
        siteconfig.set(b'send_support_usage_stats', site.send_support_usage_stats)
        siteconfig.set(b'site_static_url', site_static_url)
        siteconfig.set(b'site_static_root', site_static_root)
        siteconfig.set(b'site_media_url', site_media_url)
        siteconfig.set(b'site_media_root', site_media_root)
        siteconfig.set(b'site_admin_name', site.admin_user)
        siteconfig.set(b'site_admin_email', site.admin_email)
        siteconfig.save()
        if platform.system() != b'Windows':
            abs_sitelist = os.path.abspath(site.sitelist)
            print(b'Saving site %s to the sitelist %s\n' % (
             site.install_dir, abs_sitelist))
            sitelist = SiteList(abs_sitelist)
            sitelist.add_site(site.install_dir)

    def setup_support(self):
        """Set up the support page for the installation."""
        if site.send_support_usage_stats:
            site.register_support_page()


class UpgradeCommand(Command):
    """Upgrades an existing site installation.

    This will synchronize media trees and upgrade the database, unless
    otherwise specified.
    """

    def add_options(self, parser):
        """Add any command-specific options to the parser."""
        group = OptionGroup(parser, b"'upgrade' command", self.__doc__.strip())
        group.add_option(b'--no-db-upgrade', action=b'store_false', dest=b'upgrade_db', default=True, help=b"don't upgrade the database")
        group.add_option(b'--all-sites', action=b'store_true', dest=b'all_sites', default=False, help=b'Upgrade all installed sites')
        parser.add_option_group(group)

    def run(self):
        """Run the command."""
        site.setup_settings()
        diff_dedup_needed = site.get_diff_dedup_needed()
        static_media_upgrade_needed = site.get_static_media_upgrade_needed()
        data_dir_exists = os.path.exists(os.path.join(site.install_dir, b'data'))
        print(b'Rebuilding directory structure')
        site.rebuild_site_directory()
        site.generate_cron_files()
        if site.get_settings_upgrade_needed():
            print(b'Upgrading site settings_local.py')
            site.upgrade_settings()
        if options.upgrade_db:
            print(b'Updating database. This may take a while.\n\nThe log output below, including warnings and errors,\ncan be ignored unless upgrade fails.\n\n------------------ <begin log output> ------------------')
            site.sync_database()
            site.migrate_database()
            print(b'------------------- <end log output> -------------------\n\nResetting in-database caches.')
            site.run_manage_command(b'fixreviewcounts')
        site.harden_passwords()
        from djblets.siteconfig.models import SiteConfiguration
        siteconfig = SiteConfiguration.objects.get_current()
        if siteconfig.get(b'send_support_usage_stats'):
            site.register_support_page()
        print()
        print(b'Upgrade complete!')
        if not data_dir_exists:
            print()
            print(b"A new 'data' directory has been created inside of your site")
            print(b'directory. This will act as the home directory for programs')
            print(b'invoked by Review Board.')
            print()
            print(b'You need to change the ownership of this directory so that')
            print(b'the web server can write to it.')
        if static_media_upgrade_needed:
            from django.conf import settings
            if b'manual-updates' not in siteconfig.settings:
                siteconfig.settings[b'manual-updates'] = {}
            siteconfig.settings[b'manual-updates'][b'static-media'] = False
            siteconfig.save()
            static_dir = b'%s/htdocs/static' % site.abs_install_dir.replace(b'\\', b'/')
            print()
            print(b'The location of static media files (CSS, JavaScript, images)')
            print(b'has changed. You will need to make manual changes to ')
            print(b'your web server configuration.')
            print()
            print(b'For Apache, you will need to add:')
            print()
            print(b'    <Location "%sstatic">' % settings.SITE_ROOT)
            print(b'        SetHandler None')
            print(b'    </Location>')
            print()
            print(b'    Alias %sstatic "%s"' % (settings.SITE_ROOT,
             static_dir))
            print()
            print(b'For lighttpd:')
            print()
            print(b'    alias.url = (')
            print(b'        ...')
            print(b'        "%sstatic" => "%s",' % (settings.SITE_ROOT,
             static_dir))
            print(b'        ...')
            print(b'    )')
            print()
            print(b'    url.rewrite-once = (')
            print(b'        ...')
            print(b'        "^(%sstatic/.*)$" => "$1",' % settings.SITE_ROOT)
            print(b'        ...')
            print(b'    )')
            print()
            print(b'Once you have made these changes, type the following ')
            print(b'to resolve this:')
            print()
            print(b'    $ rb-site manage %s resolve-check static-media' % site.abs_install_dir)
        if diff_dedup_needed:
            print()
            print(b'There are duplicate copies of diffs in your database that can be condensed.')
            print(b'These are the result of posting several iterations of a change for review on')
            print(b'older versions of Review Board.')
            print()
            print(b'Removing duplicate diff data will save space in your database and speed up')
            print(b'future upgrades.')
            print()
            print(b'To condense duplicate diffs, type the following:')
            print()
            print(b'    $ rb-site manage %s condensediffs' % site.abs_install_dir)


class ManageCommand(Command):
    """Runs a Django management command on the site."""
    help_text = b'Runs a Django management command on the site. Usage: `rb-site manage <path> <command> -- <arguments>.` Run `manage -- --help` for the list of commands.'

    def add_options(self, parser):
        """Add any command-specific options to the parser."""
        group = OptionGroup(parser, b"'manage' command", self.help_text)
        parser.add_option_group(group)

    def run(self):
        """Run the command."""
        site.setup_settings()
        from reviewboard import initialize
        initialize()
        if len(args) == 0:
            ui.error(b'A manage command is needed.', done_func=lambda : sys.exit(1))
        else:
            site.run_manage_command(args[0], args[1:])
            sys.exit(0)


COMMANDS = {b'install': InstallCommand(), 
   b'upgrade': UpgradeCommand(), 
   b'manage': ManageCommand()}

def parse_options(args):
    """Parse the given options."""
    global options
    parser = OptionParser(usage=b'%prog command [options] path', version=b'%%prog %s\nPython %s\nInstalled to %s' % (
     VERSION, sys.version, os.path.dirname(reviewboard.__file__)))
    parser.add_option(b'-d', b'--debug', action=b'store_true', dest=b'debug', default=DEBUG, help=b'display debug output')
    sorted_commands = list(COMMANDS.keys())
    sorted_commands.sort()
    for cmd_name in sorted_commands:
        command = COMMANDS[cmd_name]
        command.add_options(parser)

    options, args = parser.parse_args(args)
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    command = args[0]
    if command == b'upgrade' and options.all_sites:
        sitelist = SiteList(options.sitelist)
        site_paths = sitelist.sites
        if len(site_paths) == 0:
            print(b'No Review Board sites listed in %s' % sitelist.path)
            sys.exit(0)
    elif len(args) >= 2 and command in COMMANDS:
        site_paths = [
         args[1]]
    else:
        parser.print_help()
        sys.exit(1)
    globals()[b'args'] = args[2:]
    return (
     command, site_paths)


def main():
    """Main application loop."""
    global site
    global ui
    import_module(b'djblets.log')
    logging.basicConfig(level=logging.INFO)
    command_name, site_paths = parse_options(sys.argv[1:])
    command = COMMANDS[command_name]
    ui = ConsoleUI()
    for install_dir in site_paths:
        site = Site(install_dir, options)
        os.putenv(b'HOME', os.path.join(site.install_dir, b'data').encode(b'utf-8'))
        command.run()
        ui.run()


if __name__ == b'__main__':
    main()