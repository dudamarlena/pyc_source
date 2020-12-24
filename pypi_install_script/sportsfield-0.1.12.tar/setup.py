#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
setup(
  name = 'sportsfield',         
  packages = ['sportsfield'],   
  version = '0.1.12',      
  license='MIT',        
  description = 'creating different types of sports field',   
  author = 'Vivekpandian',                   
  author_email = 'vivekpandian08@gmail.com',      
  url = 'https://github.com/vivekpandian08/sportsfield',       
  keywords = ['pitch', 'soccer', 'tennis'],   
  changes='modify the requirements, pip install matplotlip, change Soccer to soccer, change class, change in __init__, remove init, change in class name, take field out of the class,remove class,field interchange,ananya change,remove init',  
  install_requires=[           
          'matplotlib',
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

