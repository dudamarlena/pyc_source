# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jeju/do.py
# Compiled at: 2016-11-09 20:45:11
import logging, logging.handlers, time, os, pwd, re, sys, urllib2, platform, os.path
from optparse import OptionParser
import mistune, jeju
from jeju.executor.shell import *
from jeju.executor.editor import *
from jeju.executor.expect import *
from jeju.executor.python import *
from jeju.executor.yaml import *
N_LOOKAHEAD = 2
LOOKAHEAD = None
options = None
KV = {}
CUSTOM_KV = {}
temp_key = None
is_kv = False
welcome = '\n\n     ___  _______      ___  __   __ \n    |   ||       |    |   ||  | |  |\n    |   ||    ___|    |   ||  | |  |\n    |   ||   |___     |   ||  |_|  |\n ___|   ||    ___| ___|   ||       |\n|       ||   |___ |       ||       |\n|_______||_______||_______||_______|\n\nhttps://github.com/pyengine/jeju\n\nCopyright(c) 2016 Choonho Son.\nAll rights reserved.\n\nVersion: %s\n\n' % jeju.__version__
usage = 'usage: %prog [options] arg'
logging.basicConfig(level=logging.DEBUG, datefmt='%m-%d %H:%M')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)

def clear():
    os.system('clear')


executor = {'bash': shell_bash, 
   'c': editor_text, 
   'expect': shell_expect, 
   'text': editor_text, 
   'ini': editor_ini, 
   'python': execute_python, 
   'yaml': execute_yaml}
idx = (0, 0, 0)

def toi(level):
    global idx
    x, y, z = idx
    if level == 1:
        x = x + 1
        y = 0
        z = 0
        idx = (x, y, z)
        return '%s.' % x
    if level == 2:
        y = y + 1
        z = 0
        idx = (x, y, z)
        return '%s-%s.' % (x, y)
    if level == 3:
        z = z + 1
        idx = (x, y, z)
        return '%s-%s-%s.' % (x, y, z)


def change_user(user_name):
    pw_record = pwd.getpwnam(user_name)
    os.putenv('USER', user_name)
    os.putenv('HOME', pw_record.pw_dir)
    os.setgid(pw_record.pw_gid)
    os.setegid(pw_record.pw_gid)
    os.setuid(pw_record.pw_uid)
    os.seteuid(pw_record.pw_uid)


def change_dir(new_dir):
    os.chdir(new_dir)


class JunRenderer(mistune.Renderer):

    def __init__(self, **kwargs):
        mistune.Renderer.__init__(self, **kwargs)

    def block_code(self, code, lang):
        global KV
        global LOOKAHEAD
        global options
        if options.interactive:
            print code
            yn = raw_input('execute next? (Yes/No/Skip)')
            if yn.lower() == 'n' or yn.lower() == 'no':
                sys.exit()
            elif yn.lower() == 's' or yn.lower() == 'skip':
                return 'Skipped'
        output = executor[lang](code=code, lookahead=LOOKAHEAD, kv=KV)
        if type(output) != dict:
            logging.error(output)
            return '<pre><code class="lang-bash">%s</code></pre>\n' % (lang, output)
        else:
            result = ''
            if output.has_key('input') and output['input'] != None and output['input'] != '':
                added = output['input']
                added = added.rstrip('\n')
                if not lang:
                    added = mistune.escape(added, smart_amp=False)
                    return '<pre><code>%s\n</code></pre>\n' % added
                added = mistune.escape(added, quote=True, smart_amp=False)
                result = result + '<b>Input:</b></br>'
                result = result + '<pre><code class="lang-%s">%s\n</code></pre>\n' % (lang, added)
            if output.has_key('output') and output['output'] != None and output['output'] != '':
                logging.debug(output['output'])
                added = output['output']
                added = added.rstrip('\n')
                if not lang:
                    added = mistune.escape(added, smart_amp=False)
                    return '<pre><code>%s\n</code></pre>\n' % added
                added = mistune.escape(added, quote=True, smart_amp=False)
                result = result + '<b>Output:</b></br>'
                result = result + '<pre><code class="lang-%s">%s\n</code></pre>\n' % (lang, added)
            if output.has_key('error') and output['error'] != None and output['error'] != '':
                logging.error(output['error'])
                added = output['error']
                added = added.rstrip('\n')
                if not lang:
                    added = mistune.escape(added, smart_amp=False)
                    return '<pre><code>%s\n</code></pre>\n' % added
                added = mistune.escape(added, quote=True, smart_amp=False)
                result = result + '<b>Error:</b></br>'
                result = result + '<pre><code class="lang-%s">%s\n</code></pre>\n' % (lang, added)
            return result

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        logging.debug('%s %s' % (toi(level), text))
        time.sleep(1)
        return '<h%d>%s</h%d>\n' % (level, text, level)


class Jeju(mistune.Markdown):

    def pop(self):
        global LOOKAHEAD
        if len(self.tokens) <= 0:
            return None
        else:
            if len(self.tokens) >= N_LOOKAHEAD:
                r_idx = 0 - N_LOOKAHEAD
                if self.tokens[r_idx]['type'] == 'code':
                    LOOKAHEAD = self.tokens[(-1)]
            self.token = self.tokens.pop()
            return self.token

    def output(self, text, rules=None):
        self.tokens = self.block(text, rules)
        self.tokens.reverse()
        self.inline.setup(self.block.def_links, self.block.def_footnotes)
        out = self.renderer.placeholder()
        while self.pop():
            out += self.tok()

        return out

    def tok(self):
        t = self.token['type']
        if t.endswith('_start'):
            t = t[:-6]
        return getattr(self, 'output_%s' % t)()

    def output_table(self):
        global CUSTOM_KV
        global is_kv
        global temp_key
        aligns = self.token['align']
        aligns_length = len(aligns)
        cell = self.renderer.placeholder()
        is_kv = False
        header = self.renderer.placeholder()
        for i, value in enumerate(self.token['header']):
            if i == 0:
                if value.lower() == 'keyword':
                    is_kv = True
                else:
                    is_kv = False
            if i == 1 and is_kv == True:
                if value.lower() == 'value':
                    is_kv = True
                else:
                    is_kv = False
            align = aligns[i] if i < aligns_length else None
            flags = {'header': True, 'align': align}
            cell += self.renderer.table_cell(self.inline(value), **flags)

        header += self.renderer.table_row(cell)
        body = self.renderer.placeholder()
        for i, row in enumerate(self.token['cells']):
            cell = self.renderer.placeholder()
            for j, value in enumerate(row):
                if is_kv == True:
                    if j == 0:
                        temp_key = value
                    elif j == 1:
                        if CUSTOM_KV.has_key(temp_key) == True:
                            logging.info('%s = %s is overrided by user (%s = %s)' % (temp_key, value, temp_key, CUSTOM_KV[temp_key]))
                        else:
                            KV[temp_key] = value
                            logging.info('Update K[%s] = %s' % (temp_key, value))
                        if temp_key == 'USER':
                            logging.info('Change current user %s -> %s' % (os.environ['USER'], value))
                            change_user(value)
                        if temp_key == 'PWD':
                            logging.info('Change working directory %s -> %s' % (os.environ['PWD'], value))
                            change_dir(value)
                        temp_key = None
                align = aligns[j] if j < aligns_length else None
                flags = {'header': False, 'align': align}
                cell += self.renderer.table_cell(self.inline(value), **flags)

            body += self.renderer.table_row(cell)

        return self.renderer.table(header, body)


def open_doc(f):
    item = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f)
    if len(item) == 1:
        fp = urllib2.urlopen(f)
        output = fp.read()
    elif len(item) == 0:
        try:
            fp = open(f)
            output = fp.read()
            fp.close()
        except:
            logging.info('Guide book does not exist in local disk')
            guess = '%s/%s' % (options.repo, f)
            logging.info('Find repository: %s' % guess)
            try:
                ret = urllib2.urlopen(guess)
                if ret.code == 200:
                    output = ret.read()
            except:
                distro = detect_dist()
                os = distro['distname'].split(' ')[0].lower()
                guess = '%s/%s/%s' % (options.repo, os, f)
                logging.info('Find repository: %s' % guess)
                try:
                    ret = urllib2.urlopen(guess)
                    if ret.code == 200:
                        output = ret.read()
                except:
                    ver2 = distro['ver'].split('.')
                    guess = '%s/%s/%s.%s/%s' % (options.repo, os, ver2[0], ver2[1], f)
                    logging.info('Find repository: %s' % guess)
                    try:
                        ret = urllib2.urlopen(guess)
                        output = ret.read()
                    except:
                        return '# Guide book does not exist! '

    return output


def detect_dist():
    a, b, c = platform.linux_distribution()
    result = {'distname': a, 'ver': b, 
       'id': c}
    return result


text = '\n# Hello World\n\nThis is hello world example.\nJeju will read this document, then execute this based on code.\n\n# How to program with C\n\n## create source code\n\nJeju will create hello.c file in current working directory.\n\nedit hello.c\n~~~c\n// comment\n#include <stdio.h>\n\nint main()\n{\n    printf("Hello World\\n");\n    return 0;\n}\n~~~\n\n# Compile\n\nJeju will compile above created file, hello.c\n\n~~~bash\ngcc -o hello hello.c\n./hello\n~~~\n\n'

def parse_kv(param):
    items = param.split(',')
    v = ''
    for item in items:
        kv = item.split('=')
        if len(kv) == 1:
            v = '%s,%s' % (v, kv[0])
        else:
            k, v = kv
        CUSTOM_KV[k] = v
        KV[k] = v


def main():
    global options
    parser = OptionParser()
    parser.add_option('-m', '--markdown', dest='md', help='Specification documents based on Markdown style', metavar='md file')
    parser.add_option('-l', '--logging', dest='logging', help='Logging level (CRITICAL | ERROR | WARNING | INFO | DEBUG),                     default=DEBUG', metavar='logging level', default='DEBUG')
    parser.add_option('-L', '--logging-file', dest='log_file', help='Logging file (/tmp/jeju.log),                     default=/tmp/jeju.log', metavar='logging file')
    parser.add_option('-V', '--verbose', dest='verbose', help='Verbose level (console | file | all), default=all', metavar='verbose level', default='all')
    parser.add_option('-i', '--interactive', dest='interactive', help='Interactive mode asking for execution', action='store_true', default=False)
    parser.add_option('-k', '--kv', dest='kv', help="Additional custom/overriding KEY=VALUEs, seperated by comma(,)\n                    ex) -k 'k1=value1,k2=value2'\n                    ", metavar='key=value')
    parser.add_option('-r', '--repo', dest='repo', help='Repository of jeju guide book', default='https://raw.githubusercontent.com/pyengine/jeju-guide/master')
    parser.add_option('-v', '--version', dest='version', help='Show current version', action='store_true', default=False)
    options, args = parser.parse_args()
    if options.version:
        print jeju.__version__
        sys.exit()
    if options.kv:
        parse_kv(options.kv)
    if not options.md:
        print 'Default instruction is hello world'
        code = text
    else:
        code = open_doc(options.md)
    jun = JunRenderer()
    markdown = Jeju(renderer=jun)
    if options.verbose and options.verbose == 'file':
        pass
    else:
        clear()
        print welcome
        time.sleep(3)
    if options.md:
        prefix, f = os.path.split(options.md)
    else:
        f = 'test'
    if options.logging == 'DEBUG':
        level = logging.DEBUG
    elif options.logging == 'INFO':
        level = logging.INFO
    elif options.logging == 'WARNING':
        level = logging.WARNING
    elif options.logging == 'ERROR':
        level = logging.ERROR
    elif options.logging == 'CRITICAL':
        level = logging.CRITICAL
    else:
        level = logging.DEBUG
    console.setLevel(level)
    if options.log_file:
        fh = logging.FileHandler(options.log_file)
        formatter = logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(level)
        logging.getLogger('').addHandler(fh)
        jeju.__logging__ = 'file'
    import socket
    if KV.has_key('HOSTNAME') == False:
        KV['HOSTNAME'] = socket.gethostname()
    else:
        logging.info('Hostname is overrided')
    if KV.has_key('IP') == False:
        try:
            KV['IP'] = socket.gethostbyname(KV['HOSTNAME'])
        except:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('google.com', 80))
            KV['IP'] = s.getsockname()[0]

    else:
        logging.info('IP is overrided')
    if options.md:
        logging.info('Start Jeju: %s' % options.md)
    else:
        logging.info('Start Jeju: test')
    if options.kv:
        logging.info('       -kv: %s' % options.kv)
    logging.info('Update K[%s] = %s' % ('HOSTNAME', KV['HOSTNAME']))
    logging.info('Update K[%s] = %s' % ('IP', KV['IP']))
    output = markdown(code)
    fp = open('/tmp/%s.html' % f, 'w')
    fp.write(output)
    fp.close()


if __name__ == '__main__':
    main()