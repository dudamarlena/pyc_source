from setuptools import setup

setup(
    name='text_preprocessor',
    version='0.0.2',
    author='Puke',
    author_email='1129090915@qq.com',
    description='This is a text preprocessor for nlp.',
    long_description='Just use it.',
    license='Apache',
    url='https://pypi.python.org/pypi',
    packages=['text_preprocessor'],
    install_requires=[
        'jieba',
        'numpy',
        'keras'
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ]
)
