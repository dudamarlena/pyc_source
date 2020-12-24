from setuptools import setup

distributed_version = '0.0.4-alpha'

setup(
    name='galoup',
    version=distributed_version,
    packages=['galoup'],
    url='https://github.com/liampulles/galoup',
    license='MIT',
    author='Liam Pulles',
    author_email='me@liampulles.com',
    description='Galoup is a Python framework for rolling your own project management tool.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        "colorama"
    ]
)
