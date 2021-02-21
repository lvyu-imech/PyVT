#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

setup(
    name="pyvt",
    version="1.0",
    author="Yu Lv & Qing Liu",
    author_email="ylv@ae.msstate.edu",
    license='MIT License',
    python_requires='>=3.7.*', 
    packages=find_packages(),
    install_requires=["numpy", "vtk", "PyQt5", "matplotlib"],
    package_data={'pyvt': ['icons/*']},
    include_package_data=True,
    entry_points={'console_scripts' : ['pyvt = pyvt:code_entry']},
    zip_safe=False
    )
