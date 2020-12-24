# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gwik/dev/geventhttpclient/src/geventhttpclient/tests/test_no_module_ssl.py
# Compiled at: 2016-07-05 05:26:31
# Size of source mod 2**32: 1095 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, pytest, gevent, gevent.ssl

class DisableSSL(object):

    def __enter__(self):
        self._modules = dict()
        self._modules['ssl'] = sys.modules.pop('ssl', None)
        sys.modules['ssl'] = None
        for module_name in [k for k in sys.modules.keys() if k.startswith('gevent')]:
            self._modules[module_name] = sys.modules.pop(module_name)

    def __exit__(self, *args, **kwargs):
        sys.modules.update(self._modules)


def test_import_with_nossl():
    with DisableSSL():
        from geventhttpclient import httplib
        from geventhttpclient import HTTPClient


def test_httpclient_raises_with_no_ssl():
    with DisableSSL():
        from geventhttpclient import HTTPClient
        with pytest.raises(Exception):
            HTTPClient.from_url('https://httpbin.org/')


if __name__ == '__main__':
    test_import_with_nossl()
    test_httpclient_raises_with_no_ssl()