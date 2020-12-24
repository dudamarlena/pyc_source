from distutils.core import setup
from setuptools import find_packages

setup(name="img_merge",  # 包名
      version='20200506',  # 版本号
      description='',
      long_description='',
      author='',
      author_email='409766147@qq.com',
      url='',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )

#!/usr/bin/env python
