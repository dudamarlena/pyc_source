from distutils.core import setup
import os.path

def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass

def get_readme():
    return get_file(os.path.dirname(__file__), 'README.rst')

setup(
  name = 'mulscrap',         # How you named your package folder (MyLib)
  packages = ['mulscrap'],   # Chose the same as "name"
  version = '0.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'NAV scrap',   # Give a short description about your library
  long_description='NAV scrap',
  author = 'kongyot',                   # Type in your name
  author_email = 'kongyot@gmail.com',      # Type in your E-Mail
  url = '',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['NAV'],   # Keywords that define your package best
  classifiers=[
    'Programming Language :: Python :: 3.7',    
  ],
)