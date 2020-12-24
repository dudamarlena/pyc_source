# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/texturepacker/unwrapper.py
# Compiled at: 2012-03-04 14:57:13
"""Given the alleged URL of a texture pack, find plausible forum and download URLs.

This is tricky because often they are embedded in a page that is wrapped in
a bit.ly link which is wrapped in an adf.ly link and the download is hosted on Mediafire
behind yet another layer of redirects.
"""
import sys, os, httplib2, re
from BeautifulSoup import BeautifulSoup
import json
from urlparse import urljoin

def unwrapper_for(url_pattern, follow_redirects=True):
    """Decorator for unwrapper functions.

    Arguments --
        url_pattern -- regex for matching URLs that this applies to.
            NOTE. The initial http:// and www. will have already been stripped.
        follow_redirects -- set this to false to not follow redirects
    """
    if isinstance(url_pattern, basestring):
        url_pattern = re.compile(url_pattern)

    def func_wrapper(func):
        func.url_pattern = url_pattern
        func.follow_redirects = follow_redirects
        return func

    return func_wrapper


ADFLY_RE = re.compile("\n    function \\s close_bar\\(\\) \\s \\{ \\s+\n    self\\.location \\s = \\s '(?P<next>[^']*)'; \\s+\n    \\}\n    ", re.VERBOSE)

@unwrapper_for('^adf\\.ly')
def unwrap_adfly(url, resp, body, http=None):
    m = ADFLY_RE.search(body)
    if m:
        return m.groupdict()


@unwrapper_for('^bit\\.ly')
def unwrap_bitly(url, resp, body):
    return {'next': (
              resp['content-location'], resp, body)}


@unwrapper_for('^planetminecraft\\.com/texture_pack/[a-z-]+-\\d+/$')
def unwrap_planetminecraft(url, resp, body):
    """Planet Minecraft texture-pack section.

    Attempt to fish out the genuine download and forum URLs linked therefrom"""
    urls = {'home': resp['content-location'], 
       'download': resp['content-location']}
    soup = BeautifulSoup(body)
    table_elt = soup.first('div', 'resource-share').table
    for tr_elt in table_elt.findAll('tr'):
        a_elt = tr_elt.td.a
        label = a_elt['title']
        href = a_elt['href']
        if label == 'Download Texture Pack':
            urls['next'] = urljoin(url, href)
        elif label == 'Visit Forum post':
            urls['forum'] = href

    return urls


@unwrapper_for('^planetminecraft\\.com/texture_pack/[a-z-]+-\\d+/download/file/\\d+/$', follow_redirects=False)
def unwrap_planetminecraft_download(url, resp, body):
    """The dowload link from Planet Minecraft"""
    return {'next': resp['location'].replace(' ', '%20')}


URL_SCORES = [
 (
  re.compile('^http://(www\\.)?mediafire\\.com/'), 50),
 (
  re.compile('^http://bit\\.ly/'), 25),
 (
  re.compile('^http://adf\\.ly/'), 25)]
LABEL_SCORES = [
 (
  re.compile('download', re.IGNORECASE), 100)]
LICENCE_SCORES = [
 (
  re.compile('^http://creativecommons.org/licenses/'), 100)]
WOT_NO_SLASH_RE = re.compile('^https?://[\\w.-]+$')

@unwrapper_for('^minecraftforum\\.net')
def unwrap_minecraftforum(url, resp, body):
    urls = {'forum': url}
    soup = BeautifulSoup(body)
    post_elt = soup.first('div', 'entry-content')
    best_href = None
    best_score = 0
    for a_elt in post_elt.findAll('a', 'bbc_url'):
        try:
            href = a_elt['href']
            if href == url:
                continue
            licence_score = sum(pat_score for pat, pat_score in LICENCE_SCORES if pat.search(href))
            if licence_score:
                urls['licence'] = href
                continue
            score = sum(pat_score for pat, pat_score in URL_SCORES if pat.search(href))
            labels = []
            try:
                label = ('').join(a_elt.findAll(text=True))
                if label:
                    labels.append(label)
            except AttributeError:
                pass

            label = a_elt.findPreviousSibling(text=True)
            if label:
                labels.append(label)
            for label in labels:
                score += sum(pat_score for pat, pat_score in LABEL_SCORES if pat.search(label))

            if a_elt.img:
                score += 10
            if score > best_score:
                best_href, best_score = href, score
        except KeyError as e:
            print >> sys.stderr, a_elt, 'did not have', e

    if best_href:
        if WOT_NO_SLASH_RE.match(best_href):
            best_href += '/'
        urls['next'] = best_href
    return urls


MEDIAFIRE_PKR_RE = re.compile("^<!--\\s*var LA=\\s*false;\\s*pKr='([^']+)';")
MEDIAFIRE_CALL_RE = re.compile('^DoShow\\("notloggedin_wrapper"\\);\\s*cR\\(\\);\\s*(\\w+)\\(\\);')
MEDIAFIRE_CALL2_RE = re.compile("\\w+\\('\\w+','([a-f\\d]+)'\\)")

@unwrapper_for('^mediafire\\.com/\\?')
def unwrap_mediafire(url, resp, body):
    """Mediafire wrap downloads in a mass of obsfucated JavaScript. Extract and return the next URL."""
    urls = {'download': url}
    soup = BeautifulSoup(body)
    secret_qk = url.split('?', 1)[1]
    for elt in soup.body.findAll('script', type='text/javascript', language=None):
        s = elt.string
        s = s and s.strip()
        if s:
            m = MEDIAFIRE_CALL_RE.search(s)
            if m:
                secret_func = m.group(1)
                break

    FUNC_PAT = re.compile("\n        function \\s %s .*\n        unescape\\('(?P<cyphertext>[a-f\\d]+)'\\); \\s*\n        \\w+ = (?P<count>\\d+) ; \\s*\n        for \\( .* \\) .*\n        \\w+ = \\w+ \\+ \\(String.fromCharCode\\(parseInt\\(\\w+.substr\\(i\\s\\*\\s2,\\s2\\),\\s16\\) \\^\n                (?P<key>[\\d^]+)\n        \\)\\); \\s*\n        eval\\(\\w+\\);\n        " % secret_func, re.VERBOSE)
    for elt in soup.body.findAll('script', type='text/JavaScript', language='JavaScript'):
        m = MEDIAFIRE_PKR_RE.search(elt.string)
        if m:
            secret_pKr = m.group(1)
            m = FUNC_PAT.search(elt.string)
            if m:
                plaintext = mediafire_decode(m.group('cyphertext'), m.group('count'), m.group('key'))
                m = MEDIAFIRE_CALL2_RE.match(plaintext)
                secret_pk1 = m.group(1)
            break

    urls['next'] = 'http://www.mediafire.com/dynamic/download.php?qk=%s&pk1=%s&r=%s' % (
     secret_qk, secret_pk1, secret_pKr)
    return urls


def mediafire_decode(cyphertext, count, key):
    """Mediafire use a simple cypher to obscure some codes embedded in their HTML.

    Arguments --
        cyphertext -- lowercase hexadecimal digits. Mediafire needlessly wrap it in unescape(...).
        count -- number of pairs of digits to consider; a int or string representation of an int.
        key -- the expression XORed with all bytes, in the form of a string
                containing ^-separated integers. For example, "13^7".

    Returns --
        A byte string, usually containg JavaScript code to pass to eval.
    """
    count = int(count)
    key = reduce(lambda x, y: x ^ y, [ int(x) for x in key.split('^') ])
    plaintext = ('').join(chr(int(cyphertext[2 * i:2 * i + 2], 16) ^ key) for i in range(count))
    return plaintext


MF_DOWNLOAD_ENIGMA_RE = re.compile("\n    unescape\\('(?P<cyphertext>[a-f\\d]+)'\\);\n    \\w+ = (?P<count>\\d+) ;\n    for \\(i = 0; i < \\w+; i\\+\\+ \\)\n    \\w+ = \\w+ \\+ \\(String.fromCharCode\\(parseInt\\(\\w+.substr\\(i\\s\\*\\s2,\\s2\\),\\s16\\) \\^\n            (?P<key>[\\d^]+)\n    \\)\\);\n    eval\\(\\w+\\); ", re.VERBOSE)
MF_DOWNLOAD_ROTOR_RE = re.compile("(\\w+)='(\\w+)';")
MF_DOWNLOAD_INNERHTML_RE = re.compile('\n    case \\s 15:  # Ensure we have the correct branch of the switch\n    .*?\n    href=\\\\"(?P<prefix>http://download\\d+.mediafire.com/)"\n    \\s* \\+ \\s*\n    (?P<key>\\w+)\n    \\s* \\+ \\s*\n    "(?P<suffix>[^"]+\\.zip)\\\\"\n    ', re.VERBOSE)

@unwrapper_for('^mediafire\\.com/dynamic/download\\.php\\?')
def unwrap_mediafire_download(url, resp, body):
    u"""Pull out the link to the actual download from Medafire’s hidden page"""
    m = MF_DOWNLOAD_ENIGMA_RE.search(body)
    if m:
        code = mediafire_decode(m.group('cyphertext'), m.group('count'), m.group('key'))
        enigma = dict(MF_DOWNLOAD_ROTOR_RE.findall(code))
        m = MF_DOWNLOAD_INNERHTML_RE.search(body)
        href = m.group('prefix') + enigma[m.group('key')] + m.group('suffix')
        return {'next': href}
    return {}


@unwrapper_for('.*')
def unwrap_anything_and_save_it(url, resp, body):
    """For debugging! This unwrapper saves its arguments to disk for later analysis."""
    name = url.split('/')[2].replace('www.', '')
    with open('%s.json' % name, 'wb') as (strm):
        json.dump(resp, strm, indent=4)
    print >> sys.stderr, 'Wrote headers to %s.json' % name
    with open('%s.html' % name, 'wb') as (strm):
        strm.write(body)
    print >> sys.stderr, 'Wrote body to %s.html' % name
    return {}


URL_IS_DOWNLOAD_SCORES = [
 (
  re.compile('^http://(www\\.)?mediafire.com/', re.IGNORECASE), 50),
 (
  re.compile('\\.zip$', re.IGNORECASE), 50)]

def guess_url_is_download(url):
    """Return a positive number if this URL looks likely to be a ZIP download."""
    return sum(score for pat, score in URL_IS_DOWNLOAD_SCORES if pat.search(url))


URL_IS_HOME_SCORES = [
 (
  re.compile('^http://(www\\.)?planetminecraft\\.com/texture_pack/[\\w-]+/', re.IGNORECASE), 100)]

def guess_url_is_home(url):
    """Return a positive number if this URL looks likely to be an external homepage for the pack.."""
    return sum(score for pat, score in URL_IS_HOME_SCORES if pat.search(url))


UNWRAPPERS = [
 unwrap_planetminecraft,
 unwrap_planetminecraft_download,
 unwrap_adfly,
 unwrap_bitly,
 unwrap_minecraftforum,
 unwrap_mediafire,
 unwrap_mediafire_download]
COOKIE_EXPIRES_RE = re.compile('\n    expires=\n    (Mon|Tue|Wed|Thu|Fri|Sat|Sun), \\s [^;,]+\n    [;,]?\n    ', re.VERBOSE)

class Unwrapper(object):
    """Device for peeling back layers of redirection web sites to get the actual download link.

    The `unwrap` methodis used to attempt to find download etc. URLs.

    """

    def __init__(self, http=None):
        self.http = http or httplib2.Http()

    def unwrap(self, url, until=None):
        """Try to find actual download and forum URLs, starting with this one.

        Arguments --
            url (string) -- the published URL for the resource (may be the actual URL
                or the address of a forum page linking to it etc.)
            until (Set of string) -- stop when all of the named categorized URLs are known.
                Use this when you want to document the resource
                but not necessarly find the final one.

        Returns --
            A dictionary  with some or none of the following keys defined:

            final -- the URL that could not be further processed; generally
                if all has gone well this will be the actual URL of the resource itself.
            forum -- a forum post concerning this resource (this happens when
                the alleged URL of the resource is actually a link to the post).
            download -- the URL to quote as the one to download the resource from
                (may still involve a redirection via Mediafire etc.).
            home -- the URL to quote as the home page of the resource

        If `until` is not specified, then carry on until there is no more
        dereferencing to do.

        This may make one or more HTTP requests, and will consume
        memory as it holds the intermediate resources for examination.
        """
        if until:
            until = set(until)
        cookie_jar = {}
        queue = [url]
        result = {}
        while queue:
            url_resp_body = queue.pop(0)
            need_download = isinstance(url_resp_body, basestring)
            if need_download:
                url = url_resp_body
            else:
                url, resp, body = url_resp_body
            x = url
            if x.startswith('http://'):
                x = x[7:]
            if x.startswith('www.'):
                x = x[4:]
            for func in UNWRAPPERS:
                if func.url_pattern.search(x):
                    if need_download:
                        headers = {}
                        self.http.follow_redirects = func.follow_redirects if hasattr(func, 'follow_redirects') else True
                        if cookie_jar:
                            headers['cookie'] = (';').join('%s=%s' % (key, val) for key, val in cookie_jar.items())
                        resp, body = self.http.request(url, headers=headers)
                        if 'set-cookie' in resp:
                            cookies_line = COOKIE_EXPIRES_RE.sub('', resp['set-cookie'])
                            for cookie_def in cookies_line.split(','):
                                parts = cookie_def.strip().split(';')
                                cookie_name, cookie_value = parts[0].split('=', 1)
                                cookie_jar[cookie_name] = cookie_value

                    res = func(url, resp, body)
                    if res and 'forum' in res and 'next' in res:
                        u = res['next']
                        if 'download' not in res and guess_url_is_download(u):
                            res['download'] = u
                        if 'home' not in res and guess_url_is_home(u):
                            res['home'] = u
                    result.update(res)
                    break
            else:
                result['final'] = url

            if until and not until - set(result.keys()):
                break
            if 'next' in result:
                queue.append(result.pop('next'))

        return result


default_unwrapper = None

def unwrap(*args, **kwargs):
    """"Shortcut for unwrapping a URL.

    Equivalent to Unwrapper().unwrap(...).
    """
    global default_unwrapper
    if not default_unwrapper:
        default_unwrapper = Unwrapper()
    return default_unwrapper.unwrap(*args, **kwargs)


if __name__ == '__main__':
    import pprint
    u = 'http://adf.ly/380075/forestdepths'
    u = 'http://www.planetminecraft.com/texture_pack/the-clean-lines-texture-pack-357/'
    pprint.pprint(Unwrapper().unwrap(u))