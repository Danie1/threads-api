from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='threads-api',
    version='1.0.4',
    description='Unofficial Python client for Meta Threads API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Danie1',
    author_email='',
    url='https://github.com/danie1/threads-api',
    py_modules=find_packages(),
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