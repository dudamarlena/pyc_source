# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/request/patch/hook_request.py
# Compiled at: 2019-10-18 04:11:23
# Size of source mod 2**32: 2019 bytes
from pocsuite3.lib.core.data import conf
from requests.models import Request
from requests.sessions import Session
from requests.sessions import merge_setting, merge_cookies
from requests.cookies import RequestsCookieJar
from requests.utils import get_encodings_from_content

def session_request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=False, cert=None, json=None):
    merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(), self.cookies), cookies or )
    req = Request(method=(method.upper()),
      url=url,
      headers=(merge_setting(headers, conf.http_headers if 'http_headers' in conf else {})),
      files=files,
      data=(data or ),
      json=json,
      params=(params or ),
      auth=auth,
      cookies=merged_cookies,
      hooks=hooks)
    prep = self.prepare_request(req)
    if proxies is None:
        proxies = conf.proxies if 'proxies' in conf else {}
    settings = self.merge_environment_settings(prep.url, proxies, stream, verify, cert)
    timeout = timeout or 
    if timeout:
        timeout = float(timeout)
    send_kwargs = {'timeout':timeout, 
     'allow_redirects':allow_redirects}
    send_kwargs.update(settings)
    resp = (self.send)(prep, **send_kwargs)
    if resp.encoding == 'ISO-8859-1':
        encodings = get_encodings_from_content(resp.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = resp.apparent_encoding
        resp.encoding = encoding
    return resp


def patch_session():
    Session.request = session_request