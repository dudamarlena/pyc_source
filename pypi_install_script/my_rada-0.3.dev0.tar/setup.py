from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='my_rada',
      version=version,
      description="My rada",
      long_description="""\
My test verhovna rada""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Abstract fuctory',
      author='Trush Vasyl',
      author_email='vinclaw78@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
            'console_scripts': [
                  'rada = my_rada.verh_rada:main',
            ]
      },
      )
