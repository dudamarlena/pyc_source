from distutils.core import setup
import sys
import os

setup(
    name='Aman',
    author='Hamza Ali',
    version='1.0',
    packages=['aman',],
    license='MIT',
    long_description=open('README.md').read(),
    scripts=['bin/aman']
)

# Creating directory containing aman storage file
HOME_PATH = os.getenv('HOME')
DIR = '.aman'
try:
	os.mkdir('{}/{}'.format(HOME_PATH, DIR))
except FileExistsError:
	pass

# Creating file to store aliases
ALIAS_FILE_NAME = 'aliases'
ALIAS_FILE_PATH = '{}/{}/{}'.format(HOME_PATH, DIR, ALIAS_FILE_NAME)
try:
	with open(ALIAS_FILE_PATH, 'w') as f:
		pass
except FileExistsError:
	pass
