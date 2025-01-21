# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))  
project = 'DataVIZQA'
copyright = '2025, Malek-Mehyar'
author = 'Malek-Mehyar'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc", # Automatically document Python modules  
    "sphinx.ext.autosummary",    # Automatically document Python modules
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.napoleon",  # Support Google-style docstrings
    "sphinx_rtd_theme", 
            # RTD theme
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
