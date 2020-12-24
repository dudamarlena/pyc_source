# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buildout/python_libevent.py
# Compiled at: 2011-07-28 12:20:48
import logging, shutil, subprocess, os, tempfile, urllib
from zc.recipe.egg import Eggs
logger = logging.getLogger('zc.buildout')

class Recipe(Eggs):
    __module__ = __name__

    def __init__(self, buildout, name, options):
        super(Recipe, self).__init__(buildout, name, options)
        self.libevent_source = options['libevent']

    def install(self):
        curr_dir = os.getcwd()
        tempdir = tempfile.mkdtemp()
        try:
            filename = os.path.join(tempdir, 'libevent.tar.gz')
            logger.info('Downloading libevent source from %s', self.libevent_source)
            urllib.urlretrieve(self.libevent_source, filename)
            assert os.path.isfile(filename)
            os.chdir(tempdir)
            logger.info('Extracting libevent...')
            contents_before = set(os.listdir(tempdir))
            ret = subprocess.call(['tar', 'xzf', filename])
            assert ret == 0
            new_contents = list(contents_before.symmetric_difference(os.listdir(tempdir)))
            assert len(new_contents) == 1
            libevent_root = os.path.join(tempdir, new_contents[0])
            os.chdir(libevent_root)
            logger.info('Compiling libevent...')
            ret = subprocess.call(['sh', './configure', '--with-pic'])
            assert ret == 0
            ret = subprocess.call(['make', '-j', '4'])
            assert ret == 0
            os.environ['LIBEVENT_ROOT'] = libevent_root
            return super(Recipe, self).install()
        finally:
            os.chdir(curr_dir)
            shutil.rmtree(tempdir)