#!/usr/bin/env python
# vi: et sw=2 fileencoding=utf-8
#============================================================================
# Django Email Tracking
# Copyright (c) 2018 Pispalan Insinööritoimisto Oy (http://www.pispalanit.fi)
#
# All rights reserved.
# Redistributions of files must retain the above copyright notice.
#
# @description [File description]
# @created     21.08.2018
# @author      Harry Karvonen <harry.karvonen@pispalanit.fi>
# @copyright   Copyright (c) Pispalan Insinööritoimisto Oy
# @license     MIT
#============================================================================

import setuptools

setuptools.setup(
  name="django_email_tracking",
  version="0.0.1",
  author="Harry Karvonen",
  author_email="harry.karvonen@pispalanit.fi",
  description="Simple email tracking package for Django",
  url="https://git.pispalanit.fi/pit/django-email-tracking/",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 2.7",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
