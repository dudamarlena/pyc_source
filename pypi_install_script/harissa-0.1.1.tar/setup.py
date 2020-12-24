from setuptools import setup, find_packages
 
# notez qu'on importe la lib
# donc assurez-vous que l'import n'a pas d'effet de bord
import harissa
 
# Ceci n'est qu'un appel de fonction. Mais il est trèèèèèèèèèèès long
# et il comporte beaucoup de paramètres
setup(
 
    # le nom de votre bibliothèque, tel qu'il apparaitra sur pypi
    name='harissa',
 
    # la version du code
    version=harissa.__version__,
 
    # Liste les packages à insérer dans la distribution
    # plutôt que de le faire à la main, on utilise la foncton
    # find_packages() de setuptools qui va cherche tous les packages
    # python recursivement dans le dossier courant.
    # C'est pour cette raison que l'on a tout mis dans un seul dossier:
    # on peut ainsi utiliser cette fonction facilement
    packages=find_packages(),
 
    # votre pti nom
    author='Ulysse Herbach',
 
    # Votre email, sachant qu'il sera publique visible, avec tous les risques
    # que ça implique.
    author_email='ulysse.herbach@ens-lyon.fr',
 
    # Une description courte
    description='Tools for mechanistic-based gene network inference',
 
    # Une description longue, sera affichée pour présenter la lib
    # Généralement on dump le README ici
    long_description=open('README.md').read(),
 
    # Vous pouvez rajouter une liste de dépendances pour votre lib
    # et même préciser une version. A l'installation, Python essayera de
    # les télécharger et les installer.
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    # install_requires=['numpy', 'scipy', 'matplotlib'],
    # Version minimale de Python
    python_requires='>=2.7',
 
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
 
    # Une url qui pointe vers la page officielle de votre lib
    url='https://github.com/ulysseherbach/harissa',
 
    # Il est d'usage de mettre quelques metadata à propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # Il n'y a pas vraiment de règle pour le contenu. Chacun fait un peu
    # comme il le sent. Il y en a qui ne mettent rien.
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    # Platformes
    platforms='any',
    # C'est un système de plugin, mais on s'en sert presque exclusivement
    # Pour créer des commandes, comme "django-admin".
    # Par exemple, si on veut créer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # créé automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    # entry_points = {
    #     'console_scripts': [
    #         'proclame-sm = sm_lib.core:proclamer',
    #     ],
    # },
 
    # A fournir uniquement si votre licence n'est pas listée dans "classifiers"
    # ce qui est notre cas
    license='MIT',
    
    # Mots-clés
    keywords='stochastic gene networks',
    # Il y a encore une chiée de paramètres possibles, mais avec ça vous
    # couvrez 90% des besoins
 
)

