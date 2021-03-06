import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TimeBoss", # Replace with your own username
    version="0.1.3",
    author="Christian Haack",
    author_email="chr.hck@gmail.com",
    description="A lightweight python timing class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrhck/TimeBoss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy"]
)
