# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='bodyparser',
    version='1.1.1',

    author='Kazaryan Sargis',
    author_email='basandbuddy@mail.ru',

    url='https://github.com/YaSargis/bodyparser',
    description='parse http request body to object',

    packages=find_packages(),
    install_requires=['peppercorn'],

    license='MIT License',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='bodyparser parse body http',
)
