from setuptools import find_namespace_packages, setup

__version__ = "0.1.0"

setup(
    name="bitcoinrpc",
    version=__version__,
    description="Lightweight bitcoin async JSON-RPC python client",
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
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["typing_extensions", "httpx", "orjson"],
)
