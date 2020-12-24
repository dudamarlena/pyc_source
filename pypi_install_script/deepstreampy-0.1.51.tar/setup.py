# coding: utf8
################################################################################
#
#   Autore          :   Allan Nava
#   Modificato      :   Allan Nava
#   Data            :   18/03/2020
#   Aggiornamento   :   18/03/2020
#
#################################################################################
#
import os
from setuptools import setup, find_packages
#pipenv --python 3.7
#
def requirements(filename='requirements.txt'):
    with open(filename) as f:
        requirements = f.read().splitlines()
        return requirements
    #
#
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
#
setup(name='deepstreampy',
      version='0.1.51',
      author='Yavor Paunov - Allan Nava',
      author_email='contact@yavorpaunov.com',
      description='A deepstream.io client.',
      license='MIT',
      url='https://github.com/Allan-Nava/deepstreampy',
      packages=find_packages(),
      download_url = 'https://github.com/Allan-Nava/deepstreampy/archive/v0.1.51.tar.gz', 
      classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
      install_requires=requirements(),
      long_description=read('README.md'),
      test_suite='tests')
#