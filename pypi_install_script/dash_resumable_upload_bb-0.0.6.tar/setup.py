from setuptools import setup

exec (open('dash_resumable_upload_bb/version.py').read())


setup(
    name='dash_resumable_upload_bb',
    version=__version__,
    author='marrenr',
    packages=['dash_resumable_upload_bb'],
    include_package_data=True,
    license='MIT',
    description='Dash Resumable Upload component for large files.',
    install_requires=[],
    download_url='https://github.com/den-mi/dash-resumable-upload-bb/archive/0.0.6.tar.gz'
)
