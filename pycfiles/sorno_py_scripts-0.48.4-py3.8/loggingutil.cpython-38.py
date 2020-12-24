# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/loggingutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 6341 bytes
"""Utilities to work with the standard logging library.

Most of the time, you simply need to do the following in the file containing
your main function (the entry point of your program):

    import logging
    from sorno import loggingutil

    _log = logging.getLogger()  # to get the root logger
    loggingutil.setup_logger(_log)

This sets a reasonable useful format for logging messages. See the doc of the
setup_logger function for more options.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from logging.handlers import TimedRotatingFileHandler
import os, subprocess, sys

def setup_logger(logger, debug=False, stdout=False, log_to_file=None, add_thread_id=False, logging_level=None, use_path=False, suppress_stream_handler_broken_pipe_error=True):
    """Setup a given logger with the parameters given.

    The logger being edited always outputs to stdout or stderr with
    logging.StreamHandler in the standard logging module in additional to
    other handlers.

    Args:
        logger: The standard module logging.Logger instance to be edited
        debug: A boolean. True if the logger should be set to debug level.
            This argument is overridden if a non-None argument is passed to
            the logging_level parameter.
        stdout: A boolean to indicate the logger should use stdout or stderr
            for the logging.StreamHandler
        log_to_file: A filepath for a file being logged to.
            logging.handlers.TimedRotatingFileHandler and a new file is used
            daily with the old file renamed with the date.
        add_thread_id: A boolean. True if the logging format string should
            include the thread id.
        use_path: A boolean. True if the logging format string should use the
            file path name instead of the module name.
        suppress_stream_handler_broken_pipe_error: A boolean. True if
            suppressing the broken pipe error caused by flusing the stream in
            logging.StreamHandler. It's usually because of the output is
            getting piped to the unix "head" command on other commands that
            closes the standard input pipe prematurely.

    Returns:
        Nothing, since the logger is edited in-place.
    """
    if logging_level is None:
        if debug:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO
    formatter = create_logging_formatter(add_thread_id=add_thread_id,
      use_path=use_path)
    hdlr = create_stream_handler(formatter=formatter,
      stdout=stdout,
      suppress_stream_handler_broken_pipe_error=suppress_stream_handler_broken_pipe_error)
    logger.handlers = []
    logger.addHandler(hdlr)
    logger.setLevel(logging_level)
    if log_to_file is not None:
        init_command = 'mkdir -p %s' % os.path.dirname(log_to_file)
        subprocess.check_call(init_command, shell=True)
        hdlr = TimedRotatingFileHandler(log_to_file,
          when='midnight',
          interval=1)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)


def suppress_stream_handler_broken_pipe_error_in_flush(stream_handler):
    old_flush = stream_handler.flush

    def wrapper--- This code section failed: ---

 L. 105         0  SETUP_FINALLY        16  'to 16'

 L. 106         2  LOAD_DEREF               'old_flush'
                4  LOAD_FAST                'args'
                6  LOAD_FAST                'kwargs'
                8  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         72  'to 72'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 107        16  DUP_TOP          
               18  LOAD_GLOBAL              IOError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    70  'to 70'
               24  POP_TOP          
               26  STORE_FAST               'e'
               28  POP_TOP          
               30  SETUP_FINALLY        58  'to 58'

 L. 108        32  LOAD_FAST                'e'
               34  LOAD_ATTR                errno
               36  LOAD_CONST               32
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 109        42  POP_BLOCK        
               44  POP_EXCEPT       
               46  CALL_FINALLY         58  'to 58'
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            40  '40'

 L. 111        52  RAISE_VARARGS_0       0  'reraise'
               54  POP_BLOCK        
               56  BEGIN_FINALLY    
             58_0  COME_FROM            46  '46'
             58_1  COME_FROM_FINALLY    30  '30'
               58  LOAD_CONST               None
               60  STORE_FAST               'e'
               62  DELETE_FAST              'e'
               64  END_FINALLY      
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            22  '22'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            14  '14'

Parse error at or near `POP_EXCEPT' instruction at offset 44

    stream_handler.flush = wrapper


def create_plain_logger(logger_name, debug=False, stdout=True, logging_level=None, suppress_stream_handler_broken_pipe_error=True):
    plain_logger = logging.getLogger(logger_name)
    plain_logger.propagate = False
    if logging_level is None:
        if debug:
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO
    else:
        plain_logger.setLevel(logging_level)
        if stdout:
            out = sys.stdout
        else:
            out = sys.stderr
    formatter = logging.Formatter(fmt='%(message)s',
      datefmt='%Y')
    handler = create_stream_handler(formatter=formatter,
      stdout=stdout,
      suppress_stream_handler_broken_pipe_error=suppress_stream_handler_broken_pipe_error)
    plain_logger.addHandler(handler)
    return plain_logger


def create_logging_formatter(add_thread_id=False, use_path=False):
    format_str = '%(asctime)s'
    if add_thread_id:
        format_str += ' thread:%(thread)s'
    else:
        format_str += ' %(levelname)s '
        if use_path:
            format_str += '%(pathname)s'
        else:
            format_str += '%(name)s'
    format_str += ':%(lineno)s: %(message)s'
    detail_formatter = logging.Formatter(fmt=format_str,
      datefmt='%Y-%m-%d %H:%M:%S')
    return detail_formatter


def create_stream_handler(formatter=None, stdout=False, suppress_stream_handler_broken_pipe_error=True):
    if formatter is None:
        formatter = create_logging_formatter()
    elif stdout:
        stream = sys.stdout
    else:
        stream = sys.stderr
    hdlr = logging.StreamHandler(stream=stream)
    hdlr.setFormatter(formatter)
    if suppress_stream_handler_broken_pipe_error:
        suppress_stream_handler_broken_pipe_error_in_flush(hdlr)
    return hdlr


if __name__ == '__main__':
    plain_stdout_logger = create_plain_logger('plain_logger',
      stdout=True)
    plain_stdout_logger.info('plain stdout logger at info level')
    plain_stdout_logger.debug('should not see this one')
    plain_stdout_debug_logger = create_plain_logger('plain_debug_logger',
      stdout=True,
      debug=True)
    plain_stdout_debug_logger.info('plain stdout debug logger at info level')
    plain_stdout_debug_logger.debug('plain stdout debug logger at debug level')
    plain_stderr_logger = create_plain_logger('plain_stderr_logger',
      stdout=False)
    plain_stderr_logger.info('plain stderr logger at info level')
    plain_stderr_logger.debug('should not see this one')