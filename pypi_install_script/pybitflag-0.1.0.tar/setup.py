from distutils.core import setup
setup(
  name = 'pybitflag',         # How you named your package folder (MyLib)
  packages = ['pybitflag'],   # Chose the same as "name"
  version = '0.1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Store / retrieve multiple states or values in a single 64 bit integer',   # Give a short description about your library
  author = 'Steve Zhan',                   # Type in your name
  author_email = 'sridwan981@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/sridwan',   # Provide either the link to your github or to your website
  download_url = 'https://bitbucket.org/NarindoCMA/bitflag/get/0.1.0.tar.gz',    # I explain this later on
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
  ],
)
