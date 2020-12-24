from distutils.core import setup
from setuptools import find_packages

setup(name='HSAuth',  # 包名
      version='1.0.3',  # 版本号
      description='',
      long_description='',
      author='',
      author_email='',
      url='https://gitlab.com/zmbgitlab',
      license='',
      install_requires=['Flask', 'requests'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
