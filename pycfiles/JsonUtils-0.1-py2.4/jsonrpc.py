# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jsonutils/jsonrpc.py
# Compiled at: 2006-09-18 22:08:38
__version__ = '1.0'
import json, cgi, re, sys
textTemplate = 'Content-Type: text/plain\n\n%(content)s'
NameAllowedRegExp = re.compile('^[a-zA-Z]\\w*$')

def nameAllowed(name):
    """checks if a name is allowed.
        """
    if NameAllowedRegExp.match(name):
        return True
    else:
        return False


def getTracebackStr():
    import traceback, StringIO
    s = StringIO.StringIO('')
    traceback.print_exc(file=s)
    return s.getvalue()


class JSONRPCError:
    __module__ = __name__

    def __init__(self, msg=''):
        self.name = self.__class__.__name__
        self.msg = msg


class InvalidJsonRpcRequest(JSONRPCError):
    __module__ = __name__


class InvalidMethodParameters(JSONRPCError):
    __module__ = __name__


class MethodNotFound(JSONRPCError):
    __module__ = __name__


class ApplicationError(JSONRPCError):
    __module__ = __name__


class JsonRpcHandler:
    __module__ = __name__

    def __init__(self, services=None):
        """Create RPC request/response handler for authorized methods listed in dictionary 'services'"""
        self.services = services or {}

    def getMethodByName(self, name):
        """searches for an object with the name given inside the object given.
                        "obj.child.meth" will return the meth obj.
                """
        try:
            method = self.services._getMethodByName(name)
        except:
            for meth in self.services:
                if nameAllowed(name):
                    method = self.services[name]

        return method

    def sendResponse(self, id, result, error):
        response = json.write({'id': id, 'result': result, 'error': error})
        print textTemplate % {'content': response}

    def handleJsonRpc(self):
        fields = cgi.FieldStorage()
        request = fields.getfirst('request')
        try:
            if request == None:
                raise InvalidJsonRpcRequest
            req = json.read(request)
            id = req['id']
            params = req['params']
            methodname = req['method']
        except:
            self.sendResponse(None, None, InvalidJsonRpcRequest('Empty or malformed JSON-RPC request.').__dict__)
            return ()

        try:
            method = self.getMethodByName(methodname)
        except:
            method = None
            self.sendResponse(id, None, MethodNotFound(req['method']).__dict__)
            return ()

        if method:
            try:
                result = method(*params)
                if id is not None:
                    self.sendResponse(id, result, None)
                    return ()
            except SystemExit:
                pass
            except:
                s = getTracebackStr()
                self.sendResponse(id, None, ApplicationError(s).__dict__)
                return ()

        return


if __name__ == '__main__':
    jsontxt = 'request={\n\t\t"method": "foo",\n\t\t"params": ["spam", 321],\n\t\t"id": 1234\n\t}'
    if len(sys.argv) < 2:
        sys.argv.append(jsontxt)

    def foo(*args):
        return args


    services = {'foo': foo}
    myJson = JsonRpcHandler(services)
    myJson.handleJsonRpc()