# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/options.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 8811 bytes
import argparse, sys, tld, urllib.parse, os, re
from xsrfprobe.files import config
from xsrfprobe.core.colors import R, G
from xsrfprobe.core.updater import updater
from xsrfprobe.files.dcodelist import IP
from xsrfprobe import __version__, __license__
print('\n    \x1b[1;91mXSRFProbe\x1b[0m, \x1b[1;97mA \x1b[1;93mCross Site Request Forgery \x1b[1;97mAudit Toolkit\x1b[0m\n')
parser = argparse.ArgumentParser(usage='xsrfprobe -u <url> <args>')
parser._action_groups.pop()
required = parser.add_argument_group('Required Arguments')
optional = parser.add_argument_group('Optional Arguments')
required.add_argument('-u', '--url', help='Main URL to test', dest='url')
optional.add_argument('-c', '--cookie', help='Cookie value to be requested with each successive request. If there are multiple cookies, separate them with commas. For example: `-c PHPSESSID=i837c5n83u4, _gid=jdhfbuysf`.', dest='cookie')
optional.add_argument('-o', '--output', help='Output directory where files to be stored. Default is the output/ folder where all files generated will be stored.', dest='output')
optional.add_argument('-d', '--delay', help='Time delay between requests in seconds. Default is zero.', dest='delay', type=float)
optional.add_argument('-q', '--quiet', help='Set the DEBUG mode to quiet. Report only when vulnerabilities are found. Minimal output will be printed on screen. ', dest='quiet', action='store_true')
optional.add_argument('-H', '--headers', help='Comma separated list of custom headers you\'d want to use. For example: ``--headers "Accept=text/php, X-Requested-With=Dumb"``.', dest='headers', type=str)
optional.add_argument('-v', '--verbose', help='Increase the verbosity of the output (e.g., -vv is more than -v). ', dest='verbose', action='store_true')
optional.add_argument('-t', '--timeout', help='HTTP request timeout value in seconds. The entered value may be either in floating point decimal or an integer. Example: ``--timeout 10.0``', dest='timeout', type=(float or int))
optional.add_argument('-E', '--exclude', help="Comma separated list of paths or directories to be excluded which are not in scope. These paths/dirs won't be scanned. For example: `--exclude somepage/, sensitive-dir/, pleasedontscan/`", dest='exclude', type=str)
optional.add_argument('--user-agent', help='Custom user-agent to be used. Only one user-agent can be specified.', dest='user_agent', type=str)
optional.add_argument('--max-chars', help='Maximum allowed character length for the custom token value to be generated. For example: `--max-chars 5`. Default value is 6.', dest='maxchars', type=int)
optional.add_argument('--crawl', help='Crawl the whole site and simultaneously test all discovered endpoints for CSRF.', dest='crawl', action='store_true')
optional.add_argument('--no-analysis', help='Skip the Post-Scan Analysis of Tokens which were gathered during requests', dest='skipal', action='store_true')
optional.add_argument('--malicious', help='Generate a malicious CSRF Form which can be used in real-world exploits.', dest='malicious', action='store_true')
optional.add_argument('--skip-poc', help='Skip the PoC Form Generation of POST-Based Cross Site Request Forgeries.', dest='skippoc', action='store_true')
optional.add_argument('--no-verify', help='Do not verify SSL certificates with requests.', dest='no_verify', action='store_true')
optional.add_argument('--display', help='Print out response headers of requests while making requests.', dest='disphead', action='store_true')
optional.add_argument('--update', help='Update XSRFProbe to latest version on GitHub via git.', dest='update', action='store_true')
optional.add_argument('--random-agent', help='Use random user-agents for making requests.', dest='randagent', action='store_true')
optional.add_argument('--version', help='Display the version of XSRFProbe and exit.', dest='version', action='store_true')
args = parser.parse_args()
if not len(sys.argv) > 1:
    parser.print_help()
    quit()
if args.update:
    updater()
    quit()
if args.version:
    print('\x1b[1;96m [+] \x1b[1;91mXSRFProbe Version\x1b[0m : v' + __version__)
    print('\x1b[1;96m [+] \x1b[1;91mXSRFProbe License\x1b[0m : ' + __license__ + '\n')
    quit()
if args.maxchars:
    config.TOKEN_GENERATION_LENGTH = args.maxchars
if args.user_agent:
    config.USER_AGENT = args.user_agent
if args.skipal:
    config.SCAN_ANALYSIS = False
if args.skippoc:
    config.POC_GENERATION = False
if args.malicious:
    config.GEN_MALICIOUS = True
if not args.version:
    if not args.update:
        if args.url:
            if 'http' in args.url:
                config.SITE_URL = args.url
            else:
                config.SITE_URL = 'http://' + args.url
        else:
            print(R + 'You must supply a url/endpoint.')
if args.crawl:
    config.CRAWL_SITE = True
    config.DISPLAY_HEADERS = False
if args.cookie:
    for cook in args.cookie.split(','):
        config.COOKIE_VALUE.append(cook)
        config.USER_AGENT_RANDOM = False

if args.disphead:
    config.DISPLAY_HEADERS = True
if args.no_verify:
    config.VERIFY_CERT = False
if args.timeout:
    config.TIMEOUT_VALUE = args.timeout
if args.headers:
    for m in args.headers.split(','):
        config.HEADER_VALUES[m.split('=')[0].strip()] = m.split('=')[1].strip()

if args.exclude:
    exc = args.exclude
    m = exc.split(',').strip()
    for s in m:
        config.EXCLUDE_DIRS.append(urllib.parse.urljoin(config.SITE_URL, s))

if args.randagent:
    config.USER_AGENT_RANDOM = True
    config.USER_AGENT = ''
if config.SITE_URL:
    try:
        if args.output:
            try:
                if not os.path.exists(args.output + tld.get_fld(config.SITE_URL)):
                    os.makedirs(args.output + tld.get_fld(config.SITE_URL))
            except FileExistsError:
                pass

            config.OUTPUT_DIR = args.output + tld.get_fld(config.SITE_URL) + '/'
        else:
            try:
                os.makedirs('xsrfprobe-output/' + tld.get_fld(config.SITE_URL))
            except FileExistsError:
                pass

            config.OUTPUT_DIR = 'xsrfprobe-output/' + tld.get_fld(config.SITE_URL) + '/'
    except tld.exceptions.TldDomainNotFound:
        direc = re.search(IP, config.SITE_URL).group(0)
        if args.output:
            try:
                if not os.path.exists(args.output + direc):
                    os.makedirs(args.output + direc)
            except FileExistsError:
                pass

            config.OUTPUT_DIR = args.output + direc + '/'
        else:
            try:
                os.makedirs('xsrfprobe-output/' + direc)
            except FileExistsError:
                pass

            config.OUTPUT_DIR = 'xsrfprobe-output/' + direc + '/'

if args.quiet:
    config.DEBUG = False