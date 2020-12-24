import sys
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


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
    'pytest',
    'requests_mock',
    'mock',  # needed for Python 2
]

dev_require = tests_require + [
    'ipython'
]


setup(name='dragonpanda',
      version='0.1.0',
      description='Python Client for the DragonPanda API',
      long_description='This software is provided as a way to include DragonPanda API functionality in your own Python '
                       'software. You can read about the DragonPanda API at http://www.dragonpanda.net',
      url='https://github.com/datarobot/dragonpandaclient-py',
      author='DragonPanda',
      author_email='support@dragonpanda.net',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=[
          'requests', 'requests_toolbelt'
      ],
      tests_require=tests_require,
      extras_require={
          'dev': dev_require
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
