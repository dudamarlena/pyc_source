"""
Gmail-Notify
==========

Gmail-Notify is a cooler looking GMail Notifier for our favorite OS.
"""

from distutils.core import setup
from gmailnotifier import __version__

print __version__
setup(

    # Required metadata
    name='Gmail-Notify',
    version=__version__,

    # Scripts
    scripts = ['bin/gmail-notifier'],
    # package information
    packages = [
        'gmailnotifier'
    ],

    package_dir = {
        'gmailnotifier': 'gmailnotifier',
    },

    package_data = {
        'gmailnotifier': [
            'images/*',
            'ui/gmail-notify-prefs/*',
            'sounds/*'
        ],
    },

    # Additional pypi metadata
    description = 'Cooler looking GMail Notifier for Ubuntu.',

    long_description = __doc__,

    url = 'http://www.soundc.de/gmail-notifier/',

    author='Uday K Verma',
    author_email='uday.karan@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Communications',
        'Topic :: Communications :: Email'
    ]
)
