import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='malwoverviewwin',
    version='2.5.0.1',
    packages=['malwoverviewwin', 'malwoverviewwin\conf'],
    scripts=['malwoverviewwin\malwoverview.py','malwoverviewwin\conf\configmalw.py'],
    author="Alexandre Borges",
    author_email="alexandreborges@blackstormsecurity.com",
    description="Malwoverview is a first response tool for profiling malware samples, URLs, submitting and downloading malware samples.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexandreborges/malwoverview",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    python_requires='>=3.7',
    install_requires = [
        "pefile >= 2019.4.18",
        "python-magic >= 0.4.15",
        "colorama >= 0.4.3",
        "simplejson >= 3.17.0",
        "requests >= 2.22.0",
        "validators >= 0.14.1",
        "geocoder >= 1.38.1",
        "polyswarm-api >= 1.1.1",
        "python-magic-bin==0.4.14",
    ],
)
