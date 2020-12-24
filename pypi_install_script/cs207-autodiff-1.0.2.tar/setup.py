from distutils.core import setup
setup(
  name = 'cs207-autodiff',         # How you named your package folder (MyLib)
  packages = ['autodiff'],   # Chose the same as "name"
  version = '1.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automatic differentiatoin package for CS207',   # Give a short description about your library
  author = 'CS207 group 30',                   # Type in your name
  author_email = 'csiviy@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/rocketscience0/cs207-FinalProject/tree/milestone3',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Automatic differentiation'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy==1.17.3',
          'pytest',
          'pytest-cov',
          'codecov',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)