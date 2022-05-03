from setuptools import setup, find_packages
import os

with open('requirements.txt') as file_requirements:
    requirements = file_requirements.read().splitlines()

setup_requirements = [
    'nose==1.3.7',
    'flake8==3.3.0'
]

setup(
    name='athena',
    version='0.1',
    description='parallel computation made simple',
    url='https://github.com/jordanrule/athena',
    packages=find_packages(exclude=os.path.join('tests')),
    install_requires=requirements,
    setup_requires=setup_requirements,
    test_suite='nose.collector'
)
