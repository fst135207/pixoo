#!/usr/bin/python
"""
    Setup.py file for pixoo package
"""
from setuptools import setup


setup(
    name="pixoo",
    version="0.7.0",
    author="Felix Stalder",
    description=(
        "Pixoo64 pixel display programmed with python with adaptiv weather Icons, temperature, date, time",
    ),
    license="BSD",
    keywords="pixoo",
    url="https://github.com/fst135207/pixoo#readme",
    packages=['pixoo'],
    install_requires=[
        'requests ~= 2.31.0',
        'Pillow ~= 10.0.0',
    ],
)
