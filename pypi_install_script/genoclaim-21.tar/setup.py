#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='genoclaim',
    version='21',
    url='https://bitbucket.org/bthate/genoclaim',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=""" "the king admitted he knows these medicine are poison, which makes his acts knowingly, should be enough to plead quilty for genocide." - https://genoclaim.rtfd.io - OTP-CR-117_19 - otp.informationdesk@icc-cpi.int""",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib"],
    scripts=["bin/genoclaim"],
    packages=["genoclaim"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
