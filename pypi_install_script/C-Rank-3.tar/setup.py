from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='C-Rank',
      version='03',
      url='https://github.com/maurodlt/C-Rank',
      license='MIT',
      author='Mauro DL Tosi',
      author_email='maurodlt@hotmail.com',
      description='Extracts Keyphrases from Documents',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=True,
      download_url='https://github.com/user/maurodlt/C-Rank/archive/v_02.tar.gz',
      install_requires=[
          'nltk',
          'networkx',
          'pybabelfy',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
