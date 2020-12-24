from distutils.core import setup
setup(
  name = 'rohandes',         # How you named your package folder (MyLib)
  packages = ['rohandes'],   # Chose the same as "name"
  version = '0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'ROHAN',   # Give a short description about your library
  author = 'Azfar Mohamed',                   # Type in your name
  author_email = 'caputfora@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/azfar154/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['ROHAN', 'DESPHANDE', 'NOTHING'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
long_description="""
This is the description of the project a simple way to use it is.
import rohandes
rohandes.rohan()
""",
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Programming Language :: Python :: 3.6',
  ],
)
