import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitcoinUsingIFTTT",
    version="1.4",
    author="Praveen",
    author_email="praveenacchusn123@gmail.com",
    description="A package that allows to sent bitcoin alerts throgh IFTTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules = ['bitcoin'],
    package_dir = {'': 'src'},
    #download_url = 'https://github.com/praveenNagaraj97-au7/bitcoinAlertWithTelegram/archive/0.2.tar.gz',
    url="https://github.com/praveenNagaraj97-au7/bitcoinAlertWithTelegram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[            
          'tqdm',
          'beautifulsoup4',
          'pytz',
      ],

) 
