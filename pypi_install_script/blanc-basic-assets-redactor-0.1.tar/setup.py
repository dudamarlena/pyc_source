#!/usr/bin/env python
from distutils.core import setup

# Use blanc_basic_assets_redactor.VERSION for version numbers
version_tuple = __import__('blanc_basic_assets_redactor').VERSION
version = '.'.join([str(v) for v in version_tuple])

setup(
    name='blanc-basic-assets-redactor',
    version=version,
    description='Blanc Basic Assets RedactorJS Upload for Django',
    long_description=open('README.rst').read(),
    url='http://www.blanctools.com/',
    maintainer='Alex Tomkins',
    maintainer_email='alex@blanc.ltd.uk',
    platforms=['any'],
    packages=[
        'blanc_basic_assets_redactor',
        'blanc_basic_assets_redactor.templatetags',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD-2',
)
