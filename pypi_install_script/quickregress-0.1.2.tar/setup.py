import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='quickregress',         # How you named your package folder (MyLib)
    packages=['quickregress'],   # Chose the same as "name"
    version='0.1.2',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Provides a low-effort wrapper for sklearn\'s polynomial regression',   # Give a short description about your library
    long_description_content_type="text/markdown",
    long_description=long_description,
    author='Ryan Hattie',                   # Type in your name
    author_email='ryan@hattie.email',      # Type in your E-Mail
    url='https://github.com/hexaguin/quickregress',   # Provide either the link to your github or to your website
    download_url='https://github.com/hexaguin/quickregress/archive/v_01.tar.gz',    # I explain this later on
    keywords=['sklearn', 'regression'],
    install_requires=[            # I get to this in a second
        'numpy',
        'sklearn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
