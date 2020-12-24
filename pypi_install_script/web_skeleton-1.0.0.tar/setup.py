# -*- encoding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

if sys.version_info[:2] < (2, 6):
    raise RuntimeError('Requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

from web_skeleton import __version__

requires = [
    'ghtml',
    'yuicompressor',
    'mako',
    'envoy',
    'webassets',
]

setup(
    name='web_skeleton',
    version=__version__,
    description='Static html code generator to build Js-Yuneta applications.',
    long_description=README + '\n\n',  # + CHANGES,
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    author='ginsmar',
    author_email='niyamaka at yuneta.io',
    url='https://bitbucket.org/yuneta/web-skeleton',
    license='MIT License',
    keywords='html static generator mako webassets scss sass compass yuneta',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=[],
    test_suite="web-skeleton.tests",
    entry_points="""\
        [console_scripts]
        web-skeleton = web_skeleton.main:main
    """,
)
