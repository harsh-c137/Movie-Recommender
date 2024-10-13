from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

AUTHOR_NAME = 'Harsh Deshpande'
SRC_REPO = 'src'
LIST_OF_REQUIREMENTS = ['streamlit']

setup(
    name = SRC_REPO,
    version = '0.0.1',
    author = AUTHOR_NAME,
    author_email = 'harshdeshpande2001@gmail.com',
    description = 'A simple python package to deploy Movie Reco machine learning project on web app',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    packages = [SRC_REPO],
    python_requires = '>= 3.7',
    install_requires = LIST_OF_REQUIREMENTS
)