from distutils.core import setup
setup(
  name = 'simporter_test_helpers',         # How you named your package folder (MyLib)
  packages = ['simporter_test_helpers'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Just testing pypi',   # Give a short description about your library
  author = 'Kupazavr',                   # Type in your name
  author_email = 'kirill@simporter.com',      # Type in your E-Mail
  url = 'https://github.com/Kupazavr/helpers',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Kupazavr/helpers/archive/master.zip',    # I explain this later on
  keywords = ['simporter_test_helpers', 'simporter', 'simporter_helpers'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)