
from setuptools import setup 
setup(name='yxspkg_encrypt',   
      version='1.2.3',    
      description='A simple API to encrypt data. Encrypt algorithm is based on linear congruence',    
      author='Blacksong',    
      install_requires=['rsa'],
      py_modules=['yxspkg_encrypt'],
      platforms='any',
      author_email='blacksong@yeah.net',      
      entry_points={
        'console_scripts': ['encrypt=yxspkg_encrypt:main'],
    },
      url='https://github.com/blacksong',
      classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)   
