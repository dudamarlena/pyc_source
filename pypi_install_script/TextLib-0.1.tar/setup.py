from distutils.core import setup

setup(
    name='TextLib',  # How you named your package folder (MyLib)
    packages=['TextLib'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A library for creating Text-Based Adventures',  # Give a short description about your library
    author='Riley Miller',  # Type in your name
    author_email='draxdo@gmail.com',  # Type in your E-Mail
    url='https://github.com/user/Draxdo',  # Provide either the link to your github or to your website
    download_url='https://github.com/Draxdo/TextLib/archive/0.1.tar.gz',  # I explain this later on
    keywords=['Text-Based Adventure', 'Game', 'Text'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
