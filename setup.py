#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import os

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

here = os.path.abspath(os.path.dirname(__file__))

# put package test requirements here
requirements = [
    "wheel",
    "future",
    "sh",
    "boto",
    "requests",
    "markdown",
    "jinja2",
    "pyconfig",
    "PyYaml",
    "redis",
    "multipledispatch"
]

# put package test requirements here
test_requirements = [

]

setup(
    name='stackhut',
    version='0.1.0',
    description="Run your software in the cloud",
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst').replace('.. :changelog:', '') + '\n\n' +
                      read('AUTHORS.rst')),
    license='Apache',
    author="StackHut",
    author_email='stackhut@stackhut.com',
    url='https://github.com/stackhut/stackhut-tool',    
    packages=[
        'stackhut', 'stackhut.barrister'
    ],
#    package_dir={'stackhut-tool':
#                 'stackhut-tool'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stackhut = stackhut.__main__:main',
        ],
    },
    install_requires=requirements,
    zip_safe=False,
    test_suite='tests',
    tests_require=test_requirements,

    keywords='stackhut',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Private :: Do Not Upload', # hack to force invalid package for upload

    ],
)