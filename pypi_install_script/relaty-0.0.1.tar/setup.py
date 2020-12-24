from distutils.core import setup
setup(
  name = 'relaty',         # How you named your package folder (MyLib)
  packages = ['relaty'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Small package to build Choose Your Own Adventure-like stories',   # Give a short description about your library
  author = 'Pablo Toledo Margalef',                   # Type in your name
  author_email = 'pabloatm980@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/PaPablo/relaty/archive/v0.0.1.tar.gz',    # I explain this later on
  keywords = ['fiction', 'interactive', 'writing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'click',
          'PyYAML',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Games/Entertainment',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)