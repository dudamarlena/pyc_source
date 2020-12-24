# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\cfscrape.py
# Compiled at: 2019-12-03 10:25:40
# Size of source mod 2**32: 14666 bytes
"""
Source: https://raw.githubusercontent.com/Anorov/cloudflare-scrape/master/cfscrape/__init__.py
"""
import logging, random, re, ssl, subprocess, copy, time, os
from base64 import b64encode
from collections import OrderedDict
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.compat import urlparse, urlunparse
from requests.exceptions import RequestException
from urllib3.util.ssl_ import create_urllib3_context, DEFAULT_CIPHERS
import assets.user_agents as user_agents
__version__ = '2.0.7'
DEFAULT_USER_AGENT = random.choice(user_agents)
DEFAULT_HEADERS = OrderedDict((
 ('Host', None),
 ('Connection', 'keep-alive'),
 ('Upgrade-Insecure-Requests', '1'),
 (
  'User-Agent', DEFAULT_USER_AGENT),
 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
 ('Accept-Language', 'en-US,en;q=0.9'),
 ('Accept-Encoding', 'gzip, deflate')))
BUG_REPORT = 'Cloudflare may have changed their technique, or there may be a bug in the script.\n\nPlease read https://github.com/Anorov/cloudflare-scrape#updates, then file a bug report at https://github.com/Anorov/cloudflare-scrape/issues."'
ANSWER_ACCEPT_ERROR = 'The challenge answer was not properly accepted by Cloudflare. This can occur if the target website is under heavy load, or if Cloudflare is experiencing issues. You can\npotentially resolve this by increasing the challenge answer delay (default: 8 seconds). For example: cfscrape.create_scraper(delay=15)\n\nIf increasing the delay does not help, please open a GitHub issue at https://github.com/Anorov/cloudflare-scrape/issues'
DEFAULT_CIPHERS += ':!ECDHE+SHA:!AES128-SHA:!AESCCM:!DHE:!ARIA'

class CloudflareAdapter(HTTPAdapter):
    __doc__ = ' HTTPS adapter that creates a SSL context with custom ciphers '

    def get_connection(self, *args, **kwargs):
        conn = (super(CloudflareAdapter, self).get_connection)(*args, **kwargs)
        if conn.conn_kw.get('ssl_context'):
            conn.conn_kw['ssl_context'].set_ciphers(DEFAULT_CIPHERS)
        else:
            context = create_urllib3_context(ciphers=DEFAULT_CIPHERS)
            conn.conn_kw['ssl_context'] = context
        return conn


class CloudflareError(RequestException):
    pass


class CloudflareCaptchaError(CloudflareError):
    pass


class CloudflareScraper(Session):

    def __init__(self, *args, **kwargs):
        self.delay = kwargs.pop('delay', None)
        headers = OrderedDict(kwargs.pop('headers', DEFAULT_HEADERS))
        headers.setdefault('User-Agent', DEFAULT_USER_AGENT)
        (super(CloudflareScraper, self).__init__)(*args, **kwargs)
        self.headers = headers
        self.org_method = None
        self.mount('https://', CloudflareAdapter())

    @staticmethod
    def is_cloudflare_iuam_challenge(resp):
        return resp.status_code in (503, 429) and resp.headers.get('Server', '').startswith('cloudflare') and b'jschl_vc' in resp.content and b'jschl_answer' in resp.content

    @staticmethod
    def is_cloudflare_captcha_challenge(resp):
        return resp.status_code == 403 and resp.headers.get('Server', '').startswith('cloudflare') and b'/cdn-cgi/l/chk_captcha' in resp.content

    def request(self, method, url, *args, **kwargs):
        resp = (super(CloudflareScraper, self).request)(method, url, *args, **kwargs)
        if self.is_cloudflare_captcha_challenge(resp):
            self.handle_captcha_challenge(resp, url)
        if self.is_cloudflare_iuam_challenge(resp):
            resp = (self.solve_cf_challenge)(resp, **kwargs)
        return resp

    def cloudflare_is_bypassed(self, url, resp=None):
        cookie_domain = '.{}'.format(urlparse(url).netloc)
        return self.cookies.get('cf_clearance', None, domain=cookie_domain) or resp and resp.cookies.get('cf_clearance', None, domain=cookie_domain)

    def handle_captcha_challenge(self, resp, url):
        error = 'Cloudflare captcha challenge presented for %s (cfscrape cannot solve captchas)' % urlparse(url).netloc
        if ssl.OPENSSL_VERSION_NUMBER < 269488128:
            error += '. Your OpenSSL version is lower than 1.1.1. Please upgrade your OpenSSL library and recompile Python.'
        raise CloudflareCaptchaError(error, response=resp)

    def solve_cf_challenge(self, resp, **original_kwargs):
        start_time = time.time()
        body = resp.text
        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        if self.org_method is None:
            self.org_method = resp.request.method
        submit_url = '%s://%s/%s' % (parsed_url.scheme, domain, re.findall('\\<form id="challenge-form" action="\\/(.*)\\?', resp.text)[0])
        cloudflare_kwargs = copy.deepcopy(original_kwargs)
        headers = cloudflare_kwargs.setdefault('headers', {})
        headers['Referer'] = resp.url
        try:
            cloudflare_kwargs['data'] = OrderedDict(re.findall('name="(s|jschl_vc|pass)"(?: [^<>]*)? value="(.+?)"', body))
            params = cloudflare_kwargs['params'] = {'__cf_chl_jschl_tk__': re.findall('\\<form id="challenge-form" action=".*\\?__cf_chl_jschl_tk__=(.*?)"', resp.text)[0]}
            for k in ('jschl_vc', 'pass'):
                if k not in cloudflare_kwargs['data']:
                    raise ValueError('%s is missing from challenge form' % k)

        except Exception as e:
            try:
                raise ValueError('Unable to parse Cloudflare anti-bot IUAM page: %s %s' % (
                 e.message, BUG_REPORT))
            finally:
                e = None
                del e

        answer, delay = self.solve_challenge(body, domain)
        cloudflare_kwargs['data']['jschl_answer'] = answer
        method = re.findall('\\<form id=\\"challenge-form\\" action=\\"\\/.*\\?.*method=\\"(.*?)\\"', body)[0]
        cloudflare_kwargs['allow_redirects'] = False
        time.sleep(max(delay - (time.time() - start_time), 0))
        redirect = (self.request)(method, submit_url, **cloudflare_kwargs)
        if 'Location' in redirect.headers:
            redirect_location = urlparse(redirect.headers['Location'])
            if not redirect_location.netloc:
                redirect_url = urlunparse((
                 parsed_url.scheme,
                 domain,
                 redirect_location.path,
                 redirect_location.params,
                 redirect_location.query,
                 redirect_location.fragment))
                return (self.request)(method, redirect_url, **original_kwargs)
            return (self.request)(method, (redirect.headers['Location']), **original_kwargs)
        return (self.request)((self.org_method), submit_url, **cloudflare_kwargs)

    def solve_challenge(self, body, domain):
        try:
            challenge, ms = re.search('setTimeout\\(function\\(\\){\\s*(var s,t,o,p,b,r,e,a,k,i,n,g,f.+?\\r?\\n[\\s\\S]+?a\\.value\\s*=.+?)\\r?\\n(?:[^{<>]*},\\s*(\\d{4,}))?', body).groups()
            innerHTML = re.search('<div(?: [^<>]*)? id=\\"cf-dn.*?\\">([^<>]*)', body)
            innerHTML = innerHTML.group(1) if innerHTML else ''
            challenge = '\n                var document = {\n                    createElement: function () {\n                      return { firstChild: { href: "http://%s/" } }\n                    },\n                    getElementById: function () {\n                      return {"innerHTML": "%s"};\n                    }\n                  };\n                %s; a.value\n            ' % (
             domain,
             innerHTML,
             challenge)
            challenge = b64encode(challenge.encode('utf-8')).decode('ascii')
            delay = self.delay or (float(ms) / float(1000) if ms else 8)
        except Exception:
            raise ValueError('Unable to identify Cloudflare IUAM Javascript on website. %s' % BUG_REPORT)

        js = '            var atob = Object.setPrototypeOf(function (str) {                try {                    return Buffer.from("" + str, "base64").toString("binary");                } catch (e) {}            }, null);            var challenge = atob("%s");            var context = Object.setPrototypeOf({ atob: atob }, null);            var options = {                filename: "iuam-challenge.js",                contextOrigin: "cloudflare:iuam-challenge.js",                contextCodeGeneration: { strings: true, wasm: false },                timeout: 5000            };            process.stdout.write(String(                require("vm").runInNewContext(challenge, context, options)            ));        ' % challenge
        try:
            result = subprocess.check_output([
             'node', '-e', js],
              stdin=(subprocess.PIPE), stderr=(subprocess.PIPE))
        except OSError as e:
            try:
                if e.errno == 2:
                    raise EnvironmentError("Missing Node.js runtime. Node is required and must be in the PATH (check with `node -v`). Your Node binary may be called `nodejs` rather than `node`, in which case you may need to run `apt-get install nodejs-legacy` on some Debian-based systems. (Please read the cfscrape README's Dependencies section: https://github.com/Anorov/cloudflare-scrape#dependencies.")
                raise
            finally:
                e = None
                del e

        except Exception:
            logging.error('Error executing Cloudflare IUAM Javascript. %s' % BUG_REPORT)
            raise

        try:
            float(result)
        except Exception:
            raise ValueError('Cloudflare IUAM challenge returned unexpected answer. %s' % BUG_REPORT)

        return (
         result, delay)

    @classmethod
    def create_scraper(cls, sess=None, **kwargs):
        """
        Convenience function for creating a ready-to-go CloudflareScraper object.
        """
        scraper = cls(**kwargs)
        if sess:
            attrs = ['auth',
             'cert',
             'cookies',
             'headers',
             'hooks',
             'params',
             'proxies',
             'data']
            for attr in attrs:
                val = getattr(sess, attr, None)
                if val:
                    setattr(scraper, attr, val)

        return scraper

    @classmethod
    def get_tokens(cls, url, user_agent=None, **kwargs):
        scraper = cls.create_scraper()
        if user_agent:
            scraper.headers['User-Agent'] = user_agent
        try:
            resp = (scraper.get)(url, **kwargs)
            resp.raise_for_status()
        except Exception:
            logging.error("'%s' returned an error. Could not collect tokens." % url)
            raise

        domain = urlparse(resp.url).netloc
        cookie_domain = None
        for d in scraper.cookies.list_domains():
            if d.startswith('.') and d in '.' + domain:
                cookie_domain = d
                break
        else:
            raise ValueError('Unable to find Cloudflare cookies. Does the site actually have Cloudflare IUAM ("I\'m Under Attack Mode") enabled?')

        return (
         {'__cfduid':scraper.cookies.get('__cfduid', '', domain=cookie_domain), 
          'cf_clearance':scraper.cookies.get('cf_clearance',
            '', domain=cookie_domain)},
         scraper.headers['User-Agent'])

    @classmethod
    def get_cookie_string(cls, url, user_agent=None, **kwargs):
        """
        Convenience function for building a Cookie HTTP header value.
        """
        tokens, user_agent = (cls.get_tokens)(url, user_agent=user_agent, **kwargs)
        return ('; '.join(('='.join(pair) for pair in tokens.items())), user_agent)


create_scraper = CloudflareScraper.create_scraper
get_tokens = CloudflareScraper.get_tokens
get_cookie_string = CloudflareScraper.get_cookie_string