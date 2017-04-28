import codecs
from setuptools import setup, find_packages


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()


setup(
        name='watchedserial',
        version='1.0.1',
        description=('Module for handling pySerial Serial objects connecting '
            'and disconnecting'),
        long_description=long_description(),
        author='Eric Oswald',
        author_email='eoswald39@gmail.com',
        license='MIT',
        packages=find_packages(exclude=['examples, test']),
        install_requires=['pyserial']
)
