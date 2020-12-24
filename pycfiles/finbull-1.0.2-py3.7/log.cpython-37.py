# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangjiangfeng/Documents/IdeaProjects/baidu/bainuo-feed/FinBull/finbull/log.py
# Compiled at: 2019-08-01 06:20:43
# Size of source mod 2**32: 12438 bytes
import six, logging, os, traceback, json, finbull.error
from urllib import parse
LOG_DIR = './logs/'
MODULE = 'app'
FOTMAT = '%(levelname)s: %(asctime)s %(f_module)s [filename=%(f_filename)s lineno=%(f_lineno)d process=%(process)d thread=%(thread)d thread_name=%(threadName)s created=%(created)f msecs=%(msecs)d %(message)s]'
ACCESS_FORMAT = '%(asctime)s %(module)s %(process)d [%(message)s]'
LEVEL_NOTICE = 21
LEVEL_FATAL = 41
logging.addLevelName(LEVEL_NOTICE, 'NOTICE')
logging.addLevelName(LEVEL_FATAL, 'FATAL')
app_log = logging.getLogger('finbull.log.app')
app_log_wf = logging.getLogger('finbull.log.app_wf')
app_service_log = logging.getLogger('finbull.log.app.service')
app_service_log_wf = logging.getLogger('finbull.log.app.service.wf')

def _get_current_trackback():
    """
    get current traceback

    traceback is wrong in the log file.
    so we should find it by myself.
    """
    traces = traceback.extract_stack()
    for i, trace in enumerate(traces):
        if trace[0].endswith('finbull/log.py') or trace[0].endswith('finbull/log.pyc') or trace[0].endswith('finbull/log.pyo'):
            if trace[2] in ('debug', 'notice', 'warning', 'fatal', 'service_debug',
                            'service_notice', 'service_warning', 'service_fatal'):
                return traces[(i - 1)]

    return traces[0]


def _json_parser(v):
    if isinstance(v, (list, dict)):
        return json.dumps(v, default=repr)
    return str(v)


_default_parse = repr

def set_parser(parser):
    """ set parser
    """
    global _default_parse
    _default_parse = parser


class FilenameFilter(logging.Filter):
    __doc__ = 'Summary\n    FilenameFilter\n    '

    def filter(self, record):
        """Summary
        filter
        """
        record.f_filename = os.path.abspath(_get_current_trackback()[0])
        return True


class ModuleFilter(logging.Filter):
    __doc__ = 'Summary\n    ModuleFilter\n    '

    def filter(self, record):
        """Summary
        filter
        """
        record.f_module = _get_current_trackback()[2]
        return True


class LinenoFilter(logging.Filter):
    __doc__ = 'Summary\n    LinenoFilter\n    '

    def filter(self, record):
        """Summary
        filter
        """
        record.f_lineno = _get_current_trackback()[1]
        return True


def init(log_dir=LOG_DIR, module=MODULE, debug=True):
    """Summary
    feed log init.

    Attribute:
        log_dir: log dir
        module: log name
        debug:
    """
    try:
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
    except:
        pass

    if debug is True:
        app_log.setLevel(logging.DEBUG)
        app_log_wf.setLevel(logging.DEBUG)
        app_service_log.setLevel(logging.DEBUG)
        app_service_log_wf.setLevel(logging.DEBUG)
    else:
        app_log.setLevel(logging.INFO)
        app_log_wf.setLevel(logging.WARNING)
        app_service_log.setLevel(logging.INFO)
        app_service_log_wf.setLevel(logging.WARNING)
    formatter = logging.Formatter(FOTMAT)
    filename_filter = FilenameFilter()
    module_filter = ModuleFilter()
    lineno_filter = LinenoFilter()
    app_log_hd = logging.handlers.TimedRotatingFileHandler(log_dir + '/' + module + '.log', 'H', 1, 168)
    app_log_hd.suffix = '%Y%m%d%H'
    app_log_hd.setFormatter(formatter)
    app_log.addHandler(app_log_hd)
    app_log.addFilter(filename_filter)
    app_log.addFilter(module_filter)
    app_log.addFilter(lineno_filter)
    app_log.propagate = False
    app_log_wf_hd = logging.handlers.TimedRotatingFileHandler(log_dir + '/' + module + '.log.wf', 'H', 1, 168)
    app_log_wf_hd.suffix = '%Y%m%d%H'
    app_log_wf_hd.setFormatter(formatter)
    app_log_wf.addHandler(app_log_wf_hd)
    app_log_wf.addFilter(filename_filter)
    app_log_wf.addFilter(module_filter)
    app_log_wf.addFilter(lineno_filter)
    app_log_wf.propagate = False
    app_service_log_hd = logging.handlers.TimedRotatingFileHandler(log_dir + '/' + module + '.service.log', 'H', 1, 168)
    app_service_log_hd.suffix = '%Y%m%d%H'
    app_service_log_hd.setFormatter(formatter)
    app_service_log.addHandler(app_service_log_hd)
    app_service_log.addFilter(filename_filter)
    app_service_log.addFilter(module_filter)
    app_service_log.addFilter(lineno_filter)
    app_service_log.propagate = False
    app_service_log_wf_hd = logging.handlers.TimedRotatingFileHandler(log_dir + '/' + module + '.service.log.wf', 'H', 1, 168)
    app_service_log_wf_hd.suffix = '%Y%m%d%H'
    app_service_log_wf_hd.setFormatter(formatter)
    app_service_log_wf.addHandler(app_service_log_wf_hd)
    app_service_log_wf.addFilter(filename_filter)
    app_service_log_wf.addFilter(module_filter)
    app_service_log_wf.addFilter(lineno_filter)
    app_service_log_wf.propagate = False


def _urlencode(value):
    """Summary
    _urlencode
    """
    return parse.quote_plus(value)


def debug(*args):
    """Summary
    add a DEBUG log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_log.debug('%s=%s' % (args[0], value))
    else:
        if isinstance(args[0], dict):
            app_log.debug(' '.join(['%s=%s' % (key, value) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.debug, parameters error. need str or dict.')


def service_debug(*args):
    """Summary
    add a service DEBUG log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_service_log.debug('%s=%s' % (args[0], _urlencode(str(value))))
    else:
        if isinstance(args[0], dict):
            app_service_log.debug(' '.join(['%s=%s' % (key, _urlencode(str(value))) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.service_debug, parameters error. need str or dict.')


def notice(*args, **kwargs):
    """Summary
    add a NOTICE log
    """
    _parse = kwargs.get('parse_function', _default_parse)
    key, value = ('msg', 'None')
    if len(args) <= 0:
        key, value = ('msg', 'None')
    else:
        if len(args) <= 1:
            if isinstance(args[0], dict):
                app_log.log(LEVEL_NOTICE, ' '.join(['%s=%s' % (k, _parse(v)) for k, v in args[0].items()]))
                return
                key, value = 'msg', args[0]
            else:
                key, value = args[0], args[1]
        elif isinstance(value, six.string_types):
            app_log.log(LEVEL_NOTICE, '%s=%s' % (key, value))
        else:
            if isinstance(value, (list, dict)):
                app_log.log(LEVEL_NOTICE, '%s=%s' % (key, _parse(value)))
            else:
                raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
                  errmsg='can not call log.notice, parameters error. need str or dict.')


def service_notice(*args):
    """Summary
    add a service NOTICE log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_service_log.log(LEVEL_NOTICE, '%s=%s' % (args[0], _urlencode(str(value))))
    else:
        if isinstance(args[0], dict):
            app_service_log.log(LEVEL_NOTICE, ' '.join(['%s=%s' % (key, _urlencode(str(value))) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.notice, parameters error. need str or dict.')


def warning(*args):
    """Summary
    add a WARNING log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_log_wf.warning('%s=%s' % (args[0], value))
    else:
        if isinstance(args[0], dict):
            app_log_wf.warning(' '.join(['%s=%s' % (key, value) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.warning, parameters error. need str or dict.')


def service_warning(*args):
    """Summary
    add a service WARNING log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_service_log_wf.warning('%s=%s' % (args[0], _urlencode(str(value))))
    else:
        if isinstance(args[0], dict):
            app_service_log_wf.warning(' '.join(['%s=%s' % (key, _urlencode(str(value))) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.warning, parameters error. need str or dict.')


def fatal(*args):
    """Summary
    add a FATAL log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_log_wf.log(LEVEL_FATAL, '%s=%s' % (args[0], value))
    else:
        if isinstance(args[0], dict):
            app_log_wf.log(LEVEL_FATAL, ' '.join(['%s=%s' % (key, value) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.fatal, parameters error. need str or dict.')


def service_fatal(*args):
    """Summary
    add a service FATAL log
    """
    if isinstance(args[0], six.string_types):
        value = 'None' if len(args) <= 1 else args[1]
        app_service_log_wf.log(LEVEL_FATAL, '%s=%s' % (args[0], _urlencode(str(value))))
    else:
        if isinstance(args[0], dict):
            app_service_log_wf.log(LEVEL_FATAL, ' '.join(['%s=%s' % (key, _urlencode(str(value))) for key, value in args[0].items()]))
        else:
            raise finbull.error.BaseError(errno=(finbull.error.ERRNO_FRAMEWORK),
              errmsg='can not call log.fatal, parameters error. need str or dict.')


if __name__ == '__main__':
    import tornado.web, tornado.ioloop
    from tornado.httpclient import AsyncHTTPClient
    init()

    class MainHandler(tornado.web.RequestHandler):
        __doc__ = 'Summary\n        MainHandler\n        '

        def get(self):
            """Summary

            Returns:
                TYPE: Description
            """
            notice('port', 'start 8999')
            notice('aaa', 'bbfdl;akr3i2u53214%#&^%&^%#$@Wgfdlk                sjf红额外哦IQ缴费机啊街坊大姐唉算了；就发')
            warning('get_error_func', 'fdaljfda辅导课辣椒水放假的撒娇 ')
            fatal('get_user_info', 'failed to get user infomation')
            notice('fdafda', '地方大快速链接++++')
            notice({'a':'b',  'c':'d'})
            self.write('Hello, world')


    app = tornado.web.Application([
     (
      '/', MainHandler)])
    app.listen(8999)
    tornado.ioloop.IOLoop.current().run_sync(lambda : AsyncHTTPClient().fetch('http://localhost:8999/',
      follow_redirects=False, raise_error=False))
    tornado.ioloop.IOLoop.current().run_sync(lambda : AsyncHTTPClient().fetch('http://localhost:8999/',
      follow_redirects=False, raise_error=False))