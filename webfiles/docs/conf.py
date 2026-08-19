# docs/conf.py
import os
import sys
from datetime import datetime

# If your docs are in a package, add the package path here:
# sys.path.insert(0, os.path.abspath('..'))

project = "AuraOS"
author = "Anthony Dulong"
release = "5.0"

extensions = [
    "myst_parser",
]

# Source suffix mapping for .rst and .md
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"

language = "en"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Warn about all references that cannot be resolved
nitpicky = False  # Set to True to make more strict

# General substitutions
html_title = f"{project} documentation"
html_last_updated_fmt = "%b %d, %Y"
