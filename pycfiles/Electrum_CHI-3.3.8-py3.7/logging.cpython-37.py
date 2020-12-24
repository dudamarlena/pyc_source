# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/logging.py
# Compiled at: 2019-08-25 05:54:56
# Size of source mod 2**32: 9329 bytes
import logging, datetime, sys, pathlib, os, platform
from typing import Optional
import copy

class LogFormatterForFiles(logging.Formatter):

    def formatTime(self, record, datefmt=None):
        date = datetime.datetime.fromtimestamp(record.created).astimezone(datetime.timezone.utc)
        if not datefmt:
            datefmt = '%Y%m%dT%H%M%S.%fZ'
        return date.strftime(datefmt)

    def format(self, record):
        record = _shorten_name_of_logrecord(record)
        return super().format(record)


file_formatter = LogFormatterForFiles(fmt='%(asctime)22s | %(levelname)8s | %(name)s | %(message)s')

class LogFormatterForConsole(logging.Formatter):

    def format(self, record):
        record = _shorten_name_of_logrecord(record)
        text = super().format(record)
        shortcut = getattr(record, 'custom_shortcut', None)
        if shortcut:
            text = text[:1] + f"/{shortcut}" + text[1:]
        return text


console_formatter = LogFormatterForConsole(fmt='%(levelname).1s | %(name)s | %(message)s')

def _shorten_name_of_logrecord(record: logging.LogRecord) -> logging.LogRecord:
    record = copy.copy(record)
    if record.name.startswith('electrum.'):
        record.name = record.name[9:]
    if record.name.startswith('electrum_chi.'):
        record.name = record.name[13:]
    record.name = record.name.replace('interface.Interface', 'interface', 1)
    record.name = record.name.replace('network.Network', 'network', 1)
    record.name = record.name.replace('synchronizer.Synchronizer', 'synchronizer', 1)
    record.name = record.name.replace('verifier.SPV', 'verifier', 1)
    record.name = record.name.replace('gui.qt.main_window.ElectrumWindow', 'gui.qt.main_window', 1)
    return record


root_logger = logging.getLogger()
root_logger.setLevel(logging.WARNING)
console_stderr_handler = logging.StreamHandler(sys.stderr)
console_stderr_handler.setFormatter(console_formatter)
console_stderr_handler.setLevel(logging.WARNING)
root_logger.addHandler(console_stderr_handler)
electrum_logger = logging.getLogger('electrum_chi')
electrum_logger.setLevel(logging.DEBUG)

def _delete_old_logs(path, keep=10):
    files = sorted((list(pathlib.Path(path).glob('electrum_chi_log_*.log'))), reverse=True)
    for f in files[keep:]:
        os.remove(str(f))


_logfile_path = None

def _configure_file_logging(log_directory: pathlib.Path):
    global _logfile_path
    assert _logfile_path is None, 'file logging already initialized'
    log_directory.mkdir(exist_ok=True)
    _delete_old_logs(log_directory)
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    PID = os.getpid()
    _logfile_path = log_directory / f"electrum_chi_log_{timestamp}_{PID}.log"
    file_handler = logging.FileHandler(_logfile_path)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)


def _configure_verbosity(*, verbosity, verbosity_shortcuts):
    if not verbosity:
        if not verbosity_shortcuts:
            return
    console_stderr_handler.setLevel(logging.DEBUG)
    _process_verbosity_log_levels(verbosity)
    _process_verbosity_filter_shortcuts(verbosity_shortcuts)


def _process_verbosity_log_levels(verbosity):
    return verbosity == '*' or isinstance(verbosity, str) or None
    filters = verbosity.split(',')
    for filt in filters:
        if not filt:
            continue
        items = filt.split('=')
        if len(items) == 1:
            level = items[0]
            electrum_logger.setLevel(level.upper())
        elif len(items) == 2:
            logger_name, level = items
            logger = get_logger(logger_name)
            logger.setLevel(level.upper())
        else:
            raise Exception(f"invalid log filter: {filt}")


def _process_verbosity_filter_shortcuts(verbosity_shortcuts):
    if not isinstance(verbosity_shortcuts, str):
        return
    elif len(verbosity_shortcuts) < 1:
        return
        is_blacklist = verbosity_shortcuts[0] == '^'
        if is_blacklist:
            filters = verbosity_shortcuts[1:]
    else:
        filters = verbosity_shortcuts[0:]
    filt = ShortcutFilteringFilter(is_blacklist=is_blacklist, filters=filters)
    console_stderr_handler.addFilter(filt)


class ShortcutInjectingFilter(logging.Filter):

    def __init__(self, *, shortcut):
        super().__init__()
        self._ShortcutInjectingFilter__shortcut = shortcut

    def filter(self, record):
        record.custom_shortcut = self._ShortcutInjectingFilter__shortcut
        return True


class ShortcutFilteringFilter(logging.Filter):

    def __init__(self, *, is_blacklist, filters):
        super().__init__()
        self._ShortcutFilteringFilter__is_blacklist = is_blacklist
        self._ShortcutFilteringFilter__filters = filters

    def filter(self, record):
        if record.levelno >= logging.ERROR:
            return True
        if record.name == __name__:
            return True
        shortcut = getattr(record, 'custom_shortcut', None)
        if self._ShortcutFilteringFilter__is_blacklist:
            if shortcut is None:
                return True
            if shortcut in self._ShortcutFilteringFilter__filters:
                return False
            return True
        if shortcut is None:
            return False
        if shortcut in self._ShortcutFilteringFilter__filters:
            return True
        return False


def get_logger(name: str) -> logging.Logger:
    if name.startswith('electrum.'):
        name = name[9:]
    if name.startswith('electrum_chi.'):
        name = name[13:]
    return electrum_logger.getChild(name)


_logger = get_logger(__name__)
_logger.setLevel(logging.INFO)

class Logger:
    LOGGING_SHORTCUT = None

    def __init__(self):
        self.logger = self._Logger__get_logger_for_obj()

    def __get_logger_for_obj(self) -> logging.Logger:
        cls = self.__class__
        if cls.__module__:
            name = f"{cls.__module__}.{cls.__name__}"
        else:
            name = cls.__name__
        try:
            diag_name = self.diagnostic_name()
        except Exception as e:
            try:
                raise Exception('diagnostic name not yet available?') from e
            finally:
                e = None
                del e

        if diag_name:
            name += f".[{diag_name}]"
        logger = get_logger(name)
        if self.LOGGING_SHORTCUT:
            logger.addFilter(ShortcutInjectingFilter(shortcut=(self.LOGGING_SHORTCUT)))
        return logger

    def diagnostic_name(self):
        return ''


def configure_logging(config):
    verbosity = config.get('verbosity')
    verbosity_shortcuts = config.get('verbosity_shortcuts')
    _configure_verbosity(verbosity=verbosity, verbosity_shortcuts=verbosity_shortcuts)
    is_android = 'ANDROID_DATA' in os.environ
    if not is_android:
        if not config.get('log_to_file', False):
            pass
        else:
            log_directory = pathlib.Path(config.path) / 'logs'
            _configure_file_logging(log_directory)
    logging.getLogger('kivy').propagate = False
    from . import ELECTRUM_VERSION
    from .constants import GIT_REPO_URL
    _logger.info(f"Electrum-CHI version: {ELECTRUM_VERSION} - https://xaya.io/ - {GIT_REPO_URL}")
    _logger.info(f"Python version: {sys.version}. On platform: {describe_os_version()}")
    _logger.info(f"Logging to file: {str(_logfile_path)}")
    _logger.info(f"Log filters: verbosity {repr(verbosity)}, verbosity_shortcuts {repr(verbosity_shortcuts)}")


def get_logfile_path() -> Optional[pathlib.Path]:
    return _logfile_path


def describe_os_version() -> str:
    if 'ANDROID_DATA' in os.environ:
        from kivy import utils
        if utils.platform != 'android':
            return utils.platform
        import jnius
        bv = jnius.autoclass('android.os.Build$VERSION')
        b = jnius.autoclass('android.os.Build')
        return 'Android {} on {} {} ({})'.format(bv.RELEASE, b.BRAND, b.DEVICE, b.DISPLAY)
    return platform.platform()