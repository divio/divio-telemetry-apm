# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from telemetry_apm import __version__

setup(
    name='divio-telemetry-apm',
    version=__version__,
    description=open('README.rst').read(),
    author='Divio AG',
    author_email='info@divio.com',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[
        'django>=1.8,<2',
        'elastic-apm>=2',
        'yurl',
    ],
    include_package_data=True,
    zip_safe=False,
)
