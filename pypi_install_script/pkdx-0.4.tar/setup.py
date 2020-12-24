from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

install_requires = [
    'pykemon==0.1.2',
    'requests==2.0.1',
    'docopt==0.6.1',
    'beautifulsoup4==4.3.2'
]

version = '0.4' # VERSION

setup(name='pkdx',
    version=version,
    description="Command line tool for quick Pokemon info",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: End Users/Desktop',
      'Environment :: Console',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2 :: Only',
      'Topic :: Utilities'
    ],
    keywords='pokemon pykemon pokeapi',
    author='PocketEngi',
    author_email='pocketengi@gmail.com',
    url='https://github.com/PocketEngi/pkdx',
    license='MIT',
    packages=find_packages('pkdx'),
    package_dir = {'': 'pkdx'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['pkdx=pkdx.main:main']
    }
)
