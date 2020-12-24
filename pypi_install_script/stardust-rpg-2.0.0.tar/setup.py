#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name='stardust-rpg',
    version='2.0.0',

    description='',
    long_description=open('README.rst').read(),
    keywords='stardust role-playing d20',

    author='John Hagen',
    author_email='johnthagen@gmail.com',
    url='https://github.com/johnthagen/stardust-rpg',
    license='MIT',
    install_requires=open('requirements.txt').readlines(),
    zip_safe=False,

    packages=setuptools.find_packages(),
    include_package_data=True,
    py_modules=('manage',),

    entry_points={
        'console_scripts': [
            'stardust-rpg = manage:main',
        ]
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Topic :: Games/Entertainment :: Role-Playing',
    ],
)
