from setuptools import setup


with open('requirements/core.txt') as core_txt:
    core_req = [line for line in core_txt.read().splitlines() if line]
with open('requirements/analysis.txt') as analysis_txt:
    analysis_req = [line for line in analysis_txt.read().splitlines() if line]
with open('requirements/beagle_collection.txt') as beagle_collection_txt:
    beagle_collection_req = [line for line in beagle_collection_txt.read().splitlines() if line]
with open('requirements/rpi_collection.txt') as rpi_collection_txt:
    rpi_collection_req = [line for line in rpi_collection_txt.read().splitlines() if line]

try:
    import pypandoc
    from os import path
    here = path.abspath(path.dirname(__file__))
    long_description = pypandoc.convert(path.join(here, 'README.md'), 'rst'),
except RuntimeError:
    long_description = ""
except ImportError:
    long_description = ""

setup(
    name='scs-installer',
    version='0.1.11',
    description='Installer/Meta package for South Coast Science Software',
    author='South Coast Science',
    author_email='contact@southcoastscience.com',
    url='https://github.com/south-coast-science/scs-installer',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=[
        'dev_scripts/install_dev_analysis.py',
        'dev_scripts/install_dev_beagle_collection.py',
        'dev_scripts/install_dev_rpi_collection.py',
    ],
    install_requires=core_req,
    platforms=['any'],
    python_requires=">=3.3",
    extras_require={
        'analysis': analysis_req,
        'beagle_collection': beagle_collection_req,
        'rpi_collection': rpi_collection_req,
    }
)
