from distutils.core import setup
setup(
  name = 'autocomplete_richardshu',         # How you named your package folder (MyLib)
  packages = ['autocomplete_richardshu'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An autocomplete program that gives suggestions',   # Give a short description about your library
  author = 'Richard Shu',                   # Type in your name
  author_email = 'richardshuv@icloud.com',      # Type in your E-Mail
  url = 'https://github.com/shshu526/autocomplete_richardshu',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/shshu526/autocomplete_richardshu/archive/V0.4.tar.gz',    # I explain this later on
  keywords = ['Autocomplete', 'Trie', 'Insert', 'Delete'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pytest'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)