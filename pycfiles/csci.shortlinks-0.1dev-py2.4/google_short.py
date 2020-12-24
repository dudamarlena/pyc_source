# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/csci/shortlinks/browser/google_short.py
# Compiled at: 2009-09-09 06:57:38
"""Example script.

   Connects to an installation of Google Short Links and submits an
   API request.

   Example commands:
     Get the details of the short link 'foo':
       python api_sample.py
           --details
           --server=shortlinks.example.com
           --hmac=foobar
           --email=anything
           --url=anything
           --shortcut_name=foo
     Create a new short link 'bar' that points to www.google.com and
     is owned by owner@example.com:
       python api_sample.py
           --create
           --server=shortlinks.example.com
           --hmac=foobar
           --email=owner@example.com
           --url=http://www.google.com
           --shortcut_name=bar
     Create a new public HASHED short link that points to www.google.com and
     is owned by owner@example.com:
       python api_sample.py
           --hash
           --server=shortlinks.example.com
           --hmac=foobar
           --email=owner@example.com
           --url=http://www.google.com
           --shortcut_name=anything
           --is_public
"""
import base64, datetime, hmac, optparse, sha, sys, time, urllib, urllib2

def make_request_uri(hostname, api_method, secret, **parameters):
    """Constructs a signed api request.

       Contains a miniature implementation of an oauth signing mechanism.
       Not complete, but enough for this use case.

    Args:
      hostname: the name of the domain that short links is installed at
      api_method: the api method to be called, like get_or_create_hash
      secret: the api (hmac) secret to be used
      parameters: additional arguments that should be passed to the api-method
    Returns:
      A signed URL that the short links server would understand.
    """
    base_url = 'http://%s/js/%s' % (hostname.lower(), api_method)
    parameters['oauth_signature_method'] = 'HMAC-SHA1'
    parameters['timestamp'] = str(time.mktime(datetime.datetime.now().timetuple()))
    param_array = [ (k, v) for (k, v) in parameters.items() ]
    param_array.sort()
    keyvals = [ '%s=%s' % (urllib.quote(a, ''), urllib.quote(str(b), '')) for (a, b) in param_array ]
    unsecaped = ('&').join(keyvals)
    signature_base_string = 'GET&%s&%s' % (urllib.quote(base_url, ''), urllib.quote(unsecaped, ''))
    signature = urllib.quote(base64.b64encode(hmac.new(secret, signature_base_string, sha).digest()), '')
    return '%s?%s&oauth_signature=%s' % (base_url, unsecaped, signature)


def get_short(server='', action='get_or_create_hash', hmac='', email='', url='', short_name='anything', is_public='true'):
    request_url = make_request_uri(server, action, hmac, user=email, url=url, shortcut=short_name, is_public=str(is_public).lower())
    response = urllib2.urlopen(request_url)
    res = response.read()
    res = res.replace('true', 'True')
    res_dict = eval(res)
    end_url = 'http://' + str(server) + '/' + str(res_dict['shortcut'])
    return end_url


if __name__ == '__main__':
    main()