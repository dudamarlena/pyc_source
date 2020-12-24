
from distutils.core import setup
setup(
  name = 'jzhu_autocomplete',         # How you named your package folder (MyLib)
  packages = ['jzhu_autocomplete'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Autocomplete with a trie structure',   # Give a short description about your library
  author = 'Junyi Sabrina Zhu',                   # Type in your name
  author_email = 'sabrinazhu96@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/junyi-zhu/jzhu_autocomplete',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/junyi-zhu/jzhu_autocomplete/archive/v0.4.tar.gz',    # I explain this later on
  keywords = ['autocomplete', 'trie', 'weights'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pytest',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)

