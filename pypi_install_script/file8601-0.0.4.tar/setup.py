# https://setuptools.readthedocs.io/en/latest/setuptools.html#developer-s-guide

import configparser
from os import geteuid as os_geteuid
import pathlib
from setuptools import setup  # ,find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.config import read_configuration  # noqa E402
import sys

repo_path = pathlib.Path(__file__).parent
setup_config_dict = read_configuration("setup.cfg")
package_path = repo_path / 'src' / setup_config_dict['metadata']['name']


def getPackageVersion(version_file_path):
	""" Returns a tuple of semantic version numbers. """
	version_path = pathlib.Path(version_file_path)
	if not version_path.exists():
		raise FileNotFoundError(f"Cannot find version configuration file: {version_path.resolve()}")

	version_parser = configparser.ConfigParser()
	version_parser.read(version_path)
	if 'VERSION' not in version_parser.keys():
		raise KeyError(f"Missing key 'VERSION' in file '{version_path}'")

	version_keys = version_parser['VERSION'].keys()
	for expected_key in ('Major', 'Minor', 'Patch'):
		if expected_key not in version_keys:
			raise KeyError(f"Missing key '{expected_key}' in file '{version_path}'")

	return (version_parser['VERSION']['Major'],
	        version_parser['VERSION']['Minor'],
	        version_parser['VERSION']['Patch'])


def preInstallSequence(_setupToolsMode):
	# Do not install package as root
	if os_geteuid() == 0:
		raise Exception("Install should be as a non-privileged user")


def postInstallSequence(_setupToolsMode):
    pass


class InstallOverride(install):
	"""Additional work when running in Install mode."""
	""" https://www.anomaly.net.au/blog/running-pre-and-post-install-jobs-for-your-python-packages/ """
	def run(self):
		preInstallSequence('install')
		install.run(self)
		postInstallSequence('install')


class DevelopOverride(develop):
	"""Additional work when running in Develop mode."""
	""" https://www.anomaly.net.au/blog/running-pre-and-post-install-jobs-for-your-python-packages/ """
	def run(self):
		preInstallSequence('develop')
		develop.run(self)
		postInstallSequence('develop')


# Extract package version from VERSION.cfg file.
version_tuple = getPackageVersion(package_path / 'data/VERSION.cfg')
version_string = '.'.join(version_tuple)

'''
Workaround because of this issue: https://github.com/pypa/setuptools/issues/1633
python_requires refers to the version of the -installed- package. Not the version of the build system.
I want to validate both, so I wrote this short assert.
'''
_MIN_PYTHON_VERSION = (3, 7, 0)  # Python 3.7.0 was released June 2018
assert (sys.version_info >= _MIN_PYTHON_VERSION),\
       "Minimum Python version is {}".format('.'.join(str(v) for v in _MIN_PYTHON_VERSION))

# This comment indicates desired length of long description-->
long_description = '''\n
File8601 is a library for stamping files' names with ISO 8601
datetime, and then performing useful indexing of such files:

- Given a list/directory of such files, generates a metadata
  dictionary about file's datetime.
- Includes sort codes, for determining the chronological order
  of files in the directory(s)
'''

# Additional elements from setup.cfg are blended automatically by Setuptools
setup(packages=['file8601'],
      package_dir={'file8601': 'src/file8601'},
      package_data={'file8601': ['data/*.cfg']},
      version=version_string,
      long_description=long_description
)
