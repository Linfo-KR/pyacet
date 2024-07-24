from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'pyacet',
    version = '0.1.0',
    packages = find_packages(),
    description = 'Python Automated Custom EDA Toolkit',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'YeongIL Kim',
    author_email = 'linfo4931@gmail.com',
    url = 'https://github.com/Linfo-KR/pyacet',
    install_requires = open('requirements.txt').read().splitlines(),
)