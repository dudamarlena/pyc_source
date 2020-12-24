from setuptools import setup, find_packages, __version__
from distutils.command.sdist import sdist
from distutils.errors import (DistutilsError)
import glob
import os

try:
    SETUP_DIRNAME = os.path.dirname(__file__)
except NameError:
    # We're probably being frozen, and __file__ triggered this NameError
    # Work around this
    SETUP_DIRNAME = os.path.dirname(sys.argv[0])
if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)
METADATA = os.path.join(SETUP_DIRNAME, 'sovringui', '__metadata__.py')
exec(compile(open(METADATA).read(), METADATA, 'exec'))


class my_sdist(sdist):
    def run(self):
        ret = os.system("bash -x build-sovringui-ui.sh");
        if ret != os.EX_OK:
            raise DistutilsError("build-sovringui-ui.sh failed")
        sdist.run(self)

setup(
    name='sovringui',
    version=__version__,
    description='Sovrin Node GUI App',
    url='https://github.com/evernym/sovringui',
    author=__author__,
    author_email='dev@evernym.us',
    license=__license__,
    install_requires=[
        'tornado',
        'paramiko',
        'plenum',
        'schema'
    ],
    cmdclass={
        'sdist': my_sdist,
    },
    scripts=['bin/sovringui'],
    data_files=[
        ('share/sovringui/public', filter(os.path.isfile, glob.iglob('sovringui/public/*'))),
        ('share/sovringui/public/assets', filter(os.path.isfile, glob.iglob('sovringui/public/assets/*'))),
        ('share/sovringui/public/assets/images', filter(os.path.isfile, glob.iglob('sovringui/public/assets/images/*'))),
        ('share/sovringui/public/scripts', filter(os.path.isfile, glob.iglob('sovringui/public/scripts/*'))),
        ('share/sovringui/public/styles', filter(os.path.isfile, glob.iglob('sovringui/public/styles/*'))),
    ],
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-tornado', 'pytest-mock']
)
