# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/browser/lib/google_short.py
# Compiled at: 2009-11-12 05:32:28
__doc__ = "Example script.\n\n   Connects to an installation of Google Short Links and submits an\n   API request.\n\n   Example commands:\n     Get the details of the short link 'foo':\n       python api_sample.py\n           --details\n           --server=shortlinks.example.com\n           --hmac=foobar\n           --email=anything\n           --url=anything\n           --shortcut_name=foo\n     Create a new short link 'bar' that points to www.google.com and\n     is owned by owner@example.com:\n       python api_sample.py\n           --create\n           --server=shortlinks.example.com\n           --hmac=foobar\n           --email=owner@example.com\n           --url=http://www.google.com\n           --shortcut_name=bar\n     Create a new public HASHED short link that points to www.google.com and\n     is owned by owner@example.com:\n       python api_sample.py\n           --hash\n           --server=shortlinks.example.com\n           --hmac=foobar\n           --email=owner@example.com\n           --url=http://www.google.com\n           --shortcut_name=anything\n           --is_public\n"
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


if __name__ == '__main__':
    main()