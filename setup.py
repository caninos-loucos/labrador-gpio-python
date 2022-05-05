# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

setup(
    name='labrador_gpio',
    version='0.1.0',
    description='A Library for gpio',
    long_description_content_type='text/markdown',
    author='Geovane Fedrecheski',
    packages=find_packages(exclude=('tests', 'docs'))
)
