from setuptools import setup

setup(
    name = 'somarevex',
    version = '1.0.4',
    author = 'Tiago Batista',
    author_email = 'tiago1805@gmail.com',
    packages = ['somarevex'],
    description = 'Soma dois valores e retorna o resultado',
    long_description = 'Utiliza operações binárias avançadas a fim de realizar '
                        + 'a computação necessária para a partir '
                        + 'de dois valores, retornar a soma dos mesmos',
    license = 'MIT',
    keywords = 'soma sum calc',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)