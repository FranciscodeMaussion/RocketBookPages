from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rocketqr",
    version="0.2",
    author="Francisco de Maussion",
    author_email="franciscodemaussion@gmail.com",
    description="Generates RocketBook QR Numerated Pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FranciscodeMaussion/RocketBookPages",
    project_urls={
        "Bug Tracker": "https://github.com/FranciscodeMaussion/RocketBookPages/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(
        include=["rocketqr", "rocketqr.constants", "rocketqr.templates"]
    ),
    python_requires=">=3.6",
    data_files=[
        (
            "Source/Bases",
            [
                "Source/Bases/Rocketbook-A4-Base.pdf",
                "Source/Bases/Rocketbook-Letter-Base.pdf",
                "Source/Bases/Rocketbook-Mini-Base.pdf",
                "Source/Bases/Rocketbook-Base.svg",
            ],
        ),
        ("Source", ["Source/templates_default.json"]),
    ],
    install_requires=["Click", "PyPDF2", "console-menu", "reportlab", "qrcode"],
    entry_points="""
        [console_scripts]
        rocketqr=rocketqr.rocketqr:set_up
    """,
)
