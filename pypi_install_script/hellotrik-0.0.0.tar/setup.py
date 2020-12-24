# -*- coding:utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = [
    'numpy>=1.13',
]

if __name__ == '__main__':
    setup(name='hellotrik',
          version="0.0.0",
          author='hellotrik',
          url='https://space.bilibili.com/489142974',
          author_email="hellotrik@foxmail.com",
          description='🗡♥',
          long_description="## [🗡♥](https://hellotrik.github.io)", 
          long_description_content_type="text/markdown",
          platforms=['MS Windows', 'Mac X', 'Unix/Linux'],
          license='MIT',
          keywords=['计算机视觉'],
          packages=['hellotrik','hellotrik/kernel','hellotrik/examples',],
          include_package_data=True,
          install_requires=install_requires,
          classifiers=["Natural Language :: English",
                       "Programming Language :: Python",
                       "Operating System :: Microsoft :: Windows",
                       "Operating System :: Unix",
                       "Operating System :: MacOS",
                       "Programming Language :: Python :: 3",
                       ],
          zip_safe=True)
