from setuptools import setup, find_packages

setup(
    name="textclip-factory",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "moviepy>=2.1.2"
    ],
    author="Hao Nghiem",
    author_email="qtvhao@gmail.com",
    description="A simple factory for creating TextClip objects in MoviePy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qtvhao/TextClipFactory.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
