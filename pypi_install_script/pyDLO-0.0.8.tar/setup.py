from distutils.core import setup
setup(
  name = 'pyDLO',         # How you named your package folder (MyLib)
  packages = ['pyDLO'],   # Chose the same as "name"
  version = '0.0.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Some stuff to simulate a DLO',   # Give a short description about your library
  author = 'Alfonso Letizia',                   # Type in your name
  author_email = 'letizia.lns@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/alfonsoletizia1/pyDLO',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/alfonsoletizia1/pyDLO/archive/v0.0.8.tar.gz',    # I explain this later on
  keywords = ['DLO', 'Deformable linear objects'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
          'bspline',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

