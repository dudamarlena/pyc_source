import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='MagicStat',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU Lesser General Public License v3.0',
    description='A platform of exploring and analyzing structured data in a minute.',
    long_description=README,
    url='https://www.magicstat.co',
    author='Fatih Şen',
    author_email='fatih@merjek.com',
	keywords = ['statistics', 'data-analysis', 'correlation'],   # Keywords that define your package best
    classifiers=[
		'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3',   # GNU Lesser General Public License v3.0
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering'
    ],
)