from distutils.core import setup
setup(
    name = 'idea',
    version = '0.1',
    description = 'Stores your ideas in own database',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['idea'],
    entry_points='''
        [console_scripts]
        idea=idea:cli
    ''',
)
