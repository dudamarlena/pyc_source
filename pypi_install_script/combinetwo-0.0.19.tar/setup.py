# from distutils.core import setup
from setuptools import find_packages, setup

setup(
  name = 'combinetwo',         # How you named your package folder (MyLib)
  packages = find_packages(include=["helloworld", "helloworld.*"]),   # Chose the same as "name"
  version = '0.0.19',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  long_description_content_type="text/markdown",
  author = 'pkittipat',                   # Type in your name
  author_email = 'kittipat.phongsak@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Pkittipat/combinetwo.git',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/Pkittipat/combinetwo/archive/0.0.2.tar.gz',    # I explain this later on
  keywords = ['CPRINT', 'BPRINT'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'djangorestframework==3.9.2',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)