
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
  name = 'gmail_trainer',         # How you named your package folder (MyLib)
  packages = ['gmail_trainer'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'get mail notifications when your training is completed',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Aymeric de la Brousse',                   # Type in your name
  author_email = 'aymericdelabrousse@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aymericdelab/gmail_trainer',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aymericdelab/gmail_trainer/archive/v_07.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'google-api-python-client',
          'google-auth-httplib2',
		  'google-auth-oauthlib',
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
  ],
)