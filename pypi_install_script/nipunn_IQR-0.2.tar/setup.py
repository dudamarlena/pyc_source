from distutils.core import setup
setup(
  name = 'nipunn_IQR',         
  packages = ['nipunn_IQR'],   
  version = '0.2',      
  license='MIT',        
  description = 'Row Elimination in a dataset using interquartile range method',   
  author = 'Nipunn Malhotra',                   
  author_email = 'nipunnjg@gmail.com',      
  url = 'https://github.com/nipunnmalhotra/nipunn_IQR',   
  download_url = 'https://github.com/nipunnmalhotra/nipunn_IQR/archive/v_02.tar.gz',    
  keywords = ['Outliers removal', 'Row Elimination'],   
  install_requires=[           
          'numpy',
        'pandas'
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
  ],
)