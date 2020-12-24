# -*- coding: utf-8 -*-

import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='tinyrpc-amqp',
    version='0.1dev',
    description='AMQP transport implementation for tinyrpc.',
    long_description=read('README.rst'),
    py_modules=['tinyrpc_amqp'],
    install_requires=[
        'tinyrpc',
        'pika>=0.9.14'
    ],
    keywords='json rpc json-rpc jsonrpc amqp',
    author='Ernesto Avilés Vázquez',
    author_email='whippiii@gmail.com',
    url='http://github.com/whippiii/tinyrpc-amqp',
    license='BSD',
)
