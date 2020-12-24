from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='numertweak',
      version='0.2.3',
      description='Some utility function for the numerai competition',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='http://github.com/kmedian/numertweak',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['numertweak'],
      install_requires=[
          'setuptools>=40.0.0',
          'numpy>=1.14.5',
          'pandas>=0.23.4',],
      python_requires='>=3.6',
      zip_safe=False)
