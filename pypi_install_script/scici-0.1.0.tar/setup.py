import setuptools

setuptools.setup(
    name="scici",
    version="0.1.0",
    url="https://github.com/scici/sci",

    author="scici",
    author_email="sci@sci.ci",

    description="design, automate and share any lab experiment",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
