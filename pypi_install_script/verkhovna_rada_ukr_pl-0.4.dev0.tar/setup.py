from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='verkhovna_rada_ukr_pl',
      version=version,
      description="Ukrainian and Poland kind of parlament",
      long_description="""\
some long desc""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Oleg M',
      author_email='oleg.matviiv@gmail.com',
      url='',
      license='GPL Free License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
            'console_scripts': [
                  'rada = verkhovna_rada_ukr_pl.verh_rada:main'
            ]
      }

      )
