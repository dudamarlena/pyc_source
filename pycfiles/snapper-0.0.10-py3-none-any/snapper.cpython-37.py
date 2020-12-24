# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/revisor/Documents/Snapper/snapper.py
# Compiled at: 2019-07-08 22:22:16
# Size of source mod 2**32: 8123 bytes
import sys, os
from jinja2 import Environment, PackageLoader
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from optparse import OptionParser
from multiprocessing import Process, Queue
from os import chdir
from shutil import copyfile
from requests import get
from uuid import uuid4
from selenium.common.exceptions import TimeoutException
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

try:
    import SimpleHTTPServer
except ImportError:
    import http.server as SimpleHTTPServer

env = Environment(autoescape=True, loader=(PackageLoader('snapper', 'templates')))

def save_image(uri, file_name, driver):
    try:
        driver.get(uri)
        driver.save_screenshot(file_name)
        return True
    except TimeoutException:
        return False


def host_reachable(host, timeout):
    try:
        get(host, timeout=timeout, verify=False)
        return True
    except TimeoutException:
        return False


def host_worker--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              dict
                2  LOAD_GLOBAL              DesiredCapabilities
                4  LOAD_ATTR                PHANTOMJS
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  STORE_FAST               'dcap'

 L.  47        10  LOAD_FAST                'user_agent'
               12  LOAD_FAST                'dcap'
               14  LOAD_STR                 'phantomjs.page.settings.userAgent'
               16  STORE_SUBSCR     

 L.  48        18  LOAD_CONST               True
               20  LOAD_FAST                'dcap'
               22  LOAD_STR                 'accept_untrusted_certs'
               24  STORE_SUBSCR     

 L.  50        26  LOAD_GLOBAL              webdriver
               28  LOAD_ATTR                PhantomJS
               30  LOAD_STR                 '--ignore-ssl-errors=true'
               32  BUILD_LIST_1          1 

 L.  51        34  LOAD_FAST                'dcap'
               36  LOAD_CONST               ('service_args', 'desired_capabilities')
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  STORE_FAST               'driver'

 L.  53        42  LOAD_FAST                'driver'
               44  LOAD_METHOD              set_window_size
               46  LOAD_CONST               1024
               48  LOAD_CONST               768
               50  CALL_METHOD_2         2  '2 positional arguments'
               52  POP_TOP          

 L.  54        54  LOAD_FAST                'driver'
               56  LOAD_METHOD              set_page_load_timeout
               58  LOAD_FAST                'timeout'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  POP_TOP          

 L.  55     64_66  SETUP_LOOP          434  'to 434'
             68_0  COME_FROM           416  '416'
               68  LOAD_FAST                'hostQueue'
               70  LOAD_METHOD              empty
               72  CALL_METHOD_0         0  '0 positional arguments'
            74_76  POP_JUMP_IF_TRUE    432  'to 432'

 L.  56        78  LOAD_FAST                'hostQueue'
               80  LOAD_METHOD              get
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  STORE_FAST               'host'

 L.  57        86  LOAD_FAST                'host'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'http://'
               92  CALL_METHOD_1         1  '1 positional argument'
            94_96  POP_JUMP_IF_TRUE    328  'to 328'
               98  LOAD_FAST                'host'
              100  LOAD_METHOD              startswith
              102  LOAD_STR                 'https://'
              104  CALL_METHOD_1         1  '1 positional argument'
          106_108  POP_JUMP_IF_TRUE    328  'to 328'

 L.  58       110  LOAD_STR                 'http://'
              112  LOAD_FAST                'host'
              114  BINARY_ADD       
              116  STORE_FAST               'host1'

 L.  59       118  LOAD_STR                 'https://'
              120  LOAD_FAST                'host'
              122  BINARY_ADD       
              124  STORE_FAST               'host2'

 L.  60       126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              join
              132  LOAD_STR                 'output'
              134  LOAD_STR                 'images'
              136  LOAD_GLOBAL              str
              138  LOAD_GLOBAL              uuid4
              140  CALL_FUNCTION_0       0  '0 positional arguments'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  LOAD_STR                 '.png'
              146  BINARY_ADD       
              148  CALL_METHOD_3         3  '3 positional arguments'
              150  STORE_FAST               'filename1'

 L.  61       152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              join
              158  LOAD_STR                 'output'
              160  LOAD_STR                 'images'
              162  LOAD_GLOBAL              str
              164  LOAD_GLOBAL              uuid4
              166  CALL_FUNCTION_0       0  '0 positional arguments'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  LOAD_STR                 '.png'
              172  BINARY_ADD       
              174  CALL_METHOD_3         3  '3 positional arguments'
              176  STORE_FAST               'filename2'

 L.  62       178  LOAD_FAST                'verbose'
              180  POP_JUMP_IF_FALSE   194  'to 194'

 L.  63       182  LOAD_GLOBAL              print
              184  LOAD_STR                 'Fetching %s'
              186  LOAD_FAST                'host1'
              188  BINARY_MODULO    
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  POP_TOP          
            194_0  COME_FROM           180  '180'

 L.  64       194  LOAD_GLOBAL              host_reachable
              196  LOAD_FAST                'host1'
              198  LOAD_FAST                'timeout'
              200  CALL_FUNCTION_2       2  '2 positional arguments'
              202  POP_JUMP_IF_FALSE   232  'to 232'
              204  LOAD_GLOBAL              save_image
              206  LOAD_FAST                'host1'
              208  LOAD_FAST                'filename1'

 L.  65       210  LOAD_FAST                'driver'
              212  CALL_FUNCTION_3       3  '3 positional arguments'
              214  POP_JUMP_IF_FALSE   232  'to 232'

 L.  66       216  LOAD_FAST                'fileQueue'
              218  LOAD_METHOD              put
              220  LOAD_FAST                'host1'
              222  LOAD_FAST                'filename1'
              224  BUILD_MAP_1           1 
              226  CALL_METHOD_1         1  '1 positional argument'
              228  POP_TOP          
              230  JUMP_FORWARD        248  'to 248'
            232_0  COME_FROM           214  '214'
            232_1  COME_FROM           202  '202'

 L.  68       232  LOAD_FAST                'verbose'
              234  POP_JUMP_IF_FALSE   248  'to 248'

 L.  69       236  LOAD_GLOBAL              print
              238  LOAD_STR                 '%s is unreachable or timed out'
              240  LOAD_FAST                'host1'
              242  BINARY_MODULO    
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  POP_TOP          
            248_0  COME_FROM           234  '234'
            248_1  COME_FROM           230  '230'

 L.  70       248  LOAD_FAST                'verbose'
          250_252  POP_JUMP_IF_FALSE   266  'to 266'

 L.  71       254  LOAD_GLOBAL              print
              256  LOAD_STR                 'Fetching %s'
              258  LOAD_FAST                'host2'
              260  BINARY_MODULO    
              262  CALL_FUNCTION_1       1  '1 positional argument'
              264  POP_TOP          
            266_0  COME_FROM           250  '250'

 L.  72       266  LOAD_GLOBAL              host_reachable
              268  LOAD_FAST                'host2'
              270  LOAD_FAST                'timeout'
              272  CALL_FUNCTION_2       2  '2 positional arguments'
          274_276  POP_JUMP_IF_FALSE   308  'to 308'
              278  LOAD_GLOBAL              save_image
              280  LOAD_FAST                'host2'
              282  LOAD_FAST                'filename2'

 L.  73       284  LOAD_FAST                'driver'
              286  CALL_FUNCTION_3       3  '3 positional arguments'
          288_290  POP_JUMP_IF_FALSE   308  'to 308'

 L.  74       292  LOAD_FAST                'fileQueue'
              294  LOAD_METHOD              put
              296  LOAD_FAST                'host2'
              298  LOAD_FAST                'filename2'
              300  BUILD_MAP_1           1 
              302  CALL_METHOD_1         1  '1 positional argument'
              304  POP_TOP          
              306  JUMP_FORWARD        326  'to 326'
            308_0  COME_FROM           288  '288'
            308_1  COME_FROM           274  '274'

 L.  76       308  LOAD_FAST                'verbose'
          310_312  POP_JUMP_IF_FALSE   430  'to 430'

 L.  77       314  LOAD_GLOBAL              print
              316  LOAD_STR                 '%s is unreachable or timed out'
              318  LOAD_FAST                'host2'
              320  BINARY_MODULO    
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  POP_TOP          
            326_0  COME_FROM           306  '306'
              326  JUMP_BACK            68  'to 68'
            328_0  COME_FROM           106  '106'
            328_1  COME_FROM            94  '94'

 L.  79       328  LOAD_GLOBAL              os
              330  LOAD_ATTR                path
              332  LOAD_METHOD              join
              334  LOAD_STR                 'output'
              336  LOAD_STR                 'images'
              338  LOAD_GLOBAL              str
              340  LOAD_GLOBAL              uuid4
              342  CALL_FUNCTION_0       0  '0 positional arguments'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  LOAD_STR                 '.png'
              348  BINARY_ADD       
              350  CALL_METHOD_3         3  '3 positional arguments'
              352  STORE_FAST               'filename'

 L.  80       354  LOAD_FAST                'verbose'
          356_358  POP_JUMP_IF_FALSE   372  'to 372'

 L.  81       360  LOAD_GLOBAL              print
              362  LOAD_STR                 'Fetching %s'
              364  LOAD_FAST                'host'
              366  BINARY_MODULO    
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  POP_TOP          
            372_0  COME_FROM           356  '356'

 L.  82       372  LOAD_GLOBAL              host_reachable
              374  LOAD_FAST                'host'
              376  LOAD_FAST                'timeout'
              378  CALL_FUNCTION_2       2  '2 positional arguments'
          380_382  POP_JUMP_IF_FALSE   414  'to 414'
              384  LOAD_GLOBAL              save_image
              386  LOAD_FAST                'host'
              388  LOAD_FAST                'filename'

 L.  83       390  LOAD_FAST                'driver'
              392  CALL_FUNCTION_3       3  '3 positional arguments'
          394_396  POP_JUMP_IF_FALSE   414  'to 414'

 L.  84       398  LOAD_FAST                'fileQueue'
              400  LOAD_METHOD              put
              402  LOAD_FAST                'host'
              404  LOAD_FAST                'filename'
              406  BUILD_MAP_1           1 
              408  CALL_METHOD_1         1  '1 positional argument'
              410  POP_TOP          
              412  JUMP_BACK            68  'to 68'
            414_0  COME_FROM           394  '394'
            414_1  COME_FROM           380  '380'

 L.  86       414  LOAD_FAST                'verbose'
              416  POP_JUMP_IF_FALSE    68  'to 68'

 L.  87       418  LOAD_GLOBAL              print
              420  LOAD_STR                 '%s is unreachable or timed out'
              422  LOAD_FAST                'host'
              424  BINARY_MODULO    
              426  CALL_FUNCTION_1       1  '1 positional argument'
              428  POP_TOP          
            430_0  COME_FROM           310  '310'
              430  JUMP_BACK            68  'to 68'
            432_0  COME_FROM            74  '74'
              432  POP_BLOCK        
            434_0  COME_FROM_LOOP       64  '64'

Parse error at or near `POP_BLOCK' instruction at offset 432


def capture_snaps(hosts, outpath, timeout=10, serve=False, port=8000, verbose=True, numWorkers=1, user_agent='Mozilla/5.0                   (Windows NT6.1) AppleWebKit/537.36 (KHTML,like Gecko)                   Chrome/41.0.2228.0 Safari/537.36'):
    outpath = os.path.joinoutpath'output'
    cssOutputPath = os.path.joinoutpath'css'
    jsOutputPath = os.path.joinoutpath'js'
    imagesOutputPath = os.path.joinoutpath'images'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    if not os.path.exists(imagesOutputPath):
        os.makedirs(imagesOutputPath)
    if not os.path.exists(cssOutputPath):
        os.makedirs(cssOutputPath)
    if not os.path.exists(jsOutputPath):
        os.makedirs(jsOutputPath)
    else:
        cssTemplatePath = os.path.joinos.path.dirname(os.path.realpath(__file__))'templates''css'
        jsTemplatePath = os.path.joinos.path.dirname(os.path.realpath(__file__))'templates''js'
        copyfile(os.path.joincssTemplatePath'materialize.min.css', os.path.joincssOutputPath'materialize.min.css')
        copyfile(os.path.joinjsTemplatePath'jquery.min.js', os.path.joinjsOutputPath'jquery.min.js')
        copyfile(os.path.joinjsTemplatePath'materialize.min.js', os.path.joinjsOutputPath'materialize.min.js')
        hostQueue = Queue()
        fileQueue = Queue()
        workers = []
        for host in hosts:
            hostQueue.put(host)

        for i in range(numWorkers):
            p = Process(target=host_worker, args=(hostQueue, fileQueue, timeout,
             user_agent, verbose))
            workers.append(p)
            p.start()

        try:
            for worker in workers:
                worker.join()

        except KeyboardInterrupt:
            for worker in workers:
                worker.terminate()
                worker.join()

            sys.exit()

        setsOfSix = []
        count = 0
        hosts = {}
        while not fileQueue.empty():
            if count == 6:
                try:
                    setsOfSix.append(hosts.iteritems())
                except AttributeError:
                    setsOfSix.append(hosts.items())

                hosts = {}
                count = 0
            temp = fileQueue.get()
            hosts.update(temp)

        try:
            setsOfSix.append(hosts.iteritems())
        except AttributeError:
            setsOfSix.append(hosts.items())

        template = env.get_template('index.html')
        with open(os.path.joinoutpath'index.html', 'w') as (outputFile):
            outputFile.write(template.render(setsOfSix=setsOfSix))
        if serve:
            chdir('output')
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer('127.0.0.1', PORT)Handler
            print('Serving at port', PORT)
            httpd.serve_forever()
        else:
            return True


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', dest='filename', help='Souce from input file',
      metavar='FILE')
    parser.add_option('-l', '--list', action='store', dest='list', help='Source from commandline list')
    parser.add_option('-u', '--user-agent', action='store', dest='user_agent',
      type=str,
      default='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36                       (KHTML,like Gecko) Chrome/41.0.2228.0 Safari/537.36',
      help='The user agent used for requests')
    parser.add_option('-c', '--concurrency', action='store', dest='numWorkers',
      type=int,
      default=1,
      help='Number of cuncurrent processes')
    parser.add_option('-t', '--timeout', action='store', dest='timeout',
      type=int,
      default=10,
      help='Number of seconds to try to resolve')
    parser.add_option('-p', '--port', action='store', dest='port',
      type=int,
      default=8000,
      help='Port to run server on')
    parser.add_option('-v', action='store_true', dest='verbose', help='Display console output for fetching each host')
    options, args = parser.parse_args()
    if options.filename:
        with open(options.filename, 'r') as (inputFile):
            hosts = inputFile.readlines()
            hosts = map(lambda s: s.strip(), hosts)
    else:
        if options.list:
            hosts = []
            for item in options.list.split(','):
                hosts.append(item.strip())

        else:
            print('invalid args')
            sys.exit()
    numWorkers = options.numWorkers
    timeout = options.timeout
    verbose = options.verbose
    PORT = options.port
    user_agent = options.user_agent
    sys.webbrowser.open_new_tab('http://127.0.0.1:%s/' % PORT)
    capture_snaps(hosts, os.getcwd(), timeout, True, PORT, verbose, numWorkers, user_agent)