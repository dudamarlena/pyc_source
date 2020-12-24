# coding:utf-8

from setuptools import setup, find_packages

long_description = """\
WSGI app framework.

Firewood is a framework for web app development in Python.

See detail @ http://github.com/tomokinakamaru/firewood.

Copyright (c) 2015, Tomoki Nakamaru.

License: MIT
"""

setup(
    author='Tomoki Nakamaru',
    author_email='tomoki.nakamaru@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    description='WSGI app framework',
    install_requires=[
        'mapletree==1.0.0',
        'sqlew==1.0.0'
    ],
    license='MIT',
    long_description=long_description,
    name='firewood',
    packages=find_packages(),
    platforms='any',
    url='http://github.com/tomokinakamaru/firewood',
    version='0.2.4',
)
