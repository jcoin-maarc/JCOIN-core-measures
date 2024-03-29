from setuptools import setup,find_namespace_packages

setup(
    name='core_measures',
    install_requires=[
        "streamlit",
        "frictionless",
        "xlsxwriter",
        "openpyxl",
        "mkdocs-material"
        
    ],
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
)