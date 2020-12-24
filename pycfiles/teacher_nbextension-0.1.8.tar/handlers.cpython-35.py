# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/i/LABS/teacher_nbextension/teacher_nbextension/handlers.py
# Compiled at: 2018-05-24 13:24:26
# Size of source mod 2**32: 2236 bytes
import json, logging, logging.config, os
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join
logger = logging.getLogger(__name__)
logging.config.dictConfig({'version': 1, 
 'disable_existing_loggers': False, 
 'formatters': {'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}}, 
 
 'handlers': {'default': {'level': 'INFO', 
                          'class': 'logging.StreamHandler'}, 
              
              'file': {'level': 'DEBUG', 
                       'class': 'logging.FileHandler', 
                       'filename': os.path.join(os.path.expanduser('~'), 'jupyter.log')}, 
              
              'logstash': {'level': 'DEBUG', 
                           'class': 'logstash.LogstashHandler', 
                           'host': 'localhost', 
                           'port': 5959, 
                           'version': 1, 
                           'message_type': 'logstash'}}, 
 
 'loggers': {'': {'handlers': ['default', 'file', 'logstash'], 
                  'level': 'DEBUG', 
                  'propagate': True}}})

class ExecuteHandler(IPythonHandler):

    def get(self):
        self.finish(json.dumps({'response': 'ok'}))

    def post(self):
        data = self.request.body_arguments
        formatted = {}
        for k, v in data.items():
            formatted[k] = v
            try:
                v = v[0].decode()
                formatted[k] = v
            except:
                pass

        logger.info(formatted)
        self.finish(json.dumps({'log': 'ok'}))


def load_jupyter_server_extension(nb_app):
    nb_app.log.info('Loading the teacher_nbextension serverextension')
    web_app = nb_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/execute')
    web_app.add_handlers(host_pattern, [(route_pattern, ExecuteHandler)])