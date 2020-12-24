from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(
    name='SLAB_Diffusion',
    version='0.0.2',
    description='models the radiative diffusion of photons through a slab of CSM and evaluates the observed radius and temperature',
    #long_description=long_description,
    #long_description_content_type='text/markdown',
    url='https://github.com/maayane/SLAB-Diffusion',  # Optional
    author='Maayane T. Soumagnac',
    author_email='maayane.soumagnac@weizmann.ac.il',  # Optional
    classifiers=[ 
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3.5',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],

    keywords='astronomy',  # Optional

    packages=["SLAB_Diffusion"],
    install_requires=['numpy','matplotlib'],  # Optional
    python_requires='>=2.7.10',

    project_urls={ 	
        'Bug Reports': 'https://github.com/maayane/SLAB-Diffusion/issues',
        'Source': 'https://github.com/maayane/SLAB-Diffusion',
    },
)

