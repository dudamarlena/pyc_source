from setuptools import setup

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()
    readme = readme[:readme.find('<!--- cut --->')]

setup(
    name='sphinx-configurator',
    version='0.0.0.dev0',
    description='Manage your sphinx plugin\'s directive settings with ease',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Vladimir Goncharov',
    author_email='dev.zelta@gmail.com',
    url='https://github.com/AmatanHead/sphinx-configurator',
    py_modules=['sphinx_configurator'],
    install_requires=[
        'sphinx>=1.8.0,<2.0.0',
    ],
    python_requires='>=3.7',
    license='MIT',
    keywords='sphinx',
    project_urls={
        'Documentation': 'https://amatanhead.github.io/sphinx-configurator/',
        'Source': 'https://github.com/AmatanHead/sphinx-configurator',
        'Tracker': 'https://github.com/AmatanHead/sphinx-configurator/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Topic :: Software Development :: Documentation',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
    ],
)
