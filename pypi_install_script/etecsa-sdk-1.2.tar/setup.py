from distutils.core import setup
from setuptools import find_packages


files = ["Commercial/*","Payment/*","Commercial/ECRM/*","Payment/Transfermovil/*"]

setup(
  name = 'etecsa-sdk',
  packages = ['EtecsaSDK'],
  package_data = {'EtecsaSDK' : files },
   
  version = '1.2',     
  license='MIT',       
  description = 'Etecsa SDK',  
  author = 'sebastian',
  author_email = 'sebastian.rodriguez@etecsa.cu',      
  url = 'https://github.com/sebastiancuba/etecsa-sdk',  
  download_url = 'https://github.com/sebastiancuba/etecsa-sdk/archive/v1.1.tar.gz',    
  keywords = ['sdk'], 
  install_requires=[
      'requests',
      'validators',
      'pendulum',
          ],
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
)