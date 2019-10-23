
import os
from setuptools import setup, find_packages


basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, 'VERSION'), 'r') as _f:
    __version__ = _f.read().strip()


setup(
    name='winder',
    version=__version__,
    description="LNLS magnet's group coil winder control package",
    url='https://github.com/lnls-ima/winder',
    author='lnls-ima',
    license='GNU License',
    packages=find_packages(),
    install_requires=[
        'qtpy',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
    include_package_data=True)
