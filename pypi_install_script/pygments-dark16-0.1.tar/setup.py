#!/usr/bin/python

from setuptools import setup

setup(
    name = 'pygments-dark16',
    version = '0.1',
    description = 'Pygments version of dark "base16" theme.',
    license = 'BSD',

    author = 'Beorn Facchini',
    author_email = 'beornf@gmail.com',

    url = 'https://github.com/beornf/pygments-dark16',
    download_url = 'https://github.com/beornf/pygments-dark16/archive/1.0.tar.gz',

    packages = ['pygments_dark16'],
    install_requires = ['pygments >= 1.4'],

    entry_points = '''[pygments.styles]
                      base16-dark = pygments_dark16:Base16DarkStyle''',

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
