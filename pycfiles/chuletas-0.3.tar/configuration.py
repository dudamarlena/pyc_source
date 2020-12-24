# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: apps/example/webapp/model/configuration.py
# Compiled at: 2011-07-29 03:04:13
import os
from chula import config
app = config.Config()
app.classpath = 'controller'
app.debug = True
app.htdocs = os.path.join(os.path.dirname(__file__), '..', 'www')
app.session = False
if 'CHULA_REGEX_MAPPER' in os.environ:
    app.mapper = (
     ('^$', 'home.index'),
     ('^/home/?$', 'home.index'),
     ('^/home/index/?$', 'home.index'),
     ('^/sample/?$', 'sample.index'),
     ('^/sample/page/?$', 'sample.page'),
     ('^/bad_import/index/?$', 'bad_import.index'),
     ('^/global_exception/index/?$', 'global_exception.index'),
     ('^/syntax_exception/index/?$', 'syntax_exception.index'),
     ('^/runtime_exception/index/?$', 'runtime_exception.index'),
     ('^/webservice/ascii/?$', 'webservice.ascii'),
     ('^/webservice/broken/?$', 'webservice.broken'),
     ('^/webservice/pickle/?$', 'webservice.pickle'),
     ('^/webservice/simple_json/?$', 'webservice.simple_json'),
     ('^/webservice/xjson/?$', 'webservice.xjson'),
     ('^/blog(/(?P<username>[a-z]+))?(/(?P<date>\\d\\d\\d\\d-\\d\\d-\\d\\d))?(/(?P<commens>comments))??/?$',
 'rest.blog'))