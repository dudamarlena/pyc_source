# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/eggproxy/apache_handler.py
# Compiled at: 2008-09-22 04:57:28
import os
from mod_python import apache
from iw.eggproxy import eggs_index_proxy
from iw.eggproxy.config import EGGS_DIR

def fixup_handler(req):
    options = req.get_options()
    document_root = EGGS_DIR
    url_prefix = options['URLPrefix']
    url_prefix = [ part for part in url_prefix.split('/') if part ]
    url_prefix_len = len(url_prefix)
    uri_path = req.parsed_uri[apache.URI_PATH]
    uri_path = [ part for part in uri_path.split('/') if part ][url_prefix_len:]
    real_path = os.path.join(document_root, *uri_path)
    if os.path.exists(real_path) and not os.path.isdir(real_path):
        req.handler = 'default-handler'
        return apache.DECLINED
    req.handler = 'mod_python'
    req.add_handler('PythonHandler', modpython_handler)
    return apache.OK


def modpython_handler(req):
    options = req.get_options()
    document_root = EGGS_DIR
    url_prefix = options['URLPrefix']
    url_prefix = [ part for part in url_prefix.split('/') if part ]
    url_prefix_len = len(url_prefix)
    uri_path = req.parsed_uri[apache.URI_PATH]
    uri_path = [ part for part in uri_path.split('/') if part ][url_prefix_len:]
    if len(uri_path) > 0 and uri_path[(-1)] == 'index.html':
        uri_path.pop()
    real_path = os.path.join(document_root, *uri_path)
    real_path_exists = os.path.exists(real_path)
    if real_path_exists:
        if not os.path.isdir(real_path):
            return apache.DECLINED
        real_path = os.path.join(real_path, 'index.html')
        if os.path.exists(real_path):
            req.internal_redirect(req.uri + 'index.html')
            return apache.OK
    uri_path_len = len(uri_path)
    if uri_path_len > 2:
        return apache.HTTP_NOT_FOUND
    if uri_path_len == 0:
        eggs_index_proxy.updateBaseIndex()
        req.internal_redirect(req.uri + 'index.html')
        return apache.OK
    package_name = uri_path[0]
    if uri_path_len == 1:
        try:
            eggs_index_proxy.updatePackageIndex(package_name)
        except ValueError:
            return apache.HTTP_NOT_FOUND
        else:
            req.internal_redirect(req.uri)
            return apache.OK
    else:
        eggname = uri_path[1]
        try:
            eggs_index_proxy.updateEggFor(package_name, eggname)
        except ValueError:
            return apache.HTTP_NOT_FOUND

        req.internal_redirect(req.uri)
        return apache.OK
    return apache.HTTP_NOT_FOUND