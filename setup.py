# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "imm_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="ImmunoMatch",
    author_email="info@prenosis.com",
    url="",
    keywords=["Swagger", "ImmunoMatch"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['apispec/ImmMatch_API_1_0_0.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['imm_server=imm_server.__main__:main']},
    long_description="""\
    ImmunoMatch API documentation for use with Immunix ED
    """
)
