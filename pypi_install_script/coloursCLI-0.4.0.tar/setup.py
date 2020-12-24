from setuptools import setup
from coloursCLI import __version__

setup(name='coloursCLI',
      version=__version__,
      description='CLI using colours_library',
      url='https://gitlab.bitcomp.intra/eryk_malczyk/colourscli',
      author='ErykMalczyk',
      author_email='eryk.malczyk@bitcomp.fi',
      license='some_licence',
      scripts=['bin/colors'],
      packages=['coloursCLI'],
      install_requires=[
          'colours_library'
      ],
      tests_require=['pytest',],
      include_package_data=True,
      zip_safe=False)