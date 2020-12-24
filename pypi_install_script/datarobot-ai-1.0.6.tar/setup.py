import re
import sys
from os import path
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'PACKAGE_README.md')) as f:
    long_description = f.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


tests_require = [
    'pandas',
    'pytest',
    'requests_mock',
    'mock',  # needed for Python 2
    'future',  # needed for Python 2
    'pylint',
    'pylint2junit'
]

release_require = [
    'zest.releaser[recommended]>=6.13.5,<6.14',
    'readme-renderer>=24.0,<25.0',
    'setuptools >= 38.6.0',
    'wheel >= 0.31.0',
    'twine >= 1.11.0',
]

dev_require = tests_require + [
    'ipython',
    'sphinx==1.8.3',
    'sphinx_rtd_theme==0.1.9',
    'nbsphinx>=0.2.9,<1',
    'nbconvert>=5.3,<6',
    'numpydoc>=0.8.0',
]


with open('datarobotai/_version.py') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


setup(name='datarobot-ai',
      version=version,
      description='Python Client for the DataRobot AI API',
      long_description_content_type="text/markdown",
      long_description=long_description,
      url='https://github.com/datarobot/datarobot-ai-py',
      author='DataRobot, Inc',
      author_email='support@datarobot.com',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=[
          'requests', 'requests_toolbelt', 'six', 'backports.csv'
      ],
      tests_require=tests_require,
      extras_require={
          'dev': dev_require,
          'release': release_require,
          'recommended': ['pandas==0.24.2'],
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      cmdclass={'test': PyTest},
      include_package_data=True,
      zip_safe=False)
