import setuptools

setuptools.setup(
    author="Giulio Cesare Mastrocinque Santo",
    name='textualjoin',
    author_email="giuliosanto@gmail.com",
    version='0.0.1.3',
    description='TextualJoin is a python package for join dataframes based on text data.',
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=["numpy","pandas","scikit-learn","spacy","nltk", "unidecode","nested_dict"],
    zip_safe=False
)