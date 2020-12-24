from setuptools import setup
import subprocess

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='read_hnd',
	  version='0.2.3',
      description='Package to read .HND format images',
      long_description=readme(),
      author='Ben George',
      author_email='ben.geroge@oncology.ox.ac.uk',
      packages=['read_hnd'],
      install_requires=[
          'numpy',
          'scipy',
          'tqdm',
          'matplotlib'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['read_hnd=read_hnd.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)