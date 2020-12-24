from distutils.core import setup

setup(
    name='keyword_text_analyser',  # How you named your package folder (MyLib)
    packages=['keyword_text_analyser'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='A Library which extracts keywords from a given string using the TextRank algorithm which is based on '
                'the PageRank algorithm',
    # Give a short description about your library
    author='Alena Osipova',  # Type in your name
    author_email='x19114877@student.ncirl.ie',  # Type in your E-Mail
    url='https://github.com/AlenKAOs',  # Provide either the link to your github or to your website
    download_url='https://github.com/AlenKAOs/keyword_text_analyser/archive/v_01.tar.gz',  # I explain this later on
    keywords=['PageRank', 'TextRank', 'Keywords', 'Extractor'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'numpy',
        'spacy',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which python versions that you want to support
    ],
)
