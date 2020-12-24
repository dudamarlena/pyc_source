from setuptools import setup, find_packages

import re

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

with open('brawlwiki/__init__.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(),
        re.MULTILINE
    ).group(1)

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='brawlwiki',
    version=version,
    description='An easy to use wrapper for BrawlWiki API',
    long_description=long_description,
    url='https://github.com/AriusX7/brawlwiki',
    author='AriusX7',
    author_email='icyligii@gmail.com',
    license='MIT',
    keywords=['brawl stars, brawlstats, supercell', 'brawlwiki'],
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
    project_urls={
        'Source Code': 'https://github.com/AriusX7/brawlwiki',
        'Issue Tracker': 'https://github.com/AriusX7/brawlwiki/issues',
        'Documentation': 'http://brawlwiki.rtfd.io/',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English'
    ]
)
