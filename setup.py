#!/usr/bin/env python

from setuptools import setup


tests_require = [
    "pytest",
]

setup(
    name="border_radius",
    version="1.0.1",
    author="Uploadcare",
    author_email="ak@uploadcare.com",
    description="Fast accurate border-radius mask generator with CSS syntax",
    url="https://github.com/uploadcare/pillow-border-radius",
    python_requires='>=3.7',
    packages=["border_radius"],
    include_package_data=True,
    install_requires=["pillow"],
    extras_require={
        "dev": [
            "pytest==6.2.5",
            "pytest-cov==3.0.0",
            "isort==5.10.1",
            "flake8==4.0.1"
        ],
    },
)
