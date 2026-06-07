# setup.py
from setuptools import setup, find_packages

setup(
    name="judgment",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "google-generativeai",
        "sentence-transformers",
        "scikit-learn",
        "numpy",
        "pymupdf",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "judgment=cli.main:cli",
        ]
    }
)