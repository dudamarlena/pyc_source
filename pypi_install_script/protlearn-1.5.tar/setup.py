from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'protlearn',       
  packages = ['protlearn'], 
  package_data={'protlearn': ['docs/*.csv']},  
  version = '1.5',      
  license='MIT',        
  description = 'Preprocessing, feature engineering, and visualization of proteins and peptides', 
  long_description_content_type='text/markdown',
  long_description=long_description,  
  author = 'Thomas Dorfer',                   
  author_email = 'thomas.a.dorfer@gmail.com',   
  url = 'https://github.com/tadorfer/ProtLearn',   
  download_url = 'https://github.com/tadorfer/ProtLearn/archive/v1.5.tar.gz',  
  keywords = ['amino acids', 'proteins', 'peptides', 'preprocessing', 'feature engineering', 'visualization'], 
  setup_requires = ['wheel'],
  install_requires=[            
          'numpy',
          'pandas',
          'scikit-learn',
          'seaborn',
          'matplotlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)