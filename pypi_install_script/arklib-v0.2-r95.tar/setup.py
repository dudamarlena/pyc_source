#!/usr/bin/env python

# NOTE DO NOT RUN THIS SCRIPT DIRECTLY 
# RELEASE_VERSION IS REPLACED BY THE RELEASE SCRIPT

from setuptools import setup, find_packages

setup (
    name = 'arklib',
    version = 'v0.2-r95',
    description = 'Ark python library',
    author = 'Nam Pham',
    author_email = 'phamducnam@gmail.com',
    url = 'http://to/be/setup',
    packages = find_packages(),
    install_requires = ['boto', 'pyyaml'],
    entry_points = {
      'console_scripts': [
        'ark-ec2-tags = arklib.cli.ark_ec2_tags:main',
        'ark-set-dns = arklib.cli.ark_set_dns:main',
        'ark-puppet-apply = arklib.cli.ark_puppet_apply:main',
        'ark-backup-dir = arklib.cli.ark_backup_dir:main',
        'ark-restore-dir = arklib.cli.ark_restore_dir:main'
        ]
      }
    )
