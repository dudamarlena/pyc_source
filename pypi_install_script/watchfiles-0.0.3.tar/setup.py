# -*- coding: utf-8 -*-
"""Setup file for watchfiles."""

from setuptools import find_packages, setup

setup(
    name='watchfiles',
    packages=find_packages(),
    version='0.0.3',
    entry_points={
        'console_scripts': ['wf = watchfiles.watchfiles:main']
    },
    description='Polling file watcher',
    author='Cody Hiar',
    author_email='codyfh@gmail.com',
    url='https://github.com/thornycrackers/watchfiles',
    keywords=['file watcher', 'watcher'],
    license='MIT',
    install_requires=['click', 'blessings'])
