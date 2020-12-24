from setuptools import setup, find_packages

import fototex

with open("README.md", 'r') as fh:
    long_description = fh.read()

with open("requirements.txt") as req:
    install_req = req.read().splitlines()

setup(name='fototex',
      version=fototex.__version__,
      description='Fourier Transform Textural Ordination',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/benjaminpillot/foto',
      author='Philippe Verley <philippe.verley@ird.fr>, Pierre Couteron <pierre.couteron@ird.fr>, Nicolas Barbier '
             '<nicolas.barbier@ird.fr>, Marc Lang <marc.lang@irstea.fr>, Dominique Lyszczarz '
             '<observatoire@causses-et-cevennes.fr>, Claire Teillet <teillet.claire@hotmail.com>, Benjamin Pillot '
             '<benjamin.pillot@ird.fr>, Thibault Catry <thibault.catry@ird.fr>, Laurent Demagistri '
             '<laurent.demagistri@ird.fr>, Nadine Dessay <nadine.dessay@ird.fr>',
      install_requires=install_req,
      python_requires='>=3',
      license='GNU GPL v3.0',
      packages=find_packages(),
      zip_safe=False)
