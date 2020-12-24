from distutils.core import setup
setup(
  name = 'AK_PY_PKG_SIMPLY',         # How you named your package folder (MyLib)
  packages = ['AK_PY_PKG_SIMPLY'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'SIMPLFY TEXT',   # Give a short description about your library
  author = 'AKSHAY LUNGARE',                   # Type in your name
  author_email = 'lungareakshay@gmial.com',      # Type in your E-Mail
  url = 'https://github.com/lungareakshay/ak-py-pkg-simply.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lungareakshay/ak-py-pkg-simply/archive/0.5.tar.gz',    # I explain this later on
  keywords = ['SIMPLFY TEXT','AKSHAY MARATHI', 'MURAKAMI','2MAY'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        #   'validators',
        #   'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',#Specify which pyhton versions that you want to support
  ],
)