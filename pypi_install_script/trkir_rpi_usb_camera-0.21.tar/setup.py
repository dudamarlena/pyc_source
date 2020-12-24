import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='trkir_rpi_usb_camera',
    version='0.21',
    scripts=['trkir-usb-install', 'trkir-usb-camera'],
    author="VPA.GROUP",
    author_email="noreply@ivpa.ru",
    description="Raspberry PI script for PT Flir and IR cameras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.vpa.group/trkir/hardware",
    packages=setuptools.find_packages(),
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: POSIX :: Linux",
    ],
)
