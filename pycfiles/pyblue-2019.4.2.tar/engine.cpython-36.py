# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ialbert/web/pyblue-central/pyblue/engine.py
# Compiled at: 2019-04-02 09:06:58
# Size of source mod 2**32: 15407 bytes
"""
Really simple static site generator. Uses Django templates
"""
import argparse, imp, io, json, logging, os, re, shutil, sys, time
from builtins import *
import bottle, django, importlib
from django.conf import settings
from django.template.backends.django import get_installed_libraries
from django.template.loader import get_template
__author__ = 'ialbert'
from pyblue import VERSION
PYBLUE_EXTRA_DIRS = 'PYBLUE_EXTRA_DIRS'
DESCRIPTION = 'PyBlue %s, static site generator' % VERSION
logger = logging.getLogger('pyblue')

def strip(x):
    return x.strip()


def join(*args):
    return os.path.abspath((os.path.join)(*args))


class PyBlue(object):
    IGNORE_EXTS = {
     '.pyc'}

    def __init__(self, root, args):
        self.auto_refresh = not args.no_scan
        self.context = args.context
        self.time_check = not args.no_time
        self.root, self.files = None, []
        self.set_root(root)
        self.django_init()
        ctx_path = join(self.root, self.context)
        try:
            ctx = None
            if os.path.isfile(ctx_path):
                ctx = imp.load_source('ctx', ctx_path)
            else:
                logger.warning('cannot find context module {}'.format(ctx_path))
        except Exception as exc:
            logger.warning('unable to import context module: {} error: {}'.format(ctx_path, exc))

        def render(path):
            if self.auto_refresh:
                self.set_root(self.root)
            logger.debug('%s' % path)
            fname = join(self.root, path)
            page = File(fname=fname, root=(self.root))
            if page.is_template:
                params = dict(page=page, root=(self.root), context=ctx, files=(self.files))
                template = get_template(page.fname)
                html = template.render(params)
                return html
            else:
                return bottle.static_file(path, root=(self.root))

        self.render = render
        self.app = bottle.Bottle()
        self.app.route('/', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda : self.render('index.html'))
        self.app.route('/<path:path>', method=['GET', 'POST', 'PUT', 'DELETE'])(lambda path: self.render(path))

    def serve(self, host='0.0.0.0', port=8080):
        """
        Launch the WSGI app development web server
        """
        import waitress
        logger.info('{}:{}'.format(host, port))
        waitress.serve((self.app), host=host, port=port, _quiet=True)

    def generate(self, output):
        """
        Generates the site in the output directory
        """
        if os.path.isfile(output):
            logger.error('invalid output directory: {}'.format(output))
            return
        if not os.path.isdir(output):
            logger.info('creating output directory: {}'.format(output))
            os.mkdir(output)
        self.auto_refresh = False
        for f in self.files:
            if f.is_template:
                content = self.render(f.fname)
                f.write(output, content=content, check=(self.time_check))
            else:
                f.write(output, check=(self.time_check))

        logger.info('wrote {} files'.format(len(self.files)))

    def walk(self):
        files = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in sorted(filenames):
                start, ext = os.path.splitext(name)
                if ext in self.ignore_exts:
                    pass
                else:
                    absp = os.path.join(dirpath, name)
                    path = os.path.relpath(absp, self.root)
                    files.append(path)

        logger.info('found: %d files' % len(files))
        return files

    def set_root(self, path):
        """
        Sets the folder where the files to serve are located.
        Finds and stores all files in the directory.
        """
        self.root = os.path.abspath(path)
        if not os.path.isdir(self.root):
            logger.error('directory does not exist: %s' % self.root)
            sys.exit()
        self.files = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            for name in sorted(filenames):
                start, ext = os.path.splitext(name)
                if ext in self.IGNORE_EXTS:
                    pass
                else:
                    fname = os.path.join(dirpath, name)
                    self.files.append(File(fname=fname, root=(self.root)))

    def django_init(self):
        """
        Initializes the django engine. The root must have been set already."
        """
        elems = os.path.split(self.root)[:-1]
        parent = (os.path.join)(*elems)
        sys.path.append(parent)
        BASE_APP = []
        try:
            base = os.path.split(self.root)[(-1)]
            logger.debug('importing app as python module: %s' % base)
            importlib.import_module(base)
            BASE_APP = [base]
        except ImportError as exc:
            logger.debug("app '{}' cannot be imported: {}".format(base, exc))

        parent_dir = join(os.path.dirname(__file__), 'templates')
        tmpl_dir = join(self.root, 'templates')
        extra_dir = os.getenv(PYBLUE_EXTRA_DIRS, None)
        extra_dir = extra_dir.split(',') if extra_dir else []
        logger.debug(f"{PYBLUE_EXTRA_DIRS}: {extra_dir}")
        dirs = [
         self.root, tmpl_dir, parent_dir] + extra_dir
        logger.debug('template dirs: {}'.format(dirs))
        settings.configure(DEBUG=True,
          TEMPLATE_DEBUG=True,
          TEMPLATES=[
         {'BACKEND':'django.template.backends.django.DjangoTemplates', 
          'DIRS':dirs, 
          'APP_DIRS':True, 
          'OPTIONS':{'string_if_invalid':'Undefined: %s ', 
           'builtins':[
            'pyblue.templatetags.pytags',
            'django.contrib.humanize.templatetags.humanize']}}],
          INSTALLED_APPS=([
         'pyblue', 'django.contrib.humanize',
         'django.contrib.staticfiles'] + BASE_APP),
          STATIC_URL='/static/')
        django.setup()
        logger.debug('templatetags: %s' % ', '.join(get_installed_libraries()))


def mtime(fname):
    """
    Safer file modification time detection.
    """
    t = os.stat(fname).st_mtime if os.path.isfile(fname) else 0
    return t


class File(object):
    __doc__ = '\n    Represents a file object within PyBlue relative to a root directory.\n    '
    TEMPLATE_EXTENSIONS = {
     '.html', '.htm'}
    IMAGE_EXTENSIONS = {'.png', '.gif', '.jpg', 'jpeg', '.svg'}
    MARKDOWN_EXTENSION = {'.md'}

    def __init__(self, fname, root):
        self.root = root
        self.meta = dict()
        fname = os.path.abspath(fname)
        fname = os.path.relpath(fname, self.root)
        self.fname = fname
        self.fpath = self.path = os.path.join(root, fname)
        if not os.path.isfile(self.path):
            logger.warning('file does not exist: %s' % fname)
            return
        statinfo = os.stat(self.path)
        self.size = statinfo.st_size
        mt = time.gmtime(statinfo.st_mtime)
        self.last_modified = time.strftime('%A, %B %d, %Y', mt)
        self.dname = os.path.dirname(self.path)
        self.ext = os.path.splitext(fname)[1]
        self.is_template = self.ext in self.TEMPLATE_EXTENSIONS
        self.is_image = self.ext in self.IMAGE_EXTENSIONS
        self.is_markdown = self.ext in self.MARKDOWN_EXTENSION
        name = title = self.nicer_name(fname)
        self.meta = dict(fname=fname, name=name, title=title, sortkey='5')
        if self.is_template:
            meta = parse_metadata(self.path)
            self.meta.update(meta)

    @property
    def content(self):
        MAXSIZE = 52428800
        if self.size > MAXSIZE:
            logger.error('file size is too large to be rendered %s' % self.size)
            return '?'
        else:
            return io.open((self.path), encoding='utf-8').read()

    def nicer_name(self, fname):
        """
        Attempts to generate a nicer name from the filename.
        Removes underscores, dashes and extensions.
        """
        head, tail = os.path.split(fname)
        base, ext = os.path.splitext(tail)
        if not self.is_template:
            return tail
        else:
            name = base.title().replace('-', ' ').replace('_', ' ')
            return name

    @property
    def link_name(self):
        if self.is_markdown:
            base, ext = os.path.splitext(self.fname)
            return '{}.html'.format(base)
        else:
            return self.fname

    def write(self, output, content='', check=True):
        """
        Writes the text into an output folder
        """
        dest = os.path.join(output, self.fname)
        if os.path.abspath(dest) == os.path.abspath(self.path):
            raise Exception('cannot not overwrite the original file: %s' % dest)
        if check:
            if mtime(dest) > mtime(self.path):
                logger.debug('skip: %s' % dest)
                return
        dpath = os.path.dirname(dest)
        if not os.path.exists(dpath):
            os.makedirs(dpath)
        elif self.is_template and content:
            logger.info('saving: %s' % dest)
            with io.open(dest, 'wt', encoding='utf-8') as (fp):
                fp.write(content)
        else:
            logger.info('copying: %s' % dest)
            shutil.copyfile(self.path, dest)

    def relpath(self, start=None):
        """
        Relative path of this file from a start location
        """
        start = start or self
        rpath = os.path.relpath(self.root, start.dname)
        rpath = os.path.join(rpath, self.fname)
        return rpath

    def __getattr__(self, name):
        """
        Metadata may be accessed as an attributes on the class.
        This gets triggered as a fallback if an attribute is not found.
        """
        value = self.meta.get(name, None)
        return value

    def __repr__(self):
        """
        User friendly representation
        """
        return '%s: %s (%s)' % (self.__class__.__name__, self.name, self.fname)

    def __bool__(self):
        return True


def parse_metadata(path):
    """
    Attempts to parse out metadata from django comments.
    Each comment is assumed to be key = value where the value is a JSON object.
    """
    PATTERN = re.compile('^{#\\s?(?P<name>\\w+)\\s?=\\s?(?P<value>[\\S\\s]+)\\s?#}')
    lines = io.open(path, encoding='utf-8').read().splitlines()[:100]
    lines = map(strip, lines)
    meta = dict()
    for line in lines:
        m = PATTERN.search(line)
        if m:
            name, value = m.group('name'), m.group('value')
            try:
                obj = json.loads(value)
            except ValueError as exc:
                obj = str(value).strip()

            meta[name] = obj

    return meta


def add_common_arguments(parser):
    """
    Adds the common parameters to each subparser.
    """
    pass


def get_parser():
    """
    Returns the command line parser.
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-r', dest='root', metavar='DIR', default='.', required=True, help='root directory for the site (%(default)s)')
    parser.add_argument('-o', dest='output', metavar='DIR', type=str, required=False, default='', help='the output directory for the generated site')
    parser.add_argument('-c', dest='context', metavar='FILE', type=str, required=False, default='context.py',
      help='the python module to load (%(default)s)')
    parser.add_argument('-p', metavar='NUMBER', type=int, dest='port', default=8080, help='server port to bind to (%(default)s)')
    parser.add_argument('-s', '--no-scan', dest='no_scan', default=False, action='store_true', help='turn off file scan on each request (%(default)s)')
    parser.add_argument('-n', '--no-time', dest='no_time', default=False, action='store_true', help='bypass timestamp check (%(default)s)')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true', help='increase logger verbosity (%(default)s)')
    return parser


def run():
    parser = get_parser()
    if len(sys.argv) < 3:
        sys.argv.append('--help')
    else:
        args = parser.parse_args()
        level = logging.DEBUG if args.verbose else logging.INFO
        format = '%(levelname)s\t%(funcName)s\t%(message)s'
        logging.basicConfig(format=format, level=level)
        pb = PyBlue(root=(args.root), args=args)
        if args.output:
            pb.generate(args.output)
        else:
            pb.serve(port=(args.port))


if __name__ == '__main__':
    run()