# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: graphdash/flask_utils.py
# Compiled at: 2019-04-25 09:26:58
from functools import wraps
from datetime import datetime
import socket
from flask import current_app, request, make_response

def after_request_log(response):
    name = dns_resolve(request.remote_addr)
    current_app.logger.warn(('[client {ip} {host}] {http} "{method} {path}" {status}\n    Request:   {method} {path}\n    Version:   {http}\n    Status:    {status}\n    Url:       {url}\n    IP:        {ip}\n    Hostname:  {host}\n    Agent:     {agent_platform} | {agent_browser} | {agent_browser_version}\n    Raw Agent: {agent}\n    ').format(method=request.method, path=request.path, url=request.url, ip=request.remote_addr, host=name if name is not None else '?', agent_platform=request.user_agent.platform, agent_browser=request.user_agent.browser, agent_browser_version=request.user_agent.version, agent=request.user_agent.string, http=request.environ.get('SERVER_PROTOCOL'), status=response.status))
    return response


def dns_resolve(ip_addr):
    """Safe DNS query."""
    try:
        name = socket.gethostbyaddr(ip_addr)[0]
    except (socket.herror, socket.gaierror):
        name = None

    return name


def cache(timeout):

    def _cache(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            resp.cache_control.max_age = timeout
            return resp

        return wrapper

    return _cache


def nocache(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.headers['Last-Modified'] = datetime.now()
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '-1'
        return resp

    return wrapper