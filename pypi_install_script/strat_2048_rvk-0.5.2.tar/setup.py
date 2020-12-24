# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

here = os.path.dirname(__file__)
packages = find_packages(where=here)
package_dir = {k: os.path.join(here, k.replace(".", "/")) for k in packages}

setup(name='strat_2048_rvk',
      version='0.5.2',
      description="Example of module to implement a strategy for 2048",
      long_description="Exemple de module python implémentant une "
                       "stratégie pour le jeu 2048",
      author='Kenza Abdellatif',
      author_email='kenza.abdellatif@ensae.fr',
      url='https://github.com/kenzaa20/strat_2048_rvk/',
      packages=packages,
      package_dir=package_dir,
      # requires indique quels packages doivent être installés
      # également pour que cela fonctionne
      requires='')
