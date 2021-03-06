from distutils.core import setup
setup(
  name = 'security-python',         # How you named your package folder (MyLib)
  packages = ['security-python'],   # Chose the same as "name"
  version = '1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Security Module for python',   # Give a short description about your library
  author = 'JonathanG',                   # Type in your name
  author_email = 'ceo@graffbt.com',      # Type in your E-Mail
  url = 'https://github.com/zurgeg/security-python',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/zurgeg/security-python/master/v1_3.tar.gz',    # I explain this later on
  keywords = ['Security', 'Passwords', 'Hashing'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'werkzeug'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)
