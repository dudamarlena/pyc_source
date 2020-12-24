#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.install import install

VERSION = "0.1.1"

def readme():
    """ print long description """
    with open('README.md') as f:
        long_descrip = f.read()
    return long_descrip

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name = 'homeassistant-magiwand',
    packages = ['ha_magiwand'],
    version = VERSION,
    description = 'Allow MagiQuest Wands to call into HomeAssistant Webhooks',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author = 'Ryan Veach',
    author_email = 'rveach@gmail.com',
    license="MIT",
    url = 'https://gitlab.com/rveach/homeassistant-magiwand',
    download_url = 'https://gitlab.com/rveach/homeassistant-magiwand/-/archive/master/homeassistant-magiwand-master.tar.gz',
    keywords = ['wand', "magiquest", "IR", "HomeAssistant"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'pywand>=0.1.1',
        'requests>=2.20.0',
    ],
    scripts=['ha_wand_service.py'],
    python_requires='>=3.5',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    setup_requires=['wheel'],
)
