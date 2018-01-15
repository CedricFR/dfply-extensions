from setuptools import setup, find_packages

setup(
    name = 'dfply_extensions',
    version = '0.0.1',
    author = 'Cedric Canovas',
    keywords = 'pandas dplyr plotly',
    packages = ['dfply_extensions'],
    include_package_data=True,
    package_dir={'dfply_extensions':'src'},
    install_requires=['numpy', 'pandas', 'dfply','cufflinks','plotly'],
    description = 'additional functions for dfply',
    long_description = 'See https://github.com/cedricfr/dfply-extensions/blob/master/README.md for details.',
    license = 'Apache License v2.0',
    url = 'https://github.com/cedricfr/dfply-extensions',
    test_suite='test',
)
