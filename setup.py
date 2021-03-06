import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="LootBotApi",
    version="0.5.9.3",
    description="API wrapper for Loot Bot",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Anatras02/LootBotApi",
    author="Anatras02",
    author_email="balderialessio@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["LootBotApi"],
    include_package_data=True,
    package_data={'': ['craft_needed.json']},
    install_requires=["requests", "munch"],
)
