#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'selenium',
    'pyvirtualdisplay',
]

setup_requirements = [
    # TODO(pythad): put setup requirements (distutils extensions, etc.) here
]

setup(
    name='selenium_extensions',
    version='0.1.1',
    description="Tools that will make writing tests, bots and scrapers using Selenium much easier",
    long_description=readme + '\n\n' + history,
    author="Vladyslav Ovchynnykov",
    author_email='ovd4mail@gmail.com',
    url='https://github.com/pythad/selenium_extensions',
    packages=find_packages(include=['selenium_extensions']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='selenium_extensions',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    setup_requires=setup_requirements,
)
