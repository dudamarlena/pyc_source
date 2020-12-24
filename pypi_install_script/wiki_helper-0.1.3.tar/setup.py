from setuptools import setup

setup(name='wiki_helper',
      version='0.1.3',
      description='Helpers for extracting some data from Wikipedia',
      url='https://bitbucket.org/amist/wiki_helper',
      author='Amitay Stern',
      author_email='stern.amitay@gmail.com',
      license='MIT',
      packages=['wiki_helper'],
      install_requires=[
          'requests',
          'beautifulsoup4',
      ],
      zip_safe=False)
