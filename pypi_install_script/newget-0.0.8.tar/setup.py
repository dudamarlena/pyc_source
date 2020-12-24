#!/usr/bin/env python
# coding: utf-8
#coding

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='newget',
    packages=find_packages(),
    description='A script to automate the searching part of youtube-dl',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/patrickett/newget',
    download_url='https://gitlab.com/patrickett/newget/-/archive/master/newget-master.tar',
    keywords=['newget', 'rss', 'youtube', 'youtube_dl'],
    install_requires=['Unidecode','pprint','youtube-dl','feedparser','tld','vlc','click'],
    version='0.0.8',
    entry_points={
          'console_scripts': [
              'newget = newget.__main__:main'
          ]
      },
      )
