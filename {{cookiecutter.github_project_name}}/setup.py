#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
from os.path import join as pjoin
import os
import sys

from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, setup, get_data_files, here, get_package_data
)


# The name of the project
name = '{{ cookiecutter.python_package_name }}'

# Ensure a valid python version
ensure_python('>=3.3')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = os.path.join(here, name, 'nbextension', 'static')
lab_path = os.path.join(here, name, 'labextension', '*.tgz')

# Representative files that should exist after a successful build
jstargets = [
    os.path.join(nb_path, 'extension.js'),
    os.path.join(here, 'lib', 'plugin.js'),
]

cmdclass = create_cmdclass('jsdeps')
cmdclass['jsdeps'] = combine_commands(
    install_npm(here, build_cmd='build:all'),
    ensure_targets(jstargets),
)

package_data = {
    name: get_package_data(name, [
        'nbextension/static/*.*js*',
        'labextension/*.tgz'
    ])
}

data_files = [
    ('share/jupyter/nbextensions/{{ cookiecutter.npm_package_name }}',
        get_data_files(pjoin(nb_path, '*.js*'))),
    ('share/jupyter/lab/extensions', get_data_files(lab_path))
]


setup_args = dict(
    name            = name,
    description     = '{{ cookiecutter.project_short_description }}',
    version         = version,
    scripts         = glob(pjoin('scripts', '*')),
    cmdclass        = cmdclass,
    packages        = find_packages(),
    package_data    = package_data,
    data_files      = data_files,
    author          = '{{ cookiecutter.author_name }}',
    author_email    = '{{ cookiecutter.author_email }}',
    url             = 'https://github.com/{{ cookiecutter.github_organization_name }}/{{ cookiecutter.python_package_name }}',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'Widgets', 'IPython'],
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Jupyter',
    ],
)


setuptools_args = dict(include_package_data=True)
install_requires = setuptools_args['install_requires'] = [
    'ipywidgets>=7.0.0',
]

extras_require = setuptools_args['extras_require'] = {
    'test': [
        'pytest',
        'pytest-cov',
        'nbval',
    ],
    'docs': [
        'sphinx',
        'recommonmark',
        'sphinx_rtd_theme'
    ],
}

if 'setuptools' in sys.modules:
    setup_args.update(setuptools_args)

    setup_args.pop('scripts', None)

    setup_args.update(setuptools_args)

if __name__ == '__main__':
    setup(**setup_args)
