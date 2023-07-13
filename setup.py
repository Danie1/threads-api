from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='threads-api',
    version='1.1.5',
    description='Unofficial Python client for Meta Threads.net API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Danie1',
    author_email='',
    url='https://github.com/danie1/threads-api',
    packages=find_packages(),
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)