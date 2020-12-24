from distutils.core import setup
setup(
  name = 'getDataAA',         
  packages = ['getDataAA'],  
  version = '0.1.0',     
  license='MIT',       
  description = 'Get the miles required to obtain a ticket from the AA web page',
  author = 'YOUR NAME',  
  author_email = '19.beta.Orionis@gmail.com',   
  url = 'https://github.com/bOrionis/getDataAA',  
  download_url = 'https://github.com/bOrionis/getDataAA/archive/getDataAA-0.1.0.tar.gz', 
  keywords = ['Miles', 'airplane tickets', 'Aerolineas Argentinas'],  
  install_requires=[        
          'request',
          'bs4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: End Users/Desktop',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',    
  ],
)