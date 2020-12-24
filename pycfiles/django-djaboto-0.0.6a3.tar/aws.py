# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-djaboto/djaboto/management/commands/aws.py
# Compiled at: 2013-02-28 14:44:12
import optparse, os, sys
from os.path import isfile
from time import sleep
from fabric import operations as fab_op
from fabric import api as fab_api
from fabric import colors as fab_colors
from fabric.contrib.files import exists as fab_exists
from boto import config as BotoConfig, ec2, exception as BotoException
from urllib import urlencode
from urllib2 import Request
from urllib2 import urlopen
from base64 import b64encode
import json
from django.core.management.base import BaseCommand
import djaboto
from django.conf import settings
PROJECT_TEMPLATES_DIR = os.path.join(os.path.dirname(djaboto.__file__), 'recipe')
AWS_SETTINGS_PROMPTS = {'SITENAME': (
              'Site name', ''), 
   'AWS_INSTANCE_ID': (
                     'AWS instance ID', ''), 
   'AWS_ACCESS_KEY_ID': (
                       'AWS Security Credentials, Access Key ID', ''), 
   'AWS_ACCESS_SECRET': (
                       'AWS Security Credentials, Secret Access Key', ''), 
   'AWS_REGION': (
                'Amazon Region', 'us-west-1'), 
   'AWS_TYPE': (
              'Amazon Instance Type', 't1.micro'), 
   'AWS_AMI_ID': (
                'AMI ID', 'ami-87712ac2'), 
   'AWS_USER': (
              'Instance default username', 'ubuntu'), 
   'AWS_HTTPD_USER': (
                    'Apache user', 'www-data'), 
   'AWS_HTTPD_GROUP': (
                     'Apache group', 'www-data')}

class Command(BaseCommand):
    """
    AWS command class
    """
    args = '[settings|firewall|create|update|perms|apache|restart|reboot|shell|instance|keys|addkey|rmkey|ip|terminate]'
    help = 'Manages the AWS account and settings in your project.\n\nIssuing this command without arguments will provide a list of any available AWS instances.\n\nArguments (sub commands):\n    create    - create the entire server and sync with the local file\n\n    terminate- terminate and instance and remove from .aws_fabric\n    keys     - list the IDs of keys installed on remote\n    addkey   - add new keys to remote\n    rmkey    - remove keys from remote\n    ip       - get ip address of remote\n    instance - create a bare instance and install your ssh key\n    settings - show current settings values stored for this project\n    firewall - create the AWS security groups\n    update   - synchronize files between your local system and  the remote instance\n    perms    - set permissions to default usable values on the remote instance\n    apache   - create an Apache configuration file and enable it on the remote instance\n    restart  - restart the remote Apache service\n    reboot   - reboot the remote instance\n    shell    - open a shell on the remote instance'
    conn = ''
    instance = ''
    option_list = BaseCommand.option_list + (
     optparse.make_option('-d', '--domain', action='store', type='string', dest='domain', help='Domain-name of site (fqdn root, "mydomain.com")'),
     optparse.make_option('--sitename', action='store', type='string', dest='sitename', help='Name of site (directory, "mysite")'),
     optparse.make_option('--instance', action='store', type='string', dest='aws_instance_id', help='AWS instance ID'),
     optparse.make_option('--awskeyid', action='store', type='string', dest='aws_access_key_id', help='AWS Security Credentials, Access Key ID'),
     optparse.make_option('--awssecret', action='store', type='string', dest='aws_access_secret', help='AWS Security Credentials, Secret Access Key'),
     optparse.make_option('--awsregion', action='store', type='string', dest='aws_region', default='us-west-1', help='Amazon Region'),
     optparse.make_option('--awstype', action='store', type='string', dest='aws_type', default='t1.micro', help='Amazon Instance Type'),
     optparse.make_option('--awsami', action='store', type='string', dest='aws_ami', default='ami-87712ac2', help='Amazon AMI ID'),
     optparse.make_option('--sshpubkey', action='store', type='string', dest='aws_security_key', help='path to your SSH public key file'),
     optparse.make_option('--awsuser', action='store', type='string', dest='aws_user', default='ubuntu', help='Instance username'),
     optparse.make_option('--awshttpduser', action='store', type='string', dest='aws_httpd_user', default='www-data', help='Apache username'),
     optparse.make_option('--awshttpdgroup', action='store', type='string', dest='aws_httpd_group', default='www-data', help='Apache group'),
     optparse.make_option('--push', action='store_true', dest='awsoverwrite', help='Force over-write mode to remote aws instance'),
     optparse.make_option('--reinstall', action='store_true', dest='awsreinstall', help='Force re-installation mode for remote aws python instance'),
     optparse.make_option('--initial', action='store_true', dest='initial', help='Initial install - drops existing data and creates empty database'),
     optparse.make_option('--updateos', action='store_true', dest='updateos', help='Update the OS in the process'),
     optparse.make_option('--updatepy', action='store_true', dest='updatepy', help='Update (reinstall) the python virtualenv'),
     optparse.make_option('--noupdatepy', action='store_false', dest='updatepy', help='Do NOT update (reinstall) the python virtualenv'),
     optparse.make_option('--restart', action='store_true', dest='restart', help='Restart the Apache service when finished'),
     optparse.make_option('--reboot', action='store_true', dest='reboot', help='Reboot the server when finished'),
     optparse.make_option('--fabricrc', action='store', type='string', dest='fabricrc', help='Settings file name'))
    fab_api.env['unsaved'] = False

    def handle(self, *args, **options):
        """
        Command argument processor
        """
        reboot = False
        restart = False
        if options.get('sitename', None):
            fab_api.env['SITENAME'] = options['sitename']
            fab_api.env['unsaved'] = True
        fab_api.env['rcfile'] = options.get('fabricrc', './.aws_fabric')
        rcfile = options.get('fabricrc', None)
        if rcfile:
            rcfile = os.path.abspath(rcfile)
        else:
            rcfile = os.path.abspath(os.path.join(os.getcwd(), '.aws_fabric'))
        fab_api.env['rcfile'] = rcfile
        ssh_pubkey_file = options.get('aws_security_key', None)
        self.set_awsSettings()
        if len(args) == 0:
            self.get_awsInstanceList()
        else:
            if 'instance' in args:
                self.set_awsSSHKey()
                self.get_awsInstance()
            elif 'terminate' in args:
                self.cmd_terminateInstance()
            elif 'ip' in args:
                self.cmd_getIP()
            elif 'rmkey' in args:
                self.cmd_rmKey()
            elif 'addkey' in args:
                self.cmd_addKey(ssh_pubkey_file)
            elif 'keys' in args:
                self.cmd_listKeys()
            elif 'settings' in args:
                self.list_awsSettings()
            elif 'firewall' in args:
                self.set_awsSecurityGroups()
            elif 'create' in args:
                self.set_awsSSHKey(ssh_pubkey_file)
                self.set_awsSecurityGroups()
                self.install_awsUbuntuUpgrades()
                self.sync_awsProject(push=True)
                self.install_awsPythonRequirements(reinstall=True)
                self.aws_DropDB()
                self.sync_awsDB()
                self.sync_awsStaticfiles()
                self.set_awsPermissions()
                self.set_awsApacheconf(options.get('domain', None))
                reboot = True
            elif 'dropdb' in args:
                self.aws_DropDB()
                self.sync_awsDB()
            elif 'update' in args:
                if options.get('updateos', False):
                    self.install_awsUbuntuUpgrades()
                self.sync_awsProject(push=options.get('awsoverwrite', False))
                if options.get('updatepy', False):
                    self.install_awsPythonRequirements(reinstall=options.get('awsreinstall', False))
                if options.get('initial', False):
                    self.aws_DropDB()
                self.sync_awsDB()
                if options.get('updatepy', False) or options.get('initial', False):
                    self.sync_awsStaticfiles()
                if options.get('initial', False):
                    self.set_awsPermissions()
                    self.set_awsApacheconf(options.get('domain', None))
                self.set_awsPermissions()
            elif 'perms' in args:
                self.set_awsPermissions()
            elif 'apache' in args:
                self.set_awsApacheconf(options.get('domain', None))
            elif 'shell' in args:
                self.cmd_awsShell()
            elif 'dropdb' in args:
                self.aws_DropDB()
                self.sync_awsDB()
            if reboot or 'reboot' in args or options.get('reboot', False):
                self.cmd_awsReboot()
            elif restart or 'restart' in args or options.get('restart', False):
                self.sync_awsStaticfiles()
                self.set_awsPermissions()
                self.cmd_awsApacheRestart()
        return

    def set_awsSettings(self, path=None):
        """
        Load any settings found, or prompt for them.
        """
        if not path:
            path = fab_api.env.rcfile
        if os.path.exists(path):
            comments = lambda s: s and not s.startswith('#')
            filesettings = filter(comments, open(path, 'r'))
            settings_dict = dict((k.strip(), v.strip()) for k, _, v in [ s.partition('=') for s in filesettings ])
            fab_api.env.update(settings_dict)
        for key, prompt_pair in sorted(AWS_SETTINGS_PROMPTS.items(), key=lambda x: x[0]):
            question, default = prompt_pair
            if key not in fab_api.env and not key == 'AWS_INSTANCE_ID':
                fab_api.prompt('%s :' % question, key, default)
                fab_api.env['unsaved'] = True

        fab_api.env['user'] = fab_api.env.AWS_USER
        self.save_awsSettings()

    def list_awsSettings(self):
        """
        Shows settings related to AWS actions
        """
        print '-' * 55
        print fab_colors.yellow('AWS Instance Settings:')
        print '-' * 55
        for setting in AWS_SETTINGS_PROMPTS:
            if setting in fab_api.env:
                if fab_api.env[setting]:
                    print '%55s : %-20s' % (fab_colors.yellow(AWS_SETTINGS_PROMPTS[setting][0]), fab_colors.cyan(fab_api.env[setting]))

        print '-' * 55

    def save_awsSettings(self, path=None):
        """
        Write the settings for AWS to file
        """
        if not path:
            path = fab_api.env.rcfile
        if fab_api.env.get('unsaved', False):
            fab_api.env['unsaved'] = False
            print fab_colors.green('Saving settings to %s.' % path)
            local_settings_file = open(path, 'w')
            local_settings_file.write('# This file was autocreated from Soupmix.\n')
            local_settings_file.write('# Do not edit this file directly, all changes will be lost!\n')
            for setting in AWS_SETTINGS_PROMPTS:
                if setting in fab_api.env:
                    value = fab_api.env[setting] or ''
                    if value:
                        local_settings_file.write('%s = %s\n' % (setting, value))

            local_settings_file.close()

    def get_awsInstanceList(self):
        """
        Lists all AWS instances in the account
        """
        self.get_awsConnection()
        instance_list = []
        reservations = self.conn.get_all_instances()
        if reservations:
            for reservation in reservations:
                instances = reservation.instances
                for instance in instances:
                    print '%s) %s (%s-%s)\t%s (%s/%s/%s)\t%s (%s)' % (
                     fab_colors.yellow(len(instance_list)),
                     instance.id, instance.instance_type, instance.state,
                     instance.image_id, instance.region.name, instance.architecture, instance.root_device_type,
                     instance.public_dns_name, instance.ip_address)
                    instance_list += [instance]

        else:
            print 'No instances found.'
        return instance_list

    def get_awsInstance(self, create=True):
        """
        Gets or creates an instance for AWS actions
        """
        if not self.instance:
            self.get_awsConnection()
            if 'AWS_INSTANCE_ID' in fab_api.env:
                try:
                    self.instance = self.conn.get_all_instances(instance_ids=fab_api.env.AWS_INSTANCE_ID)[0].instances[0]
                except:
                    pass

            if not self.instance:
                instance_list = self.get_awsInstanceList()
                if instance_list:
                    fab_api.prompt('Select an existing instance or hit enter to create a new one:', 'instance_selection')
                    if fab_api.env.instance_selection:
                        self.instance = instance_list[int(fab_api.env.instance_selection)]
                        fab_api.env['AWS_INSTANCE_ID'] = self.instance.id
                        print fab_colors.green('%s selected.' % (self.instance.id,))
                        fab_api.env['unsaved'] = True
            if not self.instance and create:
                fab_api.warn('Creating new instance in the %s region with the %s image.' % (fab_api.env.AWS_REGION, fab_api.env.AWS_AMI_ID))
                keyid, keyvalue = self.get_sshKey()
                reservation = self.conn.run_instances(image_id=fab_api.env.AWS_AMI_ID, instance_type=fab_api.env.AWS_TYPE, key_name=keyid, security_groups=[
                 'apache', 'developer'])
                self.instance = reservation.instances[0]
                fab_api.env['AWS_INSTANCE_ID'] = self.instance.id
                print fab_colors.green('Server instance %s created.' % (self.instance.id,))
                fab_api.env['unsaved'] = True
                sleep(60)
            self.save_awsSettings()
        while self.instance.state != 'running':
            print fab_colors.yellow('Waiting for instance...')
            sleep(5)
            self.instance.update()
            if self.instance.state == 'running':
                print fab_colors.green('Instance %s is up!' % self.instance.id)

        fab_api.env.host_string = self.instance.ip_address
        return self.instance

    def set_awsElasticIP(self):
        """
        """
        instance = self.get_awsInstance()
        elasticip = self.conn.allocate_address()
        self.conn.associate_address(instance_id=instance.id, allocation_id=elasticip.allocation_id)

    def get_sshKey(self, keyfile=None):
        if not keyfile:
            home = os.getenv('USERPROFILE') or os.getenv('HOME')
            keyfile = os.path.abspath(os.path.join(home, '.ssh', 'id_rsa.pub'))
        keyfile = os.path.expanduser(keyfile)
        try:
            kf = open(keyfile)
        except IOError as e:
            print fab_colors.red('Keyfile: %s does not exist!  Please specify a valid pubkey file with --sshpubkey=PATH_TO_SECURITY_KEY' % keyfile)
            sys.exit(0)

        keyvalue = kf.readline()
        keyid = keyvalue.split()[(-1)].strip()
        kf.close()
        return (
         keyid, keyvalue)

    def set_awsSSHKey(self, keyfile=None):
        """
        Imports your local ssh pubkey into your AWS account
        """
        try:
            keyid, keyvalue = self.get_sshKey(keyfile)
        except:
            raise Exception('SSH pubkey not found! Cannot continue!')

        self.get_awsConnection()
        try:
            keypairs = self.conn.get_all_key_pairs(keynames=[keyid])
        except BotoException.EC2ResponseError:
            self.conn.import_key_pair(keyid, keyvalue)
            print fab_colors.green("Key ID '%s' installed from %s." % (keyid, keyfile))
        else:
            print fab_colors.green("Key ID '%s' exists." % keyid)

    def set_awsSecurityGroups(self):
        """
        Creates necessary firewall security groups in your AWS account
        """
        self.get_awsConnection()
        try:
            self.conn.get_all_security_groups(groupnames=['apache'])
        except BotoException.EC2ResponseError:
            web = self.conn.create_security_group('apache', 'Apache Security Group')
            web.authorize('tcp', 80, 80, '0.0.0.0/0')
            print fab_colors.green('Apache firewall entry added.')
        else:
            print fab_colors.green('Apache firewall entry exists.')

        try:
            self.conn.get_all_security_groups(groupnames=['developer'])
        except BotoException.EC2ResponseError:
            dev = self.conn.create_security_group('developer', 'Developer Security Group')
            dev.authorize('tcp', 8000, 8000, '0.0.0.0/0')
            dev.authorize('tcp', 22, 22, '0.0.0.0/0')
            print fab_colors.green('Developer firewall entry added.')
        else:
            print fab_colors.green('Developer firewall entry exists.')

    def install_awsUbuntuUpgrades(self):
        """
        Installs the core components needed to run Django, Apache etc on Ubuntu
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        fab_api.env.key_filename = '~/.ssh/id_rsa'
        print fab_colors.yellow('Checking OS for available updates...')
        fab_api.sudo('apt-get -y update')
        fab_api.sudo('apt-get -y dist-upgrade')
        print fab_colors.yellow('Checking OS for required packages...')
        fab_api.sudo('apt-get -y install python-setuptools python-dev python-virtualenv git mercurial gcc unison python-pip node-less libtidy-dev')
        fab_api.sudo('apt-get -y install apache2 libapache2-mod-wsgi')
        fab_api.sudo('apt-get -y install python-imaging libjpeg62 libjpeg62-dev libjpeg8')
        if not fab_exists('/usr/lib/libz.so'):
            fab_api.sudo('ln -s  /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/')
        if not fab_exists('/usr/lib/libjpeg.so'):
            fab_api.sudo('ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/')
        fab_api.sudo('apt-get install -y mysql-server mysql-client python-mysqldb libmysqlclient-dev build-essential python-dev')
        fab_api.sudo('apt-get -y install python-mysqldb')
        fab_api.sudo('apt-get -y clean')
        if not fab_exists('/home/ubuntu/django'):
            fab_api.run('mkdir /home/ubuntu/django')
        if not fab_exists('/home/ubuntu/django/cache'):
            fab_api.run('mkdir /home/ubuntu/django/cache')

    def cmd_awsReboot(self):
        """
        Reboot the AWS server
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Rebooting instance...')
        fab_api.sudo('reboot')
        sleep(60)
        while self.instance.state != 'running':
            print fab_colors.yellow(self.instance.state)
            sleep(5)
            self.instance.update()

    def aws_DropDB(self):
        """
        Drop the database and recreate
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        fab_api.prompt('What is the server MySQL root password:', 'mysqlpwd')
        fab_api.run('mysql -u root -p%s -e "DROP DATABASE IF EXISTS django_%s;"' % (fab_api.env.mysqlpwd, fab_api.env.SITENAME))
        fab_api.run('mysql -u root -p%s -e "CREATE DATABASE django_%s;"' % (fab_api.env.mysqlpwd, fab_api.env.SITENAME))
        fab_api.run('mysql -u root -p%s -e "GRANT ALL ON django_%s.* TO \'djangouser\'@\'localhost\' IDENTIFIED BY \'%s\';"' % (fab_api.env.mysqlpwd, fab_api.env.SITENAME, fab_api.env.mysqlpwd))

    def install_awsPythonRequirements(self, reinstall=False):
        """
        Installs the Python virtual environment needed for safe-n-sane Django using the
        requirements.txt file contents
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Updating Python virtual environment (this may take around 20 minutes the first time)...')
        if reinstall:
            print fab_colors.yellow('Creating Python virtual environment...')
            fab_api.run('rm -rf ~/django/python')
            fab_api.run('virtualenv --no-site-packages --distribute ~/django/python')
        with fab_api.settings(fab_api.cd('~/django/%s' % fab_api.env.SITENAME), fab_api.prefix('source ~/django/python/bin/activate')):
            fab_api.run('pip install --upgrade --download-cache=/home/ubuntu/django/cache --source=/home/ubuntu/django/cache distribute==0.6.30')
            fab_api.run('pip install --upgrade --download-cache=/home/ubuntu/django/cache --source=/home/ubuntu/django/cache MySQL-python==1.2.3')
            fab_api.run('pip install --upgrade --download-cache=~/django/cache --source=~/django/cache -r requirements.txt')

    def sync_awsProject(self, push=False):
        """
        Sync the local copy up to the remote server
        """
        instance = self.get_awsInstance()
        here = os.getcwd()
        there = 'ssh://ubuntu@%s//home/ubuntu/django/%s' % (instance.ip_address, fab_api.env.SITENAME)
        print fab_colors.yellow('Synchronizing project files...')
        with fab_api.settings(warn_only=True):
            if push:
                fab_api.local('unison -ignore "Path httpdocs"  -silent -force %s %s %s' % (here, here, there))
            else:
                fab_api.local('unison -auto -ignore "Path httpdocs"  %s %s' % (here, there))

    def sync_awsPurify(self):
        """
        Clear the menu cache or errors may ensue!
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Cleaning menu entries...')
        with fab_api.settings(fab_api.cd('~/django/%s' % fab_api.env.SITENAME), fab_api.prefix('source ~/django/python/bin/activate')):
            fab_api.run('python manage.py reset --noinput menus')

    def sync_awsDB(self, push=False):
        """
        Run the django database maintenance commands within the AWS server instance
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Initializing/updating database...')
        with fab_api.settings(fab_api.cd('~/django/%s' % fab_api.env.SITENAME), fab_api.prefix('source ~/django/python/bin/activate')):
            fab_api.run('python manage.py syncdb --noinput --verbosity=0')
            fab_api.run('python manage.py migrate --verbosity=0')

    def sync_awsStaticfiles(self):
        """
        Link the static files from the various modules into a common file tree for serving up on Apache
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Collecting static files from included modules...')
        with fab_api.settings(fab_api.cd('~/django/%s' % fab_api.env.SITENAME), fab_api.prefix('source ~/django/python/bin/activate')):
            if fab_exists('~/django/%s/httpdocs/static' % fab_api.env.SITENAME):
                fab_api.sudo('rm -rf ~/django/%s/httpdocs/static' % fab_api.env.SITENAME)
            fab_api.run('python manage.py collectstatic -l --noinput --verbosity=0')

    def set_awsApacheconf(self, domain=None):
        """
        Enable the Apache config
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        if not domain:
            fab_api.prompt('Base domain to host as:', 'domain', fab_api.env.SITENAME + '.com')
        else:
            fab_api['domain'] = domain
        fab_api.env['django_base_dir'] = '/home/%s/django/' % fab_api.env.AWS_USER
        print fab_colors.yellow('Creating and installing Apache configuration file...')
        target = '/etc/apache2/sites-available/%s.conf' % fab_api.env.domain
        template = os.path.join('etc', 'apache2_vhost.conf')
        fab_op.put(template, target, use_sudo=True)
        if fab_exists('/etc/apache2/sites-enabled/000-default'):
            fab_api.prompt('Disable 000-default? (y/n) ', 'nopchdflt')
            if fab_api.env.nopchdflt == 'y':
                fab_api.sudo('a2dissite 000-default')
        fab_api.sudo('a2ensite %s.conf' % fab_api.env.domain)

    def cmd_awsApacheRestart(self):
        """
        Restart Apache
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Graceful Apache...')
        fab_api.sudo('apache2ctl graceful')

    def cmd_terminateInstance(self):
        """terminate instance and remove from .aws_fabric"""
        instance = self.get_awsInstance()
        print fab_colors.red('You are about to TERMINATE an instance. This CANNOT be undone.')
        print fab_colors.red('!!!!!!!!!! You will LOSE all its DATA. !!!!!!!!!!!!!!!!!!!!!!!')
        print 'id: %s ip_address: %s' % (instance.id, instance.ip_address)
        output = raw_input('\nTo proceed, type the ip address of this instance: ')
        if output == instance.ip_address:
            instance.terminate()
        path = fab_api.env.get('rcfile')
        if isfile(path):
            with open(path) as (file):
                new_lines = [ line for line in file if 'AWS_INSTANCE_ID' not in line ]
            with open(path, 'w') as (file):
                file.writelines(new_lines)
        print fab_colors.yellow('\ninstance terminated')

    def _list_keys_on_remote(self, id_only=False):
        """get ssh keys on remote"""
        with fab_api.hide('everything'):
            output = fab_api.run('cat ~/.ssh/authorized_keys')
        if id_only:
            return [ line.split()[(-1)] for line in output.splitlines() ]
        else:
            return output.splitlines()

    def cmd_rmKey(self):
        """rm keys from remote"""
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        ids = self._list_keys_on_remote(id_only=True)

        def prompt_for_delete():
            print fab_colors.yellow('\n========================\nThese keys are installed.')
            for num, id in enumerate(ids):
                print '(%s) %s' % (num, id)

            print fab_colors.yellow('\nEnter the numbers of the keys to delete, seperated by spaces.')
            input = raw_input('nums: ')
            to_delete = [ int(num) for num in input.split() if num.isdigit() ]
            to_delete = filter(lambda x: 0 <= x < len(ids), to_delete)
            if not to_delete:
                print fab_colors.red('\nYou didnt choose anything. Lets start over...')
                prompt_for_delete()
            if len(to_delete) >= len(ids):
                print fab_colors.red('\nDO NOT delete all keys. you will be LOCKED OUT permanently.')
                prompt_for_delete()
            key_id, key_value = self.get_sshKey()
            if [ 'fail' for num in to_delete if ids[num] == key_id ]:
                print fab_colors.red('\nDUDE. Do NOT delete you own key. Get a grip...')
                prompt_for_delete()
            print fab_colors.yellow('\nYou would like to delete:')
            for num in sorted(to_delete):
                print '(%s) %s' % (num, ids[num])

            output = raw_input('\nIs this correct? ' + fab_colors.yellow('[yes|no]') + ' : ')
            if output == 'yes':
                old_keys = enumerate(self._list_keys_on_remote())
                new_keys = [ key for num, key in old_keys if num not in to_delete ]
                new_keys = ('\n').join(new_keys)
                with fab_api.hide('everything'):
                    fab_api.run('echo "%s" > ~/.ssh/authorized_keys' % new_keys)
                to_print = fab_colors.yellow('\ndeleted keys ')
                to_print += fab_colors.yellow(' and ').join([ ids[num] for num in to_delete ])
                to_print += fab_colors.yellow(' from remote.')
                print to_print
            else:
                prompt_for_delete()

        prompt_for_delete()

    def cmd_addKey(self, keyfile=None):
        """
        add keys to remote
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Enter ssh pub keys, one per line.\nEnter blank line to terminate input.')
        keys = []
        while True:
            output = raw_input('ssh pub key: ')
            if output:
                keys.append(output)
            else:
                break

        for key in keys:
            with fab_api.hide('everything'):
                fab_api.run('echo "%s" >> ~/.ssh/authorized_keys' % key)

        print fab_colors.yellow('keys have been added to remote instance.')

    def cmd_listKeys(self):
        """list the id/user of all installed ssh keys on remote instance"""
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Pub Key IDs...')
        print ('\n').join(self._list_keys_on_remote(id_only=True))

    def cmd_getIP(self):
        """print the ip of our instance"""
        instance = self.get_awsInstance(create=False)
        if instance:
            print instance.ip_address
        else:
            print 'no instance created yet'

    def cmd_awsShell(self):
        """
        Open an interactive shell on the AWS server instance
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        fab_api.open_shell()

    def cmd_awsManage(self, *args, **options):
        """
        Run any series of available Django command in the aws instance
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        with fab_api.settings(fab_api.cd('~/django/%s' % fab_api.env.SITENAME), fab_api.prefix('source ~/django/python/bin/activate')):
            for cmd in args[0]:
                fab_api.run(command='python manage.py %s' % cmd)

    def set_awsPermissions(self):
        """
        Set file permissions to usable values
        """
        instance = self.get_awsInstance()
        fab_api.env.host_string = instance.ip_address
        print fab_colors.yellow('Settings apropriate default permissions on project files...')
        fab_api.sudo('chown -R %s:%s ~/django/%s/%s/static' % (fab_api.env.AWS_USER, fab_api.env.AWS_HTTPD_GROUP, fab_api.env.SITENAME, fab_api.env.SITENAME))
        fab_api.sudo('chmod -R ug+rw ~/django/%s/%s/static' % (fab_api.env.SITENAME, fab_api.env.SITENAME))
        fab_api.sudo('chown -R %s:%s ~/django/%s/' % (fab_api.env.AWS_USER, fab_api.env.AWS_HTTPD_GROUP, fab_api.env.SITENAME))
        fab_api.sudo('chmod -R ug+rw ~/django/%s/' % fab_api.env.SITENAME)

    def get_awsConnection(self):
        """
        Get or create the connection object to AWS
        """
        if self.conn:
            return self.conn
        self.conn = ec2.connect_to_region(region_name=fab_api.env.AWS_REGION, aws_access_key_id=fab_api.env.AWS_ACCESS_KEY_ID, aws_secret_access_key=fab_api.env.AWS_ACCESS_SECRET)
        if not self.conn:
            raise Exception('No AWS Connection! Cannot continue!')
        return self.conn


class RESTRequest(Request):

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
        self.method = method

    def get_method(self):
        if self.method:
            return self.method
        return Request.get_method(self)


class DeployKey():

    def __init__(self, spice_repo=None, repo_owner=None, owner_passwd=None):
        self.spice_repo = spice_repo
        self.repo_owner = repo_owner
        self.owner_passwd = owner_passwd

    def decode_list(self, jsonData):
        rv = []
        for item in jsonData:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = self.decode_list(item)
            elif isinstance(item, dict):
                item = self.decode_dict(item)
            rv.append(item)

        return rv

    def decode_dict(self, jsonData):
        rv = {}
        for key, value in jsonData.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = self.decode_list(value)
            elif isinstance(value, dict):
                value = self.decode_dict(value)
            rv[key] = value

        return rv

    def getCred(self):
        credentials = b64encode(('{0}:{1}').format(self.owner, self.owner_passwd).encode()).decode('ascii')
        return credentials

    def getURL(self):
        url = 'https://api.bitbucket.org/1.0/repositories/%s/%s/deploy-keys' % (self.owner, self.spice_repo)
        return url

    def getHeaders(self):
        headers = {'Authorization': 'Basic ' + self.getCred()}
        return headers

    def getKeys(self):
        request = RESTRequest(url=self.getURL(), headers=self.getHeaders(), method='GET')
        connection = urlopen(request)
        content = connection.read()
        return json.loads(content, object_hook=self.decode_dict)

    def postKey(self, ssh_key, key_label):
        data = urlencode({'key': ssh_key, 'label': key_label})
        request = RESTRequest(url=self.getURL(), headers=self.getHeaders(), data=data, method='POST')
        connection = urlopen(request)
        connection.read()

    def delKey(self, key_id):
        request = RESTRequest(url='%s/%s' % (self.getURL(), key_id), headers=self.getHeaders(), method='DELETE')
        connection = urlopen(request)
        connection.read()