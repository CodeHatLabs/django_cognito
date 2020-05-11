import os
from setuptools import setup, find_packages


setup(
    name='django_cognito',
    version=0.0,
    author='Code Hat Labs, LLC',
    author_email='dev@codehatlabs.com',
    url='https://github.com/CodeHatLabs/django_cognito',
    description='Django tools for AWS Cognito integration',
    packages=find_packages(),
    long_description="",
    keywords='python',
    zip_safe=False,
    install_requires=[
        'requests',
        'boto3',
        'python-jose',
    ],
    test_suite='',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
