from setuptools import setup, find_packages

setup(name='inoa',
    version='0.0.0',
    url='https://gitlab.com/ubp-ds/innovations/inoa-python.git',
    author='Red Periabras',
    author_email='raperiabras@unionbankph.com',
    description='Utility package for names',
    packages=find_packages(),
    install_requires=[
        'pandas==0.23.3',
        'numpy==1.14.5',
        'tensorflow==1.9.0',
        'Keras==2.2.2',
        'dill==0.3.1.1'
    ],
    package_dir={'inoa': 'inoa'},
    package_data={'inoa': ['bin/']},
    long_description=open('README.md').read(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.5'
    )
