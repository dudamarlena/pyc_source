import io
from setuptools import find_packages, setup


# Read in the README for the long description on PyPI
def long_description():
    with io.open('clustering_jhk/README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(name='clustering_jhk',
      version='0.2',
      description='practice for K-Means algorithm',
      long_description=long_description(),
      author='Ji-Hoon Kim',
      author_email='genesis717.jhk@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
          ],
      zip_safe=False)