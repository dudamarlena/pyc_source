from distutils.core import setup
setup(
  name = 'eulerlabs',        
  packages = ['eulerlabs'],   
  #version = '',      
  license='MIT',        
  description = 'SQL driven Data Science in Python',  
  author = 'Anil Singh',                  
  author_email = 'singh.ap79@gmail.com',      
  url = 'https://github.com/AnilSingh79/eulerlabs',  
  download_url = 'https://github.com/AnilSingh79/eulerlabs/archive/v1.tar.gz',   
  keywords = ['Data Science', 'SQLite', 'SQL', 'CSV','SQL query'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
