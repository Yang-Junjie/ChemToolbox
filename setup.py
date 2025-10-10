# setup.py
from setuptools import setup, find_packages
import os

# 读取 README
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ChemToolbox",
    version="0.1.0",
    author="YangJunjie",
    author_email="1973690778@qq.com",
    description="A chemistry toolbox for parsing formulas and calculating molar mass.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            
        ],
    },
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    include_package_data=True,
)