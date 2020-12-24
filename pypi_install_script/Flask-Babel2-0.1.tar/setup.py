"""
Flask-Babel
-----------

Adds i18n/l10n support to Flask applications with the help of the
`Babel`_ library.

Links
`````

* `documentation <http://pythonhosted.org/Flask-Babel/>`_
.. _Babel: http://babel.edgewall.org/

"""
from setuptools import setup


setup(
    name='Flask-Babel2',
    version='0.1',
    url='http://github.com/lepture/flask-babel',
    license='BSD',
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    description='Adds i18n/l10n support to Flask applications',
    long_description=__doc__,
    py_modules=['flask_babel'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Babel',
        'pytz',
        'speaklater>=1.2',
        'Jinja2>=2.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
