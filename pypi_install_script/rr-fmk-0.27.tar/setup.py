from distutils.core import setup
#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["usuarios/*"]


setup(
  name = 'rr-fmk',
  packages = ['rr-fmk'], # this must be the same as the name above
  version = '0.27',
  description = 'repositorio con funciones reutilizables para django ',
  author = 'Rodrigo Ramos',
  author_email = 'rodrigohernan.ramos@gmail.com',
  package_data = {'rr-fmk' : files },
  include_package_data=True,
  url = 'https://github.com/RodrigoHernan/rr-django', # use the URL to the github repo
  download_url = 'https://github.com/RodrigoHernan/rr-django/tree/master/',
  keywords = ['testing', 'logging', 'example'],
  classifiers = [],
)