from distutils.core import setup
setup(
    name = 'hollywood',
    version = '0.0.1',
    description = 'Get by this package info about films from IMDB',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['hollywood'],
    entry_points='''
        [console_scripts]
        hollywood=hollywood:cli
    ''',
)
