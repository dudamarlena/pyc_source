# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/doc.py
# Compiled at: 2019-08-05 00:35:42
__doc__ = "\n### Usage: ctdoc [-w]\n\n### Options:\n    -h, --help  show this help message and exit\n    -w, --web   build web docs\n    -a, --auto  use auto mode (even with a plugin)\n    -o, --omit  omit any files from autodoc?\n\nRun from cantools root (contains setup.py, cantools/, README.md, etc), from root\nof a CT plugin, or from within a custom project. In cantools, builds docs for all\nfrontend (js) and CLI (py) files. In plugin, docs consist of about file (about.txt),\ninitialization config (init.py) and default frontend config (js/config.js). In custom\n(project) mode (when ctdoc is run somewhere other than cantools root or a plugin root,\nand additionally a configuration file, doc.cfg, is present), for each path declared in\ndoc.cfg, include the docstring of each file specified, as well as the contents of\nabout.txt (if present). Lastly, auto mode doesn't require configuration (doc.cfg) --\ninstead, it recurses through the directories of your project, and includes the contents of\nany about.txt files, as well as (the top of) any py/js file that starts with a docstring.\n"
import os, json
from optparse import OptionParser
from cantools import __version__, config
from cantools.util import read, write, log, cp, cmd
WEB = []
ALTS = {'pubsub': os.path.join('pubsub', '__init__')}
HERE = os.path.abspath('.').split(os.path.sep)[(-1)]
CUSTOM = os.path.isfile('doc.cfg') and read('doc.cfg')
ISPLUGIN = not CUSTOM and HERE.startswith('ct') and HERE
AUTO = HERE != 'cantools' and not CUSTOM and not ISPLUGIN
if not CUSTOM and not AUTO:
    if ISPLUGIN:
        JSPATH = os.path.join(HERE, 'js')
        BPATH = '.'
        ALTS['init'] = os.path.join(ISPLUGIN, 'init')
    else:
        JSPATH = os.path.join(HERE, 'CT')
        BPATH = os.path.join(HERE, 'scripts')

def space(data):
    return '    ' + data.replace('\n', '\n    ')


def dsBack(cmd):
    cpath = os.path.join(BPATH, '%s.py' % (ALTS.get(cmd, cmd),))
    log(cpath, 2)
    bdata = read(cpath)
    fdata = ISPLUGIN and space(bdata) or '## ct%s\n%s' % (cmd, bdata[4:].split('\n"""')[0])
    WEB[(-1)]['children'].append({'name': cmd, 
       'content': fdata})
    return fdata


def dsFront(mod, modname=None, iline=None):
    modname = modname or 'CT.%s' % (mod[:-3],)
    iline = iline or mod == 'ct.js' and '&lt;script src="/js/CT/ct.js"&gt;&lt;/script&gt;' or 'CT.require("%s");' % (modname,)
    log(modname, 2)
    mdata = read(os.path.join(JSPATH, mod))
    rdata = ('\n').join([
     '## %s' % (modname,),
     "### Import line: '%s'" % (iline,),
     ISPLUGIN and mod == 'config.js' and space(mdata) or mdata[3:].split('\n*/')[0]])
    WEB[(-1)]['children'].append({'name': mod, 
       'content': rdata})
    return rdata


def back():
    log('back', 1)
    wobj = {'children': []}
    WEB.append(wobj)
    f = []
    if ISPLUGIN:
        wobj['name'] = 'Back (Init Config)'
        fdata = [dsBack('init')]
    else:
        wobj['name'] = 'Back (CLI)'
        fdata = list(map(dsBack, ['init', 'start', 'deploy', 'pubsub', 'migrate', 'index', 'doc']))
    f.append('# %s' % (wobj['name'],))
    f += fdata
    return f


def front():
    log('front', 1)
    wobj = {'children': []}
    WEB.append(wobj)
    f = []
    if not ISPLUGIN:
        wobj['name'] = 'Front (JS Library)'
        plist = os.listdir(JSPATH)
        plist.sort()
        fdata = list(map(dsFront, [ i for i in plist if i.endswith('js') ]))
    elif os.path.isfile(os.path.join(JSPATH, 'config.js')):
        wobj['name'] = 'Front (JS Config)'
        fdata = [dsFront('config.js', 'core.config.%s' % (ISPLUGIN,), 'CT.require("core.config");')]
    if 'name' in wobj:
        f.append('# %s' % (wobj['name'],))
        f += fdata
    return f


def customChunk(path, fnames):
    log('custom chunk: %s' % (path,), 1)
    kids = []
    wobj = {'name': path, 'children': kids}
    WEB.append(wobj)
    f = ['## %s' % (path,)]
    afile = os.path.join(path, 'about.txt')
    if os.path.isfile(afile):
        adata = read(afile)
        f.append(adata)
        kids.append({'name': 'about', 
           'content': adata})
    for fname in fnames:
        fdata = read(os.path.join(path, fname))
        if fname == 'config.js' or fname.startswith('ct.cfg'):
            fdata = space(fdata)
        elif fname.endswith('.js'):
            fdata = fdata[3:].split('\n*/')[0]
        elif fname.endswith('.py'):
            fdata = fdata[4:].split('\n"""')[0]
        f.append('### %s\n%s' % (fname, fdata))
        kids.append({'name': fname, 
           'content': fdata})

    return f


frules = {'.js': {'top': '/*\n', 
           'bottom': '\n*/'}, 
   '.py': {'top': '"""\n', 
           'bottom': '\n"""'}}
hashead = set()

def sethead(curdir, data):
    dirname = curdir.rsplit(os.path.sep, 1)[(-1)]
    if dirname not in hashead:
        hashead.add(dirname)
        data.append('%s %s' % ('#' * len(curdir.split(os.path.sep)), dirname))
        wobj = {'name': dirname, 'children': []}
        WEB.append(wobj)
    return WEB[(-1)]['children']


OMIT = ''

def autodoc(data, curdir, contents):
    global OMIT
    about = 'about.txt'
    if curdir != HERE:
        about = os.path.join(curdir, about)
    if os.path.isfile(about):
        kids = sethead(curdir, data)
        adata = read(about)
        data.append(adata)
        kids.append({'name': 'about', 
           'content': adata})
    for fname in contents:
        if fname in OMIT:
            continue
        for flag, rule in list(frules.items()):
            if fname.endswith(flag):
                fdata = read(os.path.join(curdir, fname))
                if fdata.startswith(rule['top']):
                    kids = sethead(curdir, data)
                    fstr = fdata[len(rule['top']):].split(rule['bottom'])[0]
                    data.append('%s# %s' % ('#' * len(curdir.split(os.path.sep)), fname))
                    data.append(fstr)
                    kids.append({'name': fname, 
                       'content': fstr})


def build():
    global OMIT
    parser = OptionParser('ctdoc [-w]')
    parser.add_option('-w', '--web', action='store_true', dest='web', default=False, help='build web docs')
    parser.add_option('-a', '--auto', action='store_true', dest='auto', default=False, help='use auto mode (even with a plugin)')
    parser.add_option('-o', '--omit', dest='omit', default='', help='omit any files from autodoc?')
    options, args = parser.parse_args()
    log('building docs')
    ds = []
    if AUTO or options.auto:
        OMIT = options.omit
        os.path.walk(HERE, autodoc, ds)
    else:
        abdata = (ISPLUGIN or CUSTOM) and '# %s\n%s' % (HERE, read('about.txt')) or config.about % (__version__,)
        ds.append(abdata)
        WEB.append({'name': HERE, 
           'children': [
                      {'name': 'about', 
                         'content': abdata}]})
        if CUSTOM:
            for line in CUSTOM.split('\n'):
                path, fnames = line.split(' = ')
                ds.extend(customChunk(path, fnames.split('|')))

        else:
            ds.extend(back())
            ds.extend(front())
    log('writing data', important=True)
    log('README.md', 1)
    write(('\n\n').join(ds), 'README.md')
    if options.web:
        log('web docs enabled!', 1)
        log('building docs web application', 2)
        if not os.path.isdir('docs'):
            cmd('ctinit docs -p ctdocs')
        log('copying data', 2)
        cp('core.data = %s;' % (json.dumps(WEB, indent=4),), os.path.join('docs', 'js', 'core', 'data.js'))
    log('goodbye')


if __name__ == '__main__':
    build()