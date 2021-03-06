# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
import re

from os.path import join, dirname
from setuptools import setup


VERSION_RE = re.compile('__version__ = \'([\d\.]+)\'')


def read_version():
    with open('pixelpin_auth_django/__init__.py') as file:
        version_line = [line for line in file.readlines()
                        if line.startswith('__version__')][0]
        return VERSION_RE.match(version_line).groups()[0]


def long_description():
    return open(join(dirname(__file__), 'README.md')).read()


def load_requirements():
    return open(join(dirname(__file__), 'requirements.txt')).readlines()

setup(
    name='pixelpin-auth-django',
    version=read_version(),
    author=['Matias Aguirre', 'Callum Brankin'],
    author_email="callum@pixelpin.co.uk",
    description='Python PixelPin Authentication, Django integration.',
    license='BSD',
    keywords='django, social auth, pixelpin auth',
    url='https://github.com/python-social-auth/social-app-django',
    packages=[
        'pixelpin_auth_django',
        'pixelpin_auth_django.migrations'
    ],
    long_description=long_description(),
    install_requires=load_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    zip_safe=False
)
