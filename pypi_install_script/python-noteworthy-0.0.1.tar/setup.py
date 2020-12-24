from setuptools import setup, find_namespace_packages

setup(name='python-noteworthy',
      url="https://noteworthy.im",
      author_email="hi@decentralabs.io",
      version='0.0.1',
      packages=find_namespace_packages(include=['noteworthy.*']),
      entry_points={
          'console_scripts': [
              'notectl = noteworthy.notectl.__main__:main'
          ]
      },
      )