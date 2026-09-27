from setuptools import setup, find_packages

setup(
    name="genpark-inbox-triage",
    version="1.0.0",
    description="Personal inbox cognitive triage engine classifying actionability and reading effort.",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "Personal inbox cognitive triage engine classifying actionability and reading effort.",
    long_description_content_type="text/markdown",
    author="GenPark AI Engineering",
    author_email="engineering@genpark.ai",
    url="https://github.com/Alpha-Park/genpark-personal-inbox-cognitive-triage-skill",
    py_modules=["client", "mcp_server"],
    python_requires=">=3.9",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
