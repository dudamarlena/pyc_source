from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pysinfit',
      version='1.0',
      description='Python module and wrapper for sinfit analysis',
      long_description='A set of module and functions to help in the sinfit processing and analysis of atmospheric gravity waves data',
      url='https://bitbucket.org/pascalbo/pysinfit/',
      author='Pascal Bourgault',
      author_email='pascal.bourgault@gmail.com',
      keywords='scientific atmospheric science physics',
      license='APACHE 2.0',
      classifiers=[
      	'Development Status :: 4 - Beta',
      	'Intended Audience :: Science/Research',
      	'License :: OSI Approved :: Apache Software License',
      	'Topic :: Scientific/Engineering :: Atmospheric Science',
      	'Topic :: Scientific/Engineering :: Physics',
      	'Programming Language :: Python :: 3',
      	'Programming Language :: Other'
      	],
      packages=['pysinfit'],
      install_requires=[
       'numpy',
       'scipy',
       'basemap',
       'netcdf4',
       'mirpyidl'
      ],
      zip_false=False)
