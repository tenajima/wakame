from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wakame",
    version="0.2.0",
    author="tenajima",
    author_email="tenajima@gmail.com",
    url="https://github.com/tenajima/wakame",
    install_requires=["pandas", "mecab-python3"],
    description="janomeライクなインターフェイスを提供するmecabのラッパーです.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Development Status :: 3 - Alpha",
    ],
)
