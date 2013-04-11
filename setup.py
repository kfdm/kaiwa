from setuptools import setup
from kaiwa.version import __version__

setup(
    name='kaiwa',
    description='Extract conversations into a more readable format',
    author='Paul Traylor',
    url='http://github.com/kfdm/kaiwa/',
    version=__version__,
    packages=['kaiwa'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'kaiwa = kaiwa.cli:main'
        ]
    }
)
