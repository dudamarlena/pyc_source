# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/main.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 18387 bytes
import os, re, ssl, time, warnings, difflib, http.cookiejar
from bs4 import BeautifulSoup
try:
    from urllib.parse import urlencode
    from urllib.error import HTTPError, URLError
    from urllib.request import build_opener, HTTPCookieProcessor
except ImportError:
    print("\x1b[1;91m [-] \x1b[1;93mXSRFProbe\x1b[0m isn't compatible with Python 2.x versions.\n\x1b[1;91m [-] \x1b[0mUse Python 3.x to run \x1b[1;93mXSRFProbe.")
    quit()

try:
    import requests, stringdist, bs4
except ImportError:
    print(' [-] Required dependencies are not installed.\n [-] Run \x1b[1;93mpip3 install -r requirements.txt\x1b[0m to fix it.')

from xsrfprobe.core.options import *
from xsrfprobe.core.colors import *
from xsrfprobe.core.inputin import inputin
from xsrfprobe.core.request import Get, Post
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.prettify import formPrettify
from xsrfprobe.core.banner import banner, banabout
from xsrfprobe.core.forms import testFormx1, testFormx2
from xsrfprobe.core.logger import ErrorLogger, GetLogger
from xsrfprobe.core.logger import VulnLogger, NovulLogger
from xsrfprobe.files.config import *
from xsrfprobe.files.discovered import FORMS_TESTED
from xsrfprobe.modules import Debugger
from xsrfprobe.modules import Parser
from xsrfprobe.modules import Crawler
from xsrfprobe.modules.Origin import Origin
from xsrfprobe.modules.Cookie import Cookie
from xsrfprobe.modules.Tamper import Tamper
from xsrfprobe.modules.Entropy import Entropy
from xsrfprobe.modules.Referer import Referer
from xsrfprobe.modules.Encoding import Encoding
from xsrfprobe.modules.Analysis import Analysis
from xsrfprobe.modules.Checkpost import PostBased
warnings.filterwarnings('ignore')

def Engine():
    os.system('clear')
    banner()
    banabout()
    web, fld = inputin()
    form1 = testFormx1()
    form2 = testFormx2()
    Cookie0 = http.cookiejar.CookieJar()
    Cookie1 = http.cookiejar.CookieJar()
    if not VERIFY_CERT:
        context = ssl._create_unverified_context()
        sslHandler = urllib.request.HTTPSHandler(context=context)
        resp1 = build_opener(HTTPCookieProcessor(Cookie0), sslHandler)
        resp2 = build_opener(HTTPCookieProcessor(Cookie1), sslHandler)
    else:
        resp1 = build_opener(HTTPCookieProcessor(Cookie0))
        resp2 = build_opener(HTTPCookieProcessor(Cookie1))
    actionDone = []
    csrf = ''
    ref_detect = 0
    ori_detect = 0
    form = Debugger.Form_Debugger()
    bs1 = BeautifulSoup(form1).findAll('form', action=True)[0]
    bs2 = BeautifulSoup(form2).findAll('form', action=True)[0]
    init1 = web
    hdrs = [('Cookie', ','.join(cookie for cookie in COOKIE_VALUE))]
    [hdrs.append((k, v)) for k, v in HEADER_VALUES.items()]
    resp1.addheaders = resp2.addheaders = hdrs
    resp1.open(init1)
    resp2.open(init1)
    try:
        url = CRAWL_SITE or web
        try:
            response = Get(url).text
            verbout(O, 'Trying to parse response...')
            soup = BeautifulSoup(response)
        except AttributeError:
            verbout(R, 'No response received, site probably down: ' + url)

        i = 0
        if REFERER_ORIGIN_CHECKS:
            verbout(O, 'Checking endpoint request validation via ' + color.GREY + 'Referer' + color.END + ' Checks...')
            if Referer(url):
                ref_detect = 1
            verbout(O, 'Confirming the vulnerability...')
            verbout(O, 'Confirming endpoint request validation via ' + color.GREY + 'Origin' + color.END + ' Checks...')
            if Origin(url):
                ori_detect = 1
            verbout(O, 'Retrieving all forms on ' + color.GREY + url + color.END + '...')
            for m in Debugger.getAllForms(soup):
                verbout(O, 'Testing form:\n' + color.CYAN)
                formPrettify(m.prettify())
                verbout('', '')
                FORMS_TESTED.append('(i) ' + url + ':\n\n' + m.prettify() + '\n')
                try:
                    if m['action']:
                        pass
                except KeyError:
                    m['action'] = '/' + url.rsplit('/', 1)[1]
                    ErrorLogger(url, 'No standard form "action".')

                action = Parser.buildAction(url, m['action'])
                if action not in actionDone:
                    if action != '':
                        if FORM_SUBMISSION:
                            try:
                                result, genpoc = form.prepareFormInputs(m)
                                r1 = Post(url, action, result)
                                result, genpoc = form.prepareFormInputs(m)
                                r2 = Post(url, action, result)
                                if COOKIE_BASED:
                                    Cookie(url, r1)
                                else:
                                    try:
                                        if m['name']:
                                            query, token = Entropy(result, url, r1.headers, m.prettify(), m['action'], m['name'])
                                    except KeyError:
                                        query, token = Entropy(result, url, r1.headers, m.prettify(), m['action'])

                                    fnd, detct = Encoding(token)
                                    if fnd == 1:
                                        if detct:
                                            VulnLogger(url, 'Token is a string encoded value which can be probably decrypted.', '[i] Encoding: ' + detct)
                                    else:
                                        NovulLogger(url, 'Anti-CSRF token is not a string encoded value.')
                                    if query:
                                        if token:
                                            txor = Tamper(url, action, result, r2.text, query, token)
                                    o2 = Get(url).text
                                    try:
                                        form2 = Debugger.getAllForms(BeautifulSoup(o2))[i]
                                    except IndexError:
                                        verbout(R, 'Form Index Error')
                                        ErrorLogger(url, 'Form Index Error.')
                                        continue

                                    verbout(GR, 'Preparing form inputs...')
                                    contents2, genpoc = form.prepareFormInputs(form2)
                                    r3 = Post(url, action, contents2)
                                    if POST_BASED and (not query or txor):
                                        try:
                                            if m['name']:
                                                PostBased(url, r1.text, r2.text, r3.text, action, result, genpoc, m.prettify(), m['name'])
                                        except KeyError:
                                            PostBased(url, r1.text, r2.text, r3.text, action, result, genpoc, m.prettify())

                                    else:
                                        print(color.GREEN + ' [+] The form was requested with a Anti-CSRF token.')
                                        print(color.GREEN + ' [+] Endpoint ' + color.BG + ' NOT VULNERABLE ' + color.END + color.GREEN + ' to POST-Based CSRF Attacks!')
                                        NovulLogger(url, 'Not vulnerable to POST-Based CSRF Attacks.')
                            except HTTPError as msg:
                                verbout(R, 'Exception : ' + msg.__str__())
                                ErrorLogger(url, msg)

                actionDone.append(action)
                i += 1

        else:
            verbout(GR, 'Initializing crawling and scanning...')
            crawler = Crawler.Handler(init1, resp1)
            while crawler.noinit():
                url = next(crawler)
                print(C + 'Testing :> ' + color.CYAN + url)
                try:
                    soup = crawler.process(fld)
                    if not soup:
                        continue
                    i = 0
                    if REFERER_ORIGIN_CHECKS:
                        verbout(O, 'Checking endpoint request validation via ' + color.GREY + 'Referer' + color.END + ' Checks...')
                        if Referer(url):
                            ref_detect = 1
                        verbout(O, 'Confirming the vulnerability...')
                        verbout(O, 'Confirming endpoint request validation via ' + color.GREY + 'Origin' + color.END + ' Checks...')
                        if Origin(url):
                            ori_detect = 1
                    verbout(O, 'Retrieving all forms on ' + color.GREY + url + color.END + '...')
                    for m in Debugger.getAllForms(soup):
                        FORMS_TESTED.append('(i) ' + url + ':\n\n' + m.prettify() + '\n')
                        try:
                            if m['action']:
                                pass
                        except KeyError:
                            m['action'] = '/' + url.rsplit('/', 1)[1]
                            ErrorLogger(url, 'No standard "action" attribute.')

                        action = Parser.buildAction(url, m['action'])
                        if action not in actionDone:
                            if action != '':
                                if FORM_SUBMISSION:
                                    try:
                                        result, genpoc = form.prepareFormInputs(m)
                                        r1 = Post(url, action, result)
                                        result, genpoc = form.prepareFormInputs(m)
                                        r2 = Post(url, action, result)
                                        if COOKIE_BASED:
                                            Cookie(url, r1)
                                        else:
                                            try:
                                                if m['name']:
                                                    query, token = Entropy(result, url, r1.headers, m.prettify(), m['action'], m['name'])
                                            except KeyError:
                                                query, token = Entropy(result, url, r1.headers, m.prettify(), m['action'])
                                                ErrorLogger(url, 'No standard form "name".')

                                            fnd, detct = Encoding(token)
                                            if fnd == 1:
                                                if detct:
                                                    VulnLogger(url, 'String encoded token value. Token might be decrypted.', '[i] Encoding: ' + detct)
                                            else:
                                                NovulLogger(url, 'Anti-CSRF token is not a string encoded value.')
                                            if query:
                                                if token:
                                                    txor = Tamper(url, action, result, r2.text, query, token)
                                            o2 = Get(url).text
                                            try:
                                                form2 = Debugger.getAllForms(BeautifulSoup(o2))[i]
                                            except IndexError:
                                                verbout(R, 'Form Index Error')
                                                ErrorLogger(url, 'Form Index Error.')
                                                continue

                                            verbout(GR, 'Preparing form inputs...')
                                            contents2, genpoc = form.prepareFormInputs(form2)
                                            r3 = Post(url, action, contents2)
                                            if POST_BASED and (query == '' or txor == True):
                                                try:
                                                    if m['name']:
                                                        PostBased(url, r1.text, r2.text, r3.text, m['action'], result, genpoc, m.prettify(), m['name'])
                                                except KeyError:
                                                    PostBased(url, r1.text, r2.text, r3.text, m['action'], result, genpoc, m.prettify())

                                            else:
                                                print(color.GREEN + ' [+] The form was requested with a Anti-CSRF token.')
                                                print(color.GREEN + ' [+] Endpoint ' + color.BG + ' NOT VULNERABLE ' + color.END + color.GREEN + ' to P0ST-Based CSRF Attacks!')
                                                NovulLogger(url, 'Not vulnerable to POST-Based CSRF Attacks.')
                                    except HTTPError as msg:
                                        verbout(color.RED, ' [-] Exception : ' + color.END + msg.__str__())
                                        ErrorLogger(url, msg)

                        actionDone.append(action)
                        i += 1

                except HTTPError as e:
                    if str(e.code) == '403':
                        verbout(R, 'HTTP Authentication Error!')
                        verbout(R, 'Error Code : ' + O + str(e.code))
                        ErrorLogger(url, e)
                        quit()
                except URLError as e:
                    verbout(R, 'Exception at : ' + url)
                    time.sleep(0.4)
                    verbout(O, 'Moving on...')
                    ErrorLogger(url, e)
                    continue

        GetLogger()
        print('\n' + G + 'Scan completed!' + '\n')
        Analysis()
    except KeyboardInterrupt as e:
        verbout(R, 'User Interrupt!')
        time.sleep(1.5)
        Analysis()
        print(R + 'Aborted!')
        ErrorLogger('KeyBoard Interrupt', 'Aborted')
        GetLogger()
        sys.exit(1)
    except Exception as e:
        print('\n' + R + 'Encountered an error. \n')
        print(R + 'Please view the error log files to view what went wrong.')
        verbout(R, e.__str__())
        ErrorLogger(url, e)
        GetLogger()