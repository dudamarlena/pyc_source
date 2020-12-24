from distutils.core import setup

setup(
  name = 'ShivFlow',
  packages = ['ShivFlow'],  
  version = '1.0.0',   
  license='MIT',        
  description = 'An asynchronous machine learning python library',
  author = 'Shivster',  
  author_email = 'shivster2401@gmail.com',  
  url = 'https://github.com/Shivster2401/ShivFlow', 
  download_url = 'https://github.com/Shivster2401/ShivFlow/archive/v1.0.0.tar.gz',
  keywords = ['AI', 'ShivFlow', 'Machine Learning'], 
  install_requires=['asyncio'],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.7',
  ],
)
