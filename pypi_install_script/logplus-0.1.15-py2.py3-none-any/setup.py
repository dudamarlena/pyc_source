import os
import sys
import logging
import logging.config
import traceback
import io
import yaml


# Main
def setup(filename=None, config_yaml=None, **kwargs):
    """Setup logging configuration """

    # Make sure filename is set
    if not filename:
        raise Exception('filename parameter missing')

    # Load logging configuration
    if not config_yaml:
        path = os.path.dirname(os.path.realpath(__file__))
        config_yaml = os.path.join(path, 'logging.yaml')

    # Read logging yaml configuration file
    with open(config_yaml, 'rt') as f:
        config = yaml.safe_load(f.read())

    # Modify log file name with argument
    config["handlers"]["file_handler"]["filename"]=filename

    # Configure logging with yaml file
    logging.config.dictConfig(config)

    # Instantiate logger
    logger = logging.getLogger(__name__)

    # Assign argument values to logger
    if kwargs:
        logger = logging.LoggerAdapter(logger, kwargs)

    # Custom log methods
    def myDebug(self, msg, **kwargs):
        orig_dict = logger.extra
        if kwargs: logger.extra = {**logger.extra, **kwargs}
        self.log(logging.DEBUG, msg)
        logger.extra = orig_dict

    def myInfo(self, msg, **kwargs):
        orig_dict = logger.extra
        if kwargs: logger.extra = {**logger.extra, **kwargs}
        self.log(logging.INFO, msg)
        logger.extra = orig_dict

    def myWarning(self, msg, **kwargs):
        orig_dict = logger.extra
        if kwargs: logger.extra = {**logger.extra, **kwargs}
        self.log(logging.WARNING, msg)
        logger.extra = orig_dict

    def myError(self, msg, **kwargs):
        orig_dict = logger.extra
        if kwargs: logger.extra = {**logger.extra, **kwargs}
        self.log(logging.ERROR, msg)
        logger.extra = orig_dict

    def myCritical(self, msg, **kwargs):
        orig_dict = logger.extra
        if kwargs: logger.extra = {**logger.extra, **kwargs}
        self.log(logging.CRITICAL, msg)
        logger.extra = orig_dict

    def addLevelName(level, levelName):
        """
        Associate 'levelName' with 'level'.
        This is used when converting levels to text during message formatting.
        """
        _acquireLock()
        try:  # unlikely to cause an exception, but you never know...
            _levelToName[level] = levelName
            _nameToLevel[levelName] = level
        finally:
            _releaseLock()

    if hasattr(sys, '_getframe'):
        currentframe = lambda: sys._getframe(3)
    else:  # pragma: no cover
        def currentframe():
            """Return the frame object for the caller's stack frame."""
            try:
                raise Exception
            except Exception:
                return sys.exc_info()[2].tb_frame.f_back

    _srcfile = os.path.normcase(addLevelName.__code__.co_filename)

    def myFindCaller(self, stack_info=False, stacklevel=1):
        # Increase stack level to get calling script of logplus
        stacklevel += 1

        f = currentframe()
        if f is not None:
            f = f.f_back
        orig_f = f
        while f and stacklevel > 1:
            f = f.f_back
            stacklevel -= 1
        if not f:
            f = orig_f
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    # Define subclassed functions
    logger.__class__.debug = myDebug
    logger.__class__.info = myInfo
    logger.__class__.warn = myWarning
    logger.__class__.warning = myWarning
    logger.__class__.error = myError
    logger.__class__.critical = myCritical
    logger.logger.findCaller = myFindCaller

    # Return custom logger
    return logger


if __name__ == '__main__':

    # Test logger with log file and parameters
    arg1 = "argument1"
    uuid = "23RS2F"
    log = setup('test.log', arg1=arg1, uuid=uuid)

    # Create a log entry
    log.warning("Application message", count=1)

