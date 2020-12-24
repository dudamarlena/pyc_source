from distutils.core import setup
setup(
  name = 'pnp_datetime',         # How you named your package folder (MyLib)
  packages = ['pnp_datetime'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python datetime that simple as Plug and Play style',   # Give a short description about your library
  author = 'pypnp',                   # Type in your name
  author_email = 'pypnp@protonmail.com',      # Type in your E-Mail
  url = 'https://github.com/pypnp/pnp_datetime',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/pypnp/pnp_datetime/archive/0.2.tar.gz',    # I explain this later on
  keywords = ['datetime', 'Plug and Play', 'simple'],   # Keywords that define your package best
  install_requires=['pytz'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
  ],
)
