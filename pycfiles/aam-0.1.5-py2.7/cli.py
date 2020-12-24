# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/aam/cli.py
# Compiled at: 2014-06-06 10:51:25
import os, sys, shutil
major = sys.version_info[0]
if major < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')
from .utils import *
from .options import *
from reader.reader import *
from generator.render import *
import aam
doc = 'Aam v%s\nUsage:\n    aam init\n    aam build\n    aam -h | --help\n    aam --version\n\nOptions:\n    -h --help               Show this screen and exit.\n' % aam.__version__
from parguments import Parguments
parguments = Parguments(doc, version=aam.__version__)

def pre_init():
    hub.root.path = os.path.dirname(__file__)
    hub.root.template_path = os.path.join(os.path.dirname(__file__), 'templates')
    hub.root.static_path = os.path.join(os.path.dirname(__file__), 'static')
    hub.site.path = os.getcwd()
    hub.site.page_path = os.path.join(hub.site.path, 'pages')
    hub.site.deploy_path = os.path.join(hub.site.path, 'deploy')
    hub.site.static_path = os.path.join(hub.site.deploy_path, 'static')


@parguments.command
def init():
    """
    Usage:
        aam init

    Options:
        -h --help               Show this screen and exit.
    """
    pre_init()
    mkdir('pages')
    mkdir('deploy')
    shutil.copyfile(os.path.join(hub.root.path, 'config.ini'), 'config.ini')
    print 'Please edit config.py to config your site'


@parguments.command
def build():
    """
    Usage:
        aam build

    Options:
        -h --help               Show this screen and exit.
    """
    pre_init()
    read_config()
    read_page()
    render()
    print 'Build Finished.'


def main():
    parguments.run()