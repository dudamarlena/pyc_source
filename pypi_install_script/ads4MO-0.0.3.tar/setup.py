from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='ads4MO',
      version='0.0.3',
      description='Python module which adds new CMEMS downloads services (applied mainly to big data requests)',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/d4mo",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      python_requires='~=3.6',

      install_requires=[
        'motuclient>=1.8.1',
        'ftputil>=3.4'

      ],

      packages=find_packages(),
      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
