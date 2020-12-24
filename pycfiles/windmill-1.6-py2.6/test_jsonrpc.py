# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_wsgi_jsonrpc/test_jsonrpc.py
# Compiled at: 2011-01-13 01:48:00


def make_server(host='localhost', port=4325):
    from wsgiref import simple_server
    from windmill.dep import wsgi_jsonrpc

    class Methods(object):

        def test_1(self):
            return 'test_1'

        def test_2(self, value):
            return value

    methods = Methods()

    def test_3():
        return 'test3'

    application = wsgi_jsonrpc.WSGIJSONRPCApplication(instance=methods, methods=[test_3])
    return simple_server.make_server(host, port, application)


def test_jsonrpc_server(uri='http://localhost:4325/'):
    from windmill.dep import wsgi_jsonrpc
    json_tools = wsgi_jsonrpc.json_tools
    jsonrpc_client = json_tools.ServerProxy(uri=uri)
    assert jsonrpc_client.test_1() == {'result': 'test_1'}
    assert jsonrpc_client.test_2({'test': 4}) == {'result': {'test': 4}}
    assert jsonrpc_client.test_3() == {'result': 'test3'}


if __name__ == '__main__':
    import sys
    from threading import Thread
    run = True
    try:
        server = make_server()

        def test_wrapper():
            test_jsonrpc_server()
            run = False
            sys.exit()


        thread = Thread(target=test_wrapper)
        thread.start()
        while run:
            server.handle_request()

        sys.exit()
    except KeyboardInterrupt:
        sys.exit()