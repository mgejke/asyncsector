from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.2.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [
    x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')
]

setup(
    name='asyncsector',
    version=__version__,
    description='Asynchronous package for Sector Alarm',
    long_description=long_description,
    url='https://github.com/mgejke/asyncsector',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    keywords=['sector', 'alarm'],
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Martin Gejke',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='martin@gejke.se',
    python_requires='>=3.6.0',
    entry_points={
        'console_scripts': ['asyncsector = asyncsector.__main__:main']
    })
