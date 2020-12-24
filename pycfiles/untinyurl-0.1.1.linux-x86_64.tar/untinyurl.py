# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/untinyurl.py
# Compiled at: 2012-02-12 08:21:14
import urllib2, sys, socket, re
socket.setdefaulttimeout(5)

class NoRedirectHandler(urllib2.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl

    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


opener = urllib2.build_opener(NoRedirectHandler())
urllib2.install_opener(opener)

class HeadRequest(urllib2.Request):

    def get_method(self):
        return 'HEAD'


def follow_redirects(url):
    try:
        response = urllib2.urlopen(HeadRequest(url)).info()
        if 'Location' in response:
            return follow_redirects(response['Location'])
    except:
        pass

    return url


def untiny(string):
    return re.sub('http://[^ ]+', lambda match: follow_redirects(match.group()), string)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-h':
        print 'Expand tinyurls found in the given string.'
        sys.exit(0)
    if len(sys.argv) > 1:
        print untiny((' ').join(sys.argv[1:]))
    else:
        for line in sys.stdin:
            print untiny(line[:-1])