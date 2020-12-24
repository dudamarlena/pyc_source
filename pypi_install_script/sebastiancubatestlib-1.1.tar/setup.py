from distutils.core import setup
setup(
  name = 'sebastiancubatestlib',         # How you named your package folder (MyLib)
  packages = ['MyTestLib'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'testing ',   # Give a short description about your library
  author = 'sebastian',                   # Type in your name
  author_email = 'sebastian.rodriguez@etecsa.cu',      # Type in your E-Mail
  url = 'https://github.com/sebastiancuba/pytest',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/sebastiancuba/pytest/archive/1.1.tar.gz',    # I explain this later on
  keywords = ['TEST'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          ],
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
)