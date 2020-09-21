
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DuckDuckGoImages",
    version="2.0.1",
    author="koke",
    author_email="jpobleteriquelme@gmail.com",
    description="Download images from DuckDuckGo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JorgePoblete/DuckDuckGoImages",
    py_modules=["DuckDuckGoImages"],
    package_dir={"":"src"},
    install_requires = [
        "requests >= 2.24.0",
        "joblib >= 0.16.0",
        "Pillow >= 2.2.1"
    ],
    extras_require = {
        "dev": [
            "pytest >= 3.7"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 
