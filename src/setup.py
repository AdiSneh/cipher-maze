from setuptools import setup, find_packages

setup(
    name='cipher-maze',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'bidict',
        'decorator',
        'pydantic',
    ],
)
