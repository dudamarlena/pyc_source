from setuptools import setup, find_packages


setup(
    name = 'logsender',
    version = '0.2',
    packages = find_packages(),
    url = 'https://github.com/Hevienz/logsender',
    license = 'Apache License Version 2.0',
    author = 'Hevienz',
    author_email = 'hevienz@qq.com',
    description = "logsender works with ELK on QingCloud. It makes logging easy.",
    install_requires = [
        "requests",
        "retry.it"
    ],
    zip_saft = True,
)
