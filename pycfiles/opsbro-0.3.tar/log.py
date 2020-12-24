# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/opsbro-oss/opsbro/log.py
# Compiled at: 2017-08-30 04:15:38
import os, sys, time, datetime, logging, json
from opsbro.misc.colorama import init as init_colorama

def is_tty():
    if hasattr(sys.stdout, 'isatty'):
        return sys.stdout.isatty()
    return False


if is_tty():
    try:
        from opsbro.misc.termcolor import cprint, sprintf
        init_colorama()
    except (SyntaxError, ImportError) as exp:

        def cprint(s, color='', end='\n'):
            if end == '':
                print s,
            else:
                print s


        def sprintf(s, color='', end=''):
            return s


else:
    import codecs
    stdout_utf8 = codecs.getwriter('utf-8')(sys.stdout)

    def cprint(s, color='', end='\n'):
        if not isinstance(s, basestring):
            s = str(s)
        if end == '':
            stdout_utf8.write(s)
        else:
            stdout_utf8.write(s)
            stdout_utf8.write('\n')


    def sprintf(s, color='', end=''):
        return s


def get_unicode_string(s):
    if isinstance(s, str):
        return unicode(s, 'utf8', errors='ignore')
    return str(s)


loggers = {}

class Logger(object):

    def __init__(self):
        self.data_dir = ''
        self.log_file = None
        self.name = ''
        self.logs = {}
        self.registered_parts = {}
        self.level = logging.INFO
        self.is_force_level = False
        self.linkify_methods()
        self.last_errors_stack_size = 20
        self.last_errors_stack = {'DEBUG': [], 'WARNING': [], 'INFO': [], 'ERROR': []}
        self.last_date_print_time = 0
        self.last_date_print_value = ''
        return

    def register_part(self, pname):
        self.registered_parts[pname] = {'enabled': True}

    def linkify_methods(self):
        methods = {'DEBUG': self.do_debug, 'WARNING': self.do_warning, 'INFO': self.do_info, 'ERROR': self.do_error}
        for s, m in methods.iteritems():
            level = getattr(logging, s)
            if level >= self.level:
                setattr(self, s.lower(), m)
            else:
                setattr(self, s.lower(), self.do_null)

    def load(self, data_dir, name):
        self.name = name
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        self.log_file = open(os.path.join(self.data_dir, 'daemon.log'), 'a')

    def setLevel(self, s, force=False):
        if not force and self.is_force_level:
            return
        if force:
            self.is_force_level = True
        try:
            level = getattr(logging, s.upper())
            if not isinstance(level, int):
                raise AttributeError
            self.level = level
        except AttributeError:
            self.error('Invalid logging level configuration %s' % s)
            return

        self.linkify_methods()

    def get_errors(self):
        return self.last_errors_stack

    def __get_time_display(self):
        now = int(time.time())
        if now == self.last_date_print_time:
            return self.last_date_print_value
        self.last_date_print_value = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        return self.last_date_print_value

    def log(self, *args, **kwargs):
        part = kwargs.get('part', '')
        s_part = '' if not part else '[%s]' % part.upper()
        d_display = self.__get_time_display()
        s = '[%s][%s][%s] %s: %s' % (d_display, kwargs.get('level', 'UNSET  '), self.name, s_part, (' ').join([ get_unicode_string(s) for s in args ]))
        if 'color' in kwargs:
            cprint(s, color=kwargs['color'])
        else:
            print s
        stack = kwargs.get('stack', False)
        if stack:
            self.last_errors_stack[stack].append(s)
            self.last_errors_stack[stack] = self.last_errors_stack[stack][-self.last_errors_stack_size:]
        if self.data_dir == '':
            return
        else:
            s = s + '\n'
            f = None
            if part == '':
                if self.log_file is not None:
                    self.log_file.write(s)
            else:
                f = self.logs.get(part, None)
                if f is None:
                    f = open(os.path.join(self.data_dir, '%s.log' % part), 'a')
                    self.logs[part] = f
                f.write(s)
                f.flush()
            listener = kwargs.get('listener', '')
            if listener and hasattr(os, 'O_NONBLOCK') and f is not None:
                try:
                    fd = os.open(listener, os.O_WRONLY | os.O_NONBLOCK)
                    os.write(fd, s)
                    os.close(fd)
                except Exception as exp:
                    s = 'ERROR LISTERNER %s' % exp
                    f.write(s)

            return

    def do_debug(self, *args, **kwargs):
        self.log(level='DEBUG', color='magenta', *args, **kwargs)

    def do_info(self, *args, **kwargs):
        self.log(level='INFO', color='blue', *args, **kwargs)

    def do_warning(self, *args, **kwargs):
        self.log(level='WARNING', color='yellow', stack='WARNING', *args, **kwargs)

    def do_error(self, *args, **kwargs):
        self.log(level='ERROR', color='red', stack='ERROR', *args, **kwargs)

    def do_null(self, *args, **kwargs):
        pass

    def export_http(self):
        from opsbro.httpdaemon import http_export, response

        @http_export('/log/parts/')
        def list_parts():
            response.content_type = 'application/json'
            return json.dumps(loggers.keys())


logger = Logger()

class PartLogger(object):

    def __init__(self, part):
        self.part = part
        self.listener_path = '/tmp/opsbro-follow-%s' % part

    def debug(self, *args, **kwargs):
        kwargs['part'] = kwargs.get('part', self.part)
        if os.path.exists(self.listener_path):
            kwargs['listener'] = self.listener_path
            kwargs['level'] = 'DEBUG  '
            logger.log(color='magenta', *args, **kwargs)
            return
        logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        kwargs['part'] = kwargs.get('part', self.part)
        if os.path.exists(self.listener_path):
            kwargs['listener'] = self.listener_path
            kwargs['level'] = 'INFO   '
            logger.log(color='blue', *args, **kwargs)
            return
        logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        kwargs['part'] = kwargs.get('part', self.part)
        if os.path.exists(self.listener_path):
            kwargs['listener'] = self.listener_path
            kwargs['level'] = 'WARNING'
            logger.log(color='yellow', *args, **kwargs)
            return
        logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        kwargs['part'] = kwargs.get('part', self.part)
        if os.path.exists(self.listener_path):
            kwargs['listener'] = self.listener_path
            kwargs['level'] = 'ERROR  '
            logger.log(color='red', *args, **kwargs)
            return
        logger.error(*args, **kwargs)

    def log(self, *args, **kwargs):
        kwargs['part'] = kwargs.get('part', self.part)
        if os.path.exists(self.listener_path):
            kwargs['listener'] = self.listener_path
            logger.log(*args, **kwargs)
            return
        logger.log(*args, **kwargs)


class LoggerFactory(object):

    @classmethod
    def create_logger(cls, part):
        if part in loggers:
            return loggers[part]
        loggers[part] = PartLogger(part)
        return loggers[part]