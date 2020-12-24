#!/usr/bin/env python
from setuptools import setup, find_packages

# with open("README.rst", "r") as fh:
#     long_description = fh.read()

setup(name='piomart',
      version=open('VERSION').read().strip()
      ,description='Tool to query Ensemble restful api and get gene info'
      ,author='Diego Crespo'
      ,author_email='diegocrespo@protonmail.com'
      ,install_requires=[_.strip() for _ in open('requirements.txt')]
      ,packages=find_packages(exclude=['docs', 'tests*'])
      ,url='https://gitlab.com/diegocrespo/piomart'
      ,license='MIT'
      ,classifiers=[
        'Development Status :: 3 - Alpha'
        ,'Intended Audience :: Science/Research'
        ,'Environment :: Console'
        ,'License :: OSI Approved :: MIT License'
        ,'Programming Language :: Python :: 3'
        ,'Topic :: Scientific/Engineering :: Bio-Informatics'
      ]
      ,entry_points={
          'console_scripts': [
              'piomart=piomart.piomart:main'
          ]
      }
      ,keywords='bioinformatics dataframe ensembl commandline'
      ,python_requires='~=3.5'
     )
