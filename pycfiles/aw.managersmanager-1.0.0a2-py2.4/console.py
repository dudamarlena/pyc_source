# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aw/managersmanager/console.py
# Compiled at: 2009-10-13 12:53:10
"""Console script and utilities"""
import os, sys, user, urlparse, optparse, urlparse, socket, xmlrpclib, ConfigParser
CONFIG_FILENAME = os.path.join(user.home, '.managersmanager')
CONFIG_SKELETON = '# Main section (required)\n[main]\n\n# Remove or comment following line after having customized this file\nbootstraped = true\n\n# All Zope clusters\nclusters =\n  somecluster\n  anothercluster\n\n# HTTP connection timeout (in seconds).\n# Missing option, non positive integer or float mean no timeout\ntimeout = 10\n\n# Each item in above "clusters" must have its sections\n[somecluster]\n\n# One or more root URL (the ZEO clients of this cluster)\nroot-urls =\n  http://somehost:8080\n  http://otherhost:8080\n\n# A *Zope root* manager login\nlogin = admin\npassword = mysecret\n\n# Same thing for all clusters\n[anothercluster]\n\n# One or more root URL (the ZEO clients of this cluster)\nroot-urls =\n  http://somehost:8080\n  http://otherhost:8080\n\n# A *Zope root* manager login\nlogin = admin\npassword = mysecret\n'
USAGE = 'usage: %prog [options] command [args]\n\ncommand:\n  - list : provides a liste of Plone sites\n  - adduser <login> <password> : adds a user\n  - deluser <login> : deletes existing user'
VERSION = open(os.path.join(os.path.dirname(__file__), 'version.txt'), 'r').read().strip()

class Application(object):
    """Main application class"""
    __module__ = __name__

    def __init__(self):
        """Setting up commands and options
        """
        parser = optparse.OptionParser(usage=USAGE, version=VERSION)
        parser.add_option('-v', '--verbose', dest='verbosity', default=0, action='count', help="Add verbosity to process report for each '-v' option added")
        (self.options, self.args) = parser.parse_args()

    def run(self):
        commands_map = {'adduser': self.addUser, 'deluser': self.delUser, 'list': self.listSites}

        def invalid():
            print 'No command provided or unknown command. Use "--help" option'
            sys.exit()

        if len(self.args) == 0:
            invalid()
        command = self.args[0]
        meth = commands_map.get(command, None)
        if meth:
            meth()
        else:
            invalid()
        return

    def addUser(self):
        """Adding a user
        """
        global config
        try:
            (login, password) = self.args[1:]
        except ValueError, e:
            print 'Please provide a login and a password to "adduser" command'
            sys.exit()

        msg = 'Adding manager "%s" with password "%s"' % (login, password)
        self._report(1, msg)
        for name in config.cluster_names:
            msg = 'Processing cluster "%s"' % name
            self._report(2, msg)
            cluster = config.getCluster(name)
            cluster.addManager(login, password)

    def delUser(self):
        """Removing a user
        """
        try:
            login = self.args[1]
        except IndexError, e:
            print 'Please provide a login to "deluser" command'
            sys.exit()

        msg = 'Removing manager "%s"' % login
        self._report(1, msg)
        for name in config.cluster_names:
            msg = 'Processing cluster "%s"' % name
            self._report(2, msg)
            cluster = config.getCluster(name)
            cluster.delManager(login)

    def listSites(self):
        """Listing all sites
        """
        for name in config.cluster_names:
            msg = 'Processing cluster "%s"' % name
            self._report(0, msg)
            cluster = config.getCluster(name)
            cluster.listSites()

    def _report(self, verbosity, msg):
        """Reports a message
        """
        if verbosity <= self.options.verbosity:
            print msg


class Configuration(object):
    __module__ = __name__

    def __init__(self):
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(CONFIG_FILENAME)

    @property
    def cluster_names(self):
        return [ name for name in self.parser.get('main', 'clusters').split() if len(name) > 0 ]

    @property
    def isActive(self):
        """Ready for use
        """
        if self.parser.has_option('main', 'bootstraped'):
            value = not self.parser.getboolean('main', 'bootstraped')
        else:
            value = True
        return value

    @property
    def timeout(self):
        """Get (optional) timeout
        """
        try:
            timeout = self.parser.getfloat('main', 'timeout')
        except ConfigParser.NoOptionError, e:
            return
        except ValueError, e:
            return

        if timeout > 0.0:
            return timeout
        return

    def getCluster(self, name):
        """Returns a Cluster obj provided its name
        """
        valueOf = lambda x: self.parser.get(name, x)
        urls = [ url for url in self.parser.get(name, 'root-urls').split() if len(url) > 0 ]
        return Cluster(name, urls, valueOf('login'), valueOf('password'))

    def verify(self):
        """Checks the configuration file and issues any found error
        """
        if not self.parser.has_section('main'):
            message = 'There is no [main] section in the configuration'
            return (False, message)
        if not self.isActive:
            message = "You should remove set to 'false' the 'bootstraped' option in [main]"
            return (False, message)
        try:
            clusters = self.cluster_names
        except ConfigParser.NoOptionError, e:
            message = "The [main] section has no 'clusters' option"
            return (False, message)

        if len(clusters) == 0:
            message = "The [main] section has an empty 'clusters' option"
            return (False, message)
        for cluster in clusters:
            if not self.parser.has_section(cluster):
                message = 'There should be a cluster section [%s]' % cluster
                return (False, message)
            if not self.parser.has_option(cluster, 'root-urls'):
                message = "Cluster [%s] has no 'root-urls' option"
                return (False, message)
            urls = [ url for url in self.parser.get(cluster, 'root-urls').split() if len(url) > 0 ]
            if len(urls) == 0:
                message = "Cluster [%s] should have one or more UrL in 'root-urls'" % cluster
                return (False, message)
            for url in urls:
                protocol = urlparse.urlparse(url)[0]
                if protocol not in ('http', 'https'):
                    message = "%s is not a legal URL in 'root-urls' of cluster [%s]" % (url, cluster)
                    return (
                     False, message)

            for key in ('login', 'password'):
                if not self.parser.has_option(cluster, key):
                    message = 'Cluster [%s] should have a %s' % (cluster, key)
                    return (False, message)
                if self.parser.get(cluster, key) == '':
                    message = '%s of cluster [%s] is empty' % (key, cluster)
                    return (False, message)

        return (
         True, '')


def timedout(method):
    """Time-out decorator for meths that make XMLRPC queries
    """

    def wrapper(self, *args, **kwargs):
        default_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(config.timeout)
        value = method(self, *args, **kwargs)
        socket.setdefaulttimeout(default_timeout)
        return value

    return wrapper


class Cluster(object):
    """A Zope cluster
    """
    __module__ = __name__

    def __init__(self, name, urls, login, password):
        self.name = name
        self.urls = urls
        self.root_login = login
        self.root_password = password

    @timedout
    def addManager(self, login, password):
        """Add a manager or change its password
        """
        success = False
        print 'Adding manager %s/%s' % (login, password)
        for url in self.urls:
            proxy = self.xmlrpcProxy(url)
            try:
                (success, msg) = proxy.addManager(login, password)
            except:
                success = False

            if success:
                break

        if not success:
            print 'Failed to add "%s" as Manager' % login

    @timedout
    def delManager(self, login):
        """Remove a manager
        """
        print 'Removing manager %s' % login
        for url in self.urls:
            proxy = self.xmlrpcProxy(url)
            try:
                (success, msg) = proxy.delManager(login)
            except:
                success = False

            if success:
                break

        if not success:
            print 'Failed to add "%s" as Manager' % login

    @timedout
    def listSites(self):
        """Listing all plone sites
        """
        success = False
        for url in self.urls:
            proxy = self.xmlrpcProxy(url)
            try:
                (value, success, msg) = proxy.listPlonePaths()
            except:
                success = False

            if success:
                break

        if not success:
            print 'Failed to list Plone sites'
        print 'Plone sites:'
        for item in value:
            print '*', item

    def xmlrpcProxy(self, url):
        """An object suitable to XMLRPC calls
        """
        comps = list(urlparse.urlparse(url))
        comps[1] = '%s:%s@%s' % (self.root_login, self.root_password, comps[1])
        comps = [comps[0], comps[1], '@@rpc-managers-management/', '', '', '']
        url = urlparse.urlunparse(comps)
        if not url.endswith('/'):
            url += '/'
        proxy = xmlrpclib.ServerProxy(url)
        return proxy


config = None

def main(ignored_arg=None):
    """Console main entry point
    """
    global config
    if not os.path.isfile(CONFIG_FILENAME):
        fh = open(CONFIG_FILENAME, 'w')
        fh.write(CONFIG_SKELETON)
        fh.close()
    config = Configuration()
    app = Application()
    app.run()
    return 0