# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/config.py
# Compiled at: 2015-09-25 10:53:22
import sys, ConfigParser, cherrypy
cherrypy.engine.autoreload.files.add(__file__)

class Config(ConfigParser.SafeConfigParser):

    def check_options(self, section, opts, message):
        import cherrypy
        missing = [ o for o in opts if not self.has_option(section, o) ]
        if not missing == []:
            if len(missing) == 1:
                cherrypy.engine.log('Option ' + missing[0] + ' in config section ' + section + ' is not set. ' + message)
            else:
                cherrypy.engine.log('Options ' + (', ').join(missing) + ' in config section ' + section + ' are not set. ' + message)
            return False
        return True

    def load_config(self, dir):
        import sys, os, cherrypy, ConfigParser, socket
        self.server_dir = os.path.abspath(dir)
        found = self.read(dir + '/conf/config.ini')
        if found == []:
            cherrypy.engine.log('Config file ' + dir + '/conf/config.ini' + ' not found.')
        cherrypy.engine.autoreload.files.add(dir + '/conf/config.ini')
        sys.path.append(self.server_dir + '/modules')
        try:
            root = self.get('Server', 'root').rstrip('/')
        except ConfigParser.NoOptionError:
            root = ''
            cherrypy.engine.log("Server root directory not given. Assuming '/'.")

        self.set('Server', 'root', root)
        self.check_options('Mail', ['admin_name', 'admin_email'], 'Site administrator is not set. No contact information will be displayed in page footer.')
        default_url = 'http://' + socket.gethostname() + '/' + self.root
        if not self.check_options('Server', ['server_url'], 'Using ' + default_url + ' instead.'):
            self.set('Server', 'server_url', default_url)
        self.check_options('Mail', ['smtp_login', 'smtp_password', 'smtp_host', 'smtp_mail_from'], 'Sending e-mails will SILENTLY fail.')

    def get_default(self, section, option, default):
        import ConfigParser
        try:
            return self.get(section, option)
        except ConfigParser.NoOptionError:
            return default

    def rename_section(self, section_from, section_to):
        items = self.items(section_from)
        self.add_section(section_to)
        for item in items:
            self.set(section_to, item[0], item[1])

        self.remove_section(section_from)

    def set_sched_id(self, sched_id):
        section_name = 'Scheduler:' + sched_id
        if section_name in self.sections():
            self.remove_section('Scheduler')
            self.rename_section(section_name, 'Scheduler')
        self.set('Scheduler', 'sched_id', sched_id)

    @property
    def root(self):
        return self.get('Server', 'root')

    @property
    def server_url(self):
        return self.get('Server', 'server_url')

    @property
    def db_url(self):
        return self.get('Database', 'db_url')

    @property
    def sched_id(self):
        return self.get('Scheduler', 'sched_id')

    @property
    def runner(self):
        return self.get('Scheduler', 'runner')

    NoOptionError = ConfigParser.NoOptionError


sys.modules[__name__] = Config()