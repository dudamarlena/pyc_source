from distutils.core import setup

VERSION = 'v1.1.2'

setup(
  name = 'PyParseBio',
  packages = ['PyParseBio'],
  version = 'v1.1.2',
  license='apache-2.0',
  description = 'Pure-python parralelizable parsing of biological multipoint images',
  author = 'Wolfgang Pernice',
  author_email = 'wolfgang.pernice@gmail.com',
  url = 'https://github.com/WMAPernice/PyParseBio',
  download_url = 'https://github.com/WMAPernice/PyParseBio/archive/v1.1.2.tar.gz',
  keywords = ['Biology', 'Microscopy', 'Images', 'Python', 'Parallel'],
  install_requires=[
          'numpy',
          'scikit-image',
		  'nd2reader>=3.2.3',
		  'tqdm',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      	
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',  		
    'Programming Language :: Python :: 3.6',
  ],
)