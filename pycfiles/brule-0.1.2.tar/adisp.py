# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/brukva/adisp.py
# Compiled at: 2011-02-09 16:59:17
__doc__ = '\nAdisp is a library that allows structuring code with asynchronous calls and\ncallbacks without defining callbacks as separate functions. The code then\nbecomes sequential and easy to read. The library is not a framework by itself\nand can be used in other environments that provides asynchronous working model\n(see an example with Tornado server in proxy_example.py).\n\nUsage:\n\n## Organizing calling code\n\nAll the magic is done with Python 2.5 decorators that allow for control flow to\nleave a function, do sometihing else for some time and then return into the\ncalling function with a result. So the function that makes asynchronous calls\nshould look like this:\n\n    @process\n    def my_handler():\n        response = yield some_async_func()\n        data = parse_response(response)\n        result = yield some_other_async_func(data)\n        store_result(result)\n\nEach `yield` is where the function returns and lets the framework around it to\ndo its job. And the code after `yield` is what usually goes in a callback.\n\nThe @process decorator is needed around such a function. It makes it callable\nas an ordinary function and takes care of dispatching callback calls back into\nit.\n\n## Writing asynchronous function\n\nIn the example above functions "some_async_func" and "some_other_async_func"\nare those that actually run an asynchronous process. They should follow two\nconditions:\n\n- accept a "callback" parameter with a callback function that they should call\n  after an asynchronous process is finished\n- a callback should be called with one parameter -- the result\n- be wrapped in the @async decorator\n\nThe @async decorator makes a function call lazy allowing the @process that\ncalls it to provide a callback to call.\n\nUsing async with @-syntax is most convenient when you write your own\nasynchronous function (and can make your callback parameter to be named\n"callback"). But when you want to call some library function you can wrap it in\nasync in place.\n\n    # call http.fetch(url, callback=callback)\n    result = yield async(http.fetch)\n\n    # call http.fetch(url, cb=safewrap(callback))\n    result = yield async(http.fetch, cbname=\'cb\', cbwrapper=safewrap)(url)\n\nHere you can use two optional parameters for async:\n\n- `cbname`: a name of a parameter in which the function expects callbacks\n- `cbwrapper`: a wrapper for the callback iself that will be applied before\n  calling it\n\n## Chain calls\n\n@async function can also be @process\'es allowing to effectively chain\nasynchronous calls as it can be done with normal functions. In this case the\n@async decorator shuold be the outer one:\n\n    @async\n    @process\n    def async_calling_other_asyncs(arg, callback):\n        # ....\n\n## Multiple asynchronous calls\n\nThe library also allows to call multiple asynchronous functions in parallel and\nget all their result for processing at once:\n\n    @async\n    def async_http_get(url, callback):\n        # get url asynchronously\n        # call callback(response) at the end\n\n    @process\n    def get_stat():\n        urls = [\'http://.../\', \'http://.../\', ... ]\n        responses = yield map(async_http_get, urls)\n\nAfter *all* the asynchronous calls will complete `responses` will be a list of\nresponses corresponding to given urls.\n'
from functools import partial

class CallbackDispatcher(object):

    def __init__(self, generator):
        self.g = generator
        try:
            self.call(self.g.next())
        except StopIteration:
            pass

    def _send_result(self, results, single):
        try:
            result = results[0] if single else results
            self.call(self.g.send(result))
        except StopIteration:
            pass

    def call(self, callers):
        single = not hasattr(callers, '__iter__')
        if single:
            callers = [
             callers]
        self.call_count = len(list(callers))
        results = [None] * self.call_count
        if self.call_count == 0:
            self._send_result(results, single)
        for (count, caller) in enumerate(callers):
            caller(callback=partial(self.callback, results, count, single))

        return

    def callback(self, results, index, single, arg):
        self.call_count -= 1
        results[index] = arg
        if self.call_count > 0:
            return
        self._send_result(results, single)


def process(func):

    def wrapper(*args, **kwargs):
        CallbackDispatcher(func(*args, **kwargs))

    return wrapper


def async(func, cbname='callback', cbwrapper=lambda x: x):

    def wrapper(*args, **kwargs):

        def caller(callback):
            kwargs[cbname] = cbwrapper(callback)
            return func(*args, **kwargs)

        return caller

    return wrapper