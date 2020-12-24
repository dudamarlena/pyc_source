
from setuptools import setup

try: 
    from distutils.command import bdist_conda
except ImportError:
    pass

from os import path
import io

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(name='underware',
          author            = "Louis Moresi",
          author_email      = "louis.moresi@anu.edu.au",
          url               = "https://github.com/underworldcode/underware",
          download_url      = "",
          version           = "0.1b",
          description       = "Common Core for Underworld / Quagmire etc",
          long_description  =long_description,
          long_description_content_type='text/markdown',
          packages          = ['underware'],
          package_dir       = {'underware': 'underware'},
          # package_data      = {'underware': [Notebooks/*ipynb'] },
          # include_package_data = True,
          install_requires  = ['numpy>=1.16.0', 'scipy>=1.0.0', 'stripy>=1.2', 'petsc4py', 'mpi4py', 'h5py', 'pint'],
          )
