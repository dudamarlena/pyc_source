import os
import re
from setuptools import setup


setup(name='week-of-year',
      version='0.0.2',
      description='返回当前是今年的第几周',
      author="Neeky",
      author_email="neeky@live.com",
      maintainer='Neeky',
      maintainer_email='neeky@live.com',
      scripts=['bin/week-of-year'],
      packages=['wofy'],
      url="https://github.com/Neeky/wofy",
      python_requires='>=3.6.*',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8']
      )
