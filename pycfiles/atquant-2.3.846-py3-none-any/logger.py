# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\2.3BranchA\ToolBox\PythonToolBox\atquant\utils\logger.py
# Compiled at: 2018-08-27 20:45:27
# Size of source mod 2**32: 6874 bytes
import json, logging.config, logging.handlers, os, traceback, atquant
from atquant.utils.user_class import OutputFileManager

class LoggerManager:
    __doc__ = '\n    日志管理器\n    '
    _LoggerManager__default_log = 'atquant'
    _LoggerManager__user_log = 'userlog'
    _LoggerManager__dirname = OutputFileManager.mk_root_sub_dir('Log')
    _LoggerManager__sys_atquant = 'sys_atquant.log'
    _LoggerManager__usr_atquant = 'usr_atquant.log'
    _LoggerManager__DICT_LOG_CONFIG = '\n{\n\t"version": 1,\n\t"formatters": {\n\t\t"simple": {\n\t\t\t"format": "%(asctime)s FuctionName::%(funcName)s - %(lineno)s - %(name)s :: %(levelname)s - %(message)s"\n\t\t}\n\t},\n\t"handlers": {\n\t\t"console_handler": {\n\t\t\t"class": "logging.StreamHandler",\n\t\t\t"level": "DEBUG",\n\t\t\t"formatter": "simple",\n\t\t\t"stream": "ext://sys.stdout"\n\t\t},\n\t\t"sys_handler":{\n\t\t\t"class": "logging.handlers.RotatingFileHandler",\n\t\t\t"level":"DEBUG",\n\t\t\t"formatter": "simple",\n\t\t\t"maxBytes":5242880,\n\t\t\t"backupCount":10\n\t\t},\n\t\t"usr_handler":{\n\t\t\t"class": "logging.handlers.RotatingFileHandler",\n\t\t\t"level":"DEBUG",\n\t\t\t"formatter": "simple",\n\t\t\t"maxBytes":10485760,\n\t\t\t"backupCount":10\n\t\t}\n\t},\n\t"loggers": {\n\t\t"atquant": {\n\t\t\t"level": "DEBUG",\n\t\t\t"handlers": [\n\t\t\t\t"sys_handler"\n\t\t\t],\n\t\t\t"propagate": 0\n\t\t},\n\t\t"userlog": {\n\t\t\t"level": "DEBUG",\n\t\t\t"handlers": [\n\t\t\t\t"usr_handler"\n\t\t\t],\n\t\t\t"propagate": 0\n\t\t}\n\t}\n}\n    '

    @classmethod
    def _load_dict_config(cls):

        def load_dict():
            try:
                mod_template_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), './logging_dict.json'))
                with open(mod_template_path, 'r') as (f):
                    dict_config = json.load(f)
                dict_config['handlers']['sys_handler']['filename'] = os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__sys_atquant)
                dict_config['handlers']['usr_handler']['filename'] = os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__usr_atquant)
            except Exception:
                dict_config = json.loads(cls._LoggerManager__DICT_LOG_CONFIG)
                dict_config['handlers']['sys_handler']['filename'] = os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__sys_atquant)
                dict_config['handlers']['usr_handler']['filename'] = os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__usr_atquant)
                print(traceback.format_exc())

            return dict_config

        dict_config = load_dict()
        return dict_config

    @classmethod
    def _log_config(cls):
        dict_config = cls._load_dict_config()
        logging.config.dictConfig(dict_config)

    @classmethod
    def init_logger(cls):
        cls._log_config()

    @classmethod
    def sys_logger(cls):
        return logging.getLogger(cls._LoggerManager__default_log)

    @classmethod
    def user_logger(cls):
        return logging.getLogger(cls._LoggerManager__user_log)

    @classmethod
    def user_logpath(cls):
        return os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__usr_atquant)

    @classmethod
    def sys_logpath(cls):
        return os.path.join(cls._LoggerManager__dirname, cls._LoggerManager__sys_atquant)

    @classmethod
    def logpath(cls, log_type=None):
        """
        返回log文件的路径,默认返回系统日志路径

        :param log_type: 支持'user','sys' 分别表示用户和系统日志 
        """
        if log_type is not None and log_type == 'user':
            return cls.user_logpath()
        else:
            return cls.sys_logpath()


LoggerManager.init_logger()
logger = LoggerManager.sys_logger()
userlogger = LoggerManager.user_logger()

def write_log(logobj, *args, level='info', console=None):
    """
    真正执行写入日志

    :param logobj: logger对象
    :param args: 日志信息内容
    :param level: 支持'info','debug','warning','warn','error','critical' 
    :param console: 控制台显示的消息，None不显示
    """
    logpath = ''
    if len(args) < 1:
        logpath = ''
    else:
        if logobj is userlogger:
            logpath = LoggerManager.logpath('user')
        else:
            if logobj is logger:
                logpath = LoggerManager.logpath('sys')
            else:
                logpath = ''
            if console is not None:
                print(console, ', see detail log "%s" ' % logpath if logpath else '')
            if logobj is None or len(args) < 1:
                return
            msgs = [str(arg) for arg in args]
            msg = ','.join(msgs)
            if level == 'info':
                logobj.info(msg)
            else:
                if level == 'error':
                    logobj.error(msg)
                else:
                    if level == 'debug':
                        logobj.debug(msg)
                    else:
                        if level == 'warning':
                            logobj.warning(msg)
                        else:
                            if level == 'warn':
                                logobj.warning(msg)
                            else:
                                if level == 'critical':
                                    logobj.critical(msg)
                                else:
                                    logobj.info(msg)


def write_syslog(*args, level='info', trace_debug=False, console=None):
    """
    写入系统日志
    
    :param args: 日志信息内容
    :param level: 支持'info','debug','warning','warn','error','critical' 
    :param trace_debug: 是否启动 atquant.TRACE_DEBUG 变量
    :param console: 控制台显示的消息，None不显示
    """
    if trace_debug:
        if atquant.TRACE_DEBUG:
            write_log(logger, *args, console=console)
        elif console is not None:
            write_log(None, *args, console=console)
    else:
        write_log(logger, *args, console=console)


def write_userlog(*args, level='info', trace_debug=False, console=None):
    """
    写入用户日志

    :param args: 日志信息内容
    :param level: 支持'info','debug','warning','warn','error','critical' 
    :param trace_debug: 是否启动 atquant.TRACE_DEBUG 变量
    :param console: 控制台显示的消息，None不显示
    """
    if trace_debug:
        if atquant.TRACE_DEBUG:
            write_log(userlogger, *args, console=console)
        elif console is not None:
            write_log(None, *args, console=console)
    else:
        write_log(userlogger, *args, console=console)