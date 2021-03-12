import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virtual_camera",
    version="1.1.9",
    author="Illia Shvarov",
    author_email="illia.shvarov@gmail.com",
    description="Cross-Platform Virtual Camera using Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THOSE-EYES/virtual_camera",
    project_urls={
        "Bug Tracker": "https://github.com/THOSE-EYES/virtual_camera/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)