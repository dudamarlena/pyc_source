from distutils.core import setup
setup(
  name = 'blured',         # How you named your package folder (MyLib)
  packages = ['blured'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'monitor the weather condition of airports in US',   # Give a short description about your library
  author = 'kZ',                   # Type in your name
  author_email = 'robertmorrislike@gmail.com',      # Type in your E-Mail
  ##download_url = 'https://github.com/h4x0rMadness/BUEC500_api-design-private/archive/0.92.zip',    # I explain this later on
  keywords = ['intime', 'airports', 'weather'],   # Keywords that define your package best
  install_requires=[
            'requests',
            'dataflows',
            'pybase64',
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