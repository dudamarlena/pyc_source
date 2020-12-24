# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/utils/cfscrape.py
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
from ..assets.user_agents import user_agents
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
            raise ValueError('Unable to parse Cloudflare anti-bot IUAM page: %s %s' % (
             e.message, BUG_REPORT))

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
        else:
            return (self.request)((self.org_method), submit_url, **cloudflare_kwargs)

    def solve_challenge--- This code section failed: ---

 L. 228         0  SETUP_EXCEPT        120  'to 120'

 L. 229         2  LOAD_GLOBAL              re
                4  LOAD_ATTR                search

 L. 230         6  LOAD_STR                 'setTimeout\\(function\\(\\){\\s*(var s,t,o,p,b,r,e,a,k,i,n,g,f.+?\\r?\\n[\\s\\S]+?a\\.value\\s*=.+?)\\r?\\n(?:[^{<>]*},\\s*(\\d{4,}))?'

 L. 233         8  LOAD_FAST                'body'
               10  CALL_FUNCTION_2       2  '2 positional arguments'
               12  LOAD_ATTR                groups
               14  CALL_FUNCTION_0       0  '0 positional arguments'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'challenge'
               20  STORE_FAST               'ms'

 L. 238        22  LOAD_GLOBAL              re
               24  LOAD_ATTR                search
               26  LOAD_STR                 '<div(?: [^<>]*)? id=\\"cf-dn.*?\\">([^<>]*)'
               28  LOAD_FAST                'body'
               30  CALL_FUNCTION_2       2  '2 positional arguments'
               32  STORE_FAST               'innerHTML'

 L. 239        34  LOAD_FAST                'innerHTML'
               36  POP_JUMP_IF_FALSE    48  'to 48'
               38  LOAD_FAST                'innerHTML'
               40  LOAD_ATTR                group
               42  LOAD_CONST               1
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  JUMP_FORWARD         50  'to 50'
               48  ELSE                     '50'
               48  LOAD_STR                 ''
             50_0  COME_FROM            46  '46'
               50  STORE_FAST               'innerHTML'

 L. 254        52  LOAD_STR                 '\n                var document = {\n                    createElement: function () {\n                      return { firstChild: { href: "http://%s/" } }\n                    },\n                    getElementById: function () {\n                      return {"innerHTML": "%s"};\n                    }\n                  };\n                %s; a.value\n            '

 L. 255        54  LOAD_FAST                'domain'

 L. 256        56  LOAD_FAST                'innerHTML'

 L. 257        58  LOAD_FAST                'challenge'
               60  BUILD_TUPLE_3         3 
               62  BINARY_MODULO    
               64  STORE_FAST               'challenge'

 L. 260        66  LOAD_GLOBAL              b64encode
               68  LOAD_FAST                'challenge'
               70  LOAD_ATTR                encode
               72  LOAD_STR                 'utf-8'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  LOAD_ATTR                decode
               80  LOAD_STR                 'ascii'
               82  CALL_FUNCTION_1       1  '1 positional argument'
               84  STORE_FAST               'challenge'

 L. 262        86  LOAD_FAST                'self'
               88  LOAD_ATTR                delay
               90  JUMP_IF_TRUE_OR_POP   114  'to 114'
               92  LOAD_FAST                'ms'
               94  POP_JUMP_IF_FALSE   112  'to 112'
               96  LOAD_GLOBAL              float
               98  LOAD_FAST                'ms'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  LOAD_GLOBAL              float
              104  LOAD_CONST               1000
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  BINARY_TRUE_DIVIDE
            110_0  COME_FROM            90  '90'
              110  JUMP_FORWARD        114  'to 114'
              112  ELSE                     '114'
              112  LOAD_CONST               8
            114_0  COME_FROM           110  '110'
              114  STORE_FAST               'delay'
              116  POP_BLOCK        
              118  JUMP_FORWARD        152  'to 152'
            120_0  COME_FROM_EXCEPT      0  '0'

 L. 263       120  DUP_TOP          
              122  LOAD_GLOBAL              Exception
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   150  'to 150'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 264       134  LOAD_GLOBAL              ValueError

 L. 265       136  LOAD_STR                 'Unable to identify Cloudflare IUAM Javascript on website. %s'

 L. 266       138  LOAD_GLOBAL              BUG_REPORT
              140  BINARY_MODULO    
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  RAISE_VARARGS_1       1  'exception'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           118  '118'

 L. 289       152  LOAD_STR                 '            var atob = Object.setPrototypeOf(function (str) {                try {                    return Buffer.from("" + str, "base64").toString("binary");                } catch (e) {}            }, null);            var challenge = atob("%s");            var context = Object.setPrototypeOf({ atob: atob }, null);            var options = {                filename: "iuam-challenge.js",                contextOrigin: "cloudflare:iuam-challenge.js",                contextCodeGeneration: { strings: true, wasm: false },                timeout: 5000            };            process.stdout.write(String(                require("vm").runInNewContext(challenge, context, options)            ));        '

 L. 290       154  LOAD_FAST                'challenge'
              156  BINARY_MODULO    
              158  STORE_FAST               'js'

 L. 293       160  SETUP_EXCEPT        192  'to 192'

 L. 294       162  LOAD_GLOBAL              subprocess
              164  LOAD_ATTR                check_output

 L. 295       166  LOAD_STR                 'node'
              168  LOAD_STR                 '-e'
              170  LOAD_FAST                'js'
              172  BUILD_LIST_3          3 
              174  LOAD_GLOBAL              subprocess
              176  LOAD_ATTR                PIPE
              178  LOAD_GLOBAL              subprocess
              180  LOAD_ATTR                PIPE
              182  LOAD_CONST               ('stdin', 'stderr')
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              186  STORE_FAST               'result'
              188  POP_BLOCK        
              190  JUMP_FORWARD        282  'to 282'
            192_0  COME_FROM_EXCEPT    160  '160'

 L. 297       192  DUP_TOP          
              194  LOAD_GLOBAL              OSError
              196  COMPARE_OP               exception-match
              198  POP_JUMP_IF_FALSE   244  'to 244'
              200  POP_TOP          
              202  STORE_FAST               'e'
              204  POP_TOP          
              206  SETUP_FINALLY       234  'to 234'

 L. 298       208  LOAD_FAST                'e'
              210  LOAD_ATTR                errno
              212  LOAD_CONST               2
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 299       218  LOAD_GLOBAL              EnvironmentError

 L. 300       220  LOAD_STR                 "Missing Node.js runtime. Node is required and must be in the PATH (check with `node -v`). Your Node binary may be called `nodejs` rather than `node`, in which case you may need to run `apt-get install nodejs-legacy` on some Debian-based systems. (Please read the cfscrape README's Dependencies section: https://github.com/Anorov/cloudflare-scrape#dependencies."
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  RAISE_VARARGS_1       1  'exception'
            226_0  COME_FROM           216  '216'

 L. 303       226  RAISE_VARARGS_0       0  'reraise'
              228  POP_BLOCK        
              230  POP_EXCEPT       
              232  LOAD_CONST               None
            234_0  COME_FROM_FINALLY   206  '206'
              234  LOAD_CONST               None
              236  STORE_FAST               'e'
              238  DELETE_FAST              'e'
              240  END_FINALLY      
              242  JUMP_FORWARD        282  'to 282'

 L. 304       244  DUP_TOP          
              246  LOAD_GLOBAL              Exception
              248  COMPARE_OP               exception-match
              250  POP_JUMP_IF_FALSE   280  'to 280'
              254  POP_TOP          
              256  POP_TOP          
              258  POP_TOP          

 L. 305       260  LOAD_GLOBAL              logging
              262  LOAD_ATTR                error
              264  LOAD_STR                 'Error executing Cloudflare IUAM Javascript. %s'
              266  LOAD_GLOBAL              BUG_REPORT
              268  BINARY_MODULO    
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  POP_TOP          

 L. 306       274  RAISE_VARARGS_0       0  'reraise'
              276  POP_EXCEPT       
              278  JUMP_FORWARD        282  'to 282'
              280  END_FINALLY      
            282_0  COME_FROM           278  '278'
            282_1  COME_FROM           242  '242'
            282_2  COME_FROM           190  '190'

 L. 308       282  SETUP_EXCEPT        296  'to 296'

 L. 309       284  LOAD_GLOBAL              float
              286  LOAD_FAST                'result'
              288  CALL_FUNCTION_1       1  '1 positional argument'
              290  POP_TOP          
              292  POP_BLOCK        
              294  JUMP_FORWARD        330  'to 330'
            296_0  COME_FROM_EXCEPT    282  '282'

 L. 310       296  DUP_TOP          
              298  LOAD_GLOBAL              Exception
              300  COMPARE_OP               exception-match
              302  POP_JUMP_IF_FALSE   328  'to 328'
              306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          

 L. 311       312  LOAD_GLOBAL              ValueError

 L. 312       314  LOAD_STR                 'Cloudflare IUAM challenge returned unexpected answer. %s'
              316  LOAD_GLOBAL              BUG_REPORT
              318  BINARY_MODULO    
              320  CALL_FUNCTION_1       1  '1 positional argument'
              322  RAISE_VARARGS_1       1  'exception'
              324  POP_EXCEPT       
              326  JUMP_FORWARD        330  'to 330'
              328  END_FINALLY      
            330_0  COME_FROM           326  '326'
            330_1  COME_FROM           294  '294'

 L. 315       330  LOAD_FAST                'result'
              332  LOAD_FAST                'delay'
              334  BUILD_TUPLE_2         2 
              336  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 110

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
            if d.startswith('.'):
                if d in '.' + domain:
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
        return ('; '.join('='.join(pair) for pair in tokens.items()), user_agent)


create_scraper = CloudflareScraper.create_scraper
get_tokens = CloudflareScraper.get_tokens
get_cookie_string = CloudflareScraper.get_cookie_string