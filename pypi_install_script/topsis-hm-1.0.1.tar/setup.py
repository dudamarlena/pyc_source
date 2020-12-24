from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis-hm",
    version="1.0.1",
    description="A Python package to get toposis rankings for any table.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/haymant1998/topsos-Haymant",
    author="Haymant Mangla",
    author_email="haymant_1998@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis-hm"],
    include_package_data=True,
    install_requires=["numpy","pandas"],
    EntryPoint={
        "console_scripts": [
            "topsis-hm=topsis-hm.topsis:main",
        ]
    },
)
