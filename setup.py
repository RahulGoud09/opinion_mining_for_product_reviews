from setuptools import setup, find_packages

setup(
    name="opinion_mining",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.2",
        "nltk>=3.6.3",
        "textblob>=0.15.3",
        "beautifulsoup4>=4.9.3",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "transformers>=4.11.3",
        "torch>=1.9.0"
    ],
    python_requires=">=3.8",
) 