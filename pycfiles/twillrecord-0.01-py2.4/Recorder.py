# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twillrecord/Recorder.py
# Compiled at: 2007-03-22 07:23:51
"""TCPWatch FunkLoad Test Recorder.

Requires tcpwatch.py available at:

* http://hathawaymix.org/Software/TCPWatch/tcpwatch-1.3.tar.gz

Credits goes to Ian Bicking for parsing tcpwatch files.

$Id: Recorder.py 33463 2006-02-24 14:09:21Z bdelbosc $
"""
import os, sys, re
from cStringIO import StringIO
from optparse import OptionParser, TitledHelpFormatter
from tempfile import mkdtemp
import rfc822
from cgi import FieldStorage
from urlparse import urlsplit
from utils import truncate, trace, get_version

class Request:
    """Store a tcpwatch request."""
    __module__ = __name__

    def __init__(self, file_path):
        """Load a tcpwatch request file."""
        self.file_path = file_path
        f = open(file_path, 'rb')
        line = f.readline().split(None, 2)
        if not line:
            trace('# Warning: empty first line on %s\n' % self.file_path)
            line = f.readline().split(None, 2)
        self.method = line[0]
        url = line[1]
        (scheme, host, path, query, fragment) = urlsplit(url)
        self.host = scheme + '://' + host
        self.rurl = url[len(self.host):]
        self.url = url
        self.path = path
        self.version = line[2].strip()
        self.headers = dict(rfc822.Message(f).items())
        self.body = f.read()
        f.close()
        return

    def extractParam(self):
        """Turn muti part encoded form into params."""
        environ = {'CONTENT_TYPE': self.headers['content-type'], 'CONTENT_LENGTH': self.headers['content-length'], 'REQUEST_METHOD': 'POST'}
        form = FieldStorage(fp=StringIO(self.body), environ=environ, keep_blank_values=True)
        params = []
        try:
            keys = form.keys()
        except TypeError:
            trace('# Warning: skipping invalid http post param in file: %s may be an xmlrpc call ?\n' % self.file_path)
            return params

        for key in keys:
            if not isinstance(form[key], list):
                values = [
                 form[key]]
            else:
                values = form[key]
            for form_value in values:
                filename = form_value.filename
                if filename is None:
                    params.append([key, form_value.value])
                else:
                    filename = filename or ''
                    params.append([key, 'Upload("%s")' % filename])
                    if filename:
                        if os.path.exists(filename):
                            trace('# Warning: uploaded file: %s already exists, keep it.\n' % filename)
                        else:
                            trace('# Saving uploaded file: %s\n' % filename)
                            f = open(filename, 'w')
                            f.write(str(form_value.value))
                            f.close()

        return params

    def __repr__(self):
        params = ''
        if self.body:
            params = self.extractParam()
        return '<request method="%s" url="%s" %s/>' % (self.method, self.url, str(params))


class Response:
    """Store a tcpwatch response."""
    __module__ = __name__

    def __init__(self, file_path):
        """Load a tcpwatch response file."""
        self.file_path = file_path
        f = open(file_path, 'rb')
        line = f.readline().split(None, 2)
        self.version = line[0]
        self.status_code = line[1].strip()
        if len(line) > 2:
            self.status_message = line[2].strip()
        else:
            self.status_message = ''
        self.headers = dict(rfc822.Message(f).items())
        self.body = f.read()
        f.close()
        return

    def __repr__(self):
        return '<response code="%s" type="%s" status="%s" />' % (self.status_code, self.headers.get('content-type'), self.status_message)


class RecorderProgram:
    """A tcpwatch to funkload recorder."""
    __module__ = __name__
    USAGE = '%prog [options] [test_name]\n\n%prog launch a TCPWatch proxy and record activities, then output\na FunkLoad script or generates a FunkLoad unit test if test_name is specified.\n\nThe default proxy port is 8090.\n\nNote that tcpwatch.py executable must be accessible from your env.\n\nSee http://funkload.nuxeo.org/ for more information.\n\nExamples\n========\n  %prog foo_bar\n                        Run a proxy and create a FunkLoad test case,\n                        generates test_FooBar.py and FooBar.conf file.\n                        To test it:  fl-run-test -dV test_FooBar.py\n  %prog -p 9090\n                        Run a proxy on port 9090, output script to stdout.\n  %prog -i /tmp/tcpwatch\n                        Convert a tcpwatch capture into a script.\n'

    def __init__(self, argv=None):
        if argv is None:
            argv = sys.argv[1:]
        self.verbose = False
        self.tcpwatch_path = None
        self.prefix = 'watch'
        self.port = '8090'
        self.server_url = None
        self.class_name = None
        self.test_name = None
        self.script_path = None
        self.configuration_path = None
        self.parseArgs(argv)
        return

    def parseArgs(self, argv):
        """Parse programs args."""
        parser = OptionParser(self.USAGE, formatter=TitledHelpFormatter(), version='FunkLoad %s' % get_version())
        parser.add_option('-v', '--verbose', action='store_true', help='Verbose output')
        parser.add_option('-p', '--port', type='string', dest='port', default=self.port, help='The proxy port.')
        parser.add_option('-i', '--tcp-watch-input', type='string', dest='tcpwatch_path', default=None, help='Path to an existing tcpwatch capture.')
        (options, args) = parser.parse_args(argv)
        if len(args) == 1:
            test_name = args[0]
        else:
            test_name = None
        self.verbose = options.verbose
        self.tcpwatch_path = options.tcpwatch_path
        self.port = options.port
        if test_name:
            class_name = ('').join([ x.capitalize() for x in re.split('_|-', test_name) ])
            self.test_name = test_name
            self.class_name = class_name
            self.script_path = './%s.twill' % class_name
        return

    def startProxy(self):
        """Start a tcpwatch session."""
        self.tcpwatch_path = mkdtemp('_funkload')
        cmd = 'tcpwatch.py -p %s -s -r %s' % (self.port, self.tcpwatch_path)
        if self.verbose:
            cmd += ' | grep "T http"'
        else:
            cmd += ' > /dev/null'
        trace('Hit Ctrl-C to stop recording.\n')
        os.system(cmd)

    def searchFiles(self):
        """Search tcpwatch file."""
        items = {}
        prefix = self.prefix
        for filename in os.listdir(self.tcpwatch_path):
            if not filename.startswith(prefix):
                continue
            (name, ext) = os.path.splitext(filename)
            name = name[len(self.prefix):]
            ext = ext[1:]
            if ext == 'errors':
                trace('Error in response %s\n' % name)
                continue
            assert ext in ('request', 'response'), 'Bad extension: %r' % ext
            items.setdefault(name, {})[ext] = os.path.join(self.tcpwatch_path, filename)

        items = items.items()
        items.sort()
        return [ (v['request'], v['response']) for (name, v) in items if v.has_key('response') ]

    def extractRequests--- This code section failed: ---

 L. 236         0  LOAD_CONST               None
                3  STORE_FAST            6  'last_code'

 L. 237         6  LOAD_CONST               ('image', 'css', 'javascript')
                9  STORE_FAST           12  'filter_ctypes'

 L. 238        12  LOAD_CONST               ('.jpg', '.png', '.gif', '.css', '.js')
               15  STORE_FAST           11  'filter_url'

 L. 239        18  BUILD_LIST_0          0 
               21  STORE_FAST           10  'requests'

 L. 240        24  SETUP_LOOP          284  'to 311'
               27  LOAD_FAST             1  'files'
               30  GET_ITER         
               31  FOR_ITER            276  'to 310'
               34  UNPACK_SEQUENCE_2     2 
               37  STORE_FAST           13  'request_path'
               40  STORE_FAST            7  'response_path'

 L. 241        43  LOAD_GLOBAL           8  'Response'
               46  LOAD_FAST             7  'response_path'
               49  CALL_FUNCTION_1       1  None
               52  STORE_FAST            9  'response'

 L. 242        55  LOAD_GLOBAL          10  'Request'
               58  LOAD_FAST            13  'request_path'
               61  CALL_FUNCTION_1       1  None
               64  STORE_FAST            4  'request'

 L. 243        67  LOAD_FAST             0  'self'
               70  LOAD_ATTR            13  'server_url'
               73  LOAD_CONST               None
               76  COMPARE_OP            8  is
               79  JUMP_IF_FALSE        16  'to 98'
             82_0  THEN                     99
               82  POP_TOP          

 L. 244        83  LOAD_FAST             4  'request'
               86  LOAD_ATTR            14  'host'
               89  LOAD_FAST             0  'self'
               92  STORE_ATTR           13  'server_url'
               95  JUMP_FORWARD          1  'to 99'
             98_0  COME_FROM            79  '79'
               98  POP_TOP          
             99_0  COME_FROM            95  '95'

 L. 245        99  LOAD_FAST             9  'response'
              102  LOAD_ATTR            15  'headers'
              105  LOAD_ATTR            16  'get'
              108  LOAD_CONST               'content-type'
              111  LOAD_CONST               ''
              114  CALL_FUNCTION_2       2  None
              117  STORE_FAST            5  'ctype'

 L. 246       120  LOAD_FAST             4  'request'
              123  LOAD_ATTR            18  'url'
              126  STORE_FAST            3  'url'

 L. 247       129  LOAD_FAST             4  'request'
              132  LOAD_ATTR            19  'method'
              135  LOAD_CONST               'POST'
              138  COMPARE_OP            3  !=
              141  JUMP_IF_FALSE       134  'to 278'
            144_0  THEN                     279
              144  POP_TOP          
              145  LOAD_FAST             6  'last_code'
              148  LOAD_CONST               ('301', '302')
              151  COMPARE_OP            6  in
              154  JUMP_IF_TRUE        105  'to 262'
              157  POP_TOP          
              158  BUILD_LIST_0          0 
              161  DUP_TOP          
              162  STORE_FAST            2  '_[1]'
              165  LOAD_FAST            12  'filter_ctypes'
              168  GET_ITER         
              169  FOR_ITER             30  'to 202'
              172  STORE_FAST            8  'x'
              175  LOAD_FAST             8  'x'
              178  LOAD_FAST             5  'ctype'
              181  COMPARE_OP            6  in
              184  JUMP_IF_FALSE        11  'to 198'
              187  POP_TOP          
              188  LOAD_FAST             2  '_[1]'
              191  LOAD_FAST             8  'x'
              194  LIST_APPEND      
              195  JUMP_BACK           169  'to 169'
            198_0  COME_FROM           184  '184'
              198  POP_TOP          
              199  JUMP_BACK           169  'to 169'
              202  DELETE_FAST           2  '_[1]'
              205  JUMP_IF_TRUE         54  'to 262'
              208  POP_TOP          
              209  BUILD_LIST_0          0 
              212  DUP_TOP          
              213  STORE_FAST            2  '_[1]'
              216  LOAD_FAST            11  'filter_url'
              219  GET_ITER         
              220  FOR_ITER             33  'to 256'
              223  STORE_FAST            8  'x'
              226  LOAD_FAST             3  'url'
              229  LOAD_ATTR            22  'endswith'
              232  LOAD_FAST             8  'x'
              235  CALL_FUNCTION_1       1  None
              238  JUMP_IF_FALSE        11  'to 252'
              241  POP_TOP          
              242  LOAD_FAST             2  '_[1]'
              245  LOAD_FAST             8  'x'
              248  LIST_APPEND      
              249  JUMP_BACK           220  'to 220'
            252_0  COME_FROM           238  '238'
              252  POP_TOP          
              253  JUMP_BACK           220  'to 220'
              256  DELETE_FAST           2  '_[1]'
            259_0  COME_FROM           205  '205'
            259_1  COME_FROM           154  '154'
              259  JUMP_IF_FALSE        16  'to 278'
            262_0  THEN                     275
              262  POP_TOP          

 L. 251       263  LOAD_FAST             9  'response'
              266  LOAD_ATTR            23  'status_code'
              269  STORE_FAST            6  'last_code'

 L. 252       272  CONTINUE             31  'to 31'
              275  JUMP_FORWARD          1  'to 279'
            278_0  COME_FROM           259  '259'
            278_1  COME_FROM           141  '141'
              278  POP_TOP          
            279_0  COME_FROM           275  '275'

 L. 253       279  LOAD_FAST             9  'response'
              282  LOAD_ATTR            23  'status_code'
              285  STORE_FAST            6  'last_code'

 L. 254       288  LOAD_FAST            10  'requests'
              291  LOAD_ATTR            24  'append'
              294  LOAD_FAST             4  'request'
              297  LOAD_FAST             9  'response'
              300  BUILD_TUPLE_2         2 
              303  CALL_FUNCTION_1       1  None
              306  POP_TOP          
              307  JUMP_BACK            31  'to 31'
              310  POP_BLOCK        
            311_0  COME_FROM            24  '24'

 L. 255       311  LOAD_FAST            10  'requests'
              314  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 310

    def reindent(self, code, indent=8):
        """Improve indentation."""
        spaces = ' ' * indent
        code = code.replace('], [', '],\n%s    [' % spaces)
        code = code.replace('[[', '[\n%s    [' % spaces)
        code = code.replace(', description=', ',\n%s    description=' % spaces)
        code = code.replace('self.', '\n%sself.' % spaces)
        return code

    def convertToFunkLoad(self, request, response):
        """return a funkload python instruction."""
        text = []
        if request.method.lower() == 'get':
            text.append('go %s' % request.url)
        if request.method.lower() == 'post':
            counter = 1
            text.append('formclear %i' % counter)
            fvl = 'fv ' + str(counter) + ' '
            for param in request.extractParam():
                text.append(fvl + param[0] + ' "' + param[1] + '"')

            text.append('submit')
        return ('\n').join(text)

    def extractScript(self):
        """Convert a tcpwatch capture into a FunkLoad script."""
        files = self.searchFiles()
        requests = self.extractRequests(files)
        code = [ self.convertToFunkLoad(request, response) for (request, response) in requests ]
        if not code:
            trace('Sorry no action recorded.\n')
            return ''
        code.insert(0, '')
        return self.reindent(('\n').join(code))

    def writeScript(self, script):
        """Write the FunkLoad test script."""
        trace('Creating script: %s.\n' % self.script_path)
        if os.path.exists(self.script_path):
            trace('Error file %s already exists.\n' % self.script_path)
            return
        f = open(self.script_path, 'w')
        f.write(script)
        f.close()

    def writeConfiguration(self):
        """Write the FunkLoad configuration test script."""
        trace('Creating configuration file: %s.\n' % self.configuration_path)
        from pkg_resources import resource_string
        tpl = resource_string('funkload', 'data/ConfigurationTestCase.tpl')
        content = tpl % {'server_url': self.server_url, 'test_name': self.test_name, 'class_name': self.class_name}
        if os.path.exists(self.configuration_path):
            trace('Error file %s already exists.\n' % self.configuration_path)
            return
        f = open(self.configuration_path, 'w')
        f.write(content)
        f.close()

    def run(self):
        """run it."""
        if self.tcpwatch_path is None:
            self.startProxy()
        script = self.extractScript()
        if not script:
            return
        if self.test_name is not None:
            self.writeScript(script)
        else:
            print script
        return


if __name__ == '__main__':
    RecorderProgram().run()