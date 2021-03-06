from setuptools import setup, find_packages
import os

version = '0.1'

requires = [
    'pyramid',
    'rebecca.todict',
    'bpmappers',
    'venusian',
    ]

tests_require = [
    'pytest',
    ]

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='rebecca.todict_bpmappers',
      version=version,
      description="implementation for rebecca.todict using bpmappers",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Pyramid",
        "License :: OSI Approved :: MIT License",
        ],
      keywords='',
      author='Atsushi Odagiri',
      author_email='aodagx@gmail.com',
      url='https://github.com/rebeccaframework/rebecca.todict_bpmappers',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['rebecca'],
      include_package_data=True,
      tests_require=tests_require,
      extras_require={
        "testing": tests_require,
        },
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
