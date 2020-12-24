# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\__init__.py
# Compiled at: 2009-07-21 15:08:08
"""
The Vision Egg package.

The Vision Egg is a programming library (with demo applications) that
uses standard, inexpensive computer graphics cards to produce visual
stimuli for vision research experiments.

Today's consumer computer graphics cards, thanks to the demands of
computer gamers, are capable of drawing and updating computer graphics
suitable for producing research-quality visual stimuli. The Vision Egg
allows the vision scientist (or anyone else) to program these cards
using OpenGL, the standard in computer graphics
programming. Potentially difficult tasks, such as initializing
graphics, getting precise timing information, controlling stimulus
parameters in real-time, and synchronizing with data acquisition are
greatly eased by routines within the Vision Egg.

See the 'Core' module for the fundamental Vision Egg classes.

"""
release_name = '1.2.1'
__version__ = release_name
import VisionEgg.Configuration, VisionEgg.ParameterTypes as ve_types, os, sys, time, types, numpy, numpy.oldnumeric as Numeric, warnings, traceback, StringIO, logging, logging.handlers
if not hasattr(Numeric, 'UInt8'):
    Numeric.UInt8 = 'b'
if not hasattr(Numeric, 'Float32'):
    Numeric.UInt8 = 'f'
if not hasattr(sys, 'frozen'):
    try:
        __import__('VisionEgg.VisionEgg')
    except ImportError:
        pass
    else:
        raise RuntimeError('Outdated "VisionEgg.py" and/or "VisionEgg.pyc" found.  Please delete from your VisionEgg package directory.')
config = VisionEgg.Configuration.Config()
logger = logging.getLogger('VisionEgg')
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s (%(process)d) %(levelname)s: %(message)s')
_default_logging_started = False

def start_default_logging(maxBytes=100000):
    """Create and add log handlers"""
    global _default_logging_started
    global config
    if _default_logging_started:
        return
    if config.VISIONEGG_LOG_TO_STDERR:
        log_handler_stderr = logging.StreamHandler()
        log_handler_stderr.setFormatter(log_formatter)
        logger.addHandler(log_handler_stderr)
    if config.VISIONEGG_LOG_FILE:
        if hasattr(logging, 'handlers'):
            log_handler_logfile = logging.handlers.RotatingFileHandler(config.VISIONEGG_LOG_FILE, maxBytes=maxBytes)
        else:
            log_handler_logfile = logging.FileHandler(config.VISIONEGG_LOG_FILE)
        log_handler_logfile.setFormatter(log_formatter)
        logger.addHandler(log_handler_logfile)
    script_name = sys.argv[0]
    if not script_name:
        script_name = '(interactive shell)'
    logger.info('Script ' + script_name + ' started Vision Egg %s with process id %d.' % (VisionEgg.release_name, os.getpid()))
    _default_logging_started = True


if not sys.argv[0]:
    config.VISIONEGG_GUI_ON_ERROR = 0

class _ExceptionHookKeeper:

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        global config
        traceback_stream = StringIO.StringIO()
        traceback.print_exception(exc_type, exc_value, exc_traceback, None, traceback_stream)
        traceback_stream.seek(0)
        try:
            logger.removeHandler(log_handler_stderr)
            removed_stderr = True
        except:
            removed_stderr = False

        logger.critical(traceback_stream.read())
        if removed_stderr:
            logger.addHandler(log_handler_stderr)
        if config is not None:
            if config.VISIONEGG_GUI_ON_ERROR:
                if config.VISIONEGG_TKINTER_OK:
                    if hasattr(config, '_open_screens'):
                        for screen in config._open_screens:
                            screen.close()

                    traceback_stream = StringIO.StringIO()
                    traceback.print_tb(exc_traceback, None, traceback_stream)
                    traceback_stream.seek(0)
                    pygame_bug_workaround = False
                    if hasattr(config, '_pygame_started'):
                        if config._pygame_started:
                            pygame_bug_workaround = True
                    if sys.platform.startswith('linux'):
                        pygame_bug_workaround = False
                    if pygame_bug_workaround or hasattr(config, '_Tkinter_used'):
                        if config._Tkinter_used:
                            import GUI
                            GUI.showexception(exc_type, exc_value, traceback_stream.getvalue())
        __keep_config__ = config
        self.orig_hook(exc_type, exc_value, exc_traceback)
        config = __keep_config__
        return

    def __init__(self):
        self._sys = sys
        self.orig_hook = self._sys.excepthook
        sys.excepthook = self.handle_exception

    def __del__(self):
        self._sys.excepthook = self.orig_hook


def watch_exceptions():
    """Catch exceptions, log them, and optionally open GUI."""
    global _exception_hook_keeper
    _exception_hook_keeper = _ExceptionHookKeeper()


def stop_watching_exceptions():
    """Stop catching exceptions, returning to previous state."""
    global _exception_hook_keeper
    del _exception_hook_keeper


if config.VISIONEGG_ALWAYS_START_LOGGING:
    start_default_logging()
    watch_exceptions()
    if len(config._delayed_configuration_log_warnings) != 0:
        logger = logging.getLogger('VisionEgg.Configuration')
        for msg in config._delayed_configuration_log_warnings:
            logger.warning(msg)

def recursive_base_class_finder(klass):
    """A function to find all base classes."""
    result = [
     klass]
    for base_class in klass.__bases__:
        for base_base_class in recursive_base_class_finder(base_class):
            result.append(base_base_class)

    result2 = []
    for r in result:
        if r not in result2:
            result2.append(r)

    return result2


if sys.platform == 'win32':
    true_time_func = time.clock
else:
    true_time_func = time.time
config._FRAMECOUNT_ABSOLUTE = 0

def time_func_locked_to_frames():
    return config._FRAMECOUNT_ABSOLUTE / float(config.VISIONEGG_MONITOR_REFRESH_HZ)


time_func = true_time_func

def set_time_func_to_true_time():
    time_func = true_time_func


def set_time_func_to_frame_locked():
    time_func = time_func_locked_to_frames


def timing_func():
    """DEPRECATED.  Use time_func instead"""
    warnings.warn('timing_func() has been changed to time_func(). This warning will only be issued once, but each call to timing_func() will be slower than if you called time_func() directly', DeprecationWarning, stacklevel=2)
    return time_func()


class Parameters:
    """Parameter container.

    Simple empty class to act something like a C struct."""
    pass


class ParameterDefinition(dict):
    """Define parameters used in ClassWithParameters
    """
    DEPRECATED = 1
    OPENGL_ENUM = 2


class ClassWithParameters(object):
    """Base class for any class that uses parameters.

    Any class that uses parameters potentially modifiable in realtime
    should be a subclass of ClassWithParameters.  This class enforces
    type checking and sets default values.

    Any subclass of ClassWithParameters can define two class (not
    instance) attributes, "parameters_and_defaults" and
    "constant_parameters_and_defaults". These are dictionaries where
    the key is a string containing the name of the parameter and the
    the value is a tuple of length 2 containing the default value and
    the type.  For example, an acceptable dictionary would be
    {"parameter1" : (1.0, ve_types.Real)}

    See the ParameterTypes module for more information about types.

    """
    parameters_and_defaults = ParameterDefinition({})
    constant_parameters_and_defaults = ParameterDefinition({})
    __slots__ = ('parameters', 'constant_parameters')

    def __getstate__(self):
        """support for being pickled"""
        result = {}
        classes = recursive_base_class_finder(self.__class__)
        for klass in classes:
            if hasattr(klass, '__slots__'):
                for attr in klass.__slots__:
                    if hasattr(self, attr):
                        result[attr] = getattr(self, attr)

        return result

    def __setstate__(self, dict):
        """support for being unpickled"""
        for attr in dict.keys():
            setattr(self, attr, dict[attr])

    __safe_for_unpickling__ = True

    def __init__(self, **kw):
        """Create self.parameters and set values."""
        self.constant_parameters = Parameters()
        self.parameters = Parameters()
        classes = recursive_base_class_finder(self.__class__)
        done_constant_parameters_and_defaults = []
        done_parameters_and_defaults = []
        done_kw = []
        for klass in classes:
            if klass == object:
                continue
            if hasattr(klass, 'parameters_and_defaults') and klass.parameters_and_defaults not in done_parameters_and_defaults:
                for parameter_name in klass.parameters_and_defaults.keys():
                    if hasattr(self.parameters, parameter_name):
                        raise ValueError("More than one definition of parameter '%s'" % parameter_name)
                    (value, tipe) = klass.parameters_and_defaults[parameter_name][:2]
                    if not ve_types.is_parameter_type_def(tipe):
                        raise ValueError("In definition of parameter '%s', %s is not a valid type declaration." % (parameter_name, tipe))
                    if kw.has_key(parameter_name):
                        value = kw[parameter_name]
                        done_kw.append(parameter_name)
                    if value is not None:
                        if not tipe.verify(value):
                            print 'parameter_name', parameter_name
                            print 'value', value
                            print 'type value', type(value)
                            print 'isinstance(value, numpy.ndarray)', isinstance(value, numpy.ndarray)
                            print 'tipe', tipe
                            if not isinstance(value, numpy.ndarray):
                                value_str = str(value)
                            elif Numeric.multiply.reduce(value.shape) < 10:
                                value_str = str(value)
                            else:
                                value_str = '(array data)'
                            raise TypeError("Parameter '%s' value %s is type %s (not type %s) in %s" % (parameter_name, value_str, type(value), tipe, self))
                    setattr(self.parameters, parameter_name, value)

                done_parameters_and_defaults.append(klass.parameters_and_defaults)
            if hasattr(klass, 'constant_parameters_and_defaults') and klass.constant_parameters_and_defaults not in done_constant_parameters_and_defaults:
                for parameter_name in klass.constant_parameters_and_defaults.keys():
                    if hasattr(self.parameters, parameter_name):
                        raise ValueError("Definition of '%s' as variable parameter and constant parameter." % parameter_name)
                    if hasattr(self.constant_parameters, parameter_name):
                        raise ValueError("More than one definition of constant parameter '%s'" % parameter_name)
                    (value, tipe) = klass.constant_parameters_and_defaults[parameter_name][:2]
                    if not ve_types.is_parameter_type_def(tipe):
                        raise ValueError("In definition of constant parameter '%s', %s is not a valid type declaration." % (parameter_name, tipe))
                    if kw.has_key(parameter_name):
                        value = kw[parameter_name]
                        done_kw.append(parameter_name)
                    if type(value) != type(None):
                        if not tipe.verify(value):
                            if type(value) != Numeric.ArrayType:
                                value_str = str(value)
                            elif Numeric.multiply.reduce(value.shape) < 10:
                                value_str = str(value)
                            else:
                                value_str = '(array data)'
                            raise TypeError("Constant parameter '%s' value %s is type %s (not type %s) in %s" % (parameter_name, value_str, type(value), tipe, self))
                    setattr(self.constant_parameters, parameter_name, value)

                done_constant_parameters_and_defaults.append(klass.constant_parameters_and_defaults)

        for kw_parameter_name in kw.keys():
            if kw_parameter_name not in done_kw:
                raise ValueError("parameter '%s' passed as keyword argument, but not specified by %s (or subclasses) as potential parameter" % (kw_parameter_name, self.__class__))

        return

    def is_constant_parameter(self, parameter_name):
        classes = recursive_base_class_finder(self.__class__)
        for klass in classes:
            if klass == object:
                continue
            if klass.constant_parameters_and_defaults.has_key(parameter_name):
                return True

        return False

    def get_specified_type(self, parameter_name):
        classes = recursive_base_class_finder(self.__class__)
        for klass in classes:
            if klass == object:
                continue
            if klass.parameters_and_defaults.has_key(parameter_name):
                return klass.parameters_and_defaults[parameter_name][1]

        raise AttributeError("%s has no parameter named '%s'" % (self.__class__, parameter_name))

    def verify_parameters(self):
        """Perform type check on all parameters"""
        for parameter_name in dir(self.parameters):
            if parameter_name.startswith('__'):
                continue
            require_type = self.get_specified_type(parameter_name)
            this_type = ve_types.get_type(getattr(self.parameters, parameter_name))
            ve_types.assert_type(this_type, require_type)

    def set(self, **kw):
        """Set a parameter with type-checked value

        This is the slow but safe way to set parameters.  It is recommended to
        use this method in all but speed-critical portions of code.
        """
        for parameter_name in kw.keys():
            setattr(self.parameters, parameter_name, kw[parameter_name])
            require_type = self.get_specified_type(parameter_name)
            value = kw[parameter_name]
            this_type = ve_types.get_type(value)
            ve_types.assert_type(this_type, require_type)
            setattr(self.parameters, parameter_name, value)


def get_type(value):
    warnings.warn('VisionEgg.get_type() has been moved to ' + 'VisionEgg.ParameterTypes.get_type()', DeprecationWarning, stacklevel=2)
    return ve_types.get_type(value)


def assert_type(*args):
    warnings.warn('VisionEgg.assert_type() has been moved to ' + 'VisionEgg.ParameterTypes.assert_type()', DeprecationWarning, stacklevel=2)
    return ve_types.assert_type(*args)


def _get_lowerleft(position, anchor, size):
    """Private helper function

    size is (width, height)
    """
    if anchor == 'lowerleft':
        lowerleft = position
    else:
        if len(position) > 2:
            z = position[2]
        else:
            z = 0.0
        if len(position) > 3:
            w = position[3]
        else:
            w = 1.0
        if z != 0.0:
            warnings.warn("z coordinate (other than 0.0) specificed where anchor not 'lowerleft' -- cannot compute")
        if w != 1.0:
            warnings.warn("w coordinate (other than 1.0) specificed where anchor not 'lowerleft' -- cannot compute")
        if anchor == 'center':
            lowerleft = (
             position[0] - size[0] / 2.0, position[1] - size[1] / 2.0)
        elif anchor == 'lowerright':
            lowerleft = (
             position[0] - size[0], position[1])
        elif anchor == 'upperright':
            lowerleft = (
             position[0] - size[0], position[1] - size[1])
        elif anchor == 'upperleft':
            lowerleft = (
             position[0], position[1] - size[1])
        elif anchor == 'left':
            lowerleft = (
             position[0], position[1] - size[1] / 2.0)
        elif anchor == 'right':
            lowerleft = (
             position[0] - size[0], position[1] - size[1] / 2.0)
        elif anchor == 'bottom':
            lowerleft = (
             position[0] - size[0] / 2.0, position[1])
        elif anchor == 'top':
            lowerleft = (
             position[0] - size[0] / 2.0, position[1] - size[1])
        else:
            raise ValueError('No anchor position %s' % anchor)
    return lowerleft


def _get_center(position, anchor, size):
    """Private helper function"""
    if anchor == 'center':
        center = position
    else:
        if len(position) > 2:
            z = position[2]
        else:
            z = 0.0
        if len(position) > 3:
            w = position[3]
        else:
            w = 1.0
        if z != 0.0:
            raise ValueError("z coordinate (other than 0.0) specificed where anchor not 'center' -- cannot compute")
        if w != 1.0:
            raise ValueError("w coordinate (other than 1.0) specificed where anchor not 'center' -- cannot compute")
        if anchor == 'lowerleft':
            center = (
             position[0] + size[0] / 2.0, position[1] + size[1] / 2.0)
        elif anchor == 'lowerright':
            center = (
             position[0] - size[0] / 2.0, position[1] + size[1] / 2.0)
        elif anchor == 'upperright':
            center = (
             position[0] - size[0] / 2.0, position[1] - size[1] / 2.0)
        elif anchor == 'upperleft':
            center = (
             position[0] + size[0] / 2.0, position[1] - size[1] / 2.0)
        elif anchor == 'left':
            center = (
             position[0] + size[0] / 2.0, position[1])
        elif anchor == 'right':
            center = (
             position[0] - size[0] / 2.0, position[1])
        elif anchor == 'bottom':
            center = (
             position[0], position[1] + size[1] / 2.0)
        elif anchor == 'top':
            center = (
             position[0], position[1] - size[1] / 2.0)
        else:
            raise ValueError('No anchor position %s' % anchor)
    return center