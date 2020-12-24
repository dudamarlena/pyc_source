# -*- coding: utf-8 -*-
import os

from setuptools import setup

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'src', 'slack_bang', 'dist-requirements.txt'), session=False)
REQUIREMENTS = [str(ir.req) for ir in install_reqs]

with open(os.path.join(os.path.dirname(__file__), 'src', 'slack_bang', 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

VERSION = os.getenv('RELEASE_VERSION', '0.1.2')


# package_data = dict(
#     (package_name,)
#     for package_name in find_packages('src')
# )


setup(
    name='slack_bang',
    version=VERSION,
    packages=['slack_bang'],
    package_dir={'': 'src'},
    # package_data=package_data,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='MIT License',
    description='Send message to slack webhook',
    long_description=README,
    url='https://git.dglecom.net/projects/OPS/repos/slack_bang/browse',
    author='Ross Crawford-d\'Heureuse',
    author_email='r.crawford@douglas.de',
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    entry_points={'console_scripts': [
        'slack_bang = slack_bang.cli:post',
        'slack_bang_web = slack_bang.cli:web',
    ], },
)
