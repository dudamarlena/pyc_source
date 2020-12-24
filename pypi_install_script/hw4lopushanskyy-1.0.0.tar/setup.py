from distutils.core import setup

setup(
  name = 'hw4lopushanskyy',
  packages = ['hw4lopushanskyy'],
  version = '1.0.0',
  license='MIT',

  description = 'The Most Popular Genres Among Top Movies Sorted by Years',
  author = 'Dmytro Lopushanskyy',
  author_email = 'lopushanskyy@ucu.edu.ua',

  long_description = """
  The Most Popular Genres Among Top Movies Sorted by Years

  The research is based on the data from IMDB, the world's largest online database of information related to films.

  How it works

  In order to run the program, you need to download its distribution from PyPI. After the program launch (main() function), you will be prompted to use default data or enter your own. The user can specify the time period from which the films will be selected, as well as the minimum ratings and the number of votes per movie. If the information is entered correctly, the database analysis will begin. When this process is completed, a window will open that will show a bar chart that will show the most popular genres of movies by the selected criteria.

  Author

  Dmytro Lopushanskyy, UCU Computer Science Student, https://github.com/DmytroLopushanskyy
  """,

  long_description_content_type='text/markdown',

)
