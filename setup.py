from setuptools import setup, find_packages

setup(
    name="amgmc",
    version="1.0.0",
    description="Algebraic Multigrid with SVD-based Preconditioner for Markov Chains",
    author="Proyecto Algebra Lineal",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy>=1.26",
        "scipy>=1.11",
        "numba>=0.58.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
)
