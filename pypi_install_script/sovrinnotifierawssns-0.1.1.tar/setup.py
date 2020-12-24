from setuptools import setup, find_packages, __version__
import os, sys

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    try:
        long_description = open('README.md').read()
    except:
        long_description = ''


try:
    SETUP_DIRNAME = os.path.dirname(__file__)
except NameError:
    # We're probably being frozen, and __file__ triggered this NameError
    # Work around this
    SETUP_DIRNAME = os.path.dirname(sys.argv[0])

if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

SETUP_DIRNAME = os.path.abspath(SETUP_DIRNAME)

METADATA = os.path.join(SETUP_DIRNAME, 'sovrinnotifierawssns', '__metadata__.py')
# Load the metadata using exec() so we don't trigger an import of ioflo.__init__
exec(compile(open(METADATA).read(), METADATA, 'exec'))

setup(
    name='sovrinnotifierawssns',
    version=__version__,
    url='https://github.com/evernym/sovrin-notifier-awssns',
    license=__license__,
    author=__author__,
    author_email='evernym-dev-team@evernym.com',
    description='Sovrin Node AWS SNS Notifier',
    install_requires=[ 'boto3==1.4.1' ],
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
