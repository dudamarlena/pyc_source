# Third Party
from setuptools import setup, find_packages

# First Party
from netkit import VERSION


def run_setup():
    setup(
        name='pynetkit',
        version=VERSION,
        packages=find_packages(),
        author="Daniel Hand",
        author_email="netkit@danielhand.io",
        description="A Python library to interact with NetBox",
        url="https://github.com/dsgnr/netkit",
        download_url="https://github.com/dsgnr/netkit/archive/0.0.01.tar.gz",
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
        install_requires=["requests"],
        python_requires='!=2.*,>=3.7',
    )


if __name__ == "__main__":
    run_setup()
