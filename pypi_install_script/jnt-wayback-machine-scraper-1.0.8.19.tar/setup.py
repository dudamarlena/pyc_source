from setuptools import find_packages, setup

description = ('A command-line utility for scraping '
               'Wayback Machine snapshots from archive.org.')
long_description = description + \
                   (' For further details, '
                    'please see the code repository on github: '
                    'https://github.com/Junte/jnt-wayback-machine-scraper')

setup(
    name='jnt-wayback-machine-scraper',
    version='1.0.8.19',
    author='Junte Ltd.',
    author_email='tech@junte.com',
    description=description,
    license='ISC',
    keywords='archive.org scrapy scraper waybackmachine',
    url="https://github.com/Junte/jnt-wayback-machine-scraper",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jnt-wayback-machine-scraper = wayback_machine_scraper.__main__:main',
        ],
    },
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Scrapy',
        'Topic :: Utilities',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
    install_requires=[
        'scrapy-wayback-machine',
    ],
)
