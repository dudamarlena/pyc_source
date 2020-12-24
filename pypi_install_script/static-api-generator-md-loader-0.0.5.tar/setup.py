from setuptools import setup

url = (
    'https://github.com/cryptomaniac512/python-static-api-generator-md-loader')

setup(
    author='Nikita Sivakov',
    author_email='cryptomaniac.512@gmail.com',
    description='Markdown loader for static API generator',
    install_requires=[
        'Markdown==2.6.9',
        'static-api-generator==0.0.1',
        'markdown-full-yaml-metadata==0.0.2',
    ],
    keywords='static api generator markdown loader',
    license='MIT',
    long_description_markdown_filename='README.md',
    name='static-api-generator-md-loader',
    py_modules=['markdown_loader'],
    setup_requires=['setuptools-markdown'],
    url=url,
    version="0.0.5",
)
