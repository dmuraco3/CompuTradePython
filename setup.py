import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Quantuiti",
    version='0.0.1',
    author="Dylan Muraco",
    author_email="dylanjmuraco@gmail.com",
    description="Quantuiti library for quantitative finance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/quantuiti/python-quantuiti",
    project_urls={
        "Bug Tracker": "https://github.com/quantuiti/python-quantuiti/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
