from distutils.core import setup
setup(
  name = 'recipeio',
  packages = ['recipeio'],
  version = '0.1',
  license='Apache License 2.0',
  description = 'Recipe.io | ML Collaboration framework',   # Give a short description about your library
  author = 'Iman Kamyabi',                   # Type in your name
  author_email = 'iman@recipe.io',      # Type in your E-Mail
  url = 'https://recipe.io/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/recipe-io/recipeio/archive/v0.1.tar.gz',    # I explain this later on
  keywords = ['ML', 'RECIPEIO', 'RECIPE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)