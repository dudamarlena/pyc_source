# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vxUtils/logger.py
# Compiled at: 2017-05-08 10:53:30
# Size of source mod 2**32: 9706 bytes
"""
author: vex1023
email: vex1023@qq.com

各种各样的LOGGER 函数
"""
import logging, sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from multiprocessing.pool import ThreadPool as Pool
import six
try:
    import curses
    assert curses
except ImportError:
    curses = None

__all__ = ['endable_console_logger', 'enable_logfile', 'enable_qywechat_logger']
_DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] === %(message)s'

class _LogFormatter(logging.Formatter):

    def __init__(self, color, log_format=None, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        if log_format:
            self._log_format = log_format
        else:
            self._log_format = _DEFAULT_LOG_FORMAT
        self._color = color
        if color:
            fg_color = curses.tigetstr('setaf') or curses.tigetstr('setf') or ''
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = six.text_type(fg_color, 'ascii')
            self._colors = {logging.DEBUG: six.text_type(curses.tparm(fg_color, 4), 'ascii'), 
             logging.INFO: six.text_type(curses.tparm(fg_color, 2), 'ascii'), 
             logging.WARNING: six.text_type(curses.tparm(fg_color, 3), 'ascii'), 
             logging.ERROR: six.text_type(curses.tparm(fg_color, 5), 'ascii'), 
             logging.CRITICAL: six.text_type(curses.tparm(fg_color, 1), 'ascii')}
            self._normal = six.text_type(curses.tigetstr('sgr0'), 'ascii')

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = 'Bad message (%r): %r' % (e, record.__dict__)

        record.asctime = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
        formatted = self._log_format % record.__dict__
        if self._color:
            formatted = self._colors.get(record.levelno, self._normal) + formatted + self._normal
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            formatted = formatted.rstrip() + '\n' + record.exc_text
        return formatted.replace('\n', '\n    ')


class qyWeChatLoggerHandler(logging.Handler):

    def __init__(self, corpid, appsecret, agentid=0, user_ids=[], tag_ids=[], party_ids=[], msgtype='text'):
        from wechatpy.enterprise.client import WeChatClient as qyWechatClient
        self._client = qyWechatClient(corp_id=corpid, secret=appsecret)
        self._agent_id = agentid
        if len(user_ids) == 0:
            self._user_ids = '@all'
        else:
            self._user_ids = user_ids
        self._tag_ids = tag_ids
        self._party_ids = party_ids
        self._msgtype = msgtype
        self._pool = Pool(5)
        super(qyWeChatLoggerHandler, self).__init__()

    def emit(self, record):
        msg = self.format(record)
        try:
            if self._msgtype == 'text':
                self._pool.apply_async(func=self._client.message.send_text, kwds={'agent_id': self._agent_id, 
                 'user_ids': self._user_ids, 
                 'content': msg, 
                 'party_ids': self._party_ids, 
                 'tag_ids': self._tag_ids})
            else:
                self._pool.apply_async(func=self._client.message.send_articles, kwds={'agent_id': self._agent_id, 
                 'user_ids': self._user_ids, 
                 'articles': msg, 
                 'party_ids': self._party_ids, 
                 'tag_ids': self._tag_ids})
        except Exception as err:
            print(err)

    def format(self, record):
        if self._msgtype == 'text':
            record.asctime = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            msg = '%(asctime)s\n%(msg)s\n---- [%(filename)s] ----' % record.__dict__
        else:
            record.asctime = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
            msg = [
             {'title': '[%(levelname)s]' % record.__dict__, 
              'description': '%(asctime)s %(filename)s %(lineno)d:\n%(msg)s' % record.__dict__, 
              'url': '', 
              'image': ''}]
        return msg

    def __delete__(self, instance):
        self._pool.join()


def endable_console_logger(logger, level='info'):
    """
    增加console作为日志输入.
    """
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    logger.setLevel(getattr(logging, level.upper()))
    if not logger.handlers:
        color = False
        if curses:
            if sys.stderr.isatty():
                try:
                    curses.setupterm()
                    if curses.tigetnum('colors') > 0:
                        color = True
                except:
                    pass

        console = logging.StreamHandler()
        console.setFormatter(_LogFormatter(color=color))
        logger.addHandler(console)
    return logger


def enable_logfile(logger, logfile, level='info'):
    """

    :param logger: 日志
    :param logfile: 日志文件路径
    :param level: 日志等级
    :return:
    """
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    Formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    Rthandler = RotatingFileHandler(logfile, maxBytes=5242880, backupCount=7)
    Rthandler.setFormatter(Formatter)
    Rthandler.setLevel(level.upper())
    logger.addHandler(Rthandler)
    return logger


def enable_qywechat_logger(logger, corpid, appsecret, agentid=0, user_ids=[], tag_ids=[], party_ids=[], msgtype='text', level='warning'):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    qyhandler = qyWeChatLoggerHandler(corpid=corpid, appsecret=appsecret, agentid=agentid, user_ids=user_ids, tag_ids=tag_ids, party_ids=party_ids, msgtype=msgtype)
    qyhandler.setLevel(getattr(logging, level.upper()))
    logger.addHandler(qyhandler)
    return logger


class vxLogger:

    def __init__(self, logger='', level='INFO', logfile=None):
        if isinstance(logger, str):
            self._logger = logging.getLogger(logger)
        self._logger.setLevel(getattr(logging, level.upper()))
        if not self._logger.handlers:
            color = False
            if curses:
                if sys.stderr.isatty():
                    try:
                        curses.setupterm()
                        if curses.tigetnum('colors') > 0:
                            color = True
                    except:
                        pass

            console = logging.StreamHandler()
            console.setFormatter(_LogFormatter(color=color))
            self._logger.addHandler(console)
        if logfile:
            self.setLogFile(logfile, level=level)

    def setLogFile(self, logfile, level='INFO'):
        """
        设置日志文档
        :param logfile: 日志文件 
        :return: 
        """
        Formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
        Rthandler = RotatingFileHandler(logfile, maxBytes=5242880, backupCount=7)
        Rthandler.setFormatter(Formatter)
        Rthandler.setLevel(getattr(logging, level.upper()))
        self._logger.addHandler(Rthandler)

    def setQYWXNotifle(self, level, corpid, appsecret, agentid, user_ids=[], tag_ids=[], party_ids=[], msgtype='text'):
        """
        设置企业微信通知
        :param level: 
        :param corpid: 
        :param appsecret: 
        :param agentid: 
        :param user_ids: 
        :param tag_ids: 
        :param party_ids: 
        :param msgtype: 
        :return: 
        """
        qyhandler = qyWeChatLoggerHandler(corpid=corpid, appsecret=appsecret, agentid=agentid, user_ids=user_ids, tag_ids=tag_ids, party_ids=party_ids, msgtype=msgtype)
        qyhandler.setLevel(getattr(logging, level.upper()))
        self._logger.addHandler(qyhandler)

    def __getattr__(self, item):
        return self._logger.__getattribute__(item)