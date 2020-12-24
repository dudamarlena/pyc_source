# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = "0.1.6"

with open('README.rst') as f:
    readme = f.read()

setup(
    name='persistQueue',
    version=VERSION,
    license='MIT',
    author='logicalis',
    Maintainer='waraujo',
    author_email='eugenio@eugenio.io',
    url='http://re91877z@10.55.200.102:7990/scm/edge/lib-persist-queue.git',
    download_url=''.format(VERSION),
    description='A implementation of Class for Persist Queue',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=['queue', 'persistence', 'iot', 'embedded'],
    packages=['persistQueue'],
    install_requires=['persist-queue'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ]
)

