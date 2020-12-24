from distutils.core import setup

setup(
    name='Flask-Church',
    version='0.0.1',
    packages=['flask_church'],
    install_requires=[
        'flask',
        'church'
    ],
    keywords=['church', 'fake', 'data'],
    url='https://github.com/lk-geimfari/flask_church',
    license='BSD',
    author='Lk Geimfari',
    author_email='likid.geimfari@gmail.com',
    description='Flask-Church is a extension for \
    Flask that help you generate fake data for testing'
)
