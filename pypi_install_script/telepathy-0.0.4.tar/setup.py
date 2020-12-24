import os
from setuptools import setup, find_packages

from telepathy import __version__, __author__, __licence__


requires = [
    'docopt',
    'celery',
    'redis',
    'flask-restful',
    'Logbook',
    'rethinkdb']


def long_description():
    try:
        #with codecs.open(readme, encoding='utf8') as f:
        with open('readme.md') as f:
            return f.read()
    except IOError:
        return "failed to read README.md"


setup(
    name='telepathy',
    version=__version__,
    description='This plugin provides a RESTFul interface to intuition',
    author=__author__,
    author_email='xavier.bruhiere@gmail.com',
    packages=find_packages(),
    long_description=long_description(),
    license=__licence__,
    install_requires=requires,
    url="https://github.com/hackliff/intuition-plugins",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Distributed Computing',
    ],
    scripts=['app/telepathy'],
    data_files=[(os.path.expanduser('~/.intuition'), ['app/Procfile'])]
)
