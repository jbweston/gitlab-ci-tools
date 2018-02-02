# -*- coding: utf-8 -*-
from setuptools import setup

import versioneer


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

setup(
    name='gitlab-ci-tools',
    author='Joseph Weston',
    author_email='joseph@weston.cloud',
    description='Tools for working inside Gitlab CI',
    license='BSD 2-Clause',
    version=versioneer.get_version(),
    url='https://github.com/jbweston/gitlab-ci-tools',
    cmdclass=versioneer.get_cmdclass(),
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
