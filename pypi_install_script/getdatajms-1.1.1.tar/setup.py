from distutils.core import setup

setup(
    name = 'getdatajms',
    packages = ['getdatajms'],
    package_data = {
      'getdatajms': ['data/carInsurance_train.csv'],
   },
    version = '1.1.1',  # Ideally should be same as your GitHub release tag varsion
    description = 'Utils to download and get some data ready',
    author = 'JMS',
    author_email = 'jean.matthieu.schertzer@gmail.com',
    url = 'https://github.com/datajms/get_data_in_python',
    download_url = 'https://github.com/datajms/get_data_in_python/archive/v1.1.1.tar.gz',
    keywords = ['data', 'opendata'],
)
