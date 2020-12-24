# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib_logger.py
# Compiled at: 2018-01-09 12:40:22
import os, sys, logging, multiprocessing

class logger:
    __initialized = False
    __log_identifier = 'log_'
    __log_file_append = True
    __log_file_level = 'info'
    __log_filename = ''
    __level_list = ['debug', 'info', 'warning', 'error']
    __level = 'warning'
    __logger_dict = {}
    __logger_level_dict = {}

    def __init__(self, log_id='log_', log_file_level='info', log_file='', log_file_append=True, level_dict=None, level='warning', multiprocess_flag=False):
        frame = sys._getframe(1)
        module = frame.f_code.co_filename
        module_id = self.__log_identifier + os.path.splitext(os.path.split(module)[1])[0]
        try:
            level_dict[module_id] = level
        except:
            level_dict = {module_id: level}

        if not self.__initialized:
            self.__log_identifier = log_id
            self.__log_file_level = log_file_level
            self.__log_file_append = log_file_append
            self.__log_filename = self._file_log(log_file)
            self._logger_init()
            self.__level = level
            self.__initialized = True
            self._multiprocess_flag = multiprocess_flag
        self._logger_init_level(level_dict)
        self._module_logger(level_dict)

    def _file_log(self, log_file):
        logFolder = '/Documents/testAutoLog/'
        logPathFolder = os.path.expanduser('~') + logFolder
        if not os.path.isdir(os.path.dirname(logPathFolder)):
            os.makedirs(os.path.dirname(logPathFolder))
        if log_file == '':
            log_file = 'autoLog'
        logPathName = logPathFolder + os.path.splitext(os.path.basename(log_file))[0] + '.log'
        return logPathName

    def _logger_init(self):
        self.__log_file_append = True
        self.__log_file_level = self._formatted_level(self.__log_file_level)
        if self.__log_filename != '':
            if not self.__log_file_append:
                filemode = 'w'
                log_append = False
                try:
                    os.remove(self.__log_filename)
                except OSError:
                    pass

            else:
                filemode = 'a'
            FORMAT_BASE = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            logging.basicConfig(level=self.__log_file_level, filename=self.__log_filename, filemode=filemode, format=FORMAT_BASE)

    def _logger_init_level(self, level_dict):
        for module_id in level_dict.keys():
            try:
                level = self.__logger_level_dict[module_id]
                if self.__initialized:
                    continue
            except:
                pass

            if self.__log_identifier not in str(module_id):
                continue
            if level_dict[module_id] not in self.__level_list:
                self.__logger_level_dict[module_id] = self.__level
            else:
                self.__logger_level_dict[module_id] = level_dict[module_id]

    def _module_logger(self, level_dict):
        for module_id in level_dict.keys():
            try:
                level = self.__logger_level_dict[module_id]
                if self.__initialized:
                    continue
            except:
                pass

            self._log_module_init(module_id)

    def _set_logger_level(self, module_id):
        try:
            level = self.__logger_level_dict[module_id]
        except:
            self.__logger_level_dict[module_id] = self.__level
            level = self.__level

        module_list = self.__logger_level_dict.keys()
        if module_id not in module_list:
            return logging.WARNING
        try:
            lower_level = level.lower()
        except:
            return logging.WARNING

        if lower_level not in self.__level_list:
            return logging.WARNING
        fomat_level = self._formatted_level(level)
        return fomat_level

    def _formatted_level(self, level):
        if level.lower() == 'debug':
            return logging.DEBUG
        if level.lower() == 'info':
            return logging.INFO
        if level.lower() == 'error':
            return logging.ERROR
        if level.lower() == 'critical':
            return logging.CRITICAL
        if level.lower() == 'fatal':
            return logging.FATAL
        return logging.WARNING

    def _log_module_init(self, module_id):
        FORMAT_BASE = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        console = logging.StreamHandler()
        formatter = logging.Formatter(FORMAT_BASE)
        console.setFormatter(formatter)
        if self._multiprocess_flag:
            logger = multiprocessing.log_to_stderr()
        else:
            module_name = module_id.replace(self.__log_identifier, '')
            logger = logging.getLogger(module_name)
        logger.addHandler(console)
        logger.setLevel(self._set_logger_level(module_id))
        self.__logger_dict[module_id] = logger
        return logger

    def log(self, level, msg, cr=False, depth=-1):
        frame = sys._getframe(1)
        module = frame.f_code.co_filename
        module_id = self.__log_identifier + os.path.splitext(os.path.split(module)[1])[0]
        try:
            logger = self.__logger_dict[module_id]
        except:
            logger = self._log_module_init(module_id)

        if depth != None:
            msg = self._stack_frame(remove='log', depth=depth, cr=cr) + msg
        if level == 'debug':
            logger.debug(msg)
        elif level == 'info':
            logger.info(msg)
        elif level == 'warning':
            logger.warning(msg)
        elif level == 'error':
            logger.error(msg)
        elif level == 'critical':
            logger.critical(msg)
        elif level == 'fatal':
            logger.fatal(msg)
        return

    def _stack_frame(self, depth=-1, remove=None, cr=False):
        stackFrame = ''
        num = 0
        while True:
            if depth == 0:
                break
            frame = sys._getframe(num)
            method_name = frame.f_code.co_name
            if method_name == '<module>' or method_name == 'run':
                lineno = frame.f_lineno
                launchFile = os.path.splitext(os.path.basename(frame.f_code.co_filename))[0]
                stackFrame = '%s(%d)::' % (launchFile, lineno) + stackFrame
                break
            if frame.f_code.co_name != '_stack_frame' and frame.f_code.co_name != remove:
                lineno = frame.f_lineno
                stackFrame = frame.f_code.co_name + '(%d)::' % lineno + stackFrame
                depth -= 1
            num += 1

        stackFrame = '[' + stackFrame + ']'
        stackFrame += ' '
        if cr:
            stackFrame += '\n   '
        return stackFrame