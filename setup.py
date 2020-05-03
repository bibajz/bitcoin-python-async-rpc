import re
import sys
from pathlib import Path
from typing import List

from setuptools import find_namespace_packages, setup


def get_version(package: str) -> str:
    """
    Extract package version, located in the `src/package/__version__.py`
    """
    version = Path("src", package, "__version__.py").read_text()
    pattern = r"__version__ = ['\"]([^'\"]+)['\"]"
    return re.match(pattern, version).group(1)  # type: ignore


def get_requirements(req_file: str) -> List[str]:
    """
    Extract requirements from provided file. If installing under py3.7, include
    `typing_extensions`.
    """
    requirements_file = Path(req_file)
    requirements = []
    if requirements_file.exists():
        requirements.extend(requirements_file.read_text().split("\n"))
    if sys.version_info[:2] == (3, 7):
        requirements.append("typing_extensions==3.7.4.2")
    return requirements


def get_long_description() -> str:
    with open("README.md", encoding="utf8") as f:
        long_description = f.read()
    return long_description


setup(
    name="bitcoinrpc",
    python_requires=">=3.7",
    version=get_version("bitcoinrpc"),
    description="Lightweight Bitcoin JSON-RPC Python asynchronous client",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="bitcoin async json-rpc",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/bibajz/bitcoin-python-async-rpc",
    author="Libor Martinek",
    author_email="libasmartinek@protonmail.com",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=get_requirements("requirements.txt"),
)
