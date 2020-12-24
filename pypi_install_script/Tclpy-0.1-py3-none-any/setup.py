import setuptools
with open('Tclpy/README.md', 'r') as rd:
    ld = rd.read()


setuptools.setup(
    name = 'Tclpy',
    version = '0.1',


    author = 'Robert',
    author_email = 'xsumagravity@gmail.com',


    description = 'Tkinter in python might not work if not in bash.',
    lf = ld,


    url="",
    packages = setuptools.find_packages(),


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ]
)