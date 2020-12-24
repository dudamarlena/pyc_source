# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/application.py
# Compiled at: 2009-01-14 10:36:41


class Root:
    pass


root = Root()

def process_url(path):
    obj = root
    for name in path:
        registrations = queryAdapter(IRegistrations, obj)
        if registrations:
            registrations.register()
        traverser = ITraverser(obj)
        path.pop(0)
        obj = traverser.traverse(obj, path)
        assert IContent.providedBy(obj)

    result = IView(obj)()
    assert isinstance(view, unicode)
    return result.encode('utf-8')


class Application:

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response('Hello %s!' % req.params.get('name', 'World'))
        return resp(environ, start_response)


app = Application()