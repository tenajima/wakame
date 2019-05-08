from setuptools import setup

setup(
    name='wakame',
    version='0.1.0',
    author='tenajima',
    author_email='tenajima@gmail.com',
    url='https://github.com/tenajima/wakame',
    install_requires=[
        'pandas',
        'mecab-python3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Mac OS X",
    ]
)