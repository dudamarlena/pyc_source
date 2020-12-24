# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
LONGDOC = """
用于读取参数文件

"""

setup(name='pfp-tsc',
      version='0.1.3',
      description='Parameter file processing',
      long_description=LONGDOC,
      author='Shicheng Tan',
      author_email='xxj.tan@gmail.com',
      license='GPL License',
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
      ],
      keywords='Parameter',
      packages=find_packages(),
)
