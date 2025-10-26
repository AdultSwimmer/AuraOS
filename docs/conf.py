# Configuration file for the Sphinx documentation builder.
# AuraOS Documentation
# Created by Anthony Dulong

import os
import sys

# -- Project information -----------------------------------------------------
project = 'AuraOS'
author = 'Anthony Dulong'
copyright = '2025, Anthony Dulong'
release = '5.0'
version = '5.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

# Add any paths that contain templates here, relative to this directory
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix of source filenames
source_suffix = '.md'

# The master toctree document
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets)
html_static_path = ['_static']

# Output directory - use ReadTheDocs environment variable if available
html_output_dir = os.environ.get('READTHEDOCS_OUTPUT', '_build') + '/html'

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
}

# Grouping the document tree into LaTeX files
latex_documents = [
    (master_doc, 'auraos.tex', 'AuraOS Documentation',
     'Anthony Dulong', 'manual'),
]

# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'auraos', 'AuraOS Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'AuraOS', 'AuraOS Documentation',
     author, 'AuraOS', 'AI Relationship Continuity System',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
