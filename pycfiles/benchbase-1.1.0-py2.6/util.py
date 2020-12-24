# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/benchbase/util.py
# Compiled at: 2011-09-16 09:34:52
import os, sys, hashlib, re, logging, gzip, pkg_resources
from commands import getstatusoutput
from mako.lookup import TemplateLookup
from docutils.core import publish_cmdline
TEMPLATE_LOOKUP = TemplateLookup(directories=[
 pkg_resources.resource_filename('benchbase', '/templates')])

def get_version():
    """Retrun the package version."""
    return pkg_resources.get_distribution('benchbase').version


def init_logging(options):
    if hasattr(logging, '_bb_init'):
        return
    level = logging.INFO
    if options.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S', filename=options.logfile, filemode='w')
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging._bb_init = True
    print 'Logging to ' + options.logfile


def render_template(template_name, **kwargs):
    mytemplate = TEMPLATE_LOOKUP.get_template(template_name)
    return mytemplate.render(**kwargs)


def md5sum(filename):
    f = open(filename)
    md5 = hashlib.md5()
    while True:
        data = f.read(8192)
        if not data:
            break
        md5.update(data)

    return md5.hexdigest()


def str2id(filename):
    return re.sub('[^a-zA-Z0-9_]', '_', filename)


def gnuplot(script_path):
    """Execute a gnuplot script."""
    path = os.path.dirname(os.path.abspath(script_path))
    if sys.platform.lower().startswith('win'):
        ret = os.system('cd "%s" && wgnuplot "%s"' % path, script_path)
        if ret != 0:
            raise RuntimeError('Failed to run wgnuplot cmd on ' + script_path)
    else:
        cmd = 'cd %s && gnuplot %s' % (path, os.path.abspath(script_path))
        (ret, output) = getstatusoutput(cmd)
        if ret != 0:
            print 'ERROR on ' + cmd


def generate_html(rst_file, html_file, report_dir):
    """Ask docutils to convert our rst file into html."""
    css_content = pkg_resources.resource_string('benchbase', '/templates/benchbase.css')
    css_dest_path = os.path.join(report_dir, 'benchbase.css')
    f = open(css_dest_path, 'w')
    f.write(css_content)
    f.close()
    cmdline = '-t --stylesheet-path=%s %s %s' % ('benchbase.css',
     os.path.basename(rst_file),
     os.path.basename(html_file))
    cmd_argv = cmdline.split(' ')
    pwd = os.getcwd()
    os.chdir(report_dir)
    publish_cmdline(writer_name='html', argv=cmd_argv)
    os.chdir(pwd)


class mygzip(gzip.GzipFile):
    """Fix to be make with work with python 2.6"""

    def __enter__(self):
        if self.fileobj is None:
            raise ValueError('I/O operation on closed GzipFile object')
        return self

    def __exit__(self, *args):
        self.close()


class BaseFilter(object):
    """Base filter."""

    def __ror__(self, other):
        return other

    def __call__(self, other):
        return other | self


class truncate(BaseFilter):
    """Middle truncate string up to length."""

    def __init__(self, length=40, extra='...'):
        self.length = length
        self.extra = extra

    def __ror__(self, other):
        if len(other) > self.length:
            mid_size = (self.length - 3) / 2
            other = other[:mid_size] + self.extra + other[-mid_size:]
        return other