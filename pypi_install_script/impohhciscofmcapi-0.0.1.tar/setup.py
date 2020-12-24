from distutils.core import setup
setup(
  name = 'impohhciscofmcapi',         # How you named your package folder (MyLib)
  packages = ['impohhciscofmcapi'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The Library for Cisco REST API Firepower',   # Give a short description about your library
  author = 'Anuchit Ketngam',                   # Type in your name
  author_email = 'porclub.por@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/impohh/impohhciscofmcapi',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/impohh/impohhciscofmcapi',    # I explain this later on
  keywords = ['Cisco FMC', 'Cisco API FMC', 'Object Cisco FMC', 'REST API Cisco Firepower'],   # Keywords that define your package best
  install_requires=[
          'openpyxl','requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
  ],
)