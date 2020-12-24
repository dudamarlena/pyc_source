# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/psphere/scripting.py
# Compiled at: 2013-02-21 17:34:08
__doc__ = '\nParse command line options, allow users to append their own options and\nread predefined configuration from the users .visdkrc file.\n'
import optparse

class BaseScript(object):

    def __init__(self, client):
        self.client = client
        self.required_opts = []
        usage = 'usage: %prog --url https://<host>/sdk --username <username> --password <password>'
        self.parser = optparse.OptionParser(usage)
        self.parser.add_option('--url', dest='url', help='the url of the vSphere server')
        self.parser.add_option('--username', dest='username', help='the username to connnect with')
        self.parser.add_option('--password', dest='password', help='the password to connect with')

    def add_option(self, opt, dest, help, required):
        self.parser.add_option(opt, dest=dest, help=help)
        if required:
            self.required_opts.append(dest)

    def get_options(self):
        """Get the options that have been set.

        Called after the user has added all their own options
        and is ready to use the variables.

        """
        options, args = self.parser.parse_args()
        visdkrc_opts = self.read_visdkrc()
        for opt in self.config_vars:
            if not getattr(options, opt):
                if visdkrc_opts:
                    if opt in visdkrc_opts:
                        setattr(options, opt, visdkrc_opts[opt])

        for opt in self.required_opts:
            if opt not in dir(options) or getattr(options, opt) == None:
                self.parser.error('%s must be set!' % opt)

        return options

    def read_visdkrc(self):
        try:
            config = open(self.visdkrc)
        except IOError as e:
            if e.errno == 2:
                return
            else:
                if e.errno == 13:
                    print 'ERROR: Permission denied opening %s' % self.visdkrc
                    return
                print 'ERROR: Could not open %s: %s' % (self.visdkrc, e.strerror)
                return

        lines = config.readlines()
        config.close()
        parsed_opts = {}
        for line in lines:
            key, value = line.split('=')
            parsed_opts[key] = value.rstrip('\n')

        visdkrc_opts = {}
        if 'VI_PROTOCOL' in parsed_opts and 'VI_SERVER' in parsed_opts and 'VI_SERVICEPATH' in parsed_opts:
            visdkrc_opts['url'] = '%s://%s%s' % (parsed_opts['VI_PROTOCOL'],
             parsed_opts['VI_SERVER'],
             parsed_opts['VI_SERVICEPATH'])
        if 'VI_USERNAME' in parsed_opts:
            visdkrc_opts['username'] = parsed_opts['VI_USERNAME']
        if 'VI_PASSWORD' in parsed_opts:
            visdkrc_opts['password'] = parsed_opts['VI_PASSWORD']
        return visdkrc_opts