from setuptools import setup


setup(
    name='parseltongue',
    version='0.0.2',
    py_modules=['parseltongue'],
    author="Mark Steve Samson",
    author_email="hello@marksteve.com",
    url='https://github.com/marksteve/parseltongue',
    description="Render HTML pages using Markdown and Jinja",
    license="MIT",
    install_requires=[
        'Jinja2==2.6',
        'markdown2==2.1.0',
    ],
    entry_points={
        'console_scripts': [
            'parseltongue=parseltongue:main'
        ],
    },
)
