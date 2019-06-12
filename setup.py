import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypdfkit-bvod",
    version="0.0.1",
    author="Bohdan Hrebeniuk",
    author_email="bogdan020699@gmail.com",
    description="A package for easy creation of pdf reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BogdanGrebenuk/pypdfkit",
    packages=setuptools.find_packages(),
    install_requires=["pdfkit", "jinja2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)