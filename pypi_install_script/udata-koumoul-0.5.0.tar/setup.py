#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
import re

from os.path import join, dirname

from setuptools import setup, find_packages

RE_MD_CODE_BLOCK = re.compile(r'```(?P<language>\w+)?\n(?P<lines>.*?)```', re.S)
RE_SELF_LINK = re.compile(r'\[(.*?)\]\[\]')
RE_LINK_TO_URL = re.compile(r'\[(?P<text>.*?)\]\((?P<url>.*?)\)')
RE_LINK_TO_REF = re.compile(r'\[(?P<text>.*?)\]\[(?P<ref>.*?)\]')
RE_LINK_REF = re.compile(r'^\[(?P<key>[^!].*?)\]:\s*(?P<url>.*)$', re.M)
RE_BADGE = re.compile(r'^\[\!\[(?P<text>.*?)\]\[(?P<badge>.*?)\]\]\[(?P<target>.*?)\]$', re.M)
RE_TITLE = re.compile(r'^(?P<level>#+)\s*(?P<title>.*)$', re.M)

BADGES_TO_KEEP = []

RST_TITLE_LEVELS = ['=', '-', '*']

RST_BADGE = '''\
.. image:: {badge}
    :target: {target}
    :alt: {text}
'''


def md2pypi(filename):
    '''
    Load .md (markdown) file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - travis ci build badges
    '''
    content = io.open(filename).read()

    for match in RE_MD_CODE_BLOCK.finditer(content):
        rst_block = '\n'.join(
            ['.. code-block:: {language}'.format(**match.groupdict()), ''] +
            ['    {0}'.format(l) for l in match.group('lines').split('\n')] +
            ['']
        )
        content = content.replace(match.group(0), rst_block)

    refs = dict(RE_LINK_REF.findall(content))
    content = RE_LINK_REF.sub('.. _\g<key>: \g<url>', content)
    content = RE_SELF_LINK.sub('`\g<1>`_', content)
    content = RE_LINK_TO_URL.sub('`\g<text> <\g<url>>`_', content)

    for match in RE_BADGE.finditer(content):
        if match.group('badge') not in BADGES_TO_KEEP:
            content = content.replace(match.group(0), '')
        else:
            params = match.groupdict()
            params['badge'] = refs[match.group('badge')]
            params['target'] = refs[match.group('target')]
            content = content.replace(match.group(0),
                                      RST_BADGE.format(**params))
    # Must occur after badges
    for match in RE_LINK_TO_REF.finditer(content):
        content = content.replace(match.group(0), '`{text} <{url}>`_'.format(
            text=match.group('text'),
            url=refs[match.group('ref')]
        ))

    for match in RE_TITLE.finditer(content):
        underchar = RST_TITLE_LEVELS[len(match.group('level')) - 1]
        title = match.group('title')
        underline = underchar * len(title)

        full_title = '\n'.join((title, underline))
        content = content.replace(match.group(0), full_title)

    return content


long_description = '\n'.join((
    md2pypi('README.md'),
    md2pypi('CHANGELOG.md'),
    ''
))


setup(
    name='udata-koumoul',
    version='0.5.0',
    description='Theme for Koumoul demo opendata portal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://demo.koumoul.com',
    author='Koumoul',
    author_email='contact@koumoul.com',
    packages=['udata_koumoul'],
    include_package_data=True,
    install_requires=[],
    entry_points={
        'udata.themes': [
            'koumoul = udata_koumoul'
        ]
    },
    license='MIT',
    zip_safe=False,
    keywords='udata, theme, udata-koumoul',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
