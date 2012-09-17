"""
py2app/py2exe build script for XBL Growl.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""
import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'xblgrowl.py'

if sys.platform == 'darwin':
    options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        options={
            'py2app': {
                'argv_emulation': True,
                'iconfile': 'xblgrowl.icns',
                'plist': {
                    'LSUIElement': True,
                },
            },
        },
    )
elif sys.platform == 'win32':
    options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    options = dict(
        scripts=[mainscript],
    )

setup(
    name='XBL Growl',
    **options
)
