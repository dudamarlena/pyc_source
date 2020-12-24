from setuptools import setup 
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(name = "amway_eap_packagerit",
version = version,
description= "this package packages Rit",
author= "Rit Chowdhury",
packages=["amway_eap_packagerit"],
install_requires=[])