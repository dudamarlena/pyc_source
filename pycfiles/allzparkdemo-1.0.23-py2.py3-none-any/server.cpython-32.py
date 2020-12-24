# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_mongrel2_server/server.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 23, 2011\n\n@package: ally http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nRuns the Mongrel2 web server.\n'
from ..ally_http import server_host, server_port, server_type, server_version
from ..ally_http.server import assemblyServer
from ally.container import ioc
from threading import Thread

@ioc.config
def workspace_path():
    """
    The workspace path where the uploads can be located, this is basically the mongrel2 workspace path this should not
    include the relative, for example "mongrel2/tmp"
    """
    return 'workspace'


@ioc.config
def send_ident():
    """The send ident to use in communication with Mongrel2, if not specified one will be created"""
    return


@ioc.config
def send_spec():
    """
    The send address to use in communication with Mongrel2, something like:
    "tcp://127.0.0.1:9997" - for using sockets that allow communication between computers
    "ipc:///tmp/send" - for using in processes that allow communication on the same computer processes
    """
    return 'ipc:///tmp/send'


@ioc.config
def recv_ident():
    """The receive ident to use in communication with Mongrel2, if not specified one will be created"""
    return ''


@ioc.config
def recv_spec():
    """The receive address to use in communication with Mongrel2, see more details at "address_request" configuration"""
    return 'ipc:///tmp/response'


ioc.doc(server_type, '\n    "mongrel2" - mongrel2 server integration, Attention!!! this is not a full server the content will be delivered\n                 by Mongrel2 server, so when you set this option please check the README.txt in the component sources\n')
ioc.doc(server_host, '\n    !!!Attention, if the mongrel2 server is selected this option is not used anymore, to change this option you need\n    to alter the Mongrel2 configurations.\n')
ioc.doc(server_port, '\n    !!!Attention, if the mongrel2 server is selected this option is not used anymore, to change this option you need\n    to alter the Mongrel2 configurations.\n')

@ioc.entity
def serverMongrel2RequestHandler():
    from ally.http.server.server_mongrel2 import RequestHandler
    b = RequestHandler()
    yield b
    b.serverVersion = server_version()
    b.assembly = assemblyServer()


@ioc.entity
def serverMongrel2():
    from ally.http.server import server_mongrel2
    b = server_mongrel2.Mongrel2Server()
    b.workspacePath = workspace_path()
    b.sendIdent = send_ident()
    b.sendSpec = send_spec()
    b.recvIdent = recv_ident()
    b.recvSpec = recv_spec()
    b.requestHandler = serverMongrel2RequestHandler()
    return b


@ioc.start
def runServer():
    if server_type() == 'mongrel2':
        from ally.http.server import server_mongrel2
        Thread(target=server_mongrel2.run, args=(serverMongrel2(),)).start()