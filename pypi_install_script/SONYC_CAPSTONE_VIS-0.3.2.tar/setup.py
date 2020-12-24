from setuptools import setup, find_packages

setup(
    name='SONYC_CAPSTONE_VIS',
    version='0.3.2',
    keywords=['SONYC', 'visualization'],
    description='SONYC Capstone Visualization Pacakge',
    long_description='This Package is used for NYU SONYC and CDS CAPSTONE TEAM. Five Modules are included, Fetch Data, Dimension Reduction, Clustering, Visualization, Debiasing',
    license='MIT',
    install_requires=["matplotlib", "numpy", "pandas", "umap", "sklearn", "h5py", "torch"],
    author='Biao',
    author_email='biaoh66@gmail.com',
    packages=find_packages(),
    platforms='any',
    url='https://github.com/Distancs/SONYC_CAPSTONE_VIS'
)
