# -*- coding: utf8 -*-

import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except:
    readme = ""
    
setup(
    name="pybossa-gravatar",
    version="0.0.1",
    author="Alexander Mendes",
    author_email="alexanderhmendes@gmail.com",
    description="A PyBossa plugin for Gravatar integration.",
    license="BSD",
    url="https://github.com/alexandermendes/pybossa-gravatar",
    packages=find_packages(),
    long_description=readme,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python 2.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    test_suite="tests",
)