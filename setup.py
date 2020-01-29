#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'django-heroku-simple'
DESCRIPTION = 'This is a fork of django-heroku, which does not require psycopg2.'
URL = ''
EMAIL = 'ehmatthes@gmail.com'
AUTHOR = 'Eric Matthes'

# What packages are required for this module to be executed?
# REQUIRED = [
#     'dj-database-url>=0.5.0', 'whitenoise', 'psycopg2', 'django'
# ]
# DEV: How many of these can be moved to extras?
# REQUIRED = [
#     'dj-database-url>=0.5.0', 'whitenoise', 'django', 'gunicorn'
# ]
# EXTRAS_REQUIRED = [
#     'psycopg2'
# ]

# DEV: How stable would this test be?
#      Is there a better default marker?
#      Would it be better to set my own unique env var, ie DEPLOY_ENVIRONMENT?
# DEV: This could be simplified into if-else.
print("--- Setting requirements for django-heroku-simple ---")
print(f"  PYTHONHOME: f{os.environ.get('PYTHONHOME')}")
if not os.environ.get('PYTHONHOME'):
    # Can't be heroku, assume local use and install minimal dependencies.
    REQUIRED = [
        'dj-database-url>=0.5.0', 'whitenoise', 'django',
    ]
elif 'heroku' in os.environ.get('PYTHONHOME'):
    # Assume we're in a heroku build process.
    REQUIRED = [
        'dj-database-url>=0.5.0', 'whitenoise', 'django', 'gunicorn', 'psycopg2'
    ]
else:
    # User has PYTHONHOME set, but we're not in Heroku.
    REQUIRED = [
        'dj-database-url>=0.5.0', 'whitenoise', 'django',
    ]
print(f"  REQUIRED: {REQUIRED}")
print("--- Finished setting required. ---")

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'django_heroku', '__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    # extra_requires = {
    #     'fail_gracefully_with_no_postgres': EXTRAS_REQUIRED,
    # },
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
