from setuptools import setup, find_packages

setup(name='automata-bless',
      version='0.0.5',
      description='A CLI application to create user accounts on Linux systems from Gitlab users/group information to use with BLESS',
      author='Brian Davis',
      author_email='slimm609@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      url = "https://github.com/slimm609/automata_bless",
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'automata=automatagl.automatagl:main',
          ],
      },
      install_requires=[
          "certifi==2019.3.9",
          "chardet==3.0.4",
          "idna==2.8",
          "PyYAML",
          "requests==2.22.0",
          "urllib3==1.25.3",
          "boto3",
      ],
    )
