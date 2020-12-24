import setuptools

setuptools.setup(
    name="pybright",
    version="0.1.2",
    url="https://github.com/plavjanik/pybright",

    author="Petr Plavjanik",
    author_email="plavjanik@gmail.com",

    description="Integration of CA Brightside to Python",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=['pprint', "semver", "cached_property"],

    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'tox',
            'autopep8',
            'bumpversion',
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
