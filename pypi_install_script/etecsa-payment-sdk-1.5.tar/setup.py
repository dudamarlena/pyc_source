from distutils.core import setup
from setuptools import find_packages


files = ["Transfermovil/*"]

setup(
  name = 'etecsa-payment-sdk',
  packages = ['PaymentSDK'],
  package_data = {'PaymentSDK' : files },
   
  version = '1.5',     
  license='MIT',       
  description = 'Etecsa Payment SDK ',  
  author = 'sebastian',
  author_email = 'sebastian.rodriguez@etecsa.cu',      
  url = 'https://github.com/sebastiancuba/etecsa-payment-sdk',  
  download_url = 'https://github.com/sebastiancuba/etecsa-payment-sdk/archive/v1.0.tar.gz',    
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