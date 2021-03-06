from distutils.core import setup
setup(
  name = 'testandtrade',         # How you named your package folder (MyLib)
  packages = ['testandtrade'],   # Chose the same as "name"
  version = '1.3.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'https://help.github.com/articles/licensing-a-repository',   # Give a short description about your library
  author = 'Ben Urwin',                   # Type in your name
  author_email = 'benurwin@outlook.com',      # Type in your E-Mail
  url = 'https://github.com/benurwin/testandtrade.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/benurwin/testandtrade/archive/1.3.0.tar.gz',    # I explain this later on
  keywords = ['backtest', 'backtesting', 'test','testing','finance','trade','trading'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
                    'dash',
                    'pandas',
                    'plotly',
                    'flask',
                    'gevent',
                    'numpy',
                    'pathos',
                    'intrinio_sdk',
                    'pyfolio'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
