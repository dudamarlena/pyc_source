from distutils.core import setup
setup(
  name = 'pull_automator',         # How you named your package folder (MyLib)
  packages = ['pull_automator'],   # Chose the same as "name"
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automates the process of pulling git updates to multiple projects',   # Give a short description about your library
  author = 'Matt Ackerman',                   # Type in your name
  author_email = 'ackerman.j.matt@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Matt-Ackerman',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Matt-Ackerman/pull_automator/archive/0.4.tar.gz',    # I explain this later on
  keywords = ['git', 'pull', 'repo'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'validators',
    'validators',
    'beautifulsoup4',
    'colorama',
    'gitdb2',
    'GitPython',
    'smmap2'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7'
  ],
)
