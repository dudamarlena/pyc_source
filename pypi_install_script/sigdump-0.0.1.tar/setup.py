import os
from setuptools import setup

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()

__version__ = '0.0.1'
__author__ = 'Masashi Shibata <m.shibata1020@gmail.com>'
__author_email__ = 'm.shibata1020@gmail.com'
__license__ = 'MIT License'
__classifiers__ = (
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
)


setup(
    name='sigdump',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/c-bata/pysigdump',
    description='Use signal to show stacktrace of a Python process',
    long_description=README,
    classifiers=__classifiers__,
    py_modules=['sigdump'],
    install_requires=[],
    keywords='process stacktrace garbagecollection',
    license=__license__,
    include_package_data=True,
)
