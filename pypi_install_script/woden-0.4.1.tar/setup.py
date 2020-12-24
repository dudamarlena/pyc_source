from setuptools import setup

setup(name='woden',
      version='0.4.1',
      packages=[
          'woden', 'woden.model', 'woden.utils', 'woden.parsers', 'woden.engine'
      ],
      url='https://github.com/awakenedhaki/odin',
      license='GNU GPLv3',
      author='awakenedhaki',
      author_email='',
      description='Web scraping library for scholarly search engine sites.',
      python_requires='>=3',
      install_requires=['requests', 'beautifulsoup4', 'click'])
