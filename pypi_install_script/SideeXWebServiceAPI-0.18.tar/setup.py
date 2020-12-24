  
from distutils.core import setup
setup(
  name = 'SideeXWebServiceAPI',
  packages = ['SideeXWebServiceAPI'],
  version = '0.18',
  license='MIT',
  description = 'The SideeX Webservice API primarily handles the transfer of test suites to the Webservice and allows the Webservice to run test cases',
  author = 'SideeX-Team',
  author_email = 'feedback@sideex.io',
  # url = 'https://github.com/joelbarmettlerUZH/Scrapeasy',
  # download_url = 'https://github.com/joelbarmettlerUZH/Scrapeasy/archive/pypi-0_1_3.tar.gz',
  keywords = ['SideeX', 'SideeX-Web-Service'],
  install_requires=[
          'requests',
          # 'asyncio',
          'aiohttp',
          # 'os'
          # 're',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)