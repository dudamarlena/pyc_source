from distutils.core import setup
setup(
    name = 'trial',
    version = '0.1.0',
    description = 'Trial package for checks apps for trial and stop them if time is ended for trial',
    author = 'Ivan Suroegin',
    author_email = 'ivan.suroegin@gmail.com',
    py_modules=['trial'],
    entry_points='''
[console_scripts]
trial=trial:cli
''',
)