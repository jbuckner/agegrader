#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme_file = f.read()

with open('LICENSE') as f:
    license_file = f.read()

setup(
    name='agegrader',
    version='0.0.1',
    description='Calculates age-graded performance factors for running races',
    long_description=readme_file,
    author='Jason Buckner',
    author_email='jason@jasonbuckner.com',
    url='https://github.com/jbuckner/agegrader',
    license=license_file,
    packages=find_packages(exclude=('tests', 'docs')),
    package_dir={'agegrader': 'agegrader'},
    package_data={
        'agegrader': ['age_grading_data.json'],
    },
    scripts=['bin/agegrader'],

)
