# -*- coding: utf-8 -*-
from setuptools import setup

requirements = [
    'python-gitlab',
]

dev_requirements = [
    'pylint',
    'pep8',
]

classifiers =[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3 :: Only',
    'Intended Audience :: Developers',
    'Topic :: Utilities',
]

with open('README.rst') as readme_file:
    long_description = readme_file.read()

# Loads version.py module without importing the whole package.
def get_version_and_cmdclass(package_path):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('version',
                                   os.path.join(package_path, '_version.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass('gitlab_ci_tools')

setup(
    name='gitlab-ci-tools',
    author='Joseph Weston',
    author_email='joseph@weston.cloud',
    description='Tools for working inside Gitlab CI',
    license='BSD 2-Clause',
    version=version,
    url='https://github.com/jbweston/gitlab-ci-tools',
    cmdclass=cmdclass,
    platforms=['GNU/Linux'],
    packages=['gitlab_ci_tools'],
    long_description=long_description,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    entry_points={
        'console_scripts': {
            'last-good-build = gitlab_ci_tools.last_good_build:main',
        }
    },
)
