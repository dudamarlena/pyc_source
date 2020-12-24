import setuptools

setuptools.setup(
    name='seinfeld_laugh_corpus',
    version='1.0.13',
    packages=['seinfeld_laugh_corpus',
              'seinfeld_laugh_corpus.corpus_creation.utils', 'seinfeld_laugh_corpus.corpus_creation.data_merger',
              'seinfeld_laugh_corpus.corpus_creation.external_tools',
              'seinfeld_laugh_corpus.corpus_creation.subtitle_getter',
              'seinfeld_laugh_corpus.corpus_creation.laugh_extraction',
              'seinfeld_laugh_corpus.corpus_creation.screenplay_downloader', 'seinfeld_laugh_corpus.humor_recogniser',
              'seinfeld_laugh_corpus.humor_recogniser.data_generation_scripts'],
    package_data={'': ['the_corpus/*']},
    url='https://github.com/ranyadshalom/seinfeld_laugh_corpus',
    license='MIT',
    author='Ran Yad-Shalom, Yoav Goldberg',
    author_email='ranyadshalom@gmail.com',
    description='A humor annotated corpus of Seinfeld episodes.'
)

