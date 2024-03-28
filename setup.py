from setuptools import setup,find_namespace_packages

setup(
    name='core_measures',
    install_requires=[
        "healdata-utils",
        "streamlit",
        "frictionless",
        "xlsxwriter",
        "openpyxl",
        "mkdocs-material"
        
    ],
    package_dir={'': '.'},
    packages=find_namespace_packages(where='.')
)