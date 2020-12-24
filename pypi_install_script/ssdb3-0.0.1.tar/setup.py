from setuptools import setup
import ssdb3
import re
import os
import sys

setup(
    name='ssdb3',
    version=ssdb3.__version__,
    author=re.sub(r'\s+<.*', r'', ssdb3.__author__),
    author_email=re.sub(r'(^.*<)|(>.*$)', r'', ssdb3.__author__),
    url=ssdb3.__url__,
    description=('An SSDB Client Library for Python3.'),
    long_description=open('README.rst').read(),
    license='BSD',
    keywords='ssdb3',
    py_modules=['ssdb3'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
