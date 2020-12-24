from setuptools import setup

setup(
    name='Flask-Heroku-Helpers',
    version='0.0.2',
    url='https://bitbucket.org/fbochu/flask_heroku_helpers',
    #license='MIT',
    author='Fabien Bochu',
    author_email='fabien.bochu@gmail.com',
    description='Flask helpers for Heroku Apps',
    long_description=open('README.md', 'r').read(),
    packages=[
        'flaskext',
        'flaskext.heroku_helpers',
    ],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-SSLify',
    ],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
