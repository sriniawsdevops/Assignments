from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws_list_all',
    version='0.2.0',
    description='List all your AWS resources, all regions, all services.',
    long_description=long_description,
    url='https://github.com/pkvanda/aws_list_all',
    author='srini',
    author_email='Katamssri@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='aws boto3 listings resources region services',
    packages=['aws_list_all'],
    install_requires=['boto3'],
    entry_points={
        'console_scripts': [
            'aws_list_all=aws_list_all.__main__:main',
            'aws-list-all=aws_list_all.__main__:main',
        ],
    },
)
