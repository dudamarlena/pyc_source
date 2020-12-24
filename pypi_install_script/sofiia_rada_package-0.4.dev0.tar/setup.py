from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='sofiia_rada_package',
      version=version,
      description="Sofiia's Verhovna Rada",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sofiia Kopach',
      author_email='sofiia.kopach@gmail.com',
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
                        'rada = sofiia_rada_package.verh_rada:main'
                  ]
      },
      )
