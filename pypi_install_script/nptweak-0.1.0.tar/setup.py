from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='nptweak',
      version='0.1.0',
      description='utility functions for numpy',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/nptweak',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['nptweak'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.14.5'],
      python_requires='>=3.7',
      zip_safe=False)
