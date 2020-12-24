#!/usr/bin/env python3
from setuptools import setup

with open('README.md','r',encoding='utf-8') as f:
    description = f.read()

setup(
    name='jdAptDirReinstall',
    version='1.0',
    description='Reinstall all packages that have files in a directory',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/JakobDev/jdAptDirReinstall',
    author='JakobDev',
    include_package_data=True,
    packages=['jdAptDirReinstall'],
    entry_points={
        'console_scripts': ['jdAptDirReinstall = jdAptDirReinstall.jdAptDirReinstall:main']
    },
    license='BSD',
    keywords=['JakobDev','ubuntu','debian','apt','apt-file'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
