# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/abl/robot/base.py
# Compiled at: 2012-09-11 08:10:42
from __future__ import with_statement
__docformat__ = 'restructuredtext en'
import sys, os, pprint, subprocess
from cStringIO import StringIO
import contextlib, inspect, logging, optparse
from time import time
from textwrap import dedent
from socket import error as socket_error
from configobj import ConfigObj
from validate import Validator
from turbomail.control import interface
from turbomail.message import Message
from errorreporter.reporter import EmailReporter, XMLExceptionDumper
from errorreporter.collector import collect_exception
from abl.util import Bunch, LockFile, LockFileObtainException, LockFileCreationException
from .mail import configure
logger = logging.getLogger('abl.robot')

def nonose(func):
    func.__test__ = False
    return func


class ErrorHandler(object):
    """
    Simple class to set up error-reporting
    based on config & the abl.errorreporter.
    """
    BODY_TEMPLATE = dedent('\nA nasty exception has occured.\n\n{% if url %}\nPlease visit\n\n  $url\n\nto see more details.\n{% end %}\n{% if not url %}\nNo web-access to exception-data configured.\n{% end %}\n\nErrocode: $id_code\n\nLast line: $last_line\n\nFull dump:\n\n$all_lines\n')

    def __init__(self, robot, error_config):
        reporters = []
        self.viewer_prefix = None
        if 'error.xml_dir' in error_config:
            xml_dumper = XMLExceptionDumper(outputdir=error_config['error.xml_dir'])
            reporters.append(xml_dumper)
        if error_config['mail.on']:
            email_reporter = EmailReporter(author=error_config.get('error.sender', robot.AUTHOR), to=error_config.get('error.rcpt', robot.EXCEPTION_MAILING), subject_template='%s $id_code $etype $edata' % error_config['error.prefix'], body_template=self.BODY_TEMPLATE, plugins=[
             self])
            reporters.append(email_reporter)
            self.viewer_prefix = error_config.get('error.viewer_url')
        self.reporters = reporters
        return

    def enrich_message_data(self, exc_data, message_data):
        url = None
        if self.viewer_prefix:
            url = '%(url_base)s/stack/%(path)s' % {'url_base': self.viewer_prefix, 
               'path': os.path.splitext(XMLExceptionDumper.make_filename(exc_data))[0]}
        message_data['url'] = url
        return

    def enrich_header_data(self, *args, **kwargs):
        pass

    def report_exception(self):
        exc_info = sys.exc_info()
        exc_data = collect_exception(*exc_info)
        for reporter in self.reporters:
            try:
                reporter.report(exc_data)
            except:
                sys.stderr.write(repr(sys.exc_info()[1]))


class RobotCallError(Exception):

    def __init__(self, cmd, ec, output):
        self.cmd = cmd
        self.ec = ec
        self.output = output

    def __str__(self):
        return 'Subcommand %r exited with %i.\n Ouput was:\n%s' % (
         (' ').join(self.cmd), self.ec, ('').join(self.output))


class RequiredOption(optparse.Option):

    def __init__(self, *args, **kwargs):
        self.required = kwargs.pop('required', False)
        if self.required and 'default' in kwargs:
            logger.warn(dedent('\n            You gave a default value to a required option, that makes no\n            sense. The args were: %r, %r\n            ' % (args, kwargs)))
        optparse.Option.__init__(self, *args, **kwargs)


class Robot(object):
    """
    Baseclass for various Robots we use.

    Configuration
    =============

    The robot can be configured using a `ConfigParser` logfile.

    The logfile can be given either by commandline, with the option
    **-c/--config**, or the robot will attempt to auto-locate the
    config-file.

    There are a couple of general configuration
    sections available for every robot. These are explained below.

    Subclasses can of course define their own sections, which should
    be documented there.

    Locking
    -------

    If there is a section called "locking", you
    can turn on file-based locking. This will prevent
    that two instances of the same robot run twice.

    You can choose to either

     - terminate if there appears another robot running
     - wait until the robot is finished, then execute. A warning is
       in order here: **This might cause queuing!** If the robots
       are faster respawned than they run, they will queue up. Currently,
       there is no way to prevent that.

    The locking-section looks like this:::

      [locking]
      filename = <lockfilename>
      terminate_when_locked = <bool> (optional, default=False)

    Mail
    ----

    If the robot is supposed to send status-emails,
    it can be configured to do so by a "mail"-section that looks
    like this:::

      [mail]
      transport = debug|smtp (optional, default=smtp)
      smtp.server = <smtp-server:port> (optional)

    Also there is the class-variable `AUTHOR` that should be
    paid attention to. It will be used as from-header when
    sending emails through `sendmail`.

    Commandline options
    ===================

    As mentioned above, the Robot has a `optparse`-based
    commandline-option-parser. This will be passed to the subclasses
    prior to parsing the commandline to allow them to register their
    own set of commandline-options.

    The options are then available using `self.opts`.

    The `Robot`-base knows these options:

      - **-c/--config** for specifying  the configuration file.

      - **--logfile** to specify the output-logfile.

      - **--loglevel** to specify the log-level.

    :ivar parser: the `optparse.OptionParser` for this robot.

    """
    CONFIG_NAME = None
    NEEDS_CONFIG = True
    CONFIGSPECS = dict(locking=dedent('\n        [locking]\n        filename = string\n        terminate_when_locked = boolean(default=True)\n        '), mail=dedent('\n        [mail]\n        transport = option(smtp, debug, default=smtp)\n        smtp.server = string(default=mail.ableton.net)\n        '), logging=dedent('\n        [logging]\n        filename=string\n        level=option(ERROR,WARN,INFO,DEBUG)\n        format=string\n        '), error_handler=dedent("\n        [error_handler]\n        error.viewer_url = string\n        error.xml_dir = string\n        error.rcpt = string\n        error.sender = string\n        error.prefix = string(default='[Robot Stumbled]')\n        mail.on = boolean(default=False)\n        "))
    EMERGENCY_LOG = '/tmp/robot_emergency.log'
    SEARCH_PATHS = ('/etc', 'etc')
    EXCEPTION_MAILING = None
    RAISE_EXCEPTIONS = False
    AUTHOR = 'dir@ableton.com'
    LOCK_TERMINATION_MESSAGE = 'Terminating because the lock was active.'

    def __init__(self):
        self.parser = self.parser_with_default_options()
        self.add_options(self.parser)
        self.logger = self.get_logger()

    def setup(self, argv=None):
        if argv is None:
            argv = sys.argv
        self.opts, self.rest = self.parser.parse_args(argv)
        self.config = self._locate_config(self.opts.config)
        self._setup_logging()
        self.error_handler = ErrorHandler(self, self.config.get('error_handler'))
        mail_config = {}
        if 'mail' in self.config:
            mail_config = self.config['mail'].dict()
        configure(mail_config)
        return

    def parser_with_default_options(self):
        parser = optparse.OptionParser(option_class=RequiredOption)
        g = optparse.OptionGroup(parser, 'Common options')
        g.add_option('-c', '--config', default=None, help="Use the given configuration file instead of '%s'." % self.CONFIG_NAME if self.CONFIG_NAME is not None else '')
        g.add_option('--logfile', default=None, help='Use the given logfile file')
        g.add_option('--loglevel', default=None, help='Use the level as loglevel. Allowed values are ERROR WARN INFO DEBUG')
        g.add_option('--logformat', default=None, help='Use the given format to output the logging messages.')
        g.add_option('--config-spec', default=False, action='store_true', help=dedent('\n            Print the config specification to STDOUT.\n            '))
        g.add_option('--default-config', default=False, action='store_true', help=dedent('\n            Print a default configuration to STDOUT.\n            '))
        parser.add_option_group(g)
        return parser

    @classmethod
    def main(cls):
        robot = cls()
        robot.setup()
        robot.run()

    def run(self):
        if self.opts.config_spec:
            self.print_config_spec()
            sys.exit(0)
        if self.opts.default_config:
            self.print_default_config()
            sys.exit(0)
        try:
            with self._locking_context():
                self.work()
        except LockFileObtainException:
            self.logger.info(self.LOCK_TERMINATION_MESSAGE)
        except LockFileCreationException:
            self.logger.error("Couldn't create a lockfile.")
        except (KeyboardInterrupt, SystemExit):
            pass
        except:
            if self.RAISE_EXCEPTIONS:
                raise
            self.error_handler.report_exception()

    def sendmail(self, subject, to, text=None, attachments=()):
        message = Message(encoding='utf-8')
        message.author = self.AUTHOR
        message.subject = subject
        message.to = to
        if text is None:
            text = ' '
        message.plain = text
        for name, attachment in attachments:
            message.attach(StringIO(attachment), name)

        tries = 2
        while tries > 0:
            try:
                interface.send(message)
            except socket_error:
                tries -= 1
                if not tries:
                    raise
            else:
                break

        return

    def get_logger(self):
        """
        Override this method to provide a logger instance.

        Defaults to `abl.robot` otherwise.
        """
        return logger

    def add_options(self, parser):
        """
        This method is called with the instantiated parser
        for commandline-options. Use this to add additional
        ones.

        It will already feature a set of options values,
        see `Robot.parser`.
        """
        pass

    def _locking_context(self):
        """
        Sets up locking for a robot.
        """
        c = self.config
        if 'locking' in c and c['locking'].get('filename', None):
            fail_on_lock = False
            if c['locking'].get('terminate_when_locked', False):
                fail_on_lock = c['locking'].as_bool('terminate_when_locked')
            return LockFile(c['locking']['filename'], cleanup=True, fail_on_lock=fail_on_lock)
        else:

            @contextlib.contextmanager
            def nop():
                yield

            return nop()

    def _locate_config(self, config_file):
        locations = []
        for location in self.SEARCH_PATHS:
            if not location.startswith('/'):
                location = os.path.join(sys.prefix, 'etc')
            locations.append(location)

        candidates = []
        if config_file is not None:
            candidates.append(config_file)
        else:
            for location in locations:
                cfn = os.path.join(location, self.CONFIG_NAME)
                if os.path.exists(cfn):
                    candidates.append(cfn)

            for cfn in candidates:
                cp = ConfigObj(cfn, configspec=self._configspec())
                vdt = Validator({})
                cp.validate(vdt)
                return cp

        if self.NEEDS_CONFIG:
            l = logging.getLogger()
            l.addHandler(logging.FileHandler(self.EMERGENCY_LOG))
            l.level = logging.DEBUG
            l.error('No config found, using emergency log!')
        cp = ConfigObj(configspec=self._configspec())
        vdt = Validator({})
        cp.validate(vdt)
        return cp

    def _setup_logging(self):
        """
        Loads a simple logging configuration from the config-file.

        The config must be located in a section like this:

        [logging]
        filename=<logfile>
        level=<LEVEL>

        where level is one of ERROR, INFO, WARN or DEBUG.

        If no level is given, the default is determined
        by the logging-module and should be WARN
        """
        args = dict(format='%(levelname)s %(asctime)s - %(message)s')
        cfg = self.config
        if 'logging' in cfg:
            args.update(cfg['logging'].dict())
        if self.opts.logfile is not None:
            lf = self.opts.logfile
            if lf != '-':
                args['filename'] = lf
            else:
                args['stream'] = sys.stderr
            if 'level' not in args:
                args['level'] = 'INFO'
        if self.opts.loglevel is not None:
            args['level'] = self.opts.loglevel
        if self.opts.logformat is not None:
            args['format'] = self.opts.logformat
        if 'filename' not in args and 'stream' not in args:
            args['stream'] = sys.stderr
        if args:
            if 'level' in args:
                args['level'] = getattr(logging, args['level'])
            root_logger = logging.getLogger()
            root_logger.handlers[:] = []
            logging.basicConfig(**args)
        logging.getLogger('turbomail').setLevel(logging.WARN)
        return

    def create_logger(self):
        return logging.getLogger(self.__class__.__module__)

    def work(self):
        """
        Overload this method to do the actual working
        """
        pass

    def error_message(self, message, exit_code=1):
        """
        Writes a message to sys.stderr, and then fails with
        exit-code.

        :Parameters:
          message : str|unicode
            The message to print

          exit_code : int
            The exit-code to fail with. Defaults to 1

        """
        sys.stderr.write(message)
        sys.stderr.write('\n')
        sys.exit(exit_code)

    @property
    def name(self):
        return self.__class__.__name__

    def _configspec(self):
        """
        Traverse the list of base-classes to gather
        the config-spec.
        """
        classes = inspect.getmro(self.__class__)
        spec = {}
        for clazz in classes:
            if hasattr(clazz, 'CONFIGSPECS'):
                cs = clazz.CONFIGSPECS
                if cs is not None:
                    for key, value in cs.iteritems():
                        if key not in spec:
                            spec[key] = value

        spec = ('\n').join(v for v in spec.values() if v is not None)
        return StringIO(spec)

    def merge_config_and_opts(self):
        """
        Merge configuration values and commandline-arguments.

        This method will merge configuration values and
        commandline options together into a single `Bunch`.

        The merging is done by

         - creating a flat namespace of config-parameters
         - overwriting all given commandline-options where
           the commandline-option is *not* the default

        **ATTENTION**: The resulting object won't have
        na namespace as the config itself has, so you need to
        be careful not to name config-values the same.

        :return: The flat merged parameters
        :rtype: Bunch
        """
        c = self.config
        parameters = {}
        for section in c:
            parameters.update(c[section].dict())

        parser = self.parser
        ol = parser._get_all_options()
        name2defaults = dict((o.dest, o.default) for o in ol)
        for name in dir(self.opts):
            if name.startswith('_'):
                continue
            value = getattr(self.opts, name)
            if name in name2defaults and name in parameters and (name2defaults[name] == value or name2defaults[name] == ('NO',
                                                                                                                         'DEFAULT') and value is None):
                continue
            parameters[name] = value

        return Bunch(**parameters)

    def print_config_spec(self):
        """
        Print the current robots configuration spec.
        """
        print self._configspec().getvalue()
        print

    def print_default_config(self):
        cp = ConfigObj(configspec=self._configspec())
        vdt = Validator({})
        cp.validate(vdt)
        d = cp.dict()

        def store_defaults(conf, d):
            for key, value in d.iteritems():
                if not isinstance(value, dict):
                    conf[key] = value
                else:
                    store_defaults(conf[key], value)

        store_defaults(cp, d)
        sys.stdout.write(('\n').join(cp.write()))
        print

    def call(self, cmd, print_output=False, **kwargs):
        """
        Call a command via `subprocess.call`. Fail on error.

       :Parameters:
          cmd : list<str>
            The command with possible arguments to execute.
        """
        start_time = time()
        np = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
        output = []
        while True:
            stdout, _ = np.communicate()
            logger.debug(stdout)
            output.append(stdout)
            if print_output:
                sys.stdout.write(stdout)
            if np.returncode is not None:
                break

        ec = np.returncode
        elapsed_time = time() - start_time
        self.get_logger().debug('%s [%.3fs]' % ((' ').join(cmd), elapsed_time))
        if ec != 0:
            raise RobotCallError(cmd, ec, output)
        return