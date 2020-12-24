# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 18:52:30 2020

@author: zhoupan
"""

from setuptools import setup, find_packages
 
setup(name='topotb',
      author="Pan Zhou, Lizhong Sun",
      author_email="zhoupan71234@xtu.edu.cn",
      description="a tool to get symmetry proberties of wavefunction for electrons and phonon from tight-binding model",
      version='0.0.1', 
      license = 'MIT License',
      install_requires = ["numpy",'scipy','pymatgen','pythtb','symmetry_representation','matplotlib'],
      include_package_data=True,
      packages = find_packages(),
      py_modules=['topotb'],  
      )  

