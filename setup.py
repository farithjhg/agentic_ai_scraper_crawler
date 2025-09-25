# crawler/setup.py
"""
Setup script for the Advanced Web Scraper module
"""
from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Install Playwright browsers
        try:
            print("Installing Playwright browsers...")
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"])
            print("Successfully installed Playwright browsers.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing Playwright browsers: {e}")
            sys.exit(1)

# Read the requirements file
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r') as f:
        requirements = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Advanced Web Scraper with LLM Support"

setup(
    name="advanced-web-scraper",
    version="1.0.0",
    description="A powerful web scraper with LLM-powered data extraction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/advanced-web-scraper",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.8",
    cmdclass={
        'install': PostInstallCommand,
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="web scraping, llm, ai, data extraction, crawling",
    entry_points={
        "console_scripts": [
            "webscraper=cli:main",
            "webscraper-ui=streamlit_app:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black",
            "flake8",
            "mypy",
        ],
        "ui": [
            "streamlit>=1.28.0",
            "plotly>=5.17.0",
            "pandas>=2.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
