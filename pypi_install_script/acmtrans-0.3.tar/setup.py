from distutils.core import setup
setup(
  name='acmtrans',         # How you named your package folder (MyLib)
  packages=['acmtrans'],   # Chose the same as "name"
  version='0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='This is a net spider program by Python to collect a list of ACM transaction papers.',   # Give a short description about your library
  author='Stephen Fan',                   # Type in your name
  author_email='caixiang@ualberta.ca',      # Type in your E-Mail
  url='https://github.com/DDSystemLab/acmtrans',   # Provide either the link to your github or to your website
  download_url='https://github.com/DDSystemLab/acmtrans/archive/0.3.tar.gz',    # I explain this later on
  keywords=['ACM', 'transaction', 'papers', 'spider'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'beautifulsoup4',
          'requests',
      ],
  classifiers=[
    # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which Pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)