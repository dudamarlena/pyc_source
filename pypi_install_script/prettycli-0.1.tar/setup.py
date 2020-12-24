from distutils.core import setup
setup(
    name='prettycli',         # How you named your package folder (MyLib)
    packages=['prettycli'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='bsd-3-clause',
    # Give a short description about your library
    description='A collection of utils for printing colors, shapes etc to the command line',
    author='Noah Yoshida',                   # Type in your name
    author_email='nyoshida@nd.edu',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/noyoshi/prettycli',
    # I explain this later on
    download_url='https://github.com/noyoshi/prettycli/archive/v0.1.tar.gz',
    # Keywords that define your package best
    keywords=['cli', 'colorizer', 'colors'],
    install_requires=[],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        # Again, pick a license
        'License :: OSI Approved :: BSD License',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
