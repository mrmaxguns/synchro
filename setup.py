"""The setup file for synchro

Based off of https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='synchro',
    version='0.0.1',
    description='A differential synchronization library for client and server-side use',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mrmaxguns/synchro',
    author='Maxim R.',
    author_email='mrmaxguns@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Communications :: File Sharing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='collaboration, differential synchronization, diff-match-patch, diff, sync',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['diff-match-patch'],
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/mrmaxguns/synchro/issues',
        'Source': 'https://github.com/mrmaxguns/synchro/',
    },
)
