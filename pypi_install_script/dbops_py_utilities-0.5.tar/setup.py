import setuptools
from distutils.core import setup
setup(
  name = 'dbops_py_utilities',         # How you named your package folder (MyLib)
  packages = setuptools.find_packages(),   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  #license='',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'python utilites for DevOps/SRE',   # Give a short description about your library
  author = 'Santosh Kumar',                   # Type in your name
  author_email = 'skumar21886@gmail.com',      # Type in your E-Mail
  #url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Demandbase/dbops-py-utilities/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['DevOps'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'django',
          'datadog',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    #'License :: ,   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)
