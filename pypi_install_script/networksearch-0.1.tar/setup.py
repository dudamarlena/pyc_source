from setuptools import setup

setup(name='networksearch',
      version='0.1',
      description='A lib for search network overlaps',
      url='https://github.com/HenriqueCaires/network-search',
      author='Henrique Caires',
      author_email='henrique@caires.net.br',
      license='MIT',
      packages=['networksearch'],
      install_requires=[
          'netaddr',
      ],
      zip_safe=False)