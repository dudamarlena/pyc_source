import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='glycon',
    version='0.2.0',
    packages=['glycon', 'glycon_menu_blocks', 'glycon_summaries'],
    include_package_data=True,
    license='GPL v3',
    description='A Django-based CMS.',
    long_description='README.md',
    url='http://www.glycon.org/',
    author='Ben Collier',
    author_email='bmcollier@gmail.com',
    scripts=['bin/glycon-setup.py'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	'Topic :: Internet :: WWW/HTTP',
   ],
)
