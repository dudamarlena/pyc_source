from distutils.core import setup
import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))


def get_version():
    f = open(os.path.join(here, "VERSION"), "r")
    return f.read()


def get_requirements():
    f = open(os.path.join(here, "requirements.txt"), "r")
    return f.read().split("\n")


setup(
    name='dprep',
    packages=['dprep'],
    version=get_version(),
    license='MIT',
    # Give a short description about your library
    description='Lightweight data preparation library for artificial intelligence and data science, built on top of pandas',
    author='Eyk Rehbein',
    author_email='eykrehbein@gmail.com',
    url='https://github.com/eykrehbein/dprep',
    download_url='https://github.com/eykrehbein/dprep/archive/v_'+get_version() + \
    '.tar.gz',
    # Keywords that define your package best
    keywords=['data', 'data science', 'ai', 'artificial intelligence'],
    install_requires=get_requirements(),
    include_package_data=True,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
