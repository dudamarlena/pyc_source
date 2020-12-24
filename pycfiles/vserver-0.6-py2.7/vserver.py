# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vserver.py
# Compiled at: 2012-03-22 06:12:04
"""Python interface to Linux-VServer for managing hosting systems.

Example:

>>> import vserver
>>> test1 = vserver.HostingVServer(u'test1')
>>> test1.build(ip=u'10.0.0.1',
...             fqdn=u'test1.localhost',
...             mirror=u'http://ftp.fr.debian.org/debian/',
...             timezone=u'Europe/Paris')
>>> test1.install_ssh()
>>> test1.delete()  # dangerous!
"""
__version__ = '0.6'
__author__ = 'Volker Grabsch'
__author_email__ = 'vog@notjusthosting.com'
__url__ = 'http://www.profv.de/python-vserver/'
__classifiers__ = '\n                   Development Status :: 5 - Production/Stable\n                   Environment :: Console\n                   Intended Audience :: Developers\n                   Intended Audience :: System Administrators\n                   License :: OSI Approved :: MIT License\n                   Operating System :: POSIX :: Linux\n                   Programming Language :: Python\n                   Topic :: Software Development :: Libraries :: Python Modules\n                   Topic :: System :: Installation/Setup\n                   Topic :: System :: Systems Administration\n                   Topic :: Utilities\n                   '
__license__ = '\nPermission is hereby granted, free of charge, to any person obtaining\na copy of this software and associated documentation files (the\n"Software"), to deal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify, merge, publish,\ndistribute, sublicense, and/or sell copies of the Software, and to\npermit persons to whom the Software is furnished to do so, subject\nto the following conditions:\n\nThe above copyright notice and this permission notice shall be\nincluded in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\nCLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\nSOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
import subprocess, os, urllib2, re

def parent_property(name):

    def _get(self):
        return getattr(self.p, name)

    def _set(self, value):
        setattr(self.p, name, value)

    return property(_get, _set)


class Error(RuntimeError):

    def __init__(self, message_format, *args):
        self._message = message_format % tuple(args)

    def __str__(self):
        return self._message.encode('UTF-8')


def text_table(format, table):
    widths = [ max(len(table_row[col]) for table_row in table)
     for col in xrange(len(table[0]) - 1)
             ]
    return ('').join(format % (tuple(s + ' ' * (widths[col] - len(s)) for col, s in enumerate(table_row[:-1])) + (table_row[(-1)],)) + '\n' for table_row in table)


class System(object):

    def __init__(self):
        pass

    def read_uri(self, uri):
        f = urllib2.urlopen(uri)
        try:
            return f.read().decode('UTF-8')
        finally:
            f.close()

    def read_binary(self, path):
        if path[0] != '/':
            raise Error('Not an absolute path: %s', path)
        f = file(path.encode('UTF-8'), 'r')
        try:
            return f.read()
        finally:
            f.close()

    def write_binary(self, path, mode, binary):
        if path[0] != '/':
            raise Error('Not an absolute path: %s', path)
        try:
            current_mode = os.stat(path.encode('UTF-8')).st_mode & 4095
            if current_mode != mode:
                raise Error('File already exists with different mode: %s\n\nCurrent mode:  %04o\nExpected mode: %04o', path, current_mode, mode)
        except OSError as e:
            pass

        fd = os.open(path.encode('UTF-8'), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, mode)
        f = os.fdopen(fd, 'w')
        try:
            f.write(binary)
        finally:
            f.close()
            os.chmod(path.encode('UTF-8'), mode)

    def run(self, command, input=None, allowed_returncodes=None):
        if isinstance(command, basestring):
            raise Error('The command should be given as list, not string: %r', command)
        if input is None:
            stdin = file(os.devnull, 'r')
        else:
            stdin = subprocess.PIPE
            input = input.encode('UTF-8')
        try:
            process = subprocess.Popen([ arg.encode('UTF-8') for arg in command ], bufsize=0, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=False, cwd=None, env={'PATH': os.getenv('PATH')}, universal_newlines=False)
        except OSError as e:
            raise Error('Command %r: %s', command, e)

        output, error = process.communicate(input)
        output = output.decode('UTF-8')
        error = error.decode('UTF-8')
        returncode = process.returncode
        if allowed_returncodes is None:
            allowed_returncodes = [
             0]
        if returncode not in allowed_returncodes:
            raise Error('Command failed: %r\n\nReturn code: %i\n\nOutput:\n%s\n\nError:\n%s', command, returncode, output.strip('\n'), error.strip('\n'))
        return (
         returncode, output.decode('UTF-8'))


class VServer(object):

    def __init__(self, name):
        self.p = System()
        self._name = name
        self._dirs = {}

    def read_uri(self, uri):
        return self.p.read_uri(uri)

    def _one_line(self, text):
        if text == '':
            raise Error('Empty line.')
        if '\n' in text[:-1]:
            raise Error('Multiple lines where a single line was expected:\n%s', text.strip('\n'))
        if text[(-1)] != '\n':
            raise Error('Incomplete line: %s', text)
        return text[:-1]

    def _path(self, path_type, path):
        if path[0] != '/':
            raise Error('Not an absolute path: %s', path)
        if not self._dirs.has_key(path_type):
            returncode, output = self.p.run(['vserver-info', self._name, path_type])
            self._dirs[path_type] = self._one_line(output)
        return self._dirs[path_type] + path

    def _read_cfg(self, path):
        return self.p.read_binary(self._path('CFGDIR', path)).decode('UTF-8')

    def _write_cfg(self, path, mode, content):
        self.p.write_binary(self._path('CFGDIR', path), mode, content.encode('UTF-8'))

    def read_binary(self, path):
        return self.p.read_binary(self._path('VDIR', path))

    def write_binary(self, path, mode, binary):
        self.p.write_binary(self._path('VDIR', path), mode, binary)

    def read(self, path):
        return self.read_binary(path).decode('UTF-8')

    def write(self, path, mode, content):
        self.write_binary(path, mode, content.encode('UTF-8'))

    def read_one_line(self, path):
        return self._one_line(self.read(path))

    def write_one_line(self, path, mode, line):
        if '\n' in line:
            raise Error('Invalid line break in: %r', line)
        self.write(path, mode, '%s\n' % (line,))

    def read_table(self, path, regex):
        regex = re.compile(regex)
        return tuple(regex.match(line).groups() for line in self.read(path).splitlines())

    def write_table(self, path, mode, format, table):
        widths = [ max(len(table_row[col]) for table_row in table)
         for col in xrange(len(table[0]) - 1)
                 ]
        self.write(path, mode, ('').join(format % (tuple(s + ' ' * (widths[col] - len(s)) for col, s in enumerate(table_row[:-1])) + (table_row[(-1)],)) + '\n' for table_row in table))

    def run(self, command, input=None, allowed_returncodes=None):
        return self.p.run(['vserver', self._name, 'exec'] + command, input, allowed_returncodes)

    def _get_running(self):
        returncode, output = self.p.run(['vserver', self._name, 'running'], allowed_returncodes=[
         0, 1])
        return returncode == 0

    def _set_running(self, running):
        if running:
            self.p.run(['vserver', self._name, 'start'])
        else:
            self.p.run(['vserver', self._name, 'stop'])

    running = property(_get_running, _set_running)

    def _get_start_on_boot(self):
        try:
            mark = self._read_cfg('/apps/init/mark')
        except IOError as e:
            return False

        if mark == 'default\n':
            return True
        if mark == '':
            return False
        raise Error('Unexpected init mark: %r', mark)

    def _set_start_on_boot(self, start_on_boot):
        if start_on_boot:
            self._write_cfg('/apps/init/mark', 420, 'default\n')
        else:
            self._write_cfg('/apps/init/mark', 420, '')

    start_on_boot = property(_get_start_on_boot, _set_start_on_boot)

    def build(self, ip, fqdn, interface, method):
        self.p.run(['vserver', self._name, 'build',
         '--hostname', self._name,
         '--interface', interface,
         '-m'] + method)
        self.write_table('/etc/hosts', 420, '%s  %s', (
         ('127.0.0.1', 'localhost'),
         (
          ip, '%s %s' % (fqdn, self._name))))
        self._write_cfg('/fstab', 420, 'none  /proc     proc    defaults        0 0\nnone  /dev/pts  devpts  gid=5,mode=620  0 0\n')
        self.running = True

    def delete(self):
        self.p.run(['vserver', self._name, 'delete'], input='Y\n')


class DebianVServer(object):

    def __init__(self, name):
        self.p = VServer(name)
        self._updated = False

    def read_uri(self, uri):
        return self.p.read_uri(uri)

    def _get_timezone(self):
        return self.p.read_one_line('/etc/timezone')

    def _set_timezone(self, timezone):
        self.p.write_binary('/etc/localtime', 420, self.p.read_binary('/usr/share/zoneinfo/%s' % (timezone,)))
        self.p.write_one_line('/etc/timezone', 420, timezone)

    timezone = property(_get_timezone, _set_timezone)
    _ssh_host_key_paths = (
     ('/etc/ssh/ssh_host_dsa_key', 384),
     ('/etc/ssh/ssh_host_dsa_key.pub', 420),
     ('/etc/ssh/ssh_host_rsa_key', 384),
     ('/etc/ssh/ssh_host_rsa_key.pub', 420))

    def _get_ssh_host_keys(self):
        return dict((path, self.p.read(path)) for path, mode in self._ssh_host_key_paths)

    def _set_ssh_host_keys(self, ssh_host_keys):
        for path, mode in self._ssh_host_key_paths:
            self.p.write(path, mode, ssh_host_keys[path])

    ssh_host_keys = property(_get_ssh_host_keys, _set_ssh_host_keys)

    def _get_ssh_config(self):
        return self.p.read_table('/etc/ssh/sshd_config', '([^# ]*)\\s*(.*)')

    def _set_ssh_config(self, ssh_config):
        self.p.write_table('/etc/ssh/sshd_config', 420, '%s  %s', ssh_config)

    ssh_config = property(_get_ssh_config, _set_ssh_config)

    def _get_apt_sources(self):
        return self.p.read_table('/etc/apt/sources.list', '(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(.+)')

    def _set_apt_sources(self, sources):
        self.p.write_table('/etc/apt/sources.list', 420, '%s  %s  %s  %s', sources)
        self._updated = False
        self._update()

    apt_sources = property(_get_apt_sources, _set_apt_sources)

    def add_apt_keys(self, keys):
        self.p.run(['apt-key', 'add', '-'], input=keys)

    def _update(self):
        if not self._updated:
            self.p.run(['aptitude', 'update', '-y'])
            self._updated = True

    def safe_upgrade(self):
        self._update()
        self.p.run(['aptitude', 'safe-upgrade', '-y'])

    def install(self, *packages):
        self._update()
        self.p.run(['aptitude', 'install', '-y', '-R'] + list(packages))

    def start_service(self, service):
        self.p.run(['/etc/init.d/%s' % (service,), 'start'])

    def stop_service(self, service):
        self.p.run(['/etc/init.d/%s' % (service,), 'stop'])

    def set_service(self, service, script):
        self.p.write('/etc/init.d/%s' % (service,), 493, script)
        self.p.run(['update-rc.d', service, 'defaults'])

    def _get_running_services(self):
        returncode, output = self.p.run(['netstat', '-lnp'])
        return output.splitlines()

    running_services = property(_get_running_services)

    def add_user(self, user):
        self.p.run(['useradd', '-m', '--', user])

    def del_user(self, user):
        self.p.run(['userdel', '-r', '--', user])

    def set_user_password(self, user, password):
        if password is None:
            self.p.run(['passwd', '-l', '--', user])
        else:
            self.p.run(['chpasswd'], input='%s:%s\n' % (user, password))
        return

    def set_apache_module_enabled(self, module, enabled):
        if enabled:
            self.p.run(['a2enmod', module])
        else:
            self.p.run(['a2dismod', module])

    def set_apache_site_enabled(self, site, enabled):
        if enabled:
            self.p.run(['a2ensite', site])
        else:
            self.p.run(['a2dissite', site])

    def add_zope_instance(self, version, user, zope_user, zope_password):
        self.p.run(['su', '-', user, '-c',
         "dzhandle -z'%s' make-instance default -m manual -u '%s:%s'" % (
          version, zope_user, zope_password)])

    running = parent_property('running')
    start_on_boot = parent_property('start_on_boot')

    def build(self, ip, fqdn, mirror, suite):
        self.p.build(ip, fqdn, 'dummy0:%s/32' % (ip,), [
         'debootstrap', '--',
         '-m', mirror,
         '-d', suite])
        self.apt_sources = (
         (
          'deb', mirror, '%s' % (suite,), 'main contrib non-free'),
         (
          'deb', 'http://security.debian.org/', '%s/updates' % (suite,), 'main contrib non-free'),
         (
          'deb', 'http://www.backports.org/debian/', '%s-backports' % (suite,), 'main contrib non-free'))
        self.safe_upgrade()

    def delete(self):
        self.p.delete()


class HostingVServer(object):

    def __init__(self, name):
        self.p = DebianVServer(name)

    def build(self, ip, fqdn, mirror, timezone):
        self.p.build(ip, fqdn, mirror, 'squeeze')
        self.p.start_on_boot = True
        self.p.timezone = timezone
        self.p.set_user_password('root', None)
        self.p.install('less', 'vim', 'emacs', 'curl', 'w3m', 'rsync', 'mmv', 'htop', 'mc', 'pwgen', 'bzip2', 'unzip', 'gcc', 'g++', 'make', 'locales-all', 'rcs', 'cvs', 'subversion', 'mercurial', 'python-pygments', 'darcs', 'git-core', 'cogito', 'netpbm', 'imagemagick', 'ffmpeg', 'ffmpeg2theora')
        running_services = self.p.running_services
        if len(running_services) != 5:
            raise Error('Unexpected running services:\n%s', ('\n').join(running_services))
        return

    def delete(self):
        self.p.delete()

    def install_ssh(self, keys_vserver=None):
        self.p.install('openssh-server', 'openssh-client')
        self.p.stop_service('ssh')
        self.p.ssh_config = (
         ('Port', '22'),
         ('Protocol', '2'),
         ('PermitRootLogin', 'no'),
         ('X11Forwarding', 'yes'),
         ('PrintMotd', 'no'),
         ('UseDNS', 'no'),
         ('ChallengeResponseAuthentication', 'no'),
         ('Subsystem', 'sftp /usr/lib/openssh/sftp-server'))
        if keys_vserver is not None:
            self.p.ssh_host_keys = keys_vserver.p.ssh_host_keys
        self.p.start_service('ssh')
        return

    def install_tex(self):
        self.p.install('texlive', 'latex-beamer', 'latex-xcolor', 'lmodern', 'bibclean', 'pgf', 'preview-latex-style', 'gs-gpl', 'psutils', 'xpdf-utils')

    def install_mailrelay(self, host, port, user, password, local_email):
        self.p.install('esmtp', 'esmtp-run')
        self.p.p.run(['chown', 'root:mail', '/etc/esmtprc'])
        self.p.p.run(['chmod', '0640', '/etc/esmtprc'])
        self.p.p.run(['chown', 'root:mail', '/usr/bin/esmtp'])
        self.p.p.run(['chmod', '2755', '/usr/bin/esmtp'])
        self.p.p.write('/etc/esmtprc', 416, 'hostname=%s:%i\nusername=%s\npassword=%s\nstarttls=disabled\nmda="/usr/sbin/sendmail -f noreply@`hostname -f` %s"\n' % (
         host, port, user, password, local_email))

    def install_postgresql(self):
        version = '8.4'
        self.p.install('postgresql-%s' % (version,), 'postgresql-server-dev-%s' % (version,), 'libpq-dev')
        self.p.stop_service('postgresql-%s' % (version,))
        self.p.p.write('/etc/postgresql/%s/main/pg_hba.conf' % (version,), 416, 'local  all  postgres  ident\nlocal  all  all       ident\n')
        postgresql_conf_path = '/etc/postgresql/%s/main/postgresql.conf' % (version,)
        self.p.p.write(postgresql_conf_path, 420, self.p.p.read(postgresql_conf_path) + "\nlisten_addresses = ''\n")
        self.p.start_service('postgresql-%s' % (version,))

    def add_postgresql_user(self, user, superuser=False, createdb=False, createrole=False):
        options = ''
        if superuser:
            options += ' SUPERUSER'
        else:
            options += ' NOSUPERUSER'
        if createdb:
            options += ' CREATEDB'
        else:
            options += ' NOCREATEDB'
        if createrole:
            options += ' CREATEROLE'
        else:
            options += ' NOCREATEROLE'
        self.p.p.run(['su', '-', 'postgres', '-c', 'psql -v ON_ERROR_STOP=1'], input='CREATE USER "%s"%s;' % (user, options))

    def install_webserver(self, default_site):
        self.p.install('awstats', 'libgeo-ipfree-perl', 'apache2-mpm-itk', 'libapache2-mod-fcgid', 'libapache2-mod-php5', 'libapache2-svn', 'libapache2-mod-wsgi', 'php5-cgi', 'php5-cli', 'php5-curl', 'php5-gd', 'php5-imagick', 'php5-imap', 'php5-json', 'php5-ldap', 'php5-mcrypt', 'php5-mhash', 'php5-mysql', 'php5-pgsql', 'php-imlib', 'php-mail-mime', 'php-soap', 'libphp-jpgraph', 'libphp-phplot', 'libcompress-zlib-perl', 'libemail-send-perl', 'libhtml-format-perl', 'libmailtools-perl', 'libnet-dns-perl', 'libnet-ip-perl', 'libnet-smtpauth-perl', 'libwww-perl', 'libxml-perl', 'libxml-parser-perl', 'libxml-libxml-perl', 'python-4suite', 'python-egenix-mxdatetime', 'python-egenix-mxtools', 'python-flup', 'python-ldap', 'python-mysqldb', 'python-pgsql', 'python-pip', 'python-psyco', 'python-psycopg2', 'python-pyopenssl', 'python-tz', 'python-unit', 'python-virtualenv', 'python-webpy', 'python-xml', 'ruby', 'ruby-dev', 'irb', 'rdoc', 'libfcgi-ruby', 'libyaml-ruby', 'libzlib-ruby', 'libopenssl-ruby', 'liberb-ruby', 'libdbd-mysql-ruby', 'libdbd-pg-ruby', 'libdbd-sqlite3-ruby', 'libtermios-ruby', 'libjson-ruby', 'libreadline-ruby', 'libredcloth-ruby', 'librmagick-ruby')
        self.p.stop_service('apache2')
        self.p.p.write('/etc/awstats/awstats.conf.local', 420, 'Lang="auto"\nAllowToUpdateStatsFromBrowser=1\n\nLogFormat=1\nWrapperScript="/"\nDirIcons="icon"\nEnableLockForUpdate=1\nAllowAccessFromWebToAuthenticatedUsersOnly=1\n\nLoadPlugin="geoipfree"\n')
        self.p.p.write('/etc/apache2/ports.conf', 420, 'Listen 80\nListen 443\n')
        self.p.p.write('/etc/apache2/conf.d/charset', 420, '#AddDefaultCharset UTF-8\n')
        self.p.p.write('/etc/apache2/mods-available/dir.conf', 420, '<IfModule mod_dir.c>\n    DirectoryIndex index.html index.wsgi index.fcgi index.cgi index.pl index.php index.xhtml index.htm\n</IfModule>\n')
        self.p.p.write('/etc/apache2/mods-available/fcgid.conf', 420, '<IfModule mod_fcgid.c>\n    AddHandler fcgid-script .fcgi\n    SocketPath /var/lib/apache2/fcgid/sock\n    IPCConnectTimeout 20\n    IPCCommTimeout 30\n</IfModule>\n')
        self.p.p.write('/etc/apache2/mods-available/wsgi.conf', 420, '<IfModule mod_wsgi.c>\n    AddHandler wsgi-script .wsgi\n</IfModule>\n')
        self.p.p.write('/etc/php5/conf.d/local_settings.ini', 420, 'memory_limit = 256M\n')
        self.p.set_apache_module_enabled('expires', True)
        self.p.set_apache_module_enabled('fcgid', True)
        self.p.set_apache_module_enabled('include', True)
        self.p.set_apache_module_enabled('php5', True)
        self.p.set_apache_module_enabled('rewrite', True)
        self.p.set_apache_module_enabled('ssl', True)
        self.p.set_apache_module_enabled('wsgi', True)
        self.p.start_service('apache2')

    def install_zope2(self, user, password, zope_user, zope_password):
        self.p.install('python-4suite', 'python-egenix-mxdatetime', 'python-egenix-mxtools', 'python-ldap', 'python-mysqldb', 'python-pgsql', 'python-psyco', 'python-psycopg2', 'python-pyopenssl', 'python-tz', 'python-unit', 'python-xml', 'zope2.10')
        self.p.set_service('zope-users', '#!/bin/sh\n\nVERSION=\'2.10\'\nUSERS=`getent passwd | awk -F: \'$3 >= 1000 && $3 < 2000 {print $1}\'`\n\ncase "$1" in\n    start)\n        for USER in $USERS; do\n            echo -e -n "Start zope instance of user $USER:\\t"\n            su - "$USER" -c "~/zope/instance/zope$VERSION/default/bin/zopectl start"\n        done\n        ;;\n    stop)\n        for USER in $USERS; do\n            echo -e -n "Stop zope instance of user $USER:\\t"\n            su - "$USER" -c "~/zope/instance/zope$VERSION/default/bin/zopectl stop"\n        done\n        ;;\n    restart)\n        "$0" stop\n        "$0" start\n        ;;\n    *)\n        echo "Usage: $0 {start|stop|restart}"\n        exit 1\n        ;;\nesac\n')
        self.p.add_user(user)
        self.p.set_user_password(user, password)
        self.p.add_zope_instance('2.10', user, zope_user, zope_password)
        self.p.start_service('zope-users')


def _test():
    """Run all doc tests of this module."""
    import doctest, vserver
    return doctest.testmod(vserver)


if __name__ == '__main__':
    _test()