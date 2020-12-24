
from distutils.core import setup
setup(
  name = 'genalgo',         
  packages = ['genalgo'],   
  version = '1.0',      
  license='MIT',        
  description = 'Basic Pythonic Implementation of Genetic Algorithm',   
  author = 'GOSHROW',                   
  author_email = 'goshrow@gmail.com',      
  url = 'https://github.com/GOSHROW/genalgo',   
  download_url = 'https://github.com/GOSHROW/genalgo/archive/v1.0-alpha.tar.gz',    
  keywords = ['python', 'genetic algorithm', 'GA', 'algorithms', 'computational intelligence', 'CI'],   
  install_requires=[            
          'secrets',
          'random',
          'pandas',
          'matplotlib',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)