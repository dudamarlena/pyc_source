import os
from setuptools import find_packages
from distutils.core import setup


setup(
  name = 'grpcool',         # How you named your package folder (MyLib)
  packages=find_packages(),
  version = '0.8',      # Start with a small number and increase it with every change you make
  license='Apache 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An easy to use grpc library.',   # Give a short description about your library
  long_description = open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
  long_description_content_type="text/markdown",
  author = 'Ilya Kharlamov',                   # Type in your name
  author_email = 'ilya.kharlamov@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ilyakharlamov/grpcool',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ilyakharlamov/grpcool/archive/0.8.tar.gz',    # I explain this later on
  keywords = ['GRPC', 'EASY', 'PROXY', 'PROTO', 'PROTOBUF'],   # Keywords that define your package best
  install_requires=list(map(
     str.strip,
     open(os.path.join(os.path.dirname(__file__), "requirements.txt")),
  )),
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
