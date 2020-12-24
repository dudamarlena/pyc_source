# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/WebInterface.py
# Compiled at: 2019-06-28 16:58:56
# Size of source mod 2**32: 3964 bytes
from .misc import url_decode

class WebInterface(object):
    __doc__ = '\n\tAllows for easily defining web interfaces for the server.\n\n\tExpects the variable "self.host" to be set to a WebHost\n\tobject before calling "connect()".\n\n\tSee implementation of __init__ class for an example initialization.\n\t'

    def __init__(self, host=None, host_kwargs={}, host_addr_kwargs={}, web_dispatcher_ident=None, dispatcher_level=None):
        if web_dispatcher_ident is None:
            disp_type = 'web'
        else:
            disp_type = (
             'web', web_dispatcher_ident)
        if host is None:
            from guavacado import WebHost
            self.host = WebHost(**host_kwargs)
            host_addr_kwargs_add = host_addr_kwargs
            if web_dispatcher_ident is not None:
                host_addr_kwargs_add.update({'disp_type': disp_type})
            (self.host.add_addr)(**host_addr_kwargs_add)
        else:
            self.host = host
        self.resource_dict = {}
        self.host.get_specialized_dispatcher(disp_type).add_resource_handler((self.identify_request), (self.handle_request), 'WebInterface', level=dispatcher_level)

    def identify_request(self, url=None, method=None, headers=None, body=None):
        if method in self.resource_dict:
            url_no_browseparams = url.split('?')[0]
            for url_prefix, url_param_count, params in self.get_possible_split_url_params(url_no_browseparams):
                if url_prefix in self.resource_dict[method]:
                    if url_param_count in self.resource_dict[method][url_prefix]:
                        callback = self.resource_dict[method][url_prefix][url_param_count]
                        args = (body,) + params
                        return (callback, args)

    def handle_request(self, callback, args):
        return callback(*args)

    def get_possible_split_url_params(self, url):
        ret = []
        split_url = url.split('/')
        remaining = split_url
        removed = []
        while len(remaining) > 0:
            prefix = '/'.join(remaining)
            param_count = len(split_url) - len(remaining)
            params = removed[:param_count]
            if prefix + '/' == url:
                ret.append((prefix, param_count, params))
                param_count = param_count - 1
                params = removed[:param_count]
            params_decoded = []
            for par in params:
                params_decoded.append(url_decode(par))

            params_decoded_tup = tuple(params_decoded)
            ret.append((prefix, param_count, params_decoded_tup))
            removed = [remaining[(-1)]] + removed
            remaining = remaining[:-1]

        return ret

    def split_url_params(self, url):
        split_url = url.split('/:')
        prefix = split_url[0]
        param_count = len(split_url) - 1
        return (prefix, param_count)

    def connect(self, resource, action, method, body_included=False):
        if isinstance(action, str):
            callback = getattr(self, action)
        else:
            callback = action
        self.connect_callback(resource, callback, method, body_included=body_included)

    def connect_callback(self, resource, callback, method, body_included=False):
        """
                connects a specified callback (function) in this object
                to the specified resource (URL)
                and http method (GET/PUT/POST/DELETE)
                """
        self.dispatcher = self.host.get_dispatcher()
        if body_included:
            disp_callback = callback
        else:

            def disp_callback(body, *args):
                return callback(*args)

        if method not in self.resource_dict:
            self.resource_dict[method] = {}
        url_prefix, url_param_count = self.split_url_params(resource)
        if url_prefix not in self.resource_dict[method]:
            self.resource_dict[method][url_prefix] = {}
        self.resource_dict[method][url_prefix][url_param_count] = disp_callback
        self.host.get_docs().log_connection(resource, callback, method)

    def start_service(self):
        self.host.start_service()

    def stop_service(self):
        self.host.stop_service()