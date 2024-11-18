from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stalwart-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A web-based management tool for Stalwart Mail Server deployment and configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/stalwart-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Communications :: Email :: Mail Transport",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi==0.115.5",
        "uvicorn",
        "pydantic==2.9.2",
        "requests",
        "docker",
        "PyYAML",
        "Jinja2",
    ],
    include_package_data=True,
    package_data={
        "stalwart_manager": ["templates/*", "config/*"],
    },
    entry_points={
        "console_scripts": [
            "stalwart-manager=stalwart_manager.main:main",
        ],
    },
)
