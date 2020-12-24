from distutils.core import setup
setup(
  name = 'topsis-tushar-101703589',         # How you named your package folder (MyLib)
  packages = ['topsis-tushar-101703589'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Topsis analysis of a numeric csv file',   # Give a short description about your library
  author = 'Tushar Mahajan',                   # Type in your name
  author_email = 'tushar2210mahajan@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/tmahajan1/topsis-tushar-101703589',   # Provide either the link to your github or to your website
  keywords = ['TOPSIS', 'MCDM', 'Statistics'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
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
