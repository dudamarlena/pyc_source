# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/runner.py
# Compiled at: 2014-11-03 07:16:44
# Size of source mod 2**32: 25747 bytes
from __future__ import with_statement
import contextlib, os.path, sys
from io import BytesIO, StringIO
import traceback, warnings, weakref
from beehive import matchers
from beehive.compat import unicode
from beehive.step_registry import setup_step_decorators
from beehive.formatter import formatters
from beehive.configuration import ConfigError
from beehive.log_capture import LoggingCapture
from beehive.runner_util import collect_feature_locations, parse_features

class MyBytesIO(BytesIO):

    def write(self, bytes_to_write, encoding='UTF-8'):
        if not isinstance(bytes_to_write, bytes):
            if sys.version_info[0] == 2:
                bytes_to_write = str(bytes_to_write)
            else:
                bytes_to_write = bytes(bytes_to_write, encoding)
        super(MyBytesIO, self).write(bytes_to_write)


class ContextMaskWarning(UserWarning):
    __doc__ = 'Raised if a context variable is being overwritten in some situations.\n\n    If the variable was originally set by user code then this will be raised if\n    *beehive* overwites the value.\n\n    If the variable was originally set by *beehive* then this will be raised if\n    user code overwites the value.\n    '


class Context(object):
    __doc__ = 'Hold contextual information during the running of tests.\n\n    This object is a place to store information related to the tests you\'re\n    running. You may add arbitrary attributes to it of whatever value you need.\n\n    During the running of your tests the object will have additional layers of\n    namespace added and removed automatically. There is a "root" namespace and\n    additional namespaces for features and scenarios.\n\n    Certain names are used by *beehive*; be wary of using them yourself as\n    *beehive* may overwrite the value you set. These names are:\n\n    .. attribute:: feature\n\n      This is set when we start testing a new feature and holds a\n      :class:`~beehive.model.Feature`. It will not be present outside of a\n      feature (i.e. within the scope of the environment before_all and\n      after_all).\n\n    .. attribute:: scenario\n\n      This is set when we start testing a new scenario (including the\n      individual scenarios of a scenario outline) and holds a\n      :class:`~beehive.model.Scenario`. It will not be present outside of the\n      scope of a scenario.\n\n    .. attribute:: tags\n\n      The current set of active tags (as a Python set containing instances of\n      :class:`~beehive.model.Tag` which are basically just glorified strings)\n      combined from the feature and scenario. This attribute will not be\n      present outside of a feature scope.\n\n    .. attribute:: aborted\n\n      This is set to true in the root namespace when the user aborts a test run\n      (:exc:`KeyboardInterrupt` exception). Initially: False.\n\n    .. attribute:: failed\n\n      This is set to true in the root namespace as soon as a step fails.\n      Initially: False.\n\n    .. attribute:: table\n\n      This is set at the step level and holds any :class:`~beehive.model.Table`\n      associated with the step.\n\n    .. attribute:: text\n\n      This is set at the step level and holds any multiline text associated\n      with the step.\n\n    .. attribute:: config\n\n      The configuration of *beehive* as determined by configuration files and\n      command-line options. The attributes of this object are the same as the\n      `configuration file settion names`_.\n\n    .. attribute:: active_outline\n\n      This is set for each scenario in a scenario outline and references the\n      :class:`~beehive.model.Row` that is active for the current scenario. It is\n      present mostly for debugging, but may be useful otherwise.\n\n    .. attribute:: log_capture\n\n      If logging capture is enabled then this attribute contains the captured\n      logging as an instance of :class:`~beehive.log_capture.LoggingCapture`.\n      It is not present if logging is not being captured.\n\n    .. attribute:: stdout_capture\n\n      If stdout capture is enabled then this attribute contains the captured\n      output as a StringIO instance. It is not present if stdout is not being\n      captured.\n\n    .. attribute:: stderr_capture\n\n      If stderr capture is enabled then this attribute contains the captured\n      output as a StringIO instance. It is not present if stderr is not being\n      captured.\n\n    If an attempt made by user code to overwrite one of these variables, or\n    indeed by *beehive* to overwite a user-set variable, then a\n    :class:`beehive.runner.ContextMaskWarning` warning will be raised.\n\n    You may use the "in" operator to test whether a certain value has been set\n    on the context, for example:\n\n        \'feature\' in context\n\n    checks whether there is a "feature" value in the context.\n\n    Values may be deleted from the context using "del" but only at the level\n    they are set. You can\'t delete a value set by a feature at a scenario level\n    but you can delete a value set for a scenario in that scenario.\n\n    .. _`configuration file settion names`: beehive.html#configuration-files\n    '
    BEEHIVE = 'beehive'
    USER = 'user'

    def __init__(self, runner):
        self._runner = weakref.proxy(runner)
        self._config = runner.config
        d = self._root = {'aborted': False, 
         'failed': False, 
         'config': self._config, 
         'active_outline': None}
        self._stack = [
         d]
        self._record = {}
        self._origin = {}
        self._mode = self.BEEHIVE
        self.feature = None

    def _push(self):
        self._stack.insert(0, {})

    def _pop(self):
        self._stack.pop(0)

    @contextlib.contextmanager
    def user_mode(self):
        try:
            self._mode = self.USER
            yield
        finally:
            self._mode = self.BEEHIVE

    def _set_root_attribute(self, attr, value):
        for frame in self.__dict__['_stack']:
            if frame is self.__dict__['_root']:
                continue
            if attr in frame:
                record = self.__dict__['_record'][attr]
                params = {'attr': attr, 
                 'filename': record[0], 
                 'line': record[1], 
                 'function': record[3]}
                self._emit_warning(attr, params)
                continue

        self.__dict__['_root'][attr] = value
        if attr not in self._origin:
            self._origin[attr] = self._mode

    def _emit_warning(self, attr, params):
        msg = ''
        if self._mode is self.BEEHIVE and self._origin[attr] is not self.BEEHIVE:
            msg = "beehive runner is masking context attribute '%(attr)s' orignally set in %(function)s (%(filename)s:%(line)s)"
        elif self._mode is self.USER:
            if self._origin[attr] is not self.USER:
                msg = "user code is masking context attribute '%(attr)s' orignally set by beehive"
            elif self._config.verbose:
                msg = "user code is masking context attribute '%(attr)s'; see the tutorial for what this means"
        if msg:
            msg = msg % params
            warnings.warn(msg, ContextMaskWarning, stacklevel=3)

    def _dump(self):
        for level, frame in enumerate(self._stack):
            print('Level %d' % level)
            print(repr(frame))

    def __getattr__(self, attr):
        if attr[0] == '_':
            return self.__dict__[attr]
        for frame in self._stack:
            if attr in frame:
                return frame[attr]

        msg = "'{0}' object has no attribute '{1}'"
        msg = msg.format(self.__class__.__name__, attr)
        raise AttributeError(msg)

    def __setattr__(self, attr, value):
        if attr[0] == '_':
            self.__dict__[attr] = value
            return
        for frame in self._stack[1:]:
            if attr in frame:
                record = self._record[attr]
                params = {'attr': attr, 
                 'filename': record[0], 
                 'line': record[1], 
                 'function': record[3]}
                self._emit_warning(attr, params)
                continue

        stack_frame = traceback.extract_stack(limit=2)[0]
        self._record[attr] = stack_frame
        frame = self._stack[0]
        frame[attr] = value
        if attr not in self._origin:
            self._origin[attr] = self._mode

    def __delattr__(self, attr):
        frame = self._stack[0]
        if attr in frame:
            del frame[attr]
            del self._record[attr]
        else:
            msg = "'{0}' object has no attribute '{1}' at the current level"
            msg = msg.format(self.__class__.__name__, attr)
            raise AttributeError(msg)

    def __contains__(self, attr):
        if attr[0] == '_':
            return attr in self.__dict__
        for frame in self._stack:
            if attr in frame:
                return True

        return False

    def embed(self, mime_type, data, caption=None):
        for formatter in self._runner.formatters:
            if hasattr(formatter, 'embedding'):
                formatter.embedding(mime_type, data, caption)
                continue

    def execute_steps(self, steps_text):
        """The steps identified in the "steps" text string will be parsed and
        executed in turn just as though they were defined in a feature file.

        If the execute_steps call fails (either through error or failure
        assertion) then the step invoking it will fail.

        ValueError will be raised if this is invoked outside a feature context.

        Returns boolean False if the steps are not parseable, True otherwise.
        """
        assert isinstance(steps_text, unicode), 'Steps must be unicode.'
        if not self.feature:
            raise ValueError('execute_steps() called outside of feature')
        original_table = getattr(self, 'table', None)
        original_text = getattr(self, 'text', None)
        self.feature.parser.variant = 'steps'
        steps = self.feature.parser.parse_steps(steps_text)
        for step in steps:
            passed = step.run(self._runner, quiet=True, capture=False)
            if not passed:
                step_line = '%s %s' % (step.keyword, step.name)
                message = '%s SUB-STEP: %s' % (step.status.upper(), step_line)
                if step.error_message:
                    message += '\nSubstep info: %s' % step.error_message
                if not False:
                    raise AssertionError(message)
                continue

        self.table = original_table
        self.text = original_text
        return True


def exec_file(filename, globals={}, locals=None):
    if locals is None:
        locals = globals
    locals['__file__'] = filename
    with open(filename) as (f):
        filename2 = os.path.relpath(filename, os.getcwd())
        code = compile(f.read(), filename2, 'exec')
        exec(code, globals, locals)


def path_getrootdir(path):
    r"""
    Extract rootdir from path in a platform independent way.

    POSIX-PATH EXAMPLE:
        rootdir = path_getrootdir("/foo/bar/one.feature")
        assert rootdir == "/"

    WINDOWS-PATH EXAMPLE:
        rootdir = path_getrootdir("D:\foo\bar\one.feature")
        assert rootdir == r"D:"
    """
    drive, _ = os.path.splitdrive(path)
    if drive:
        return drive + os.path.sep
    return os.path.sep


class PathManager(object):
    __doc__ = '\n    Context manager to add paths to sys.path (python search path) within a scope\n    '

    def __init__(self, paths=None):
        self.initial_paths = paths or []
        self.paths = None

    def __enter__(self):
        self.paths = list(self.initial_paths)
        sys.path = self.paths + sys.path

    def __exit__(self, *crap):
        for path in self.paths:
            sys.path.remove(path)

        self.paths = None

    def add(self, path):
        if self.paths is None:
            self.initial_paths.append(path)
        else:
            sys.path.insert(0, path)
            self.paths.append(path)


class ModelRunner(object):
    __doc__ = '\n    Test runner for a beehive model (features).\n    Provides the core functionality of a test runner and\n    the functional API needed by model elements.\n\n    .. attribute:: aborted\n\n          This is set to true when the user aborts a test run\n          (:exc:`KeyboardInterrupt` exception). Initially: False.\n          Stored as derived attribute in :attr:`Context.aborted`.\n    '

    def __init__(self, config, features=None):
        self.config = config
        self.features = features or []
        self.hooks = {}
        self.formatters = []
        self.undefined_steps = []
        self.context = None
        self.feature = None
        self.stdout_capture = None
        self.stderr_capture = None
        self.log_capture = None
        self.old_stdout = None
        self.old_stderr = None

    def _get_aborted(self):
        value = False
        if self.context:
            value = self.context.aborted
        return value

    def _set_aborted(self, value):
        assert self.context
        self.context._set_root_attribute('aborted', bool(value))

    aborted = property(_get_aborted, _set_aborted, doc='Indicates that test run is aborted by the user.')

    def run_hook(self, name, context, *args):
        if not self.config.dry_run:
            if name in self.hooks:
                try:
                    with context.user_mode():
                        self.hooks[name](context, *args)
                except Exception as e:
                    if 'all' in name:
                        self.aborted = True
                    if 'step' in name:
                        args[0].status = 'failed'
                    if 'scenario' in name:
                        args[0].steps[(-1)].status = 'failed'
                        args[0].compute_status()
                        args[0].feature.compute_status()
                    if 'feature' in name:
                        args[0].scenarios[(-1)].steps[(-1)].status = 'failed'
                        args[0].scenarios[(-1)].compute_status()
                        args[0].compute_status()
                        args[0]._cached_status = 'failed'
                    print('Exception in %s hook: %s' % (name, str(e)))

    def setup_capture(self):
        if not self.context:
            self.context = Context(self)
        if self.config.stdout_capture:
            if sys.version_info[0] == '2':
                self.stdout_capture = StringIO()
            else:
                self.stdout_capture = MyBytesIO()
            self.context.stdout_capture = self.stdout_capture
        if self.config.stderr_capture:
            if sys.version_info[0] == '2':
                self.stderr_capture = StringIO()
            else:
                self.stderr_capture = MyBytesIO()
            self.context.stderr_capture = self.stderr_capture
        if self.config.log_capture:
            self.log_capture = LoggingCapture(self.config)
            self.log_capture.inveigle()
            self.context.log_capture = self.log_capture

    def start_capture(self):
        if self.config.stdout_capture:
            if not self.old_stdout:
                self.old_stdout = sys.stdout
                sys.stdout = self.stdout_capture
            assert sys.stdout is self.stdout_capture
        if self.config.stderr_capture:
            if not self.old_stderr:
                self.old_stderr = sys.stderr
                sys.stderr = self.stderr_capture
            assert sys.stderr is self.stderr_capture

    def stop_capture(self):
        if self.config.stdout_capture:
            if self.old_stdout:
                sys.stdout = self.old_stdout
                self.old_stdout = None
            assert sys.stdout is not self.stdout_capture
        if self.config.stderr_capture:
            if self.old_stderr:
                sys.stderr = self.old_stderr
                self.old_stderr = None
            assert sys.stderr is not self.stderr_capture

    def teardown_capture(self):
        if self.config.log_capture:
            self.log_capture.abandon()

    def run_model(self, features=None):
        if not self.context:
            self.context = Context(self)
        if features is None:
            features = self.features
        context = self.context
        self.setup_capture()
        self.run_hook('before_all', context)
        run_feature = not self.aborted
        failed_count = 0
        undefined_steps_initial_size = len(self.undefined_steps)
        for feature in features:
            if run_feature:
                try:
                    self.feature = feature
                    for formatter in self.formatters:
                        formatter.uri(feature.filename)

                    failed = feature.run(self)
                    if failed:
                        failed_count += 1
                        if self.config.stop or self.aborted:
                            run_feature = False
                except KeyboardInterrupt:
                    self.aborted = True
                    failed_count += 1
                    run_feature = False

            for reporter in self.config.reporters:
                reporter.feature(feature)

        if self.aborted:
            print('\nABORTED: By user.')
        for formatter in self.formatters:
            formatter.close()

        self.run_hook('after_all', self.context)
        for reporter in self.config.reporters:
            reporter.end()

        failed = failed_count > 0 or self.aborted or len(self.undefined_steps) > undefined_steps_initial_size
        return failed

    def run(self):
        """
        Implements the run method by running the model.
        """
        self.context = Context(self)
        return self.run_model()


class Runner(ModelRunner):
    __doc__ = '\n    Standard test runner for beehive:\n\n      * setup paths\n      * loads environment hooks\n      * loads step definitions\n      * select feature files, parses them and creates model (elements)\n    '

    def __init__(self, config):
        super(Runner, self).__init__(config)
        self.path_manager = PathManager()
        self.base_dir = None

    def setup_paths(self):
        if self.config.paths:
            if self.config.verbose:
                print('Supplied path:' + ', '.join('"%s"' % path for path in self.config.paths))
            first_path = self.config.paths[0]
            if hasattr(first_path, 'filename'):
                first_path = first_path.filename
            base_dir = first_path
            if base_dir.startswith('@'):
                base_dir = base_dir[1:]
                file_locations = self.feature_locations()
                if file_locations:
                    base_dir = os.path.dirname(file_locations[0].filename)
                base_dir = os.path.abspath(base_dir)
                if os.path.isfile(base_dir):
                    if self.config.verbose:
                        print('Primary path is to a file so using its directory')
                    base_dir = os.path.dirname(base_dir)
            else:
                if self.config.verbose:
                    print('Using default path "./features"')
                base_dir = os.path.abspath('features')
            root_dir = path_getrootdir(base_dir)
            new_base_dir = base_dir
            while True:
                if self.config.verbose:
                    print('Trying base directory:', new_base_dir)
                if os.path.isdir(os.path.join(new_base_dir, self.config.steps_dir)):
                    break
                if os.path.isfile(os.path.join(new_base_dir, self.config.env_py)):
                    break
                if new_base_dir == root_dir:
                    break
                new_base_dir = os.path.dirname(new_base_dir)

            if new_base_dir == root_dir:
                if self.config.verbose:
                    if not self.config.paths:
                        print('ERROR: Could not find "%s" directory. Please ' % self.config.steps_dir + 'specify where to find your features.')
                    else:
                        print('ERROR: Could not find "%s" directory in your ' % self.config.steps_dir + 'specified path "%s"' % base_dir)
                raise ConfigError('No %s directory in "%s"' % (self.config.steps_dir, base_dir))
            base_dir = new_base_dir
            self.config.base_dir = base_dir
            for dirpath, dirnames, filenames in os.walk(base_dir):
                if [fn for fn in filenames if fn.endswith('.feature')]:
                    break
            else:
                if self.config.verbose:
                    if not self.config.paths:
                        print('ERROR: Could not find any "<name>.feature" files. ' + 'Please specify where to find your features.')
                    else:
                        print('ERROR: Could not find any "<name>.feature" files ' + 'in your specified path "%s"' % base_dir)
                raise ConfigError('No feature files in "%s"' % base_dir)

            self.base_dir = base_dir
            self.path_manager.add(base_dir)
            if not self.config.paths:
                self.config.paths = [
                 base_dir]
            if base_dir != os.getcwd():
                self.path_manager.add(os.getcwd())

    def before_all_default_hook(self, context):
        """
        Default implementation for :func:`before_all()` hook.
        Setup the logging subsystem based on the configuration data.
        """
        context.config.setup_logging()

    def load_hooks(self, filename=''):
        filename = filename or self.config.env_py
        hooks_path = os.path.join(self.base_dir, filename)
        if os.path.exists(hooks_path):
            exec_file(hooks_path, self.hooks)
        if 'before_all' not in self.hooks:
            self.hooks['before_all'] = self.before_all_default_hook

    def load_step_definitions(self, extra_step_paths=[]):
        step_globals = {'use_step_matcher': matchers.use_step_matcher, 
         'step_matcher': matchers.step_matcher}
        setup_step_decorators(step_globals)
        steps_dir = os.path.join(self.base_dir, self.config.steps_dir)
        paths = [steps_dir] + list(extra_step_paths)
        with PathManager(paths):
            default_matcher = matchers.current_matcher
            for path in paths:
                for dirpath, dirnames, filenames in os.walk(path):
                    for name in sorted(filenames):
                        if name.endswith('.py'):
                            step_module_globals = step_globals.copy()
                            exec_file(os.path.join(dirpath, name), step_module_globals)
                            matchers.current_matcher = default_matcher
                            continue

    def feature_locations(self):
        return collect_feature_locations(self.config.paths)

    def run(self):
        with self.path_manager:
            self.setup_paths()
            return self.run_with_paths()

    def run_with_paths(self):
        self.context = Context(self)
        self.load_hooks()
        self.load_step_definitions()
        feature_locations = [filename for filename in self.feature_locations() if not self.config.exclude(filename)]
        features = parse_features(feature_locations, language=self.config.lang)
        self.features.extend(features)
        stream_openers = self.config.outputs
        self.formatters = formatters.get_formatter(self.config, stream_openers)
        return self.run_model()