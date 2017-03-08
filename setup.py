import os.path
from setuptools import setup, find_packages

__DIR__ = os.path.abspath(os.path.dirname(__file__))

setup(
    name = 'auraio',
    version = '0.1.0',
    description = 'Communicates important information using the atmospheric lighting of an RGB LED strip connected to a Raspberry Pi',
    url = 'https://github.com/mikeshultz/auraio',
    author = 'Mike Shultz',
    author_email = 'mike@mikeshultz.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords = 'raspberrypi led lighting monitoring',
    packages = find_packages(exclude = ['build', 'dist']),
    install_requires = open("requirements.txt").readlines(),
    entry_points={
        'console_scripts': [
            'auraio=auraio.auraio:main',
        ],
    },
)