# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/jsonrpc.py
# Compiled at: 2011-10-27 22:20:43
from TutorialBase import *

class jsonrpc(HTMLPage):
    """Using JSON-RPC with servlets."""
    title = 'JSON-RPC'
    meta = {'pygwt:module': '/jsonrpc_js/jsonrpc_cli'}
    css = '\n    div#floatbox {\n        float: right;\n        width: 40%;\n        margin: 20px;\n        border: solid black 3px;\n        padding: 20px;               \n    }\n\n    div#quotebox {\n        margin-top: 10px;\n        border-top: solid black 1px;\n    }\n    '

    def write_content(self):
        self.writeln(FLOATBOX)
        self.writeln(OVERVIEW)
        self.writeln(SCRIPT)


FLOATBOX = '\n<div id="floatbox">\n    Shakespeare Quotes:\n    <div id="quotebox">\n    </div>\n</div>'
OVERVIEW = make_overview("\n\n[JSON-RPC](http://groups.google.com/group/json-rpc/web/json-rpc-2-0)\nis a remote procecure call protocol using [JSON](http://www.json.org)\nfor encoding messages between client and server.\n\nThis servlet demonstrates communicating with a server that hands out\nfamous quotes from William Shakespeare's plays and sonnets.  Every\nfive seconds a new quote is fetched from the server, placed somewhere\nrandomly in the box to the right and then fades away.  If you view the\nweb log from running this tutorial you will see repeated POST requests\nfor URI **/jsonrpc_srv**.\n\n\nIf you view the source of this servlet you will not see much code: all\nthis servlet does is serve static javascript that was previously\ncompiled from python source to javascript using the python=>javascript\ncompiler technology, pyjamas[^1].\n\n\nThe pyjamas application is loaded into the box to the right (a floated\n`DIV` element) by loading javascript bootstrap code (which you can see\nby viewing the tail end of this source).  It should be made clear that\nthe client-side of JSON-RPC is NOT provided by WSGIServlets[^2].\n\nThis is important to understand: *Only the server-side is provided by\nWSGIServlets!*\n\nThe server code, in a nutshell, is:\n\n\n        import random\n        from wsgiservlets import JSONRPCServer\n\n        class jsonrpc_srv(JSONRPCServer):\n\n            def rpc_quote(self):\n                play = random.choice(PLAYS)\n                quote = random.choice(QUOTES[play])\n                return quote, play\n\n\nwhere `PLAYS` is a list of play/sonnet titles and `QUOTES` is a\nmapping of titles to a list of quotes from that play.\n\nYou will notice the servlet is an instance of `JSONRPCServer`.  This\nis a subclass of `WSGIServlet`.  Any method with prefix `rpc_` is\navailable to be called by a client (which should call the method\nwithout the `rpc_` prefix, e.g., in this demo, the client is calling\n`quote`, not `rpc_quote`).  Any method not prefixed with `rpc_` is NOT\navailable to clients and becomes a *private* method of the server\nimplementation.\n\nSo, to create a JSON-RPC server with WSGIServlets, subclass\n`JSONRPCServer` and create methods with names beginning with `rpc_`.\nYour methods can take as input and return as output any python object\nthat can be translated to JSON.  That's it!\n\n\n\n[^1]:\n    Discussing pyjamas is beyond the scope of this tutorial.\n    Suffice it to say that pyjamas turns traditional web programming\n    into something more akin to desktop GUI programming.  Pyjamas\n    exposes the DOM to python, thus when the python is compiled to\n    javascript and then loaded into a broswer, you discover you can\n    manipulate a browser window with python code.  [Check it\n    out](http://pyjs.org).\n\n[^2]:\n\n    The author of this tutorial pre-compiled the pyjamas app and\n    included the resulting static javascript in the distribution.  The\n    original source for the application is also included in the\n    distribution (and is well documented for the curious), but\n    discussion of client-side JSON-RPC, generally, or pyjamas\n    application programming, specifically, is beyond the scope of this\n    tutorial.\n\n")
SCRIPT = '<script language="javascript" src="/jsonrpc_js/bootstrap.js"></script>'