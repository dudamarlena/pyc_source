from setuptools import setup


setup(
    name='test_vision_client',
    packages=['vision'],
    version='0.58',
    description='An upload to s3 utility',
    author='Fathom',
    author_email='mirabel.ekwenugo@andela.com',
    keywords=['upload', 'files', 's3'],
    classifiers=[],
    install_requires=[
        'requests==2.13.0',
        'pypref==2.0.0',
        'watchdog==0.8.3',
    ],
)
