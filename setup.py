from setuptools import setup, find_packages

setup(
    name='py-fps',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ursina',
    ],
    entry_points={
        'console_scripts': [
            'py-fps=src.main:main',
        ],
    },
)
