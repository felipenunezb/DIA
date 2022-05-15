"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name="dia",
    version="0.1",
    author="Felipe Nunez",
    author_email="f.nunezb@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=["pandas>1.4,<2", "openpyxl>=3.0.9", "xlrd>=2.0.1", "seaborn>=0.11.2"],
)