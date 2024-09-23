from setuptools import setup, find_packages

setup(
    name="transport_company",  # The name of your package
    description="A transport company simulation package",
    long_description=open("README.md").read(),  # Description pulled from your README
    long_description_content_type="text/markdown",
    author="oliwka",
    packages=find_packages(),  # Automatically find all packages inside transport_company
)
