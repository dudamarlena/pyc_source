# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philewels/GitHub/MultiQC/multiqc/utils/log.py
# Compiled at: 2019-11-13 05:22:37
# Size of source mod 2**32: 3056 bytes
"""
Code to initilise the MultiQC logging
"""
import coloredlogs, logging, os, shutil, sys, tempfile
from multiqc.utils import config, util_functions
LEVELS = {0:'INFO', 
 1:'DEBUG'}
log_tmp_dir = None
log_tmp_fn = '/dev/null'

def init_log(logger, loglevel=0, no_ansi=False):
    """
    Initializes logging.
    Prints logs to console with level defined by loglevel
    Also prints verbose log to the multiqc data directory if available.
    (multiqc_data/multiqc.log)

    Args:
        loglevel (str): Determines the level of the log output.
    """
    global log_tmp_dir
    global log_tmp_fn
    log_tmp_dir = tempfile.mkdtemp()
    log_tmp_fn = os.path.join(log_tmp_dir, 'multiqc.log')
    debug_template = '[%(asctime)s] %(name)-50s [%(levelname)-7s]  %(message)s'
    info_template = '[%(levelname)-7s] %(module)15s : %(message)s'
    logger.setLevel(getattr(logging, 'DEBUG'))
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, loglevel))
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES
    level_styles['debug'] = {'faint': True}
    if loglevel == 'DEBUG':
        if no_ansi or not sys.stderr.isatty():
            console.setFormatter(logging.Formatter(debug_template))
        else:
            console.setFormatter(coloredlogs.ColoredFormatter(fmt=debug_template, level_styles=level_styles))
    else:
        if no_ansi or not sys.stderr.isatty():
            console.setFormatter(logging.Formatter(info_template))
        else:
            console.setFormatter(coloredlogs.ColoredFormatter(fmt=info_template, level_styles=level_styles))
    logger.addHandler(console)
    file_handler = logging.FileHandler(log_tmp_fn, encoding='utf-8')
    file_handler.setLevel(getattr(logging, 'DEBUG'))
    file_handler.setFormatter(logging.Formatter(debug_template))
    logger.addHandler(file_handler)


def move_tmp_log(logger):
    """ Move the temporary log file to the MultiQC data directory
    if it exists. """
    try:
        logging.shutdown()
        shutil.move(log_tmp_fn, os.path.join(config.data_dir, 'multiqc.log'))
        util_functions.robust_rmtree(log_tmp_dir)
    except (AttributeError, TypeError, IOError):
        pass


def get_log_stream(logger):
    """
    Returns a stream to the root log file.
    If there is no logfile return the stderr log stream

    Returns:
        A stream to the root log file or stderr stream.
    """
    file_stream = None
    log_stream = None
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            file_stream = handler.stream
        else:
            log_stream = handler.stream

    if file_stream:
        return file_stream
    else:
        return log_stream