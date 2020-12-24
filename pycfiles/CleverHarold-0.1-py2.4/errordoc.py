# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/lib/errordoc.py
# Compiled at: 2006-08-02 05:57:51
from harold.lib import con_type
import kid
default_template = '\n<html xmlns:py="http://purl.org/kid/ns">\n    <head>\n        <title>${code} ${message}</title>\n    </head>\n    <body>\n        <h1>${message}</h1>\n        <p>${description}</p>\n        <hr />\n        <b><em>${signature}</em></b>\n    </body>\n</html>\n'

class Error:
    """ Parent for error doc types

    Subclasses must implement a 'description(env)' method.

    Subclasses and instances can override the 'template' attribute,
    and subclasses can override the 'signature(env)' method.
    """
    __module__ = __name__
    template = default_template
    output = 'html'

    def __call__(self, environ, start_response):
        """ renders an error response

        """
        values = dict(code=self.code, message=self.message, description=self.description(environ), signature=self.signature(environ))
        error = kid.Template(self.template, **values)
        headers = [('Content-type', con_type.html)]
        start_response('%(code)s %(message)s' % values, headers)
        return error.serialize(output=self.output)

    def signature(self, env):
        """ signature customized for request
        
        @param env request environment
        @return server signature string
        """
        name = env.get('SERVER_NAME', '')
        port = env.get('SERVER_PORT', 80)
        return 'WSGI (Unix) Server at %s Port %s' % (name, port)


class NotExist(Error):
    """ '400 - Bad Reqeust' error type

    """
    __module__ = __name__
    code = 400
    message = 'Bad Request'
    desc = 'The hostname you requested, %(SERVER_NAME)s, does not exist on this server.'

    def description(self, env):
        """ description customized for request
    
        @param env request environment
        @return error description string
        """
        return self.desc % (env.get('SERVER_NAME'),)


class NotFound(Error):
    """ '404 - Not Found' error type

    """
    __module__ = __name__
    code = 404
    message = 'Not Found'
    desc = 'The requested URL %s was not found on this server.'

    def description(self, env):
        """ description customized for request
    
        @param env request environment
        @return error description string
        """
        return self.desc % (env.get('PATH_INFO'),)