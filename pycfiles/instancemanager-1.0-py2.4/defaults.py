# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/defaults.py
# Compiled at: 2007-12-17 05:32:50
"""Configuration defaults for zope locations and so.

 This file comes in two editions: the program-internal defaults and
 the '.instancemanager/userdefaults.py' file in your home
 directory. The user defaults are initially the same as the internal
 defaults of instancemanager. You can adapt the settings in userdefaults.py
 to match local preferences that apply to all (or most) of your projects.

 The settings in userdefaults.py are commented out, which means they
 have no effect initially.  So when you want to change a default
 setting, you also need to remove the comment sign (#) from the front
 of that line.

 Certain things are more project-specific. These can be handled quite
 easily, too:

 * Copy this file to 'yourprojectname.py' in the '.instancemanager/'
 directory.

 * Make local modifications to the values like zope port number,
   username and the various sources.

 The project file overrides the user defaults, which in turn
 overrides defaults of instancemanager.

 Important: three extra variables are defined on-the-fly: 'user_dir',
 'project' and 'clientname'. These variables can be used in the
 variables named '*_template', as they get their variables expanded.

 'user_dir' -- User home directory (like '/home/reinout').

 'project' -- Name of the project (which you gave to instancemanager,
 like 'instancemanager yourprojectname create').

 'clientname' -- Name of the zeo client or zope server.  If you do not
 use zeo, this is the same as 'project'.  If you use zeo, in case of 3
 zeo clients, with project 'test', these names in turn are 'test',
 'test1' and 'test2'.  This is currently only available for the
 zopeconf_template.

 On Windows the zope instance will be installed as a windows service and
 all calls to zopectl are redirected to the service (via zopeservice.py)

"""
python = 'python'
zope_version = '2.8.5'
development_machine = False
zope_location_template = '/opt/zope/zope%(zope_version)s'
user = 'test'
password = 'test'
port = '8080'
ftp_port = None
webdav_port = None
icp_port = None
z3_pw_manager = 'MD5'
use_zeo = False
zeoport_offset = 1
use_zeo_client_caches = False
monitor_port = None
zeo_timeout = 10
number_of_zeo_clients = 1
listen_ip_address = None
config_basedir_template = '%(user_dir)s/svn'
zope_instance_template = '%(user_dir)s/instances/%(project)s'
zeo_server_template = '%(user_dir)s/instances/zeo/%(project)s'
datafs_template = '%(user_dir)s/instances/datafs/%(project)s.fs'
zeoconf_template = '%(user_dir)s/instances/zeoconf/%(project)s.conf'
zopeconf_template = '%(user_dir)s/instances/zopeconf/%(clientname)s.conf'
use_workingenv = False
symlink_sources = []
symlink_basedir_template = '%(user_dir)s/svn/'
symlinkbundle_sources = []
symlinkbundle_basedir_template = '%(user_dir)s/svn/'
use_svn_export = False
archive_sources = []
archive_basedir_template = '%(user_dir)s/download/'
archivebundle_sources = []
archivebundle_basedir_template = '%(user_dir)s/download/'
plone_site_name = ''
main_products = []
backup_basedir_template = '%(user_dir)s/backups/%(project)s'
number_of_backups = 2
snapshot_basedir_template = '%(user_dir)s/snapshotbackups/%(project)s'
sync_database = ''
pack_days = '1'
generic_setup_profiles = []
run_command = ''
desired_plone_version = ''
desired_atct_version = ''
multi_actions = {'fresh': ['--zope stop', '--zeo stop', '--create', '--copydatafs', '--zeo start', '--products', '--reinstall', '--zope start'], 'soft': ['--zope stop', '--products', '--reinstall', '--zope start'], 'update': ['--updatesources', '--products'], 'stop': ['--zope stop', '--zeo stop'], 'start': ['--zeo start', '--zope start']}