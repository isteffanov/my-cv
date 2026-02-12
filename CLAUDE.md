# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository generates a PDF CV from YAML data using Python, Jinja2 templates, and LaTeX. The workflow separates content (YAML) from presentation (LaTeX template).

## Build Commands

```bash
# Generate LaTeX from YAML data
python generate_cv.py > cv.tex

# Compile PDF (requires LaTeX distribution)
pdflatex cv.tex
```

## Architecture

```
my_data.yaml          → Data source (personal info, sections, entries)
        ↓
generate_cv.py        → Loads YAML, renders Jinja2 template to stdout
        ↓
templates/cv.tex.jinja → LaTeX template using moderncv class
        ↓
cv.tex                → Generated LaTeX output
        ↓
pdflatex              → Final PDF
```

## Key Files

- **my_data.yaml**: CV content organized as `personal`, `summary`, and `sections` (education, experience, mentoring, projects)
- **generate_cv.py**: Main script using Jinja2 and PyYAML
- **templates/cv.tex.jinja**: moderncv-based template with banking style

## YAML Data Structure

Each section contains entries with:
- `date`: Time period
- `title`: Main heading
- `subtitle`: Organization
- `text`: (optional) Single description
- `bullets`: (optional) Array of bullet points (supports LaTeX formatting)

## Dependencies

Python: `jinja2`, `pyyaml`
LaTeX: `moderncv` class
