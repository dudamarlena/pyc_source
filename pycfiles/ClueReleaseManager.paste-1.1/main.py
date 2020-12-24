# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/relmgr/main.py
# Compiled at: 2009-09-18 12:06:12
import logging, optparse, os, sys, pkg_resources, werkzeug
from werkzeug import _internal
from clue.relmgr import utils, wsgiapp

class Runner(object):
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = '8080'
    DEFAULT_BASEFILEDIR = 'files'

    def main(self, args=None, extraargs=None):
        logging.basicConfig()
        parser = optparse.OptionParser()
        parser.add_option('-p', '--port', dest='port', help='Port to listen on, defaults to %s' % self.DEFAULT_PORT, default=self.DEFAULT_PORT)
        parser.add_option('-i', '--interface', dest='host', help='Host to listen on, defaults to %s' % self.DEFAULT_HOST, default=self.DEFAULT_HOST)
        parser.add_option('-b', '--basefiledir', dest='basefiledir', help='Base directory to store uploaded files, ' + 'defaults to %s' % self.DEFAULT_BASEFILEDIR, default=self.DEFAULT_BASEFILEDIR)
        parser.add_option('-d', '--debug', dest='debug', action='store_true', help='Activate debug mode', default=False)
        parser.add_option('-s', '--self-register', dest='self_register', action='store_true', help='Allow self-registration', default=False)
        parser.add_option('-u', '--baseurl', dest='baseurl', help='The base url used in case of proxying', default=None)
        whodocsurl = 'http://static.repoze.org/whodocs/#middleware-configuration-via-config-file'
        parser.add_option('--security-config', dest='security_config', help='Use a separate configuration file to declare the repoze.who config. See %s for details.' % whodocsurl, default=None)
        parser.add_option('--backup-pypi', dest='backup_pypis', action='append', help='Python indexes to fall back to.  When backup index servers are configured they will be queried if the user browsing this server has the adddistro role and the this server will be updated with all metadata and files.')
        if args is None:
            args = []
        if extraargs is None:
            extraargs = sys.argv[1:]
        (options, args) = parser.parse_args(args + extraargs)
        if options.debug:
            utils.logger.setLevel(logging.DEBUG)
            utils.werklogger.setLevel(logging.DEBUG)
        pypiapp = app = wsgiapp.make_app({}, basefiledir=options.basefiledir, baseurl=options.baseurl, security_config=options.security_config, self_register=options.self_register, backup_pypis=options.backup_pypis, logger=utils.logger)
        if options.debug:
            app = werkzeug.DebuggedApplication(app, evalex=True)
        _internal._logger = utils.werklogger
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            distro = pkg_resources.get_distribution('ClueReleaseManager')
            utils.logger.info('Starting up ClueReleaseManager v%s' % distro.version)
            pypiapp.pypi.setup_model()
            utils.logger.info('Database initialized')
        werkzeug.run_simple(options.host, int(options.port), app, use_reloader=options.debug)
        return


main = Runner().main
if __name__ == '__main__':
    main()