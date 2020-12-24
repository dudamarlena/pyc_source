from distutils.core import setup
setup(
  name = 'bin_by_median',         # How you named your package folder (MyLib)
  packages = ['bin_by_median'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Calculate min-max values for each records in your dataset.',   # Give a short description about your library
  author = 'Sachin Thakur',                   # Type in your name
  author_email = 'sachin.thakur@mca.christuniversity.in',      # Type in your E-Mail
  url = 'https://github.com/sachinthakur9614/bin_by_median.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/sachinthakur9614/bin_by_median/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['binning method', 'bin_by_median', 'python','Data Mining'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'itertools',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
