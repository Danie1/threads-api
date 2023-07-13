from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='threads-api',
    version='1.1.6',
    description='Unofficial Python client for Meta Threads.net API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Saad',
    author_email='danielsaad777@gmail.com',
    url='https://github.com/danie1/threads-api',
    packages=find_packages(),
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)