from setuptools import setup, find_packages

setup(
    name='threads-api',
    version='1.0.0',
    description='Unofficial Python client for Meta Threads API',
    author='Danie1',
    author_email='',
    url='https://github.com/danie1/threads-api',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)