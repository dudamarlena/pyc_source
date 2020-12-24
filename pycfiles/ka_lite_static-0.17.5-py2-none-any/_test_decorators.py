# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/test/_test_decorators.py
# Compiled at: 2018-07-11 18:15:31
"""Test module for the @-decorator syntax, which is version-specific"""
from cherrypy import expose, tools
from cherrypy._cpcompat import ntob

class ExposeExamples(object):

    @expose
    def no_call(self):
        return 'Mr E. R. Bradshaw'

    @expose()
    def call_empty(self):
        return 'Mrs. B.J. Smegma'

    @expose('call_alias')
    def nesbitt(self):
        return 'Mr Nesbitt'

    @expose(['alias1', 'alias2'])
    def andrews(self):
        return 'Mr Ken Andrews'

    @expose(alias='alias3')
    def watson(self):
        return 'Mr. and Mrs. Watson'


class ToolExamples(object):

    @expose
    @tools.response_headers(headers=[('Content-Type', 'application/data')])
    def blah(self):
        yield ntob('blah')

    blah._cp_config['response.stream'] = True