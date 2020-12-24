import setuptools

setuptools.setup(
    name = 'hellomars',
    version = '1.0.0',
    description = 'Say hello to Mars.',
    author = 'Ryan Yuan',
    author_email = 'ryan.yuan@outlook.com',
    url = 'https://github.com/ryanyuan/hellomars',
    packages = setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'hellomars = hellomars.__main__:main'
        ]
    }
)