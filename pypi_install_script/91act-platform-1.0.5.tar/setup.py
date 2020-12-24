import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="91act-platform",
    version="1.0.5",
    author="leo",
    author_email="leo@91act.com",
    description="A small Tools",
    long_description=long_description,
    url="https://github.com/PepperPapa/xinNotes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'requests',
        'python-crontab',
        'pymysql',
        'flask',
        'Flask-Session'
    ]
)
