from setuptools import find_packages, setup

setup(
    name="explicitag",
    version="1.1.0",
    py_modules=["explicitag"],
    install_requires=["Click", "mutagen"],
    packages=find_packages(),
    include_package_data=True,
    package_data={"explicitag": ["explicit_words.txt"]},
    entry_points={
        "console_scripts": [
            "explicitag = explicitag.cli:cli",
        ],
    },
)
