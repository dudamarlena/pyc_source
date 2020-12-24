import setuptools

setuptools.setup(
    name='phdtools',
    version='0.1',
    url='https://git.rwth-aachen.de/kai.dresia/ecosim_gym_interface',
    download_url = 'https://git.rwth-aachen.de/kai.dresia/ecosim_gym_interface/-/archive/V1.0/ecosim_gym_interface-V1.0.tar.gz',
    license='MIT',
    author='Kai Dresia',
    install_requires=["cairocffi", "cairosvg", "cffi", "cloudpickle", "cssselect2", "defusedxml", "future", "gym",
                      "html5lib", "jinja2", "markupsafe", "numpy", "pillow", "pycparser", "pyglet", "pyphen", "scipy",
                      "six", "tinycss2", "weasyprint", "webencodings"],
    author_email='kai.dresia@dlr.de',
    description='A package of useful utilities :)'
)