# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/installers/ubuntu/trac.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6270 bytes
from boto.pyami.installers.ubuntu.installer import Installer
import boto, os

class Trac(Installer):
    """Trac"""

    def install(self):
        self.run('apt-get -y install trac', notify=True, exit_on_error=True)
        self.run('apt-get -y install libapache2-svn', notify=True, exit_on_error=True)
        self.run('a2enmod ssl')
        self.run('a2enmod mod_python')
        self.run('a2enmod dav_svn')
        self.run('a2enmod rewrite')
        self.run('touch /var/log/boto.log')
        self.run('chmod a+w /var/log/boto.log')

    def setup_vhost(self):
        domain = boto.config.get('Trac', 'hostname').strip()
        if domain:
            domain_info = domain.split('.')
            cnf = open('/etc/apache2/sites-available/%s' % domain_info[0], 'w')
            cnf.write('NameVirtualHost *:80\n')
            if boto.config.get('Trac', 'SSLCertificateFile'):
                cnf.write('NameVirtualHost *:443\n\n')
                cnf.write('<VirtualHost *:80>\n')
                cnf.write('\tServerAdmin %s\n' % boto.config.get('Trac', 'server_admin').strip())
                cnf.write('\tServerName %s\n' % domain)
                cnf.write('\tRewriteEngine On\n')
                cnf.write('\tRewriteRule ^(.*)$ https://%s$1\n' % domain)
                cnf.write('</VirtualHost>\n\n')
                cnf.write('<VirtualHost *:443>\n')
            else:
                cnf.write('<VirtualHost *:80>\n')
            cnf.write('\tServerAdmin %s\n' % boto.config.get('Trac', 'server_admin').strip())
            cnf.write('\tServerName %s\n' % domain)
            cnf.write('\tDocumentRoot %s\n' % boto.config.get('Trac', 'home').strip())
            cnf.write('\t<Directory %s>\n' % boto.config.get('Trac', 'home').strip())
            cnf.write('\t\tOptions FollowSymLinks Indexes MultiViews\n')
            cnf.write('\t\tAllowOverride All\n')
            cnf.write('\t\tOrder allow,deny\n')
            cnf.write('\t\tallow from all\n')
            cnf.write('\t</Directory>\n')
            cnf.write('\t<Location />\n')
            cnf.write('\t\tAuthType Basic\n')
            cnf.write('\t\tAuthName "%s"\n' % boto.config.get('Trac', 'name'))
            cnf.write('\t\tRequire valid-user\n')
            cnf.write('\t\tAuthUserFile /mnt/apache/passwd/passwords\n')
            cnf.write('\t</Location>\n')
            data_dir = boto.config.get('Trac', 'data_dir')
            for env in os.listdir(data_dir):
                if env[0] != '.':
                    cnf.write('\t<Location /trac/%s>\n' % env)
                    cnf.write('\t\tSetHandler mod_python\n')
                    cnf.write('\t\tPythonInterpreter main_interpreter\n')
                    cnf.write('\t\tPythonHandler trac.web.modpython_frontend\n')
                    cnf.write('\t\tPythonOption TracEnv %s/%s\n' % (data_dir, env))
                    cnf.write('\t\tPythonOption TracUriRoot /trac/%s\n' % env)
                    cnf.write('\t</Location>\n')
                    continue

            svn_dir = boto.config.get('Trac', 'svn_dir')
            for env in os.listdir(svn_dir):
                if env[0] != '.':
                    cnf.write('\t<Location /svn/%s>\n' % env)
                    cnf.write('\t\tDAV svn\n')
                    cnf.write('\t\tSVNPath %s/%s\n' % (svn_dir, env))
                    cnf.write('\t</Location>\n')
                    continue

            cnf.write('\tErrorLog /var/log/apache2/error.log\n')
            cnf.write('\tLogLevel warn\n')
            cnf.write('\tCustomLog /var/log/apache2/access.log combined\n')
            cnf.write('\tServerSignature On\n')
            SSLCertificateFile = boto.config.get('Trac', 'SSLCertificateFile')
            if SSLCertificateFile:
                cnf.write('\tSSLEngine On\n')
                cnf.write('\tSSLCertificateFile %s\n' % SSLCertificateFile)
            SSLCertificateKeyFile = boto.config.get('Trac', 'SSLCertificateKeyFile')
            if SSLCertificateKeyFile:
                cnf.write('\tSSLCertificateKeyFile %s\n' % SSLCertificateKeyFile)
            SSLCertificateChainFile = boto.config.get('Trac', 'SSLCertificateChainFile')
            if SSLCertificateChainFile:
                cnf.write('\tSSLCertificateChainFile %s\n' % SSLCertificateChainFile)
            cnf.write('</VirtualHost>\n')
            cnf.close()
            self.run('a2ensite %s' % domain_info[0])
            self.run('/etc/init.d/apache2 force-reload')

    def main(self):
        self.install()
        self.setup_vhost()