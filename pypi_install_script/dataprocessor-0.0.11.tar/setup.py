from distutils.core import setup
setup(
  name = 'dataprocessor',         # How you named your package folder (MyLib)
  packages = ['dataprocessor'],   # Chose the same as "name"
  version = '0.0.11',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Data piping system for a pandas DataFrame with a DateTimeIndex',   # Give a short description about your library
  author = 'Hans Roggeman',                   # Type in your name
  author_email = 'hansroggeman2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hraoyama/dataprocessor',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/hraoyama/dataprocessor/archive/0.0.1.tar.gz',    # I explain this later on
  keywords = ['data pipe', 'DataFrame', 'DateTimeIndex'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'faker',
          'pandas',
	  'numpy',
	  'datetime',
	  'typing'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6', #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7', #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8', #Specify which pyhton versions that you want to support
  ],
)