# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/logs.py
# Compiled at: 2020-04-17 06:44:40
"""
*Logger setup for python projects*

:Author:
    David Young
"""
from builtins import object
import os, sys, logging
from logging import handlers

def console_logger(level='WARNING'):
    """
    *Setup and return a console logger*

    **Key Arguments**

    - ``level`` -- the level of logging required
    

    **Return**

    - ``logger`` -- the console logger
    

    **Usage**

    ```python
    from fundamentals import logs
    log = logs.console_logger(
        level="DEBUG"
    )
    log.debug("Testing console logger")
    ```
    
    """
    import logging, logging.config, yaml
    try:
        yaml.warnings({'YAMLLoadWarning': False})
    except:
        pass

    loggerConfig = "\n  version: 1\n  formatters:\n      console_style:\n          format: '* %(asctime)s - %(levelname)s: %(pathname)s:%(funcName)s:%(lineno)d > %(message)s'\n          datefmt: '%H:%M:%S'\n  handlers:\n      console:\n          class: logging.StreamHandler\n          level: " + level + '\n          formatter: console_style\n          stream: ext://sys.stdout\n  root:\n      level: ' + level + '\n      handlers: [console]'
    logging.config.dictConfig(yaml.load(loggerConfig))
    logger = logging.getLogger(__name__)
    return logger


def setup_dryx_logging(yaml_file):
    """
    *setup dryx style python logging*

    **Key Arguments**

    - ``level`` -- the level of logging required
    

    **Return**

    - ``logger`` -- the console logger
    

    **Usage**

    ```python
    from fundamentals import logs
    log = logs.setup_dryx_logging(
        yaml_file="/Users/Dave/.config/fundamentals/fundamentals.yaml"
    )
    log.error("test error")
    ```

    Here is an example of the settings in the yaml file:

    ```yaml
    version: 1

    logging settings:
        formatters:
            file_style:
                format: '* %(asctime)s - %(name)s - %(levelname)s (%(pathname)s > %(funcName)s > %(lineno)d) - %(message)s  '
                datefmt: '%Y/%m/%d %H:%M:%S'
            console_style:
                format: '* %(asctime)s - %(levelname)s: %(pathname)s:%(funcName)s:%(lineno)d > %(message)s'
                datefmt: '%H:%M:%S'
            html_style:
                format: '<div id="row" class="%(levelname)s"><span class="date">%(asctime)s</span>   <span class="label">file:</span><span class="filename">%(filename)s</span>   <span class="label">method:</span><span class="funcName">%(funcName)s</span>   <span class="label">line#:</span><span class="lineno">%(lineno)d</span> <span class="pathname">%(pathname)s</span>  <div class="right"><span class="message">%(message)s</span><span class="levelname">%(levelname)s</span></div></div>'
                datefmt: '%Y-%m-%d <span class= "time">%H:%M <span class= "seconds">%Ss</span></span>'
        handlers:
            console:
                class: logging.StreamHandler
                level: DEBUG
                formatter: console_style
                stream: ext://sys.stdout
            file:
                class: logging.handlers.GroupWriteRotatingFileHandler
                level: WARNING
                formatter: file_style
                filename: /Users/Dave/.config/fundamentals/fundamentals.log
                mode: w+
                maxBytes: 102400
                backupCount: 1
        root:
            level: WARNING
            handlers: [file,console]
    ```
    
    """
    import logging, logging.config, yaml
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

    from os.path import expanduser
    handlers.GroupWriteRotatingFileHandler = GroupWriteRotatingFileHandler
    with open(yaml_file) as (f):
        content = f.read()
    home = expanduser('~')
    content = content.replace('~/', home + '/')
    stream = StringIO(content)
    yamlContent = yaml.load(stream)
    stream.close()
    if 'logging settings' in yamlContent:
        yamlContent = yamlContent['logging settings']
        yamlContent['version'] = 1
    if 'handlers' in yamlContent and 'file' in yamlContent['handlers'] and 'filename' in yamlContent['handlers']['file']:
        loggingDir = os.path.dirname(yamlContent['handlers']['file']['filename'])
        if not os.path.exists(loggingDir):
            os.makedirs(loggingDir)
    logging.config.dictConfig(yamlContent)
    logger = logging.getLogger(__name__)
    logging.captureWarnings(True)
    return logger


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    """
    *rotating file handler for logging*
    """

    def doRollover(self):
        """
        *Override base class method to make the new log file group writable.*
        """
        handlers.RotatingFileHandler.doRollover(self)
        currMode = os.stat(self.baseFilename).st_mode
        os.chmod(self.baseFilename, currMode | stat.S_IWGRP | stat.S_IRGRP | stat.S_IWOTH | stat.S_IROTH)


class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
    """
    *rotating file handler for logging*
    """

    def _open(self):
        prevumask = os.umask(0)
        rtv = logging.handlers.RotatingFileHandler._open(self)
        os.umask(prevumask)
        return rtv


class emptyLogger(object):
    """
    *A fake logger object so user can set ``log=False`` if required*

    **Usage**

    ```python
    if log == False:
        from fundamentals.logs import emptyLogger
        log = emptyLogger()
    ```
    
    """

    def info(self, argu):
        pass

    def error(self, argu):
        pass

    def debug(self, argu):
        pass

    def critical(self, argu):
        pass

    def warning(self, argu):
        pass