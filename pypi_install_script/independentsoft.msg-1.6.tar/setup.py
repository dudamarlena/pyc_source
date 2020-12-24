from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
  name = 'independentsoft.msg',         # How you named your package folder (MyLib)
  packages = ['independentsoft.msg'],   # Chose the same as "name"
  version = '1.6',      # Start with a small number and increase it with every change you make
  license='Other/Proprietary License',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Outlook .msg file format module',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/x-rst',
  author = 'Independentsoft',                   # Type in your name
  author_email = 'info@independentsoft.de',      # Type in your E-Mail
  url = 'http://www.independentsoft.de',   # Provide either the link to your github or to your website
  download_url = 'http://www.independentsoft.de',    # I explain this later on
  keywords = ['outlook', 'msg', 'independentsoft'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Communications :: Email',
    'Topic :: Office/Business',
    'License :: Other/Proprietary License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
  python_requires='>=3.3',
)