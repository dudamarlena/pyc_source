try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

config = {
    'description': 'scikit-learn confusion matrix',
    'author': 'scikit-learn developers',
    'url': 'https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['confusion_matrix'],
    'scripts': [],
    'name': 'confusion_matrix'
}

setup(**config)
